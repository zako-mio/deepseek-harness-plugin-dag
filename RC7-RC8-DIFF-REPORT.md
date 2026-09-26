# RC7 → RC8 差异分析报告

> DeepSeek Harness 插件级 DAG 知识库升级差异分析
> 分析日期：2026-08-20 ｜ 知识库：`0927-dsh-plugin-dag-017rc2`
> 基线：RC7（commit `99f6f02`，tag `dsh-v0.1.0-rc.7`，2026-08-17）→ 目标：RC8（commit `141eb6f`，tag `dsh-v0.1.0-rc.8`，2026-08-19）
> 方法论：`version-upgrade-cascade`（三层差异分析 + 全量重生成 + 三重验证）

---

## 一、升级范围

| 维度 | RC7 | RC8 | 变化 |
|------|-----|-----|------|
| GitHub 对比 | 99f6f02 → 141eb6f | — | **536 commits**（2026-08-18 ~ 08-19） |
| packages 目录 | 219 包 | 226 包 | **新增 9 包、删除 2 包**（净 +7） |
| 版本号 | 0.1.0-rc.7 | 0.1.0-rc.8 | 全部包批量升级 |
| 源码实质变化 | — | — | **61 包**（src/ 变更） |
| 仅 tests 变化 | — | — | **17 包** |
| 仅版本号变化 | — | — | **139 包** |
| DAG 节点 | 173 | **180** | +9 新增 -2 删除 |
| DAG 依赖边 | 545 | **578** | 新增 +33 有效边 |
| 分组 | 37 | **39** | 新增 G38 多智能体协作 / G39 代码执行运行时 |
| 拓扑层 | 17 | 17 | 分层结构保持（最长路径深度） |

---

## 二、新增 9 包 / 删除 2 包

### 新增 9 包（全量同步至 DAG）

| # | DAG 节点 | 包名 | 组 | 功能 |
|---|---------|------|----|------|
| 1 | `dsh-client-ui-brand-official` | @deepseek-ai/dsh-client-ui-brand-official | G29 | 官方品牌视觉（official 构建 profile 注入 3 个 brand slot） |
| 2 | `dsh-client-ui-reference` | @deepseek-ai/dsh-client-ui-reference | G27 | Web 端统一 `@` 菜单（file + session 引用候选） |
| 3 | `dsh-client-ui-renderer` | @deepseek-ai/dsh-client-ui-renderer | G29 | React 渲染骨架 + 应用根装配（取代 web-react） |
| 4 | `dsh-code-runtime-python` | @deepseek-ai/dsh-code-runtime-python | G39 | code-execution seam 的 CPython 子进程后端 |
| 5 | `dsh-file-reference` | @deepseek-ai/dsh-file-reference | G21 | `@file` 引用发现抽象 seam + 语法 |
| 6 | `dsh-file-reference-local` | @deepseek-ai/dsh-file-reference-local | G21 | `@file` 本地文件系统实现（有界模糊索引） |
| 7 | `dsh-experimental-agent-team` | @deepseek-ai/dsh-experimental-agent-team | G38 | 隐式 root 多智能体协作服务（私有 opt-in） |
| 8 | `dsh-experimental-tool-agent-team` | @deepseek-ai/dsh-experimental-tool-agent-team | G38 | 模型面向 Agent Teams 协作工具集 |
| 9 | `dsh-tool-pwsh-persistent` | @deepseek-ai/dsh-tool-pwsh-persistent | G14 | Windows 持久 PTY PowerShell 工具 |

### 删除 2 包

| 节点 | 原功能 | RC8 去向 | 处理 |
|------|--------|---------|------|
| `dsh-client-web-react` | Shell 侧 React glue（createSlotRenderer/bindSnapshotSelector 等） | **改名+扩展为 `dsh-client-ui-renderer`**（React glue + 应用根/文档标题/挂载服务） | 删除旧节点，新增 ui-renderer（节点迁移非纯删除） |
| `dsh-client-schema-form` | settings 编辑器的 schema/draft 模型层 | **合并进 `dsh-client-ui-settings` 的 SettingsSchemaService** | 删除节点（功能并入 ui-settings） |

---

## 三、官方 RC8 Release Notes 与源码映射

### 新增功能

| Release Note | 涉及源码包 | 变更要点 |
|--------------|-----------|---------|
| 增强多模态支持，DeepSeek 适配器支持原生图片请求，`/goal` `/plan` 图文输入，`@` 菜单引用文件/会话 | `llm/llm-deepseek`、`llm/llm`、`llm/llm-pi-ai`、`attachment/attachment`、`context/file-reference(-local)`、`client/ui-reference`、`api/remotes`、`goal/command-goal` | llm-deepseek 新增 inputModalities(['image']) + maxRequestImageBytes；file-reference seam 抽象 @file 发现；ui-reference 统一 @ 菜单源 |
| Claude Code/Codex 子代理 Profile Bundle 按需安装，Codex 非交互权限模式 + 多命名实例 | `subagent/subagent-claude-code`、`subagent/subagent-codex` | provider 改可配置 providerName；新增 cordis.patch.yml 可选注册；codex 新增 CodexPermissionMode + createRequire 包内 wrapper |
| Windows PTY 持久 PowerShell 会话，极简模式默认支持 | `shell/tool-pwsh-persistent`、`subprocess/subprocess-local`、`client/ui-agent-preset` | 新增 dsh-tool-pwsh-persistent 持久 pwsh 工具（镜像 bash-persistent） |

