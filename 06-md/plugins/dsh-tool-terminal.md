# dsh-tool-terminal

- 包名: `@deepseek-ai/dsh-tool-terminal`
- 分组: G43 终端
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/terminal/tool-terminal`

## 实现逻辑
六个面向模型的持久终端工具，用 defineTool 注册到 ctx.tools：terminal_open/send/read/signal/close/list（src/index.ts:163-403）。owner 身份取自工具执行 Agent（src/index.ts:118-121, 185），前台 send 等待就绪/静默/超时/退出（src/index.ts:280-283），后台 send 交给通用 ctx.jobs 管理（src/index.ts:251-278，src/background.ts:22-31），结果经 TextRetainer 做字节上限渲染（src/render.ts:3）。

## Provides
- 工具 terminal_open / terminal_send / terminal_read / terminal_signal / terminal_close / terminal_list（注册到 ctx.tools，src/index.ts:163-403）

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 以执行 Agent 作为终端 owner
  - 证据: `package.json:33 peerDep + src/index.ts:9 import Agent + src/index.ts:185 requireAgent(exec.agent)`
- `dsh-llm` [编译依赖] - 工具结果内容块类型
  - 证据: `package.json:34 peerDep + src/index.ts:10 import ContentBlock`
- `dsh-system-prompt` [E1+E2] - 注入终端使用指引段落
  - 证据: `package.json:37 peerDep + src/index.ts:28 inject ['systemPrompt'] + src/index.ts:157 ctx.systemPrompt.section`
- `dsh-terminal` [E1+E2] - 调用 ctx.terminals 的会话操作
  - 证据: `package.json:35 peerDep + src/index.ts:11-12 import + src/index.ts:28 inject ['terminals']`
- `dsh-tools` [E1+E2] - 注册工具定义与 schema
  - 证据: `package.json:39 peerDep + src/index.ts:14-15 import defineTool + src/index.ts:28 inject ['tools']`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
