# L3 委派 Prompt 文档（下一窗口直接复用）

> 生成日期：2026-08-17 ｜ 本文件：`07-checkpoint/L3-DELEGATE-PROMPTS.md`
> 用途：第三层 DAG 分析的子Agent 委派模板。新窗口读取本文件 + `PLAN-layer3.md` + `stage-00-l3-inventory.json` 后直接复制粘贴使用。

---

## 0. 主Agent 入口（L3 启动时先读）

```markdown
# L3 任务入口 Prompt（给新窗口主Agent）

## 任务
继续 deepseek-harness 插件级 DAG 依赖链分析的**第三层（L3：其余插件）**。

> L1 核心集（76 节点）与 L2 web-app bundle（58 节点）已完成，全量 DAG 在 webapp-dag.json（134 节点 / 434 边 / 17 层 / 29 组 / 49 seam）。

## 必读文档（按顺序）
1. D:\Opencode_Download\Mission-file\2026-08\0816-plugin-dag\PLAN-layer3.md ← 最重要，完整 L3 计划（精确 56 包范围 / 39 插件分组 / 坑经验）
2. D:\Opencode_Download\Mission-file\2026-08\0816-plugin-dag\07-checkpoint\stage-00-l3-inventory.json ← L3 清单（39 插件 8 组 + 13 seam + 4 特殊模块）
3. D:\Opencode_Download\Mission-file\2026-08\0816-plugin-dag\README.md ← L1+L2 成果总览
4. D:\Opencode_Download\Mission-file\2026-08\0816-plugin-dag\01-dag-data\webapp-dag.json ← L1+L2 合并 DAG（L3 更新此文件）
5. D:\Opencode_Download\Mission-file\2026-08\0816-plugin-dag\01-dag-data\external-seams.json ← 49 seam（L3 已追加 13 个）
6. D:\Opencode_Download\Mission-file\2026-08\0816-plugin-dag\07-checkpoint\L3-DELEGATE-PROMPTS.md ← 本文件，子Agent prompt 模板

## 执行阶段
S1: 5 路 explore 采集（用本文件 §1-§5 的 prompt）→ stage-01-l3-r1~r5.json
S2: build-dag-l3.py（复用 build-dag-l2.py，读 webapp-dag.json + L3 采集 → 合并 ~173 节点 / 37 组）
S3: inject-data-l3.py（复用 inject-data-l2.py：37 组视图 + 49 seam + disabled 保留）
S4: gen-html-l3.py（复用 gen-html-l2.py：39 插件页 + 组页 + L1/L2 重生成 + 特殊模块 08-special-modules/）
S5: drawio-worker 2-3 批（drawio-reference 强制加载）
S6: quality-gate-l3.py ALL PASS + headless/VLM
S7: README 更新 + PLAN-layer4.md + 留档询问 + Reflection

## 关键约束（同 L2）
- 三硬依据 E1/E2/E3 + 源码行引用
- 层次遍历 BFS（被依赖方先于依赖方）
- cytoscape 数据属性选择器（node[kind="plugin"]）
- python -c 禁用，脚本独立 .py
- quality-gate ALL PASS 才算完成
- 交接文件 PLAN-layer4.md 落盘
```

---

## 1. R1 采集 Prompt（G30 外部执行后端 + G37 部分）

