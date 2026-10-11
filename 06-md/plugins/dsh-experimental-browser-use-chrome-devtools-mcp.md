# dsh-experimental-browser-use-chrome-devtools-mcp

- 包名: `@deepseek-ai/dsh-experimental-browser-use-chrome-devtools-mcp`
- 分组: G13 实验特性
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/experimental/browser-use-chrome-devtools-mcp`

## 实现逻辑
函数式插件，把上游 chrome-devtools-mcp 作为每会话一个 MCP 进程挂载：解析包内 CLI 入口，按 mode 拼装 attach（--ws-endpoint 或 --browser-url）或启动（--isolated/--headless/--executable-path）参数，并固定 --no-usage-statistics (src/index.ts:26-42)。配置直接复用运行时包的 BrowserMcpConfig 类型与校验，激活前先 validateBrowserMcpConfig 拒绝非法组合，实际启动交给 mountSessionMcp（会话作用域、attach 模式标记独占）(src/index.ts:18, src/index.ts:27, src/index.ts:36-42)。

## Provides
- chrome-devtools-mcp 的会话作用域 MCP 浏览器提供者 (工具目录经 mountSessionMcp 注入)

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - 每个存活 Session 一个 MCP 进程，需要 agents 注册表
  - 证据: `src/index.ts:12 inject 'agents' + package.json:38 peerDep`
- `dsh-system-prompt` [运行时依赖] - 提示词就绪检查依赖 systemPrompt 服务
  - 证据: `src/index.ts:12 inject 'systemPrompt' + package.json:40 peerDep`
- `dsh-tools` [运行时依赖] - 上游工具目录要注册进会话的工具表
  - 证据: `src/index.ts:12 inject 'tools' + package.json:39 peerDep`
- `dsh-working-directory` [E1+E2] - MCP 进程的启动目录由会话工作目录决定
  - 证据: `src/index.ts:6 import type {} from '@deepseek-ai/dsh-working-directory' + src/index.ts:12 inject 'workingDirectory' + package.json:41 peerDep`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
