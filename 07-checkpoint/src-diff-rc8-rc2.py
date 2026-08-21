#!/usr/bin/env python3
"""
三层差异分析 - 第二层：源码文件 diff（RC8 vs RC2）
对比每个包的 src/、tests/、package.json 哈希，分类为：
- 源码实质变化（src/ 变更）
- 仅 tests 变化
- 仅版本号变化（package.json 除 version 外无实质变化）
- 无变化
"""
import json, hashlib, os, re
from pathlib import Path

OLD = Path("05-source/dsh-rc8")
NEW = Path("05-source/dsh-v0.1.1-rc.2/deepseek-harness-dsh-v0.1.1-rc.2")
OUT = Path("07-checkpoint/src-diff-rc8-rc2.json")

SKIP_DIRS = {"node_modules", "dist", "lib", ".git", "__pycache__", "coverage", ".turbo", ".temp"}

def pkg_dirs(root):
    pkgs = []
    packages = root / "packages"
    if not packages.exists():
        return pkgs
    for domain in packages.iterdir():
        if not domain.is_dir():
            continue
        for p in domain.iterdir():
            if p.is_dir() and (p / "package.json").exists():
                pkgs.append((domain.name, p.name, p))
    return sorted(pkgs)

def hash_tree(path, rel_prefix=""):
    """返回 {相对路径: sha256}，跳过构建产物"""
    result = {}
    if not path.exists():
        return result
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in files:
            if f.startswith("."):
                continue
            fp = Path(root) / f
            rel = fp.relative_to(path).as_posix()
            try:
                data = fp.read_bytes()
            except Exception:
                continue
            result[rel] = hashlib.sha256(data).hexdigest()
    return result

def hash_package_json(path):
    try:
        text = path.read_text(encoding="utf-8")
        data = json.loads(text)
    except Exception:
        return None, None
    full = hashlib.sha256(text.encode("utf-8")).hexdigest()
    # 去掉 version 字段后的哈希
    stripped = dict(data)
    stripped.pop("version", None)
    stripped_text = json.dumps(stripped, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    stripped_hash = hashlib.sha256(stripped_text.encode("utf-8")).hexdigest()
    return full, stripped_hash

def main():
    old_pkgs = pkg_dirs(OLD)
    new_pkgs = pkg_dirs(NEW)
    old_map = {(d, n): p for d, n, p in old_pkgs}
    new_map = {(d, n): p for d, n, p in new_pkgs}

    all_keys = sorted(set(old_map) | set(new_map))

    result = {
        "summary": {"added": [], "removed": [], "src_changed": [], "tests_only": [], "version_only": [], "unchanged": []},
        "packages": {}
    }

    for key in all_keys:
        domain, name = key
        pkg_id = f"{domain}/{name}"
        old_p = old_map.get(key)
        new_p = new_map.get(key)

        if old_p is None:
            result["summary"]["added"].append(pkg_id)
            result["packages"][pkg_id] = {"status": "added", "path": str(new_p.relative_to(NEW.parent))}
            continue
        if new_p is None:
            result["summary"]["removed"].append(pkg_id)
            result["packages"][pkg_id] = {"status": "removed", "path": str(old_p.relative_to(OLD.parent))}
            continue

        old_src = hash_tree(old_p / "src")
        new_src = hash_tree(new_p / "src")
        old_tests = hash_tree(old_p / "tests")
        new_tests = hash_tree(new_p / "tests")
        old_pkg_full, old_pkg_stripped = hash_package_json(old_p / "package.json")
        new_pkg_full, new_pkg_stripped = hash_package_json(new_p / "package.json")

        src_changed = old_src != new_src
        tests_changed = old_tests != new_tests
        pkg_changed = old_pkg_full != new_pkg_full
        pkg_stripped_changed = old_pkg_stripped != new_pkg_stripped

        record = {
            "old_path": str(old_p),
            "new_path": str(new_p),
            "src_changed": src_changed,
            "tests_changed": tests_changed,
            "package_json_changed": pkg_changed,
            "package_json_stripped_changed": pkg_stripped_changed,
        }

        if src_changed:
            status = "src_changed"
        elif tests_changed:
            status = "tests_only"
        elif pkg_changed and not pkg_stripped_changed:
            status = "version_only"
        elif not pkg_changed and not src_changed and not tests_changed:
            status = "unchanged"
        else:
            # package.json 有实质变化但 src/tests 无变化
            status = "version_only"  # 归入版本号类，或单独标记
            record["note"] = "package.json 非 version 字段变化"

        result["summary"][status].append(pkg_id)
        record["status"] = status
        result["packages"][pkg_id] = record

    # 写入
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    s = result["summary"]
    print(f"总包数: 旧 {len(old_pkgs)} / 新 {len(new_pkgs)}")
    print(f"新增: {len(s['added'])}")
    print(f"删除: {len(s['removed'])}")
    print(f"源码实质变化: {len(s['src_changed'])}")
    print(f"仅 tests 变化: {len(s['tests_only'])}")
    print(f"仅版本号变化: {len(s['version_only'])}")
    print(f"无变化: {len(s['unchanged'])}")
    print(f"\n输出: {OUT}")

if __name__ == "__main__":
    main()