```markdown
## ⚠️ Agent Identity — You are a SUBAGENT. Execute ONLY. No delegation. No search-agents.ps1.
## Role Activation: 源码分析 explore 子Agent
## Task: L3 第一路采集：外部执行后端 + 目录/静态托管（11 个插件）

源码根目录：D:\Opencode_Download\Mission-file\2026-08\0814-deepseek-harness源码解析\01-source-clone
装配事实：这些包**不在任何 bundle 装配中**（base/web-app/headless 均未引用），三依据以 **E1/E2 为主，E3 无**。若发现被 L1/L2 插件依赖（如 dsh-host-directory-picker 被 dsh-host-apiproxy 引用），如实填写。

### 需要分析的 11 个插件（路径已给出，读 src/index.ts + package.json）：
1. dsh-fs-e2b → packages/e2b/fs-e2b（E2B 云沙箱文件系统适配）
2. dsh-subprocess-e2b → packages/e2b/subprocess-e2b（E2B 云沙箱子进程）
3. dsh-terminal-bash → packages/terminal/terminal-bash（bash 终端实现）
4. dsh-tool-terminal → packages/terminal/tool-terminal（终端工具）
5. dsh-tool-bash-persistent → packages/shell/tool-bash-persistent（持久 bash 工具）
6. dsh-schedule → packages/schedule/schedule（定时调度）
7. dsh-host-directory-picker → packages/host/directory-picker（目录选择抽象）
8. dsh-host-directory-picker-browse → packages/host/directory-picker-browse（浏览式目录选择）
9. dsh-host-directory-picker-native → packages/host/directory-picker-native（原生目录选择）
10. dsh-host-frontend-static → packages/host/frontend-static（前端静态托管）
11. dsh-tool-ask-user → packages/interaction/tool-ask-user（询问用户工具）

### 三硬依据定义（每条依赖必须带源码行引用）：
- E1 编译依赖：package.json dependencies/peerDependencies + src import → `packages/e2b/fs-e2b/src/index.ts:12`
- E2 运行时依赖：ctx 服务注入 / ctx.get / 事件订阅 / 协议实现 → `packages/terminal/terminal-bash/src/index.ts:45`
- E3 组合依赖：若在某 bundle 装配则引用 cordis.patch.yml 行号；否则不写 E3

### 已知 seam 依赖（可直接引用 plugin_id）：
- dsh-e2b（E2B 抽象基座，seam）
- dsh-terminal（终端抽象，seam）
- dsh-subprocess-local / dsh-sandbox-local / dsh-shell-env（L1 已分析）
- dsh-tools / dsh-agent / dsh-session（L1 核心）
- dsh-host-apiproxy（L2 已分析，依赖 directory-picker）

### 输出：严格 JSON 数组（不要 Markdown 包裹），每插件对象：
{
  "id": "dsh-xxx",
  "name": "@deepseek-ai/dsh-xxx",
  "implementation": "200字内实现逻辑",
  "provides": ["注册的 ctx 服务/工具/协议"],
  "depends_on": [
    {"plugin_id": "上游id", "mechanism": "E1/E2/E3", "evidence": "源码行引用", "purpose": "依赖用途"}
  ],
  "dependents": [
    {"plugin_id": "下游id", "evidence": "源码行引用", "purpose": "消费用途"}
  ]
}
```

---

## 2. R2 采集 Prompt（G31 协议SDK + G32 LSP + G33 子代理后端 + seam 基座）

```markdown
## ⚠️ Agent Identity — You are a SUBAGENT. Execute ONLY. No delegation. No search-agents.ps1.
## Role Activation: 源码分析 explore 子Agent
## Task: L3 第二路采集：协议与 SDK + LSP + 子代理外部后端（8 插件）+ 抽象基座 seam 核实

源码根目录：D:\Opencode_Download\Mission-file\2026-08\0814-deepseek-harness源码解析\01-source-clone

### 需要分析的 8 个插件：
1. dsh-sdk-client → packages/sdk/client（SDK 客户端）
2. dsh-sdk-jsonrpc-server → packages/sdk/server（JSON-RPC 服务器）
3. dsh-lsp-stdio → packages/lsp/lsp-stdio（LSP stdio 传输）
4. dsh-tool-lsp → packages/lsp/tool-lsp（LSP 工具）
5. dsh-subagent-acp → packages/subagent/subagent-acp（ACP 子代理后端）
6. dsh-subagent-claude-code → packages/subagent/subagent-claude-code（Claude Code 子代理）
7. dsh-subagent-codex → packages/subagent/subagent-codex（Codex 子代理）
8. dsh-subagent-dsh-sdk → packages/subagent/subagent-dsh-sdk（DSH SDK 子代理）

### 额外任务：核实 7 个抽象基座 seam 的 referred_by（被依赖方）
这 7 个 seam 已在 external-seams.json（id 已建，referred_by 空）：
dsh-acp / dsh-e2b / dsh-hook-protocol / dsh-lsp / dsh-mcp-client / dsh-sdk-protocol / dsh-terminal
→ 若上述 8 插件依赖它们，在 depends_on 引用其 plugin_id；同时单独输出 seam 核实清单：
{"seam_id": "dsh-lsp", "referred_by": ["dsh-lsp-stdio", "dsh-tool-lsp"], "mechanisms": ["E1","E2"]}

### 三硬依据（同 R1）：E1/E2 为主，E3 无（不在 bundle 装配）
### 已知依赖：dsh-subagent（L1 核心）是 4 个子代理后端的宿主；dsh-tools / dsh-agent 被工具依赖

### 输出：JSON 数组（8 插件对象）+ 末尾附 seam_referred_by 数组
```

