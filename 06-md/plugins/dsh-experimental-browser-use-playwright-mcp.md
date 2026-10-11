# dsh-experimental-browser-use-playwright-mcp

- 包名: `@deepseek-ai/dsh-experimental-browser-use-playwright-mcp`
- 分组: G13 实验特性
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/experimental/browser-use-playwright-mcp`

## 实现逻辑
函数式插件，把 @playwright/mcp 的 CLI 作为每会话一个 MCP 进程挂载：固定 --browser chromium，attach 用 --cdp-endpoint，启动用 --isolated/--headless/--executable-path (src/index.ts:27-50)。启动前清空进程环境里全部 PLAYWRIGHT_MCP_* 变量，避免上游环境选项覆盖已配置的浏览器模式或引入无关 profile (src/index.ts:31-34)。配置与挂载同样复用运行时包的 BrowserMcpConfig / mountSessionMcp，attach 模式标记为独占 (src/index.ts:19, src/index.ts:28, src/index.ts:43-50)。

## Provides
- playwright-mcp 的会话作用域 MCP 浏览器提供者 (工具目录经 mountSessionMcp 注入)

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - 每个存活 Session 一个 MCP 进程，需要 agents 注册表
  - 证据: `src/index.ts:13 inject 'agents' + package.json:38 peerDep`
- `dsh-system-prompt` [运行时依赖] - 提示词就绪检查依赖 systemPrompt 服务
  - 证据: `src/index.ts:13 inject 'systemPrompt' + package.json:40 peerDep`
- `dsh-tools` [运行时依赖] - 上游工具目录要注册进会话的工具表
  - 证据: `src/index.ts:13 inject 'tools' + package.json:39 peerDep`
- `dsh-working-directory` [E1+E2] - MCP 进程的启动目录由会话工作目录决定
  - 证据: `src/index.ts:7 import type {} from '@deepseek-ai/dsh-working-directory' + src/index.ts:13 inject 'workingDirectory' + package.json:41 peerDep`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
