# dsh-tool-terminal

- 包名: `@deepseek-ai/dsh-tool-terminal`
- 分组: G30 外部执行后端
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/terminal/tool-terminal`

## 为什么需要它（设计初衷）
基于 ctx.terminals 的 6 个终端工具（open/send/read/signal/close/list），要求同一 Agent 实例，支持后台 PTY 任务。

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/terminal/tool-terminal/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/terminal

## 实现逻辑
注册六个 model-facing 工具 terminal_open/send/read/signal/close/list (src/index.ts:162-398)，inject ['terminals','tools','systemPrompt'] (:27)；owner=exec.agent 隔离 (:118,:184)；run_in_background 经 ctx.get('jobs') 起 pty-send job (:252-275)，declare module 扩展 JobKindMap (:18-22)；maxResultBytes 输出上限 (:30,:45)；systemPrompt.section 引导 (:156-160)。

## Provides
- tools: terminal_open/terminal_send/terminal_read/terminal_signal/terminal_close/terminal_list
- dsh-jobs JobKindMap 扩展 'pty-send'

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - owner 隔离与 agent 上下文
  - 证据: `package.json:38 peerDep + src/index.ts:9 import type Agent；E2: :118 requireAgent(exec.agent)`
- `dsh-llm` [编译依赖] - 输出内容块类型
  - 证据: `package.json:40 peerDep + src/index.ts:10 import type ContentBlock`
- `dsh-system-prompt` [E1+E2] - 终端使用 prompt 引导
  - 证据: `package.json:43 peerDep + src/index.ts:27 inject；E2: :156 ctx.systemPrompt.section`
- `dsh-tools` [E1+E2] - 工具注册与 ToolDefinition
  - 证据: `package.json:45 peerDep + src/index.ts:14-15 import defineTool；E2: :27 inject、:162 ctx.tools.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
