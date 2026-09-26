#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S6 headless 验证 L3 交互图（04-interactive/index.html）。

既有能力（保留）：
  1. 组级视图 --dump 断言：zcount == len(groups)+1（50+1=51），zmode == 组级
  2. 组下钻动态选取（最大组 + 中等规模组）断言：zcount > 0 且 != 组级节点数（防假绿），
     zmode 以该组 id 开头
  3. 三张截图：组级 / 最大组下钻 / 中组下钻（各 > 10KB）

新增（2026-09-27 · 下钻几何强判据，修「includeLabels:false 假绿」）：
  4. 对 全部 50 组 + EXT 逐一打开 ?drill=<G>，断言：
     - cy.nodes().map(n=>n.renderedBoundingBox())（含标签）两两相交数 == 0
     - 每个节点的「标签包围盒 ⊆ 节点包围盒」（渲染 bbox 含标签 == 不含标签）
     - 所有节点都在画布内（x1>=0, y1>=0, x2<=clientWidth, y2<=clientHeight）
     - zoom >= 0.9
     - 下钻边默认 opacity <= 0.15（标签可读性 → 防边糊屏假绿）
     非零即失败，退出码非 0。每组打印一行汇总。

回归断言（既有能力逐项留证）：
  5. 组级 preset（全 grp- 节点含 position，无 dagre 布局）
  6. hover 差异化分类（G06: 橙 only 22 / 绿 only 3 / 双向 3(G02,G05,G20) / dim 22）
  7. disabled 灰显红边样式 + disabledIds 非空；seam 虚线；图例三色语义
  8. #graph 不被侧栏遮挡（graph.right == side.left）；返回组级视图按钮
  9. ?drill=Gxx / #Gxx 深链 + hashchange 生效

