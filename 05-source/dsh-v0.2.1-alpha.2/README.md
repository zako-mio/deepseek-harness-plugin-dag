# 05-source/dsh-v0.2.1-alpha.2

官方源码留档（provenance）。

| 项 | 值 |
|---|---|
| 版本 | `dsh-v0.2.1-alpha.2` |
| commit | `d743267388641bc76f17c45ce8b4c231aed1d32c`（annotated tag 对象 `6851e496285b2c9670066fdd142e7e46da586649`） |
| 发布日期 | 2026-10-09 |
| 下载地址 | `https://github.com/deepseek-ai/deepseek-harness/archive/refs/tags/dsh-v0.2.1-alpha.2.tar.gz` |
| SHA256 | `f54cf0530ffba0ffb6bd00d08d5459918a1518cb77b22aa2b166a5dba234428a` |
| 基线版本 | `dsh-v0.1.7-rc.2`（`477b4f420553e8a52c2fbccc464d7561b239c443`，2026-09-24） |

> 获取方式：经代理直连 GitHub 官方 tag tarball 下载（**非魔改版**），`sha256sum -c` 校验通过后解压。
> 本库目标版本以此 tarball 为唯一源码真相源，不使用本机工作检出（后者含未跟踪的本地脚本）。

## 解压（解压树 165MB，不入库）

```bash
cd 05-source/dsh-v0.2.1-alpha.2
sha256sum -c dsh-v0.2.1-alpha.2.tar.gz.sha256
tar xzf dsh-v0.2.1-alpha.2.tar.gz     # → deepseek-harness-dsh-v0.2.1-alpha.2/
```

解压树路径已列入仓库根 `.gitignore`，可由 tarball 完全复现，故不入库以控制仓库体积
（沿用 0.1.7-rc.2 起确立的做法：仅 tarball + SHA256 入库）。

## 复现重建

解压后，从仓库根依次运行增量级联管线（脚本见 `07-checkpoint/v021-*.py`）：

```bash
python3 07-checkpoint/v021-inventory.py     # 解析 6 个 bundle cordis.patch.yml + 枚举 packages/*/* 与 vendor/*
python3 07-checkpoint/v021-facts.py         # 逐包扫 src/**/*.ts 提取 E1/E2/插件导出特征
python3 07-checkpoint/v021-classify.py      # 分类 nodes / seams / special / uncovered + 分组
python3 07-checkpoint/v021-delta.py         # 与 v0.1.7-rc.2 做包级结构差异
python3 07-checkpoint/v021-merge-reuse.py   # 复用未变节点的既有分析（增量核心）
python3 07-checkpoint/v021-make-shards.py   # 仅对变化/新增包分片
# （委派）子 Agent 逐包实读源码 → 07-checkpoint/v021/stage-01-shard-*.json
python3 07-checkpoint/v021-validate.py
python3 07-checkpoint/v021-build-dag.py
python3 07-checkpoint/v021-prep-inputs.py
python3 07-checkpoint/v021-clean-pages.py
python3 07-checkpoint/gen-html-l3.py
python3 07-checkpoint/gen-plugin-dyn.py     # ⚠ 必须在 gen-html-l3 --write 之后补跑
python3 07-checkpoint/gen-overview.py
python3 07-checkpoint/inject-data-l3.py
python3 07-checkpoint/gen-root-index.py
python3 07-checkpoint/gen-md-l3.py
python3 07-checkpoint/quality-gate-l3.py
python3 07-checkpoint/quality-gate-readable.py
python3 07-checkpoint/headless-verify-l3.py
```
