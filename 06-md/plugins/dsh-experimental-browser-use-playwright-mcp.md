# dsh-experimental-browser-use-playwright-mcp

- 包名: `@deepseek-ai/dsh-experimental-browser-use-playwright-mcp`
- 分组: G13 实验特性
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/experimental/browser-use-playwright-mcp`

## 实现逻辑
函数插件复用 browser-use runtime 的 `mountSessionMcp`，把 pinned Playwright MCP server 以 `--browser chromium` 挂到每个 live Session（src/index.ts:26-49）。为避免上游 `PLAYWRIGHT_MCP_*` 环境变量覆盖配置，先把同名变量清空；attach 模式用 `--cdp-endpoint`，launch 模式用 `--isolated`/`--headless`/`--executable-path`（src/index.ts:31-49）。

## Provides

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - 按 live Agent 建立 Session 作用域
  - 证据: `src/index.ts:12 inject ['browserUse','agents','tools','systemPrompt']`
- `dsh-system-prompt` [运行时依赖] - 在 system prompt 中声明浏览器能力
  - 证据: `src/index.ts:12 inject ['browserUse','agents','tools','systemPrompt']`
- `dsh-tools` [运行时依赖] - 把 MCP 工具注册进工具注册表
  - 证据: `src/index.ts:12 inject ['browserUse','agents','tools','systemPrompt']`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
