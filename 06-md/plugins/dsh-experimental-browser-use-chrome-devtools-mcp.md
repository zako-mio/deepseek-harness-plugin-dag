# dsh-experimental-browser-use-chrome-devtools-mcp

- 包名: `@deepseek-ai/dsh-experimental-browser-use-chrome-devtools-mcp`
- 分组: G13 实验特性
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/experimental/browser-use-chrome-devtools-mcp`

## 实现逻辑
函数插件（name/inject/Config/apply）复用 browser-use runtime 的 `mountSessionMcp`，把 pinned 的 Chrome DevTools MCP server 以「每个 live Session 一个进程」方式挂载（src/index.ts:25-41）。launch 模式追加 `--isolated`/`--headless`，attach 模式按 endpoint 形状追加 `--ws-endpoint` 或 `--browser-url`，并禁用 usage statistics；attach 时标记 exclusive（src/index.ts:29-41）。

## Provides

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - 按 live Agent 建立 Session 作用域
  - 证据: `src/index.ts:11 inject ['browserUse','agents','tools','systemPrompt']`
- `dsh-system-prompt` [运行时依赖] - 在 system prompt 中声明浏览器能力
  - 证据: `src/index.ts:11 inject ['browserUse','agents','tools','systemPrompt']`
- `dsh-tools` [运行时依赖] - 把 MCP 工具注册进工具注册表
  - 证据: `src/index.ts:11 inject ['browserUse','agents','tools','systemPrompt']`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
