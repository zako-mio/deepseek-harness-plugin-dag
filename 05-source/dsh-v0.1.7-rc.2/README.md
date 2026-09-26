# 05-source/dsh-v0.1.7-rc.2

官方源码留档（provenance）。

| 项 | 值 |
|---|---|
| 版本 | `dsh-v0.1.7-rc.2` |
| commit | `477b4f420553e8a52c2fbccc464d7561b239c443` |
| 发布日期 | 2026-09-24 |
| 下载地址 | `https://github.com/deepseek-ai/deepseek-harness/archive/refs/tags/dsh-v0.1.7-rc.2.tar.gz` |
| SHA256 | 见 `dsh-v0.1.7-rc.2.tar.gz.sha256` |

## 解压（解压树 155MB，不入库）

```bash
cd 05-source/dsh-v0.1.7-rc.2
sha256sum -c dsh-v0.1.7-rc.2.tar.gz.sha256
tar xzf dsh-v0.1.7-rc.2.tar.gz     # → deepseek-harness-dsh-v0.1.7-rc.2/
```

解压树路径为 `.gitignore` 所列，可由 tarball 完全复现，故不入库以控制仓库体积
（旧版 `dsh-rc8/`、`dsh-v0.1.1-rc.2/` 的解压树已在历史中入库，此处不再重复该做法）。

## 复现重建

解压后，从仓库根依次运行：

```bash
python3 07-checkpoint/v017-inventory.py
python3 07-checkpoint/v017-facts.py
python3 07-checkpoint/v017-classify.py
python3 07-checkpoint/v017-make-shards.py
# （此步骤需按 07-checkpoint/v017/CONTRACT.md 委派子 Agent 产出 21 个 stage-01-shard-*.json）
python3 07-checkpoint/v017-validate.py
python3 07-checkpoint/v017-build-dag.py
python3 07-checkpoint/v017-prep-inputs.py
python3 07-checkpoint/v017-clean-pages.py
python3 07-checkpoint/gen-html-l3.py
python3 07-checkpoint/gen-md-l3.py
python3 07-checkpoint/gen-plugin-dyn.py
python3 07-checkpoint/gen-overview.py
python3 07-checkpoint/inject-data-l3.py
python3 07-checkpoint/quality-gate-l3.py
python3 07-checkpoint/headless-verify-l3.py
```
