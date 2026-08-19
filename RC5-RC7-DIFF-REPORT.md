# RC5 → RC7 差异分析报告

> DeepSeek Harness 插件级 DAG 知识库升级差异分析
> 分析日期：2026-08-19 ｜ 知识库：`0819-plugin-dag-rc7`
> 基线：RC5（commit `47f9438`，2026-08-13）→ 目标：RC7（commit `99f6f02`，tag `dsh-v0.1.0-rc.7`，2026-08-17）

---

## 一、升级范围

| 维度 | RC5 | RC7 | 变化 |
|------|-----|-----|------|
| GitHub 对比 | 47f9438 → 99f6f02 | — | **111 commits**（2026-08-12 ~ 08-17） |
| packages 目录 | 219 包 | 219 包 | **无新增/删除包** |
| 版本号 | 0.1.0-rc.5 | 0.1.0-rc.7 | 全部包批量升级 |
| 源码实质变化 | — | — | **26 包**（src/ 变更） |
| 仅 tests 变化 | — | — | **5 包** |
| 仅版本号变化 | — | — | ~188 包 |
| 依赖关系变化 | — | — | **2 处**（acp、mcp-client 新增 attachment peer 依赖） |
| DAG 装配 | cordis.patch.yml | 字节级一致 | **装配位置零变化** |

---

## 二、官方 RC7 Release Notes 与源码映射

### 新增功能（3 条）

| Release Note | 涉及源码包 | 变更要点 |
|--------------|-----------|---------|
| 各插件可自行注册设置卡片 | `client/ui-settings-plugins`、`host/apiproxy`、`extensions/cordis-client-runner` | settings.plugin.item 槽由 list→keyed 化，卡片注册改为按命名空间 key 寻址；移除 WEB_SETTINGS_NAMESPACES/PRODUCT_SETTINGS_NAMESPACES 硬编码白名单 |
| Codex 与 Claude Code 子代理任务接入 Job Panel | `client/ui-jobs`、`subagent/tool-subagent`、`client/ui-primitives` | JobListAction 改用 useDismissOnOutsidePointer；取消判定修正（AggregateError 不误判为 cleanly killed） |
| MCP/ACP 支持持久化图片附件，PTC Mode 转发嵌套图片 | `acp/acp`、`mcp/mcp-client`、`attachment/attachment`、`fs/tool-fs`、`core/tools` | acp/mcp-client 新增 dsh-attachment peer 依赖；新增 src/content.ts（图片持久化）；图片结果注入职责移交 code-mode |

### 问题修复（5 条）

| Release Note | 涉及源码包 | 变更要点 |
|--------------|-----------|---------|
| 修复极简模式下持久 Bash 调用卡顿 | `shell/tool-bash-persistent` | 移除自定义 PS1 注入，完成判定改 `waitReason==='stdin_read'` |
| 修复大历史消息分页栈溢出 | `host/apiproxy` | Math.min 展开数组改 for 循环逐个取最小值 |
| 修复 max-tokens 截断导致会话无法继续 | `llm/llm`、`llm/llm-pi-ai`、`llm/llm-deepseek` | 新增 ReplayEnvelope 类型，截断时同步修剪 replay.blocks；pi-ai 增加 onReplayDegrade 降级 |
| 修复 Safari 输入框光标与文本错位 | `client/ui-conversation` | 新增 src/client/skeleton/safari.ts（isSafariBrowser + repairSafariTextareaLayout） |
| 升级 node-pty 1.2 beta | `subprocess/subprocess-local` | 版本 ^1.1.0→1.2.0-beta.15 |

### 体验优化（4 条）

