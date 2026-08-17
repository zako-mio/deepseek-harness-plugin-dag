# dsh-lsp-stdio

- 包名: `@deepseek-ai/dsh-lsp-stdio`
- 分组: G32 LSP集成
- 拓扑层: Layer 1
- 来源层: L3 其余
- 源码路径: `packages/lsp/lsp-stdio`

## 为什么需要它（设计初衷）
解决 agent 需要语言服务器能力却无法直接驱动 LSP 的问题：提供 ctx.lsp 的通用 stdio 语言服务器后端，按命名服务器表惰性 single-flight 启动独立服务器进程，以兼容性优先的「临时打开」序列（didOpen→操作→didClose）经 ctx.fs 读取源文件执行导航/hover 查询。其核心价值是把 LSP 变成通过 ctx.subprocess/ctx.fs 执行世界一致挂载的可组合服务，而不污染提示词或工具 schema。

发展史：位于 packages/lsp/lsp-stdio，与 lsp 抽象、tool-lsp 构成 LSP 子系统；定位为「通用宿主而非目录/安装器」，强调部署显式配置服务器映射，是 agent 获取类型感知能力的安全封装层。

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/lsp/lsp-stdio/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/lsp

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