---

## 3. R3 采集 Prompt（G34 Web上下文扩展 + G35 会话存储变体）

```markdown
## ⚠️ Agent Identity — You are a SUBAGENT. Execute ONLY. No delegation. No search-agents.ps1.
## Role Activation: 源码分析 explore 子Agent
## Task: L3 第三路采集：Web/上下文扩展 + 会话存储变体（10 个插件）

源码根目录：D:\Opencode_Download\Mission-file\2026-08\0814-deepseek-harness源码解析\01-source-clone

### 需要分析的 10 个插件：
1. dsh-web-fetch-http → packages/web/web-fetch-http（HTTP 抓取）
2. dsh-web-search-exa → packages/web/web-search-exa（Exa 搜索）
3. dsh-web-search-perplexity → packages/web/web-search-perplexity（Perplexity 搜索）
4. dsh-session-reference → packages/context/session-reference（会话引用上下文）
5. dsh-time-context → packages/context/time-context（时间上下文）
6. dsh-tmux-context → packages/context/tmux-context（tmux 上下文）
7. dsh-session-persistence-sqlite → packages/session/session-persistence-sqlite（SQLite 会话持久化）
8. dsh-storage-sqlite → packages/storage/storage-sqlite（SQLite 存储后端）
9. dsh-session-title-all-prompts-llm → packages/session/session-title-all-prompts-llm（全 prompt 会话标题）
10. dsh-tool-session-query → packages/session-query/tool-session-query（会话查询工具）

### 三硬依据（同 R1）：E1/E2 为主
### 已知依赖：
- dsh-web-search-deepseek（L1 已分析）是 web 搜索的参照实现；web-search-exa/perplexity 是其变体
- dsh-session-persistence-jsonl（L1）是 persistence-sqlite 的参照；dsh-storage-json（L2）是 storage-sqlite 参照
- dsh-session-query-sqlite（L1）是 tool-session-query 的宿主
- dsh-web / dsh-tool-web（L1）被 web-fetch-http 依赖

### 输出：JSON 数组（10 插件对象）
```

---

## 4. R4 采集 Prompt（G36 Hooks工具扩展 + 特殊模块结构分析）

```markdown
## ⚠️ Agent Identity — You are a SUBAGENT. Execute ONLY. No delegation. No search-agents.ps1.
## Role Activation: 源码分析 explore 子Agent
## Task: L3 第四路采集：Hooks/工具扩展（6 插件）+ 特殊模块结构分析（4 个）

源码根目录：D:\Opencode_Download\Mission-file\2026-08\0814-deepseek-harness源码解析\01-source-clone

### 需要分析的 6 个插件：
1. dsh-hooks-claude-code → packages/hooks/hooks-claude-code（Claude Code hooks）
2. dsh-hooks-codex → packages/hooks/hooks-codex（Codex hooks）
3. dsh-tool-cordis → packages/extensions/tool-cordis（cordis 管理工具）
4. dsh-persona → packages/preset/persona（人设预设）
5. dsh-agent-tool-presentation → packages/core/agent-tool-presentation（agent 工具呈现）
6. dsh-native-command → packages/util/native-command（原生命令）

### 特殊模块结构分析（不建 DAG 节点，单独输出结构描述 JSON）：
4 个 bundle/boot 层特殊模块：
- dsh-base → packages/bundle/base（base bundle 自身，读 cordis.patch.yml 总结装配结构）
- dsh-headless → packages/bundle/headless（独立 bundle，读其 cordis.patch.yml：装配了 code-runtime-worker-thread + headless/startup + headless）
- dsh-app-boot → packages/boot/app-boot（启动框架：addHarnessSourceSection 等）
- dsh-cmdline → packages/boot/cmdline（命令行解析）

对每个特殊模块输出：
{"id": "dsh-headless", "kind": "bundle|boot", "assembly_summary": "装配了哪些插件", "dependencies": ["被依赖的 L1/L2 插件"], "structure_notes": "启动流程/装配层次说明"}

### 三硬依据（插件部分）：E1/E2 为主
### 已知依赖：dsh-hook-protocol（seam）被 hooks-* 依赖；dsh-agent / dsh-tools / dsh-session 被各工具依赖

### 输出：JSON（6 插件对象数组 + special_modules 数组）
```