### 问题修复

| Release Note | 涉及源码包 | 变更要点 |
|--------------|-----------|---------|
| 图片过大/历史图片累计载荷过高致模型请求失败 | `llm/llm`、`llm/llm-pi-ai`、`attachment/attachment`、`attachment/attachment-local`、`host/apiproxy` | llm.offloadRequestImages 脱载最旧图片；attachment-local 新增维度上限；attachment.admitEncodedImages 统一上传准入 |
| 取消流式后回复前缀未带入后续提问/分叉 | `core/agent-loop`、`llm/llm` | assembler.interruptedBlocks() 保留已流出前缀，agent.ts 持久化 interrupted 消息 |
| 自定义 OpenAI 兼容网关请求格式/推理回传缺失 | `llm/llm-pi-ai` | compat 面大幅扩展（thinking 格式/maxTokensField/cacheControlFormat/requiresReasoningContentOnAssistantMessages） |

### 体验优化

| Release Note | 涉及源码包 | 变更要点 |
|--------------|-----------|---------|
| HOME 目录 `~` 缩写 | `host/apiproxy` | host 信息新增 home: homedir() |
| web_search 并发查询 | `web/tool-web` | 新增 queries 数组 + Promise.allSettled 并发（最多 4） |
| 子代理 reportDelivery 唤醒父任务 | `subagent/subagent`、`subagent/tool-subagent-report` | reportDelivery 语义 wakeup→next-step；新增 drainContinuableChildren |
| 大历史会话分叉性能 | `session/session-persistence-sqlite`、`session/session-persistence` | sqlite packed 行 + coordinator fork 种子复用冻结快照 |

### 其他变更（⚠️ 重点）

| Release Note | 涉及源码包 | 变更要点 |
|--------------|-----------|---------|
| **SQLite 后端数据结构不兼容** | `session/session-persistence-sqlite` | **SCHEMA 15→17**；events.data/source_event_seqs 改 ANY(BLOB)；新增 packChunkRuns 打包 + zstd 压缩；与 rc7 数据库不兼容需重建 |

### SDK

| Release Note | 涉及源码包 | 变更要点 |
|--------------|-----------|---------|
| Python SDK 覆盖 4 内置预设 + rg/glob + MCP stdio 依赖 | `code-runtime/code-runtime-python`、`fs/tool-fs-search` | code-runtime-python（新增）；tool-fs-search 新增 pkg 单文件运行时 rg 侧车 |

---

## 四、61 个源码实质变化包清单

（完整 61 包见 `src-diff-result.json` 与 `07-checkpoint/src-diff-rc7-rc8.py`）

其中与 DAG 节点强相关、已更新 implementation/provides 的关键 14 包：

| 包 | DAG 节点 | 变更类型 | 关键变更 |
|----|---------|---------|---------|
| session/session-persistence-sqlite | dsh-session-persistence-sqlite | 存储格式不兼容 | SCHEMA 15→17、packed 行、zstd、+dsh-llm 依赖 |
| llm/llm-deepseek | dsh-llm-deepseek | 新能力 | 原生多模态图片、+attachment 依赖 |
| llm/llm | dsh-llm | 修复 | offloadRequestImages、interruptedBlocks |
| llm/llm-pi-ai | dsh-llm-pi-ai | 修复 | 图片脱载、OpenAI 兼容网关 compat 面扩展 |
| api/remotes | dsh-api-remotes | 新能力 | +file-reference +session-reference 远程 namespace |
| attachment/attachment | dsh-attachment(seam) | 新能力 | admitEncodedImages 统一准入 |
| attachment/attachment-local | dsh-attachment-local | 修复 | DecodedImageLimits 维度上限 |
| subagent/subagent-claude-code | dsh-subagent-claude-code | 新能力 | Profile Bundle + providerName + permissionMode |
| subagent/subagent-codex | dsh-subagent-codex | 新能力 | Profile Bundle + CodexPermissionMode |
| subagent/subagent | dsh-subagent | 新能力 | drainContinuableChildren + diagnostic 字段 |
| subagent/tool-subagent-report | dsh-tool-subagent-report | 修复 | reportDelivery wakeup→next-step |
| web/tool-web | dsh-tool-web | 新能力 | 并发 queries 查询 |
| core/agent-loop | dsh-core-agent-loop | 修复 | 中断回复前缀持久化 |
| host/apiproxy | dsh-host-apiproxy | 修复/优化 | admitEncodedImages + home 字段 |
| fs/tool-fs-search | dsh-tool-fs-search | 修复 | pkg 单文件 rg 侧车 |

---

## 五、依赖关系变化（E1 编译依赖）

### 新增依赖边（有效，已入 DAG）

