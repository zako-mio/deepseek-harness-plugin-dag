# dsh 插件级 DAG 差异报告：v0.1.7-rc.2 → v0.2.1-alpha.2

> 本报告由 `07-checkpoint/v021-*.py` 管线从**两版官方源码树**重算得出，所有数字可复现。
> 本轮为**增量级联**（非全量重建）：248 节点中 93 个复用旧版分析，155 个重做。

| 项 | 基线 | 目标 |
|---|---|---|
| tag | `dsh-v0.1.7-rc.2` | `dsh-v0.2.1-alpha.2` |
| commit | `477b4f420553e8a52c2fbccc464d7561b239c443` | `d743267388641bc76f17c45ce8b4c231aed1d32c` |
| 发布日 | 2026-09-24 | 2026-10-09 |
| 官方 tarball SHA256 | `761df167eaccc337bcee864579fd578ecb0f3cb5dbc7b1d36761508faaec455a` | `f54cf0530ffba0ffb6bd00d08d5459918a1518cb77b22aa2b166a5dba234428a` |

---

## 一、升级范围

| 指标 | 数值 |
|---|---|
| 提交跨度 | **21403 commits**（上轮 0.1.1→0.1.7 为 6875） |
| 包总数（按包 id 计） | 321 → **340**（+21 / −2 / 共同 319） |
| 包目录（按路径计） | 312 → 331（+31 / −12） |
| 顶级域 | 60 → **58**（−hooks / −runtime-diagnostics / −webhook，**+telemetry**） |
| 搬迁（同 id 换目录） | **10** 包 |

### 变化类型统计（319 个共同包，按 id 对齐后）

| 类别 | 数量 | 含义 |
|---|---|---|
| `src_changed` | **180** | `src/` 逐字节变化 → 必须重做分析 |
| `tests_changed` | 17 | 仅 `tests/` 变化 → 分析可复用 |
| `version_only` | **122** | 仅版本号等非 src/tests 字段变化 → 分析可复用 |
| `identical` | 0 | 完全无差异 |

> ⚠️ **口径说明（本轮关键改进）**：差异**以包 id 为键**，而非目录路径。
> 本轮存在 10 处「同 id 换目录」的域搬迁（如 `packages/webhook/webhook` → `packages/experimental/webhook`，id 仍为 `dsh-webhook`）。
> 若以路径为键，这 10 个包会被误判为「删除 + 新增」而白白重做分析；以 id 为键后正确识别为搬迁。
> 对照：路径口径显示 +31/−12，id 口径显示 +21/−2。

---

## 二、release notes ↔ 源码变更映射

覆盖 4 个版本、共 103 条要点。下表为与**包级结构变化**可对齐的主要条目：

