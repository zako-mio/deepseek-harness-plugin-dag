# dsh-experimental-computer-use-cua-driver-mcp

- 包名: `@deepseek-ai/dsh-experimental-computer-use-cua-driver-mcp`
- 分组: G13 实验特性
- 拓扑层: Layer 7
- 来源层: L3 其余
- 源码路径: `packages/experimental/computer-use-cua-driver-mcp`

## 实现逻辑
函数插件以 `dsh-mcp-client` 的 Config 连接已安装的 `cua-driver` MCP 可执行文件（stdio、failOnStartupError:true）（src/index.ts:52-61）。在一个 effect 中先 `ctx.computerUse.register('cua-driver-mcp')` 再以子插件启动 MCP client，并按顺序等待子进程彻底退出后再释放保留（src/index.ts:62-70）；启动/发现失败即回滚激活。

## Provides

## Depends On (上游依赖)
- `dsh-mcp-client` [编译依赖] - 承载 MCP 连接（发现/执行/重连）并作为子插件生命周期
  - 证据: `src/index.ts:10 import * as McpClient + src/index.ts:53 McpClient.Config`
- `dsh-tools` [运行时依赖] - MCP 工具注册进工具注册表的前提服务
  - 证据: `src/index.ts:17 inject ['computerUse','tools']`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