| Release Note | 涉及源码包 | 变更要点 |
|--------------|-----------|---------|
| 优化 Cordis 动态插件面板 | `extensions/ui-cordis`、`extensions/cordis-client-runner`、`extensions/tool-cordis` | CordisPanel 改 position:fixed + 动态定位；引入 useDismissOnOutsidePointer |
| DeepSeek 模型新增 low 推理强度 | `llm/llm-deepseek` | REASONING_EFFORTS 新增 'low'，serialize 映射 thinking enabled + reasoning_effort low |
| 英文内置预设 Code mode 更名为 PTC mode | `core/tools`、`client/ui-agent-preset` | code-mode.ts 图片注入 + 文案更新；locales.ts Code mode→PTC mode |
| 提问卡片支持折叠并保留草稿 | `client/ui-user-questions` | QuestionComposer 新增 minimized 状态 + headerActions 折叠按钮 + 草稿跨折叠保留 |

### 非 Release Note 提及的变更

| 变更 | 涉及源码包 | 说明 |
|------|-----------|------|
| 移除 subagent specialization preset 能力 | `subagent/subagent`、`subagent/subagent-in-process-driver` | descriptor 版本 v3→v2 回退，删除 preset 字段 |
| ReplayEnvelope 契约重构 | `llm/llm`、`llm/llm-pi-ai`、`extensions/tool-cordis` | finish chunk 的 replayState 类型收窄为 ReplayEnvelope |

---

## 三、26 个源码实质变化包清单

| # | 包 | 版本 | 变更类型 | 关键变更 |
|---|-----|------|---------|---------|
| 1 | acp/acp | rc.5→rc.7 | 新增依赖 | 图片附件支持；新增 content.ts；peer 依赖 +attachment+llm |
| 2 | attachment/attachment | rc.5→rc.7 | 新增 API | saveImages() 批量持久化；错误码体系扩展 |
| 3 | client/ui-agent-preset | rc.5→rc.7 | 文案 | Code mode→PTC mode |
| 4 | client/ui-conversation | rc.5→rc.7 | 新文件 | Safari 光标修复 |
| 5 | client/ui-jobs | rc.5→rc.7 | 重构 | useDismissOnOutsidePointer |
| 6 | client/ui-primitives | rc.5→rc.7 | 新 hook | 新增 useDismissOnOutsidePointer |
| 7 | client/ui-settings-general | rc.5→rc.7 | 样式 | 42px 节奏对齐 |
| 8 | client/ui-settings-plugins | rc.5→rc.7 | 核心重构 | 卡片 keyed 化 + tab-store |
| 9 | client/ui-user-questions | rc.5→rc.7 | 新功能 | 提问卡片折叠+草稿 |
| 10 | core/tools | rc.5→rc.7 | 重构 | 图片注入移交 + PTC 更名 |
| 11 | extensions/cordis-client-runner | rc.5→rc.7 | 契约同步 | slot-catalog keyed 化 |
| 12 | extensions/tool-cordis | rc.5→rc.7 | 类型同步 | saveImages + ReplayEnvelope |
| 13 | extensions/ui-cordis | rc.5→rc.7 | 重构 | fixed 定位 + useDismiss |
| 14 | fs/tool-fs | rc.5→rc.7 | 重构 | 移除 deferContext 注入 |
| 15 | host/apiproxy | rc.5→rc.7 | 核心修复 | 移除命名空间白名单 + 分页栈溢出修复 + saveImages |
| 16 | llm/llm | rc.5→rc.7 | 类型新增 | ReplayEnvelope + assembler 重构 |
| 17 | llm/llm-deepseek | rc.5→rc.7 | 新能力 | low 推理强度 |
| 18 | llm/llm-pi-ai | rc.5→rc.7 | 重构 | ReplayEnvelope 双层 + onReplayDegrade |
| 19 | mcp/mcp-client | rc.5→rc.7 | 新增依赖 | MCP 图片附件 + attachment peer |
| 20 | session-query/session-query | rc.5→rc.7 | 重构 | type-only import + 鸭子类型判定 |
| 21 | shell/tool-bash-persistent | rc.5→rc.7 | 修复 | 移除 PS1 注入 + waitReason 判定 |
| 22 | subagent/subagent | rc.5→rc.7 | 移除能力 | specialization preset 移除 |
| 23 | subagent/subagent-in-process-driver | rc.5→rc.7 | 重构 | setup 改同步 |
| 24 | subagent/tool-subagent | rc.5→rc.7 | 修复 | AggregateError 取消判定 + job 文案 |
| 25 | terminal/terminal-bash | rc.5→rc.7 | 修复 | PROMPT_COMMAND 重设 PS1 |
| 26 | test-support/acp-snapshot | rc.5→rc.7 | 新功能 | promptContent 步骤 op |

