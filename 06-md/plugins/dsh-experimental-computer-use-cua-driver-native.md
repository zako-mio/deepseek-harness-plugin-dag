# dsh-experimental-computer-use-cua-driver-native

- 包名: `@deepseek-ai/dsh-experimental-computer-use-cua-driver-native`
- 分组: G13 实验特性
- 拓扑层: Layer 7
- 来源层: L3 其余
- 源码路径: `packages/experimental/computer-use-cua-driver-native`

## 实现逻辑
通过 in-process 原生 Cua Driver SDK 注册 `cua_driver_native__*` 工具：动态 `import('@trycua/cua-driver')`、`CuaDriver.create`、`listToolsJson` 解析工具目录并用 `createMcpToolDefinition` 适配（src/index.ts:88-118）。`tools/execute` 监听器把这些工具调用绑定到 lifetime signal 并跟踪 pending（src/index.ts:119-131），同时注册 computer-use systemPrompt guidance（src/index.ts:132-136）。卸载时 abort lifetime、等待 pending、`driver.shutdown()` 后 `uniffiDestroy()`（src/index.ts:59-78）。

## Provides

## Depends On (上游依赖)
- `dsh-mcp-client` [编译依赖] - 把原生工具目录适配为 MCP 形状工具定义
  - 证据: `src/index.ts:9 import createMcpToolDefinition + src/index.ts:103 createMcpToolDefinition`
- `dsh-system-prompt` [E1+E2] - 注入桌面操作 guidance 段落
  - 证据: `src/index.ts:13 import type {} from '@deepseek-ai/dsh-system-prompt' + src/index.ts:20 inject 'systemPrompt' + src/index.ts:132 systemPrompt.section`
- `dsh-tools` [E1+E2] - 注册原生工具并接管其执行信号
  - 证据: `src/index.ts:14 import type {} from '@deepseek-ai/dsh-tools' + src/index.ts:20 inject 'tools' + src/index.ts:117 tools.register + src/index.ts:119 tools/execute`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