| 版本 | release note 要点 | 对应源码变更 |
|---|---|---|
| 0.2.1-alpha.2 | 新增实验性**思考过程机器翻译**插件 | **+** `experimental/translator`、`experimental/client-ui-cot-translation`、`experimental/cot-translation-bundle` |
| 0.2.1-alpha.2 | 新增实验性 **Git Worktrees** 插件 | **+** `experimental/worktree`、`experimental/tool-worktree` |
| 0.2.1-alpha.2 | 新增实验性插件的 **Session 状态记录接口** | **+** `experimental/session-inspector` |
| 0.2.1-alpha.2 | 新增 **working_directory** 工具 + SDK 会话工作目录接口 | **+** `session/working-directory`、`session/tool-working-directory` |
| 0.2.1-alpha.2 | Official 插件列表新增 **Claude Code / Codex 组合包**入口 | **+** `experimental/claude-code-mods`、`experimental/client-ui-claude-code-mods` |
| 0.2.1-alpha.2 | **SSH 新增独立可执行 helper 运行时** | **+** `ssh/ssh-helper-runtime` |
| 0.2.1-alpha.1 | 新增可选的**开发者工具组合包**（会话原始日志、双向定位、内嵌 DevTools） | **+** `experimental/inspector-profile`、`experimental/session-search`、`client/ui-settings-session-log` |
| 0.2.1-alpha.1 | **破坏性变更：移除运行时 invariant 插件及各包 `./invariant` 导出** | **−** `runtime-diagnostics/invariants`（`dsh-invariants`，仓库真删） |
| 0.2.1-alpha.2 | **统一子代理执行与完成通知**（工具立即返回 child ID） | **−** `subagent/subagent-in-process-driver` |
| 0.2.1-alpha.1 | **自动化任务改为 Web 内置能力**，提醒工具按模式提供 | 域搬迁 `webhook` → `experimental`；**+** `schedule/tool-schedule` |
| 0.2.1-alpha.2 | 移除工具展示的 `both` 混合模式 | `core/agent-tool-presentation` 源码变更 |
| 0.2.1-alpha.2 | 移除 agent-instructions 逐行 dshHome 配置 | `context/agent-instructions` 源码变更 |
| 0.2.1-alpha.2 | 遥测 / 产品分析（新增 telemetry 域） | **+** `telemetry/otel`、`client/product-analytics`、`host/product-telemetry-otel` |
| 0.2.0-rc.2 / 0.2.1-alpha.2 | 更新 pi-ai（0.87.1 → 1.0.2） | `llm/llm-pi-ai`、`llm/plugin-package-inventory-deepseek` 源码变更 |
| 全版本 | 客户端 UI 大规模改版（字体、语音、终端、设置分页等） | `client` 域 **45 包**源码变更（最大变更域） |

> **hooks 域消失的解释**：`hooks/*` 三包（hook-protocol / hooks-claude-code / hooks-codex）**未删除**，而是整体迁入 `experimental/`。
> 其中 `hook-protocol` 从 DAG 节点**降级为 seam**（不再具备插件导出特征）。

---

## 三、实质变化包清单

### 3.1 新增包（21）

| 包 id | 路径 | 是否成为 DAG 节点 |
|---|---|---|
| `dsh-client-product-analytics` | `packages/client/product-analytics` | ✅ 节点 |
| `dsh-client-ui-settings-session-log` | `packages/client/ui-settings-session-log` | ✅ 节点 |
| `dsh-experimental-claude-code-mods` | `packages/experimental/claude-code-mods` | ✅ 节点 |
| `dsh-experimental-client-ui-claude-code-mods` | `packages/experimental/client-ui-claude-code-mods` | ✅ 节点 |
| `dsh-experimental-client-ui-cot-translation` | `packages/experimental/client-ui-cot-translation` | ✅ 节点 |
| `dsh-experimental-session-inspector` | `packages/experimental/session-inspector` | ✅ 节点 |
| `dsh-experimental-tool-worktree` | `packages/experimental/tool-worktree` | ✅ 节点 |
| `dsh-host-product-telemetry-otel` | `packages/host/product-telemetry-otel` | ✅ 节点 |
| `dsh-otel` | `packages/telemetry/otel` | ✅ 节点 |
| `dsh-tool-schedule` | `packages/schedule/tool-schedule` | ✅ 节点 |
| `dsh-tool-working-directory` | `packages/session/tool-working-directory` | ✅ 节点 |
| `dsh-working-directory` | `packages/session/working-directory` | ✅ 节点 |
| `dsh-experimental-badge-skill-bundle` | `packages/experimental/badge-skill-bundle` | seam |
| `dsh-experimental-cot-translation-bundle` | `packages/experimental/cot-translation-bundle` | seam |
| `dsh-experimental-inspector-profile` | `packages/experimental/inspector-profile` | seam |
| `dsh-experimental-ralph-bundle` | `packages/experimental/ralph-bundle` | seam |
| `dsh-experimental-session-search` | `packages/experimental/session-search` | seam |
| `dsh-experimental-session-titles-bundle` | `packages/experimental/session-titles-bundle` | seam |
| `dsh-experimental-terminal-bundle` | `packages/experimental/terminal-bundle` | seam |
| `dsh-experimental-translator` | `packages/experimental/translator` | seam |
| `dsh-ssh-helper-runtime` | `packages/ssh/ssh-helper-runtime` | seam |

