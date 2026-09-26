# 子 Agent 分析契约（v0.1.7-rc.2 插件级 DAG 重建）

你负责分析**分片文件**中列出的插件（每个插件一条），基于 `dsh-v0.1.7-rc.2` **官方源码**产出结构化分析结果，写入指定输出文件。

## 源码根目录

```
/home/zako-mio/opencode/archive/Mission-file/2026-08/0822-plugin-dag-v0.1.1-rc2/05-source/dsh-v0.1.7-rc.2/deepseek-harness-dsh-v0.1.7-rc.2
```

插件路径 = `packages/<domain>/<name>`（分片文件已给出 `path`）。

## 输入
- 分片文件：`07-checkpoint/v017/shards/<SHARD>.json`
- 每项含：`id` / `name` / `path` / `ts_files` / `declared` / `imports`（含 `loc`）/ `injects` / `ctx_services` / `events_on` / `events_emit` / `provides_hints`
- **确定性事实已预抽**：`imports` 是逐行 import 的真实证据（file:line）。你**必须实读源码**校验，不要凭空推断。

## 输出（严格 JSON，写到 `07-checkpoint/v017/stage-01-<SHARD>.json`）

```json
[
  {
    "id": "dsh-llm-deepseek",
    "name": "@deepseek-ai/dsh-llm-deepseek",
    "implementation": "中文 2-5 句，说明「以什么逻辑实现了什么功能」，必须带源码行引用，如 (src/adapter.ts:3-60)。",
    "provides": ["ctx.xxx (中文能力说明)", "..."],
    "depends_on": [
      {"plugin_id": "dsh-llm", "mechanism": "E1", "evidence": "package.json:35 peerDep + src/adapter.ts:3 import", "purpose": "中文：为何依赖它"}
    ],
    "dependents": []
  }
]
```

## 硬性规则

1. **输出必须是合法 JSON 数组**，UTF-8，无注释、无 markdown 代码围栏。用 `write` 工具直接写文件。
2. `depends_on` 的 `plugin_id`：只填**本 dsh 仓库内**的包（`@deepseek-ai/*`），写成短名（去掉 `@deepseek-ai/`），如 `dsh-llm`、`cordis-plugin-timer`。**不含** `cordis`、`schemastery`、`cosmokit` 等外部 npm 包。
3. `mechanism` 取值：
   - `E1` 编译依赖（import / peerDependencies）
   - `E2` 运行时依赖（`static inject` / `ctx.<service>` / 事件订阅）
   - `E3` 组合依赖（bundle `cordis.patch.yml` 装配位置）
   - 可组合，如 `E1+E2`
4. `evidence` 必须含**具体 file:line**，来自你实读的源码或 package.json。
5. `depends_on` **排除**自环；**排除**指向 `dsh-base` / `dsh-headless` / `dsh-web-app` / `dsh-acp-app` / `dsh-sdk-app` / `dsh-sdk-minimal` / `dsh-app-boot` / `dsh-cmdline` 的边（这些是装配框架，不进 DAG）。
6. `dependents` 一律留 `[]`（下游由主流程按 depends_on 反推，避免口径冲突）。
7. `provides` 用中文，写「对外提供的能力」，如 `ctx.fs (文件系统能力 seam，供 fs-local/fs-e2b 实现)`。无则 `[]`。
8. 分片内**每个插件都要有输出**，数量必须与输入一致。
9. ⛔ 只写你负责的输出文件，**不得修改仓库内任何其它文件**。
10. ⛔ 不联网。只读本地源码。

## 自检（写文件前必做）
- JSON 可被 `json.load` 解析
- 条目数 == 输入插件数
- 每条含 `id`/`name`/`implementation`/`provides`/`depends_on`
- 所有 `evidence` 都含 `:` 与行号

## 返回格式
```json
{"status":"success|partial|failed","summary":"≤200字","data":{"shard":"<SHARD>","plugins":N,"edges":M,"output":"<文件绝对路径>"},"files_created":[],"files_modified":[],"decisions":[],"warnings":[],"errors":[]}
```
