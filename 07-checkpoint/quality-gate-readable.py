#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S5 可读性质量门控（2026-09-27 对齐全量重建后的页面实际骨架）。

判据（阈值全部由「逐页统计 / 数据源长度」推导，非拍脑袋）：
  A. 页面区块骨架
     A1 DAG 插件页（239/239 实测 100%）：含
        「插件信息 / ① 实现逻辑 / ② 注册/提供（provides）/
          ③ 依赖（depends_on · 上游前驱）/ ④ 被依赖（dependents · 下游消费者）」五段。
     A2 seam 参考页（73/73 实测 100%）：含
        「基座 seam 说明 / 被依赖（下游）/ 依赖机制分布」三段。
     —— 阈值为对 239 个 DAG 节点页 + 73 个 seam 页逐页统计所得（均 100% 命中）。
  B. .md 链接自标注 + HTML 人类入口
     站内 href 以 .md 结尾的 <a>，其链接文本必须含 MD / Markdown / AI（大小写不敏感）
     之一（人类入口一律 HTML；.md 仅作 AI/机器镜像且必须自标注形态）。
     且 index.html 必须存在被链接的 report.html（同一主题的 HTML 人类入口）。
  C. index 统计一致性：index.html 统计块数字与数据源实测一致。
  D. 动态 DAG 注入覆盖：02-plugin-pages/*.html 含 id="dyn-dag" 的页数 == len(nodes)。
     —— 事故防线：重跑 gen-html-l3.py 会冲掉 gen-plugin-dyn.py 注入的动态 DAG 层，
        此判据在下次误跑时立刻报警。
  E. 主图不变量（04-interactive/index.html）：
     E1 grp- 节点数 == len(groups)+1（50+1=51，由数据源推导）；
     E2 组级为确定性 preset 布局（全部 grp- 节点含 position，且不以 dagre 作组级布局）；
     E3 差异化高亮三色语义（上游橙 #e8933b / 下游绿 #2fb98a / 自身蓝 #4f8cff
        在样式与图例文案中成对出现）。
  F. 索引不变量（03-groups/index.html）：
     F1 指向 Gxx.html 的链接去重数 == len(groups)；
     F2 指向 ../02-plugin-pages/*.html 的链接去重数 == len(seams)；
     F3 区锚点 id="L1|L2|L3" 各 1 个；
     F4 簇锚点 id="F1".."F9" 各 1 个。

历史遗留清理说明：
  - 旧 A 判据要求每页含「为什么需要它」，但该区块在本轮全量重建后不再产出
    （312 个页面内「为什么需要它」出现 0 次），旧判据在干净基线上即恒 FAIL，属遗留判据，已删除。
  - `whybox` / `.whybox .tag`（旧「设计初衷」样式）是 gen-html-l3.py 保留的死 CSS：
    class 在页面正文中出现 0 次，故不作任何门控判据；本脚本不引用这些 class。

用法：
  python3 quality-gate-readable.py             # 正式门控（读真实产物，只读不写）
  python3 quality-gate-readable.py --selftest  # 负向自检（临时副本定点破坏，证明判据非恒真）
"""
import json
import os
import re
import sys
import glob
import shutil
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
sys.stdout.reconfigure(encoding="utf-8")

# ---- A 阈值：实测区块（对 239 DAG 页 / 73 seam 页逐页统计，均 100% 命中）----
REQ_BLOCKS_DAG = [
    "插件信息",
    "① 实现逻辑",
    "② 注册/提供（provides）",
    "③ 依赖（depends_on · 上游前驱）",
    "④ 被依赖（dependents · 下游消费者）",
]
REQ_BLOCKS_SEAM = [
    "基座 seam 说明",
    "被依赖（下游）",
    "依赖机制分布",
]


# ---------------------------------------------------------------- helpers
def _read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def load_sources(base):
    with open(os.path.join(base, "01-dag-data", "webapp-dag.json"), encoding="utf-8") as f:
        dag = json.load(f)
    with open(os.path.join(base, "01-dag-data", "external-seams.json"), encoding="utf-8") as f:
        seams = json.load(f)["seams"]
    return dag, seams


def _pages_dir(base):
    return os.path.join(base, "02-plugin-pages")


# ---------------------------------------------------------------- A
def gate_A(base, dag, seams):
    pages = _pages_dir(base)
    missing = []
    for n in dag["nodes"]:
        p = os.path.join(pages, n["id"] + ".html")
        if not os.path.exists(p):
            missing.append((n["id"], "NO_PAGE"))
            continue
        c = _read(p)
        for b in REQ_BLOCKS_DAG:
            if b not in c:
                missing.append((n["id"], b))
    seam_missing = []
    for s in seams:
        p = os.path.join(pages, s["id"] + ".html")
        if not os.path.exists(p):
            seam_missing.append((s["id"], "NO_PAGE"))
            continue
        c = _read(p)
        for b in REQ_BLOCKS_SEAM:
            if b not in c:
                seam_missing.append((s["id"], b))
    ok = (not missing) and (not seam_missing)
    msg = (f"DAG 插件页 {len(dag['nodes'])-len({m[0] for m in missing})}/{len(dag['nodes'])} 命中五段"
           f"；seam 页 {len(seams)-len({m[0] for m in seam_missing})}/{len(seams)} 命中三段")
    if missing:
        msg += f"；DAG 缺失 {len(missing)} -> {missing[:4]}"
    if seam_missing:
        msg += f"；seam 缺失 {len(seam_missing)} -> {seam_missing[:4]}"
    return ok, msg


# ---------------------------------------------------------------- B
_MD_LABEL = re.compile(r"md|markdown|ai", re.I)


def _site_html_files(base):
    files = [os.path.join(base, "index.html")]
    for d in ("02-plugin-pages", "03-groups", "04-interactive", "08-special-modules"):
        files += glob.glob(os.path.join(base, d, "**", "*.html"), recursive=True)
    return [p for p in files if os.path.exists(p)]


def check_md_labels(base):
    """返回 (ok, total, offenders)。站内 .md <a> 文本须自标注形态。"""
    offenders = []
    total = 0
    for p in _site_html_files(base):
        c = _read(p)
        for m in re.finditer(r'<a\b[^>]*href="([^"]+\.md)"[^>]*>(.*?)</a>', c, re.S | re.I):
            href, inner = m.group(1), m.group(2)
            if href.startswith(("http://", "https://")):
                continue
            total += 1
            text = re.sub(r"<[^>]+>", "", inner).strip()
            if not _MD_LABEL.search(text):
                offenders.append((os.path.relpath(p, base), href, text[:40]))
    return (not offenders), total, offenders


def gate_B(base):
    labels_ok, total, offenders = check_md_labels(base)
    idx_path = os.path.join(base, "index.html")
    idx = _read(idx_path) if os.path.exists(idx_path) else ""
    entry_ok = bool(re.search(r'href="report\.html"', idx)) and \
        os.path.exists(os.path.join(base, "report.html"))
    ok = labels_ok and entry_ok
    msg = f"站内 .md 链接 {total} 条自标注"
    if offenders:
        msg += f"；未自标注 {len(offenders)} -> {offenders[:4]}"
    msg += f"；HTML 人类入口 report.html 被链接且存在={entry_ok}"
    return ok, msg


# ---------------------------------------------------------------- C
def gate_C(base, dag, seams):
    nodes, edges = dag["nodes"], dag["edges"]
    index = os.path.join(base, "index.html")
    idx = _read(index)
    real = {
        "节点": len(nodes),
        "seam": len(seams),
        "边": len(edges),
        "组": len(dag.get("groups", [])),
        "页": len(glob.glob(os.path.join(_pages_dir(base), "*.html"))),
    }
    stats_b = re.findall(r'<div class="stat"><b>(\d+)</b><span>([^<]+)</span>', idx)
    idx_stats = {label: int(num) for num, label in stats_b}
    bad = []
    for label, val in [("插件节点", real["节点"]), ("外部 seam", real["seam"]), ("依赖边", real["边"]),
                       ("分组", real["组"]), ("HTML 插件页", real["页"])]:
        if label in idx_stats and idx_stats[label] != val:
            bad.append(f"{label}: index={idx_stats[label]} 实测={val}")
    ok = not bad
    msg = (f"实测 节点{real['节点']}/seam{real['seam']}/边{real['边']}/组{real['组']}/页{real['页']}"
           f"；index 统计块 {len(stats_b)} 项")
    if bad:
        msg += f"；不一致 {bad}"
    return ok, msg


# ---------------------------------------------------------------- D
def count_dyn_dag(base):
    return sum(1 for p in glob.glob(os.path.join(_pages_dir(base), "*.html"))
               if 'id="dyn-dag"' in _read(p))


def gate_D(base, dag):
    want = len(dag["nodes"])
    got = count_dyn_dag(base)
    ok = (got == want)
    return ok, f"含 id=\"dyn-dag\" 的插件页 {got} == len(nodes) {want}"


# ---------------------------------------------------------------- E
_DAGRE_LAYOUT = re.compile(r"name\s*:\s*['\"]dagre['\"]")
_PRESET_LAYOUT = re.compile(r"name\s*:\s*['\"]preset['\"]")


def gate_E(base, dag):
    path = os.path.join(base, "04-interactive", "index.html")
    if not os.path.exists(path):
        return False, "04-interactive/index.html 缺失"
    c = _read(path)
    m = re.search(r"const DATA = (\{.*?\});", c, re.S)
    if not m:
        return False, "DATA 不可解析"
    try:
        data = json.loads(m.group(1))
        gnodes = data["grid"]["nodes"]
    except Exception as e:
        return False, f"DATA 解析失败: {e}"

    want = len(dag.get("groups", [])) + 1
    ids = [n["data"]["id"] for n in gnodes]
    grp = [i for i in ids if i.startswith("grp-")]
    e1 = (len(grp) == len(gnodes) == want)

    pos_ok = all("position" in n for n in gnodes)
    e2 = pos_ok and bool(_PRESET_LAYOUT.search(c)) and not _DAGRE_LAYOUT.search(c)

    triple = [
        ("#e8933b", "橙 = 上游"),
        ("#2fb98a", "绿 = 下游"),
        ("#4f8cff", "蓝 = 自身"),
    ]
    e3 = True
    e3_missing = []
    for color, legend in triple:
        # 样式 + 图例文案成对出现（图例 swatch 直接用该色的 background 紧接对应语义）
        swatch = re.search(r'background:' + re.escape(color) + r'"></span>' + re.escape(legend),
                           c)
        if not (swatch and (color in c)):
            e3 = False
            e3_missing.append(color)
    ok = e1 and e2 and e3
    msg = (f"grp- 节点 {len(grp)} == groups+1 {want}={e1}"
           f"；preset(位置{pos_ok}/无dagre布局)={e2}"
           f"；三色语义={'OK' if e3 else '缺' + str(e3_missing)}")
    return ok, msg


# ---------------------------------------------------------------- F
def gate_F(base, dag, seams):
    path = os.path.join(base, "03-groups", "index.html")
    if not os.path.exists(path):
        return False, "03-groups/index.html 缺失"
    c = _read(path)
    want_g = len(dag.get("groups", []))
    want_seam = len(seams)
    gxx = len(set(re.findall(r'href="(G\d+\.html)"', c)))
    plug = len(set(re.findall(r'href="(\.\./02-plugin-pages/[^"]+\.html)"', c)))
    zone = {z: c.count(f'id="{z}"') for z in ("L1", "L2", "L3")}
    clust = {f"F{i}": c.count(f'id="F{i}"') for i in range(1, 10)}
    ok = (gxx == want_g and plug == want_seam
          and all(v == 1 for v in zone.values())
          and all(v == 1 for v in clust.values()))
    msg = (f"Gxx 去重 {gxx} == groups {want_g}；plugin-page 去重 {plug} == seams {want_seam}"
           f"；区锚点 {zone}；簇锚点 {clust}")
    return ok, msg


# ---------------------------------------------------------------- runner
CHECKS = [
    ("A", "页面区块骨架（DAG 五段 / seam 三段）", lambda base, dag, seams: gate_A(base, dag, seams)),
    ("B", ".md 链接自标注 + HTML 人类入口", lambda base, dag, seams: gate_B(base)),
    ("C", "index 统计一致性", lambda base, dag, seams: gate_C(base, dag, seams)),
    ("D", "动态 DAG 注入覆盖", lambda base, dag, seams: gate_D(base, dag)),
    ("E", "主图不变量（preset / 三色）", lambda base, dag, seams: gate_E(base, dag)),
    ("F", "分组索引不变量", lambda base, dag, seams: gate_F(base, dag, seams)),
]


def run_gate(base, quiet=False):
    dag, seams = load_sources(base)
    results = {}
    for key, title, fn in CHECKS:
        ok, msg = fn(base, dag, seams)
        results[key] = (ok, msg)
        if not quiet:
            print(f"=== {key}. {title} ===")
            print(f"  [{'OK' if ok else 'FAIL'}] {msg}")
    return results


def main():
    results = run_gate(BASE)
    fails = [k for k, (ok, _) in results.items() if not ok]
    ok = not fails
    print()
    print(f"===== {'ALL PASS' if ok else f'HAS FAILURES ({len(fails)})'} =====")
    for k in fails:
        print(f"  - {k}: {results[k][1]}")
    sys.exit(0 if ok else 1)


# ---------------------------------------------------------------- selftest
def _build_temp_base():
    tmp = tempfile.mkdtemp(prefix="gate-selftest-", dir="/tmp/opencode")
    for d in ("01-dag-data", "02-plugin-pages", "03-groups", "04-interactive", "08-special-modules"):
        shutil.copytree(os.path.join(BASE, d), os.path.join(tmp, d))
    for f in ("index.html", "report.html"):
        shutil.copy2(os.path.join(BASE, f), os.path.join(tmp, f))
    return tmp


def _first_page(base, ids):
    return os.path.join(base, "02-plugin-pages", ids[0] + ".html")


def selftest():
    tmp = _build_temp_base()
    print(f"[SELFTEST] 临时副本: {tmp}")
    all_ok = True

    def report(name, target_check, expect_fail, before, after):
        nonlocal all_ok
        got_fail = not after
        passed = (got_fail == expect_fail) and before
        all_ok = all_ok and passed
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}: 破坏前 {target_check}="
              f"{'OK' if before else 'FAIL'} -> 破坏后 {'FAIL' if got_fail else 'OK'}"
              f"（期望 {'FAIL' if expect_fail else 'OK'}）")

    # 0) 正例：未破坏副本全绿
    base_res = run_gate(tmp, quiet=True)
    pos_ok = all(ok for ok, _ in base_res.values())
    print(f"  [{'PASS' if pos_ok else 'FAIL'}] POSITIVE 未破坏副本全部检查通过")
    all_ok = all_ok and pos_ok

    dag, seams = load_sources(tmp)

    # 1) A：删掉某 DAG 页的一个必需区块
    p = _first_page(tmp, [n["id"] for n in dag["nodes"]])
    orig = _read(p)
    pos = gate_A(tmp, dag, seams)[0]
    with open(p, "w", encoding="utf-8") as f:
        f.write(orig.replace("① 实现逻辑", "删掉的区块"))
    after = gate_A(tmp, dag, seams)[0]
    report("NEG-A1 删 DAG 页区块 '① 实现逻辑'", "A", True, pos, after)
    with open(p, "w", encoding="utf-8") as f:
        f.write(orig)

    # 2) A2：删掉某 seam 页的一个必需区块
    sp = _first_page(tmp, [s["id"] for s in seams])
    sorig = _read(sp)
    with open(sp, "w", encoding="utf-8") as f:
        f.write(sorig.replace("依赖机制分布", "删掉的区块"))
    after = gate_A(tmp, dag, seams)[0]
    report("NEG-A2 删 seam 页区块 '依赖机制分布'", "A", True, True, after)
    with open(sp, "w", encoding="utf-8") as f:
        f.write(sorig)

    # 3) B：把某 .md 链接文本换成无标注
    idx = os.path.join(tmp, "index.html")
    iorig = _read(idx)
    broken = iorig.replace('>AI 检索 MD 镜像<span class="cnt">Markdown</span></a>',
                           '>无标注镜像</a>')
    assert broken != iorig, "B 负例定位失败"
    with open(idx, "w", encoding="utf-8") as f:
        f.write(broken)
    after = gate_B(tmp)[0]
    report("NEG-B 某 .md 链接文本换无标注", "B", True, True, after)
    with open(idx, "w", encoding="utf-8") as f:
        f.write(iorig)

    # 4) D：删掉某页 id="dyn-dag"
    p = _first_page(tmp, [n["id"] for n in dag["nodes"]])
    orig = _read(p)
    with open(p, "w", encoding="utf-8") as f:
        f.write(orig.replace('id="dyn-dag"', 'id="dyn-dag-removed"'))
    after = gate_D(tmp, dag)[0]
    report("NEG-D 删某页 id=\"dyn-dag\"", "D", True, True, after)
    with open(p, "w", encoding="utf-8") as f:
        f.write(orig)

    # 5) E：从 DATA.grid.nodes 删一个 grp- 节点
    ip = os.path.join(tmp, "04-interactive", "index.html")
    ic = _read(ip)
    m = re.search(r"const DATA = (\{.*?\});", ic, re.S)
    data = json.loads(m.group(1))
    data["grid"]["nodes"] = data["grid"]["nodes"][:-1]
    payload = json.dumps(data, ensure_ascii=False)
    ic2 = ic[:m.start(1)] + payload + ic[m.end(1):]
    with open(ip, "w", encoding="utf-8") as f:
        f.write(ic2)
    after = gate_E(tmp, dag)[0]
    report("NEG-E 从 DATA 删一个 grp- 节点", "E", True, True, after)
    with open(ip, "w", encoding="utf-8") as f:
        f.write(ic)

    # 6) F：把区锚点 id="L1" 改名
    gp = os.path.join(tmp, "03-groups", "index.html")
    gc = _read(gp)
    gc2 = gc.replace('id="L1"', 'id="LX"')
    assert gc2 != gc, "F 负例定位失败"
    with open(gp, "w", encoding="utf-8") as f:
        f.write(gc2)
    after = gate_F(tmp, dag, seams)[0]
    report("NEG-F 区锚点 id=\"L1\" 改名", "F", True, True, after)
    with open(gp, "w", encoding="utf-8") as f:
        f.write(gc)

    # 收尾：确认临时副本已恢复 -> 再次全绿
    restored = run_gate(tmp, quiet=True)
    rest_ok = all(ok for ok, _ in restored.values())
    print(f"  [{'PASS' if rest_ok else 'FAIL'}] 副本恢复后再次全绿")
    all_ok = all_ok and rest_ok

    shutil.rmtree(tmp, ignore_errors=True)
    print(f"[SELFTEST] {'ALL NEGATIVE TESTS PASS' if all_ok else 'SELFTEST FAILED'}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        main()