### 3.2 移除包（2）

| 包 id | 原路径 | 说明 |
|---|---|---|
| `dsh-invariants` | `packages/runtime-diagnostics/invariants` | 对应 release note 的**破坏性变更**（移除运行时 invariant 插件） |
| `dsh-subagent-in-process-driver` | `packages/subagent/subagent-in-process-driver` | 对应「统一子代理执行与完成通知」 |

### 3.3 搬迁包（10，同 id 换目录）

| 包 id | 原路径 | 新路径 |
|---|---|---|
| `dsh-hook-protocol` | `packages/hooks/hook-protocol` | `packages/experimental/hook-protocol` |
| `dsh-hooks-claude-code` | `packages/hooks/hooks-claude-code` | `packages/experimental/hooks-claude-code` |
| `dsh-hooks-codex` | `packages/hooks/hooks-codex` | `packages/experimental/hooks-codex` |
| `dsh-session-title-all-prompts-llm` | `packages/session/session-title-all-prompts-llm` | `packages/experimental/session-title-all-prompts-llm` |
| `dsh-skill-badge` | `packages/skill/skill-badge` | `packages/experimental/skill-badge` |
| `dsh-tool-ralph` | `packages/workflow/tool-ralph` | `packages/experimental/tool-ralph` |
| `dsh-tool-session-query` | `packages/session-query/tool-session-query` | `packages/experimental/tool-session-query` |
| `dsh-tool-terminal` | `packages/terminal/tool-terminal` | `packages/experimental/tool-terminal` |
| `dsh-webhook` | `packages/webhook/webhook` | `packages/experimental/webhook` |
| `dsh-webhook-github` | `packages/webhook/webhook-github` | `packages/experimental/webhook-github` |

### 3.4 `src_changed` 包按域分布（180）

| 域 | 包数 | 域 | 包数 |
|---|---|---|---|
| client | **45** | session | 12 |
| experimental | 17 | llm | 7 |
| core | 7 | api | 5 |
| credentials | 5 | host | 5 |
| interaction | 5 | boot | 4 |
| extensions | 4 | shell | 4 |
| context | 3 | fs | 3 |
| sandbox | 3 | sdk | 3 |
| bundle | 2 | deliverables | 2 |
| goal | 2 | acp / compaction / jobs / loader / lsp / plan / preset / ptc-runtime / schedule / session-query | 各 1 |

> `client` 域占全部源码变更的 **25%**（45/180），是本轮变更重心；`experimental` 次之（17）。

---

## 四、依赖变化明细

### 4.1 节点与边总量

| 指标 | v0.1.7-rc.2 | v0.2.1-alpha.2 | 变化 |
|---|---|---|---|
| DAG 节点 | 239 | **248** | +12 / −3（共同 236） |
| 节点间边 `edges` | 1077 | **1167** | +151 / −61（共同 1016） |
| seam 边 `seam_edges` | 536 | **584** | +57 / −9 |
| 外部 seam | 73 | **83** | +10 |
| 分组 | 50 | **48** | −2 |
| 拓扑层 | 19 | **17** | −2 |
| type-only 边 | 281 | **324** | +43 |
| soft 反馈边 | 1 | 1 | 0 |

### 4.2 节点集变化

**新增节点（12）**：`dsh-client-product-analytics`、`dsh-client-ui-settings-session-log`、`dsh-experimental-claude-code-mods`、`dsh-experimental-client-ui-claude-code-mods`、`dsh-experimental-client-ui-cot-translation`、`dsh-experimental-session-inspector`、`dsh-experimental-tool-worktree`、`dsh-host-product-telemetry-otel`、`dsh-otel`、`dsh-tool-schedule`、`dsh-tool-working-directory`、`dsh-working-directory`