---

## 5. R5 采集 Prompt（G37 示例与框架）

```markdown
## ⚠️ Agent Identity — You are a SUBAGENT. Execute ONLY. No delegation. No search-agents.ps1.
## Role Activation: 源码分析 explore 子Agent
## Task: L3 第五路采集：示例与框架（5 个插件）

源码根目录：D:\Opencode_Download\Mission-file\2026-08\0814-deepseek-harness源码解析\01-source-clone

### 需要分析的 5 个插件：
1. dsh-acp-demo → packages/examples/acp-demo（ACP 示例）
2. dsh-agent-spine-demo → packages/examples/agent-spine-demo（agent spine 示例）
3. dsh-sdk-jsonrpc-demo → packages/examples/jsonrpc-demo（JSON-RPC SDK 示例）
4. dsh-typert-generator → packages/typert/generator（typert 代码生成器）
5. dsh-native-command → packages/util/native-command（原生命令，若 R4 已采集则跳过并在返回中注明）

### 三硬依据（同 R1）：E1/E2 为主，示例包依赖关系可能较浅
### 已知依赖：examples 演示如何使用 dsh-sdk-protocol / dsh-acp / dsh-e2b 等 seam；typert-generator 被 dsh-typert-*（L1）生成工具链依赖

### 输出：JSON 数组（5 插件对象，含依赖与用途）
```

---

## 6. S2 建模提示（build-dag-l3.py 改造要点）

```markdown
复用 build-dag-l2.py，改造点：
1. 数据源：读 webapp-dag.json（L1+L2）+ stage-01-l3-r1~r5.json（L3 采集）
2. L3 分组：新增 G30-G37 八组（stage-00-l3-inventory.json 已定义）
3. 环修复方法论（L2 实证，必用）：
   - is_assembly_meta()：过滤指向 bundle 包（dsh-base/dsh-headless）的 E3 元信息边（L3 特殊模块不进 DAG，但若 L3 插件依赖它们，应作为 external seam 处理）
   - slot/协议注册方向：实现包依赖抽象基座（如 dsh-subprocess-e2b → dsh-e2b）
   - dependents 不反推边（删 7c 逻辑）
   - 双向耦合合并节点（若真存在）
4. 新 seam 追加：L3 插件依赖的 7 个抽象基座 seam 已有 id（external-seams.json 49 个），直接引用；采集回的 referred_by 更新到 external-seams.json
5. 输出：更新 webapp-dag.json（全量 ~173 节点 / 37 组 / 边界 ~500）
```

## 7. S3-S7 提示（复用 L2 管线）

```markdown
S3 inject-data-l3.py：读 L3 扩展 DAG + external-seams.json（49 seam）→ 注入 index.html DATA
   - 组级视图：37 组 + EXT；disabled 保留 22 个
   - 图例静态文字：29 组 → 37 组 / 134 插件 → ~173 插件（index.html 第 44-49 行）
S4 gen-html-l3.py：39 L3 插件页 + 8 组页 + L1/L2 页重生成（含 L3 下游）
   - 特殊模块单独生成 08-special-modules/ 页（base/headless/boot 4 个）
S5 drawio：2-3 批（G30-G37），drawio-reference 强制加载，scale=2
S6 quality-gate-l3.py：数据源切 L3 扩展 DAG，ALL PASS + headless/VLM
S7 README + PLAN-layer4.md + 留档询问 + Reflection
```