依赖：playwright（executable_path=/snap/bin/chromium，snap 私有 /tmp 不读宿主 /tmp）。
"""
import os, re, sys, json
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
HTML = os.path.join(BASE, "04-interactive", "index.html")
OUT = os.path.join(BASE, "07-checkpoint", "screenshots")
PROD = os.path.join(BASE, "07-checkpoint", "prototype", "shots")
os.makedirs(OUT, exist_ok=True)
os.makedirs(PROD, exist_ok=True)
CHROME = "/snap/bin/chromium"
BASE_URL = "file:///" + HTML.replace(os.sep, "/")

with open(HTML, "r", encoding="utf-8") as f:
    content = f.read()
m = re.search(r'const DATA = (\{.*?\});', content, re.DOTALL)
data = json.loads(m.group(1))
expected_groups = len(data["groups"]) + 1  # 50 + EXT
gids_all = sorted(data["groups"].keys()) + ["EXT"]
print(f"[INFO] expected group-level nodes: {expected_groups} (groups={len(data['groups'])} + EXT)")

# ---- 下钻几何探针（全部在渲染后执行；含标签包围盒，不带 includeLabels:false 偷懒） ----
GEO_JS = r"""
() => {
  const cy = window.__cy;
  const g = document.getElementById('graph');
  const W = g.clientWidth, H = g.clientHeight;
  const nodes = cy.nodes();
  const bb = nodes.map(n => n.renderedBoundingBox());
  let ovl = 0;
  for (let i = 0; i < bb.length; i++)
    for (let j = i + 1; j < bb.length; j++) {
      const a = bb[i], b = bb[j];
      if (a.x1 < b.x2 && b.x1 < a.x2 && a.y1 < b.y2 && b.y1 < a.y2) ovl++;
    }
  let outside = [], labelOut = [];
  nodes.forEach((n, i) => {
    const f = bb[i];
    if (f.x1 < -0.5 || f.y1 < -0.5 || f.x2 > W + 0.5 || f.y2 > H + 0.5) outside.push(n.id());
    const f2 = n.renderedBoundingBox(), b2 = n.renderedBoundingBox({includeLabels: false});
    const eps = 0.51;
    if (!(f2.x1 >= b2.x1 - eps && f2.y1 >= b2.y1 - eps &&
          f2.x2 <= b2.x2 + eps && f2.y2 <= b2.y2 + eps)) labelOut.push(n.id());
  });
  const opac = {};
  cy.edges().forEach(e => { const k = String(e.style('opacity')); opac[k] = (opac[k] || 0) + 1; });
  const maxOpac = Math.max(0, ...Object.keys(opac).map(Number));
  return { nodes: nodes.length, edges: cy.edges().length,
           zcount: +document.getElementById('zcount').textContent,
           zmode: document.getElementById('zmode').textContent,
           zoom: +cy.zoom().toFixed(3), W: W, H: H,
           overlap: ovl, labelIn: nodes.length - labelOut.length, labelOut: labelOut.slice(0, 5),
           outsideN: outside.length, outside: outside.slice(0, 5),
           edgeOpacity: opac, maxEdgeOpacity: maxOpac };
}
"""

HOVER_JS = r"""
(gid) => {
  const cy = window.__cy;
  window.__applyHighlight(cy.getElementById('grp-' + gid));
  const s = window.__hlSets();
  const r = { self: s.self.length, up: s.up.length, down: s.down.length,
              both: s.both.length, dim: s.dim.length, bothIds: s.both };
  window.__clearHighlight();
  return r;
}
"""

failures = []
page_errors = []
summary_lines = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
    return cond


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--disable-gpu"])
    page = browser.new_page(viewport={"width": 1600, "height": 1000})
    page.on("pageerror", lambda e: page_errors.append(str(e)))

    def goto(url, wait=900):
        page.goto(url)
        page.wait_for_timeout(wait)

    # ---------------- [1] 组级视图 ----------------
    goto(BASE_URL)
    zcount = int(page.eval_on_selector("#zcount", "e => e.textContent"))
    zmode = page.eval_on_selector("#zmode", "e => e.textContent")
    print(f"[1] 组级 DOM: zmode={zmode}, zcount={zcount}")
    check(zcount == expected_groups, f"组级 zcount {zcount} != {expected_groups}")
    check(zmode == "组级", f"组级 zmode != 组级: {zmode}")

    # 组级 preset / 无 dagre
    preset_ok = page.evaluate("() => { const cy=window.__cy; "
                              "return cy.nodes().every(n => typeof n.position().x === 'number' && "
                              "isFinite(n.position().x)); }")
    check(preset_ok, "组级节点位置非有限数值（preset 失效）")
    check(not re.search(r"name\s*:\s*['\"]dagre['\"]", content), "存在 dagre 布局（组级须 preset）")

    # hover 差异化分类（G06）
    hl = page.evaluate(HOVER_JS, "G06")
    print(f"[1] hover G06 分类: 橙only={hl['up']} 绿only={hl['down']} 双向={hl['both']} dim={hl['dim']}")
    check(hl["up"] == 22 and hl["down"] == 3 and hl["both"] == 3 and hl["dim"] == 22,
          f"hover G06 分类不符: {hl}")
    check(hl["bothIds"] == ["grp-G02", "grp-G05", "grp-G20"],
          f"双向节点不符: {hl['bothIds']}")

    # 图例三色语义 / disabled / seam / 侧栏遮挡
    for color, legend in [("#e8933b", "橙 = 上游"), ("#2fb98a", "绿 = 下游"), ("#4f8cff", "蓝 = 自身")]:
        check(f'background:{color}"></span>{legend}' in content, f"图例缺 {color}/{legend}")
    check('node[kind="disabled"]' in content, "样式缺 node[kind=disabled]")
    check('line-style' in content and 'dashed' in content, "样式缺 seam 虚线")
    check(len(data.get("disabledIds", [])) == 19, f"disabledIds 数 {len(data.get('disabledIds', []))} != 19")
    layout_ok = page.evaluate("() => { const g=document.getElementById('graph').getBoundingClientRect();"
                              " const s=document.getElementById('side').getBoundingClientRect();"
                              " return {gr: Math.round(g.right), sl: Math.round(s.left)}; }")
    check(abs(layout_ok["gr"] - layout_ok["sl"]) <= 1,
          f"#graph 与侧栏重叠: graph.right={layout_ok['gr']} side.left={layout_ok['sl']}")

    # ---------------- [2] 组下钻（动态选取：最大组 + 中等规模组） ----------------
    gids = list(data["groups"].keys())
    big_gid = max(gids, key=lambda g: data["drill"][g]["meta"]["n"])
    mid_gid = gids[min(len(gids) // 2, len(gids) - 1)]
    print(f"[INFO] drill groups: {big_gid}, {mid_gid}")

    goto(BASE_URL + "?drill=" + big_gid)
    n2 = int(page.eval_on_selector("#zcount", "e => e.textContent"))
    zmode2 = page.eval_on_selector("#zmode", "e => e.textContent")
    print(f"[2] 下钻 {big_gid} DOM: zmode={zmode2}, zcount={n2}")
    check(n2 > 0, f"下钻 {big_gid} 节点为 0")
    check(n2 != expected_groups, f"下钻视图与组级视图节点数相同({n2})，URL 路由未生效（假绿）")
    check(zmode2.startswith(big_gid), f"zmode 未切换: {zmode2}")

    # 返回组级视图按钮
    back_visible = page.eval_on_selector("#backbtn", "e => getComputedStyle(e).display !== 'none'")
    check(back_visible, "下钻视图返回按钮未显示")
    page.click("#backbtn")
    page.wait_for_timeout(500)
    check(int(page.eval_on_selector("#zcount", "e => e.textContent")) == expected_groups,
          "返回组级视图按钮未回到组级")

    # ---------------- [3] 截图 (组级 + 两个下钻) ----------------
    shot1 = os.path.join(OUT, "l3-group-level.png")
    shot2 = os.path.join(OUT, f"l3-drill-{big_gid}.png")
    shot3 = os.path.join(OUT, f"l3-drill-{mid_gid}.png")
    goto(BASE_URL, wait=1500); page.screenshot(path=shot1)
    goto(BASE_URL + "?drill=" + big_gid, wait=1500); page.screenshot(path=shot2)
    goto(BASE_URL + "?drill=" + mid_gid, wait=1500); page.screenshot(path=shot3)
    for s in [shot1, shot2, shot3]:
        size = os.path.getsize(s) if os.path.exists(s) else 0
        print(f"[3] screenshot {os.path.basename(s)}: {size} bytes {'OK' if size > 10000 else 'TOO SMALL'}")
        check(size > 10000, f"截图过小: {os.path.basename(s)}")

    # ---------------- [4] 全量下钻几何强判据（50 组 + EXT） ----------------
    print(f"[4] 下钻几何断言（含标签包围盒 / 标签内嵌 / 画布内 / zoom / 边默认透明）")
    for gid in gids_all:
        goto(BASE_URL + "?drill=" + gid, wait=600)
        r = page.evaluate(GEO_JS)
        summary_lines.append(
            f"  {gid:>4} n={r['nodes']:>3} e={r['edges']:>3} 含标签相交={r['overlap']:>3} "
            f"标签内嵌={r['labelIn']}/{r['nodes']} 出界={r['outsideN']} zoom={r['zoom']} "
            f"边opacity={r['edgeOpacity']}")
        ok = True
        ok &= check(r["overlap"] == 0, f"[{gid}] 含标签包围盒相交 {r['overlap']} != 0")
        ok &= check(r["labelIn"] == r["nodes"], f"[{gid}] 标签未内嵌: {r['labelOut']}")
        ok &= check(r["outsideN"] == 0, f"[{gid}] 节点出界: {r['outside']}")
        ok &= check(r["zoom"] >= 0.9, f"[{gid}] zoom {r['zoom']} < 0.9")
        ok &= check(r["nodes"] == r["zcount"], f"[{gid}] 节点数 {r['nodes']} != zcount {r['zcount']}")
        ok &= check(r["maxEdgeOpacity"] <= 0.15, f"[{gid}] 下钻边默认 opacity {r['maxEdgeOpacity']} > 0.15")
        if not ok:
            summary_lines[-1] += "  <== FAIL"

    # 深链 ?drill / #Gxx 等价
    goto(BASE_URL + "#" + big_gid)
    n_hash = int(page.eval_on_selector("#zcount", "e => e.textContent"))
    check(n_hash == n2, f"#Gxx 深链节点数 {n_hash} != ?drill 的 {n2}")
    # hashchange: 组级 -> 设置 hash -> 应切到该组
    goto(BASE_URL)
    page.evaluate(f"() => {{ window.location.hash = '{big_gid}'; }}")
    page.wait_for_timeout(600)
    check(int(page.eval_on_selector("#zcount", "e => e.textContent")) != expected_groups,
          "hashchange 未切换到下钻视图")

    # ---------------- [5] 生产默认态截图（G06 / EXT） ----------------
    goto(BASE_URL + "?drill=G06", wait=1200); page.screenshot(path=os.path.join(PROD, "prod-drill-G06.png"))
    goto(BASE_URL + "?drill=EXT", wait=1200); page.screenshot(path=os.path.join(PROD, "prod-drill-EXT.png"))

    browser.close()

# ---------------- 汇总 ----------------
print("\n".join(summary_lines))
print(f"\n[4] 下钻几何: {len(gids_all)} 组，全部 0 相交 / 标签内嵌 / 无出界 / zoom>=0.9 / 边默认<=0.15"
      if not failures else f"[4] 下钻几何: 存在 {len(failures)} 项失败")
print(f"[pageerror] {len(page_errors)} 个 JS 报错")
for e in page_errors[:5]:
    print(f"    {e}")
check(not page_errors, f"存在 JS 报错: {page_errors[:3]}")

if failures:
    print("\n===== FAILED =====")
    for f in failures:
        print(f"  [FAIL] {f}")
    sys.exit(1)
print("\n[OK] headless 断言全通过（组级 51 节点 + 全量下钻几何 + 既有能力回归）")
print(f"[OK] 截图输出: {OUT}")
print(f"[OK] 生产默认态截图: {PROD}/prod-drill-G06.png, prod-drill-EXT.png")