**新增 9 包自身依赖**（30 条）+ **既有包新增依赖**（以下关键边）：

| from | to | 说明 |
|------|----|------|
| api/remotes | file-reference / session-reference | @ 菜单引用文件/会话远程 namespace |
| llm-deepseek | attachment(seam) | 原生多模态图片 |
| commands | attachment(seam) / llm | /goal /plan 图文输入 |
| session-persistence-sqlite | llm | 打包 StreamChunk 类型 |
| session-reference | typert-protocol(seam) | 会话引用远程契约 |
| web-app | ui-attachment / ui-brand-official / ui-reference / ui-renderer / file-reference / file-reference-local / session-reference / launch-environment(seam) / subprocess(seam) | E3 装配新增 |

**seam referred_by 更新**：
- `dsh-attachment`：+2（commands、llm-deepseek）
- `dsh-typert-protocol`：+2（client-ui-goal、session-reference）+1（file-reference）
- `dsh-client-connection`：净 +1（+tool +workspace -user-questions）
- `dsh-code-runtime` +1、`dsh-terminal` +1、`dsh-timeout` +1、`dsh-session-persistence` +1、`dsh-launch-environment` +1、`dsh-subprocess` +1、`dsh-pwsh-local` +1

### 声明移除但运行时仍引用（DAG 保留）

RC8 中大量 UI 包**移除了对 `dsh-client-ui-primitives` / `dsh-client-ui-slots` 的 peerDependencies 声明**（UI 依赖声明层解耦重构），但**源码 src 仍通过 import 实际引用**。经逐条源码验证（`verify-removed.py`，68 条声明删除边中 63 条仍 import），DAG 依赖边**按实际引用保留**，并在 33 个受影响插件页注入「RC8 变更 · 依赖声明调整」标注。

仅 3 条真正不再引用的边已删除（directory-picker-browse/native→slots、cordis-client-runner→slots）+ web-react 节点删除关联边。

### E3 组合依赖（装配文件）

- `bundle/base`、`bundle/headless` 的 cordis.patch.yml：**字节级一致**（装配零变化）
- `bundle/web-app`：新增 session-reference、file-reference-local、ui-renderer、ui-brand-official、ui-attachment、ui-reference 装配
- `subagent/subagent-codex`、`subagent/subagent-claude-code`：**新增 cordis.patch.yml**（Profile Bundle 可选注册）

---

## 六、知识库更新明细

### 数据层
- `webapp-dag.json`：173→180 节点（+9 -2）；545→578 边；37→39 组（+G38/G39）；17 层（最长路径重算）
- `external-seams.json`：attachment/typert-protocol/client-connection/code-runtime/terminal/timeout/session-persistence/launch-environment/subprocess/pwsh-local 的 referred_by 更新
- 版本标注：6 处 `版本 0.1.0-rc.7` → `rc.8`（历史 `0.0.1-rc.1/rc.3/rc.6` 保留，旧值零残留）

### 页面层（全量重生成）
- `02-plugin-pages/`：221→229 页（180 插件 + 49 seam，双身份 1）
- `03-groups/`：39 组页 + 索引
- `04-interactive/index.html`：DATA 更新（180 插件 + 49 seam + 825 边 + 40 组级节点），图例文本更新
- `06-md/`：180 插件 + 49 seam MD 镜像
- `08-special-modules/`：4 页保留

### 其他产物
- `README.md`、`index.html`：统计更新 + RC8 版本说明
- 33 个受影响插件页注入「RC8 声明调整」标注

---

## 七、验证结果

- **静态门控**：`quality-gate-l3.py` ALL PASS（7 项：JSON/DAG无环 180/180/HTML断链 0/vendor/插件页覆盖/DATA 校验/MD 覆盖，0 错误 0 警告）
- **headless DOM**：组级视图 40 节点渲染成功、zcount=40、无 JS 错误
- **VLM 截图验证**：
  - 交互图组级 40 节点、图例 180/40/39 组、中文完整、配色正确
  - 新增插件页（tool-pwsh-persistent / session-persistence-sqlite / agent-team）渲染正确
  - SQLite 不兼容说明正确展示（SCHEMA 15→17、需重建）
- **源码三依据重验**：61 包变更 + 9 新增 + 2 删除逐条核对 rc8 官方源码（`05-source/dsh-rc8/`）
- **纯官方源码**：RC8 tarball 下载自 `https://github.com/deepseek-ai/deepseek-harness/archive/refs/tags/dsh-v0.1.0-rc.8.tar.gz`，SHA256 `3cff6b7646f264c467a81257d472bf0f5d06e08d5790865d5aa65c6a8fa38ffa`，无魔改

---

## 八、已知保留项

- 交互图 `04-interactive/index.html` 无 URL drill 路由（`?drill=` 参数未解析，仅点击下钻可用）——RC7 遗留，非本次引入
- 页面中 `0.0.1-rc.1` / `0.0.1-rc.3` / `0.1.0-rc.6` 为各包**历史版本演进记录**，按设计保留
- `vendor/` 目录（@deepseek-ai/cordis 等）不在 packages/ 树内，后两者为 seam（path 为空）
