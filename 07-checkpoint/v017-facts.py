#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v0.1.7-rc.2 事实提取器（确定性）
对每个包扫描 src/**/*.ts，提取：
  E1  源码 import（含 file:line）+ package.json peer/deps 声明
  E2  static inject 服务名 / ctx.<service> 访问 / ctx.on|emit 事件
  E3  bundle patch 装配位置（来自 inventory.json）
输出 07-checkpoint/v017/facts.json
"""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
SRC = os.path.join(BASE, "05-source", "dsh-v0.1.7-rc.2", "deepseek-harness-dsh-v0.1.7-rc.2")
OUT = os.path.join(SCRIPT_DIR, "v017")

inv = json.load(open(os.path.join(OUT, "inventory.json"), encoding="utf-8"))
packages = inv["packages"]

RE_IMPORT = re.compile(r"""^\s*import\s+(?:type\s+)?(?:[^'"]*?from\s+)?['"]([^'"]+)['"]""")
RE_EXPORT_FROM = re.compile(r"""^\s*export\s+(?:type\s+)?(?:\*|\{[^}]*\})\s+from\s+['"]([^'"]+)['"]""")
RE_STATIC_INJECT = re.compile(r"""inject\s*[:=]\s*(\[[^\]]*\])""")
RE_CTX = re.compile(r"""\bctx\.([A-Za-z_$][A-Za-z0-9_$]*)""")
RE_EVENT_ON = re.compile(r"""\bctx\.(?:on|once|prependListener)\(\s*['"`]([\w:.\-/]+)['"`]""")
RE_EVENT_EMIT = re.compile(r"""\bctx\.(?:emit|parallel|bail|serial)\(\s*['"`]([\w:.\-/]+)['"`]""")
RE_SERVICE_SET = re.compile(r"""\bctx\.(?:set|provide)\(\s*['"]([\w:.\-/]+)['"]""")
RE_PROVIDE_MSG = re.compile(r"""provide\s*[:=]\s*['"]([^'"]+)['"]""")
# 插件导出特征
RE_PLUGIN_MARKERS = {
    "export_default": re.compile(r"""^\s*export\s+default\b""", re.M),
    "export_apply": re.compile(r"""^\s*export\s+(?:async\s+)?(?:function|const|let|var)\s+apply\b""", re.M),
    "export_inject": re.compile(r"""^\s*export\s+(?:const|let|var)\s+inject\b""", re.M),
    "export_name": re.compile(r"""^\s*export\s+(?:const|let|var)\s+name\b""", re.M),
    "extends_service": re.compile(r"""extends\s+Service\b"""),
    "inject_field": re.compile(r"""\binject\s*[:=]\s*\["""),
    "usage_ctx": re.compile(r"""\bctx\.[A-Za-z_$]"""),
}


def pkg_of_spec(spec):
    """把 import 说明符映射到包短名（= 节点 id），如 @deepseek-ai/dsh-fs/sub -> dsh-fs"""
    if not spec.startswith("@deepseek-ai/"):
        return None
    parts = spec.split("/")
    if len(parts) < 2:
        return None
    return parts[1]


def to_id(name):
    """包短名即节点 id（保留 dsh- 前缀）"""
    return name


facts = {}
for pid, p in sorted(packages.items()):
    pdir = os.path.join(SRC, p["path"])
    files = []
    for f in p.get("ts_files", []):
        files.append(f)
    imports = []
    injects = []
    ctx_services = {}
    events_on = {}
    events_emit = {}
    provides_hints = []
    markers = {k: 0 for k in RE_PLUGIN_MARKERS}
    n_lines = 0

    for rel in files:
        fp = os.path.join(pdir, rel)
        try:
            with open(fp, encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
        except OSError:
            continue
        n_lines += len(lines)
        text = "".join(lines)
        for k, rx in RE_PLUGIN_MARKERS.items():
            markers[k] += len(rx.findall(text))
        for i, ln in enumerate(lines, 1):
            m = RE_IMPORT.match(ln) or RE_EXPORT_FROM.match(ln)
            if m:
                spec = m.group(1)
                pid_dep = pkg_of_spec(spec)
                if pid_dep:
                    imports.append({"dep": to_id(pid_dep), "spec": spec, "loc": f"{rel}:{i}"})
            m = RE_STATIC_INJECT.search(ln)
            if m:
                svcs = re.findall(r"""['"]([\w:.\-/]+)['"]""", m.group(1))
                if svcs:
                    injects.append({"services": svcs, "loc": f"{rel}:{i}"})
            for m in RE_CTX.finditer(ln):
                svc = m.group(1)
                if svc in ("on", "emit", "effect", "get", "set", "provide", "inject", "parallel", "bail", "serial", "once", "scope", "mixin", "plugin", "logger", "root", "is"):
                    continue
                ctx_services.setdefault(svc, []).append(f"{rel}:{i}")
            for m in RE_EVENT_ON.finditer(ln):
                events_on.setdefault(m.group(1), []).append(f"{rel}:{i}")
            for m in RE_EVENT_EMIT.finditer(ln):
                events_emit.setdefault(m.group(1), []).append(f"{rel}:{i}")
            for m in RE_SERVICE_SET.finditer(ln):
                provides_hints.append({"name": m.group(1), "loc": f"{rel}:{i}"})

    facts[pid] = {
        "id": pid,
        "name": p["name"],
        "path": p["path"],
        "domain": p["domain"],
        "version": p.get("version"),
        "ts_count": p.get("ts_count", 0),
        "loc": n_lines,
        "declared": {
            "peer": sorted({x.split("/")[1] for x in p["deps"]["peer"] if x.startswith("@deepseek-ai/") and x.count("/") >= 1}),
            "deps": sorted({x.split("/")[1] for x in p["deps"]["deps"] if x.startswith("@deepseek-ai/") and x.count("/") >= 1}),
        },
        "imports": imports,
        "import_pkgs": sorted({i["dep"] for i in imports}),
        "injects": injects,
        "ctx_services": {k: v[:6] for k, v in ctx_services.items()},
        "events_on": {k: v[:4] for k, v in events_on.items()},
        "events_emit": {k: v[:4] for k, v in events_emit.items()},
        "provides_hints": provides_hints[:20],
        "markers": markers,
        "assembled_in": [],
    }

# assembled_in 单独算（清晰起见）
pid_to_bundles = {}
for b, bd in inv["bundles"].items():
    for r in bd["insert_rows"]:
        nm = r.get("name")
        if not nm:
            continue
        qid = nm.split("/")[1] if nm.startswith("@deepseek-ai/") else nm.split("/")[0]
        pid_to_bundles.setdefault(qid, set()).add(b)
for pid in facts:
    facts[pid]["assembled_in"] = sorted(pid_to_bundles.get(pid, set()))

with open(os.path.join(OUT, "facts.json"), "w", encoding="utf-8") as f:
    json.dump(facts, f, ensure_ascii=False, indent=1)

# 统计
n_import_edges = sum(len(v["import_pkgs"]) for v in facts.values())
print(f"[OK] facts for {len(facts)} packages")
print(f"[INFO] total distinct import-pkg references: {n_import_edges}")
plug = [k for k, v in facts.items() if v["markers"]["export_default"] or v["markers"]["export_apply"] or v["markers"]["export_inject"]]
print(f"[INFO] plugin-marker packages: {len(plug)}")
lib = [k for k, v in facts.items() if not any(v["markers"].values())]
print(f"[INFO] no-marker (pure library) packages: {len(lib)}")
print("      ", sorted(lib)[:40])
