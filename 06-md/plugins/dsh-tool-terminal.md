# dsh-tool-terminal

- 包名: `@deepseek-ai/dsh-tool-terminal`
- 分组: G13 实验特性
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/experimental/tool-terminal`

## 实现逻辑
以「六个模型可见工具 + 通用后台作业适配」实现：apply 注册 terminal_open/send/read/signal/close/list 六个 defineTool，全部经 requireAgent 从执行的 Agent 取 owner、经 ctx.terminals 做 owner 隔离的持久终端操作，并用 finalizeContent 按 maxResultBytes 统一截断 (src/index.ts:149-158, src/index.ts:165-407)。terminal_send 支持 run_in_background：经 ctx.get('jobs') 以 kind 'pty-send' 启动作业，把后台读取经 sendSource 适配成 registry 拉取源，保持字节游标单调 (src/index.ts:255-283, src/background.ts:22-30)。渲染层用 dsh-output-retention 的 TextRetainer 保证 UTF-8 边界，并追加截断、分页、等待原因与会话状态标记 (src/render.ts:56-98, src/render.ts:120-158)。

## Provides
- ctx.tools (注册 terminal_open/terminal_send/terminal_read/terminal_signal/terminal_close/terminal_list 六个模型可见持久终端工具)
- ctx.systemPrompt (注册 tool:pty 章节，说明何时使用持久终端与推断空闲的语义)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 从工具执行上下文取得发起 Agent 作为终端会话的 owner 身份
  - 证据: `package.json:33 peerDep + src/index.ts:11 import Agent + src/index.ts:120-123 requireAgent`
- `dsh-llm` [编译依赖] - 构造模型可见的文本内容块作为工具结果
  - 证据: `package.json:34 peerDep + src/index.ts:12 import ContentBlock`
- `dsh-system-prompt` [运行时依赖] - 向系统提示注册 tool:pty 使用指导章节，约束模型何时使用持久终端
  - 证据: `package.json:37 peerDep + src/index.ts:30 inject 'systemPrompt' + src/index.ts:159-162 ctx.systemPrompt.section/getSectionOrder`
- `dsh-terminal` [E1+E2] - 声明并调用 terminals 服务完成 spawn/startSend/read/signal/kill/list 全部 owner 隔离的 PTY 操作
  - 证据: `package.json:35 peerDep + src/index.ts:13-14 import TerminalSessionId/TerminalSendOperation + src/index.ts:30 inject 'terminals' + src/index.ts:189 ctx.terminals.spawn`
- `dsh-tools` [E1+E2] - 声明 tools 服务并注册六个工具定义（含参数 schema、输出 schema、渲染与呈现回调）
  - 证据: `package.json:39 peerDep + src/index.ts:16-17 import defineTool/ToolDefinition + src/index.ts:30 inject 'tools' + src/index.ts:165 ctx.tools.register`
- `dsh-working-directory` [E1+E2] - 解析会话当前目录，作为终端会话初始 cwd 与相对 cwd 的解析基准
  - 证据: `package.json:41 peerDep + src/index.ts:7 type import + src/index.ts:30 inject 'workingDirectory' + src/index.ts:188 ctx.workingDirectory.ensure`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