---

## 四、依赖关系变化（E1 编译依赖）

**仅 2 处依赖变化**（其余 24 包依赖不变）：

| 包 | 新增 peerDependencies | 影响 |
|----|----------------------|------|
| acp/acp | `@deepseek-ai/dsh-attachment`, `@deepseek-ai/dsh-llm` | 图片持久化 + 模型 inputModalities 校验 |
| mcp/mcp-client | `@deepseek-ai/dsh-attachment` | MCP 结果图片持久化 |

**external-seams.json 更新**：
- `dsh-attachment` referred_by 4→6（新增 dsh-acp、dsh-mcp-client），ref_count 4→6

---

## 五、知识库更新明细

### 数据层
- `webapp-dag.json`：20 个节点 implementation/provides 按 RC7 源码更新；7 处版本标注 rc.5→rc.7
- `external-seams.json`：attachment 依赖更新（referred_by +2，ref_count 4→6）

### 页面层
- 全量重生成：`02-plugin-pages/`（221 页）、`03-groups/`（38 页）、`04-interactive/index.html`、`06-md/`（221 MD）、`08-special-modules/`（4 页）
- 14 个文件版本标注 rc.5→rc.7（7 HTML + 7 MD）

### drawio 移除（用户决策）
- **完全移除 `05-drawio/` 目录（348 文件：174 drawio + 174 png）**
- 只保留 HTML 动态图（交互图 + 插件页内嵌动态 DAG）
- 同步更新 README.md、index.html、REPORT.md、L3-EXEC-REPORT.md 的 drawio 引用
- 同步移除 quality-gate-l3.py/l2.py/gate.py 的 drawio 校验步骤（第4步）

### 修复的 bug
- **交互图 dagre 布局未注册**：gen-overview.py 模板漏引 cytoscape-dagre.min.js，导致 "No such layout 'dagre'" 无法渲染 → 已补引用
- **交互图样式选择器错误**：gen-overview.py 用 `node.plugin`（class 选择器）但节点 data 是 `kind:'plugin'` → 改为 `node[kind="plugin"]`（属性选择器），disabled 样式插入标记同步修正

### 质量门控
`quality-gate-l3.py` ALL PASS（7 项：JSON/DAG无环/HTML断链0/vendor/插件页覆盖/DATA校验/MD覆盖，0 错误 0 警告）

---

## 六、验证结果

- **headless + VLM 验证通过**：交互图组级 38 节点渲染正常、插件页内嵌动态 DAG 正常、中文完整无截断
- **RC7 源码三依据重验**：26 包变更逐条核对 RC7 官方源码（`05-source/dsh-rc7/`）
- **纯官方源码**：RC7 tarball 下载自 `https://github.com/deepseek-ai/deepseek-harness/archive/refs/tags/dsh-v0.1.0-rc.7.tar.gz`，SHA256 校验一致，无魔改

---

## 七、已知保留项

- 页面中 `0.0.1-rc.1` / `0.0.1-rc.3` / `0.1.0-rc.6` 为各包**历史版本演进记录**（如"0.1.0-rc.6 转公开"），属历史事实，按设计保留
- `append-reflection*.py` 中的 drawio 描述为历史执行记录文本，保留
- `PLAN-layer3.md` / `L3-DYN-DAG-REPORT.md` 为历史计划/报告文档，drawio 提及作为历史记录保留
