# dsh-lsp-stdio

- 包名: `@deepseek-ai/dsh-lsp-stdio`
- 分组: G32 LSP集成
- 拓扑层: Layer 1
- 来源层: L3 其余
- 源码路径: `packages/lsp/lsp-stdio`

## 实现逻辑
通用 stdio language-server 后端插件，为 ctx.lsp capability seam 提供服务：一个插件实例按命名表配置多条 server 命令并各注册独立 provider；每 provider 按 canonical workspace 懒启动/单飞一个 server 进程，服务 transient-open 查询(goToDefinition/findReferences/goToImplementation/hover)；源码经 ctx.fs 读取、进程经 ctx.subprocess 启动（local/remote 实现共享同一 host）。命名导出插件，effect 作用域生命周期，dispose 时从 ctx.lsp 注销并拆除全部 live server。

## Provides
- ctx.lsp 命名 provider 表(lsp-stdio)
- LspInstance/LspConnection
- framing(encodeMessage/MessageDecoder)/translate(normalizeLocations/hover/negotiatePositionEncoding) 工具
- transient-open 只读查询服务

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - assertNever 穷尽检查
  - 证据: `packages/lsp/lsp-stdio/src/translate.ts:15`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
