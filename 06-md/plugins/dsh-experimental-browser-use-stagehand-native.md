# dsh-experimental-browser-use-stagehand-native

- 包名: `@deepseek-ai/dsh-experimental-browser-use-stagehand-native`
- 分组: G13 实验特性
- 拓扑层: Layer 7
- 来源层: L3 其余
- 源码路径: `packages/experimental/browser-use-stagehand-native`

## 实现逻辑
以 `SessionResources` 为每个 live Session 惰性拥有一个原生 Stagehand 浏览器运行时（launch 模式先 `launchChromium` 再连 CDP，attach 模式独占已有端点），并注册 `stagehand_navigate/tabs/screenshot/act/observe/extract` 工具（src/index.ts:84-164、166-209）。工具执行经 `tools/execute` 绑定到确切 live Agent，把调用方 signal 与 operation signal 串接后再走下一层（src/index.ts:192-209）；原生操作在 worker 内以 SDK `localBrowser.connect`+`Stagehand.create` 实现，含截图/自然语言 action（src/native.ts:95-159）。

## Provides

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 按 owner Agent 隔离浏览器运行时并注入 initiator
  - 证据: `src/index.ts:16 import type {} from '@deepseek-ai/dsh-agent' + src/index.ts:25 inject + src/index.ts:185 requireInitiator`
- `dsh-mcp-client` [编译依赖] - 把原生方法适配为 MCP 形状的工具定义
  - 证据: `src/index.ts:10 import createMcpToolDefinition + src/index.ts:179 createMcpToolDefinition`
- `dsh-system-prompt` [E1+E2] - 注入 Stagehand 使用与安全 guidance
  - 证据: `src/index.ts:18 import type {} + src/index.ts:25 inject + src/index.ts:191 systemPrompt.section`
- `dsh-tools` [E1+E2] - 注册浏览器工具并接管其执行信号
  - 证据: `src/index.ts:19 import type {} + src/index.ts:25 inject + src/index.ts:179 tools.register + src/index.ts:192 tools/execute`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