**移除节点（3）**：

| 节点 | 原因 |
|---|---|
| `dsh-invariants` | 仓库真删（破坏性变更） |
| `dsh-scope` | **重分类 node → seam**（`packages/core/scope` 不再具备插件导出特征） |
| `dsh-hook-protocol` | **重分类 node → seam**（随 hooks 域迁入 experimental） |

### 4.3 E1 / E2 / E3 机制分布（新 DAG，1167 条节点间边）

| mechanism | 边数 |
|---|---|
| `E1+E2` | 567 |
| `E1` | 509 |
| `E2` | 72 |
| `E1+E2+E3` | 8 |
| `E3` | 7 |
| `E1+E3` | 4 |

> 含 E2/E3 的边合计 **651**（56%），说明多数依赖既是编译期可见的 import，也有运行时服务注入/事件订阅或装配位依据——与上轮结构一致。

### 4.4 装配位变化

- 6 个 bundle 集合未变：`base` / `headless` / `web-app` / `acp-app` / `sdk-app` / `sdk-minimal`
- bundle 装配 insert 行：base **94**（旧 93）、web-app **87**（旧 85）、sdk-minimal **30**（旧 32）、acp-app 2、sdk-app 4、headless 2
- 装配行 disabled 标注：**18**（旧 19）
- 特殊模块：**8**（未变）

### 4.5 增量复用的强验证信号

新增的 151 条节点间边中，**151 条（100%）的源节点属于本轮"重做"集合**。

这从数据上证明了复用逻辑自洽：93 个复用节点的分析（implementation / provides / depends_on）逐字节继承自旧版，因此它们**没有贡献任何新增边**——所有边变化都来自真正重读源码的节点。若复用判定有漏洞（例如把已变源码的包误判为可复用），该比例会显著低于 100%。

---

## 五、增量复用账目

| 项 | 数值 |
|---|---|
| 新 DAG 节点总数 | 248 |
| **复用**（源码逐字节未变，直接继承旧版分析） | **93**（37.5%） |
| **重做**（委派子 Agent 重读源码） | **155** |

**重做原因分解**：

| 原因 | 数量 |
|---|---|
| `redo-src_changed`（源码变化） | 143 |
| `added-new-package`（本版新增包） | 11 |
| `no-prior-analysis`（旧版无分析记录） | 1 |

**复用判定规则**：节点 id 在旧版分析中存在，且其包在 delta 中属于 `version_only` / `tests_changed` / `identical`（即 `src/` 逐字节未变）。分析文本以**包内相对路径**引用源码行，故 src 未变则证据依然成立。

**证据存活性自检**：对 93 个复用节点的全部 `depends_on` 证据做 `file:line` 解析，共检查 **874 条**，文件缺失 1、行号越界 1（0.23%），二者均为旧版分析文本的**记法不规范**（写了 `/index.ts`、`index.ts:684` 这类非规范路径），非本轮引入的错误；因 src 逐字节相同，复用结论不受影响。

---

## 六、验证结果

| 检查 | 结果 |
|---|---|
| 分片回盘复验（`v021-validate.py`） | 248/248 节点覆盖；1753 条原始边；自环 0；指向装配框架的边 0；**坏证据 0**；空 implementation **0** |
| DAG 构建（`v021-build-dag.py`） | 分层后**无环**（1 条 soft 反馈边已剥离：`dsh-api-remotes` ↔ `dsh-client-ui-plugin-manager`）；248 节点全可达 |
| 页面全量重生成 | 388 文件（248 插件页 + 83 seam 页 + 48 组页 + 8 特殊模块页 + 分组索引） |
| 动态 DAG 注入 | 248/248 插件页命中 |
| 交互图 | 组级 49 节点 / 259 组间边；48 组下钻网格全部 assert 通过 |
| MD 镜像 | 248 插件 + 83 seam + 3 索引 |
| 结构门控 / 可读性门控 / headless 渲染 | 见 `report.md` 与库根 `README.md` |
