#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""迁移收尾：把库内残留的旧绝对路径改为自推导 BASE；更新文档中的旧目录名"""
import os, re, sys, py_compile
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = "/home/zako-mio/opencode/archive/Mission-file/2026-08/" \
      "0822-plugin-dag-v0.1.1-rc2"
OLD_DIRNAME = "0822-plugin-dag-v0.1.1-rc2"
NEW_DIRNAME = "0927-dsh-plugin-dag-017rc2"
DEF = 'SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))\nBASE = os.path.dirname(SCRIPT_DIR)'

pat_d = re.compile(r'r"' + re.escape(OLD) + r'([^"]*)"')
pat_s = re.compile(r"'?" + re.escape(OLD) + r"([^\"']*)[\"']")


def to_expr(suffix):
    parts = [p for p in re.split(r"[/\\]", suffix) if p]
    if not parts:
        return "BASE"
    return "os.path.join(BASE, " + ", ".join(repr(p) for p in parts) + ")"


changed = []
for dp, dn, fn in os.walk(BASE_DIR):
    dn[:] = [d for d in dn if d not in (".git", "__pycache__")]
    for f in fn:
        p = os.path.join(dp, f)
        if f.endswith(".py"):
            try:
                s = open(p, encoding="utf-8").read()
            except Exception:
                continue
            if OLD not in s:
                continue
            orig = s
            s = pat_d.sub(lambda m: to_expr(m.group(1)), s)
            s = re.sub(r'r?"' + re.escape(OLD) + r'([^"]*)"', lambda m: to_expr(m.group(1)), s)
            s = re.sub(r"'?" + re.escape(OLD) + r"([^\"']*)['\"]", lambda m: to_expr(m.group(1)), s)
            if s != orig and "BASE = os.path.dirname(SCRIPT_DIR)" not in s and "BASE = os.path.dirname(os.path.dirname(" not in s:
                # 插入 BASE 定义（放在首个 import 之后）
                lines = s.split("\n")
                idx = 0
                for i, ln in enumerate(lines[:40]):
                    if ln.startswith(("import ", "from ")):
                        idx = i
                lines.insert(idx + 1, DEF)
                s = "\n".join(lines)
                if not re.search(r"^import os\b|^import .*\bos\b", s, re.M):
                    s = "import os\n" + s
            open(p, "w", encoding="utf-8").write(s)
            changed.append(os.path.relpath(p, BASE_DIR))
        elif f.endswith((".md", ".html", ".json", ".txt")):
            s = open(p, encoding="utf-8").read()
            if OLD in s:
                s = s.replace(OLD, BASE_DIR)
                open(p, "w", encoding="utf-8").write(s)
                changed.append(os.path.relpath(p, BASE_DIR) + " [path]")
            elif OLD_DIRNAME in s:
                s = s.replace(OLD_DIRNAME, NEW_DIRNAME)
                open(p, "w", encoding="utf-8").write(s)
                changed.append(os.path.relpath(p, BASE_DIR) + " [name]")

print("changed files:")
for c in sorted(set(changed)):
    print("  ", c)

# 语法编译检查
bad = []
for dp, dn, fn in os.walk(os.path.join(BASE_DIR, "07-checkpoint")):
    dn[:] = [d for d in dn if d != "__pycache__"]
    for f in fn:
        if f.endswith(".py"):
            p = os.path.join(dp, f)
            try:
                py_compile.compile(p, doraise=True)
            except Exception as e:
                bad.append((os.path.relpath(p, BASE_DIR), str(e)[:120]))
print("\npy_compile 失败:", len(bad))
for b in bad:
    print("  ", b)
