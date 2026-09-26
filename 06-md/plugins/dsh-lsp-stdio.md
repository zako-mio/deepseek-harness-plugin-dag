# dsh-lsp-stdio

- 包名: `@deepseek-ai/dsh-lsp-stdio`
- 分组: G24 LSP 集成
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/lsp/lsp-stdio`

## 实现逻辑
通用 stdio 语言服务器后端：apply() 先经 ctx.subprocess.resolveExecutable 解析每个配置项的可执行文件，再为每个条目构造 LocalLspProvider 并通过 ctx.lsp.registerProvider 注册，注册失败逆序回滚（src/index.ts:126-186）。每个 Provider 按规范工作区单一实例池化，经 ctx.fs 读源码、经 ctx.subprocess 惰性拉起进程并服务只读查询，选中传输在下次查询前或期间故障时透明替换一次（src/index.ts:216-380、src/host.ts:32-120）。LspInstance 拥有 initialize 握手、串行队列、瞬时 didOpen→request→didClose 与有界 teardown（src/instance.ts:110-320）；LspConnection 实现 Content-Length 分帧 JSON-RPC 与 id 关联（src/connection.ts:66-317、src/framing.ts:30-87）。

## Provides
- ctx.lsp (stdio 本地语言服务器 Provider 实现：按 provider id 注册、每规范工作区惰性单飞一个进程并服务只读查询，src/index.ts:171-185)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
