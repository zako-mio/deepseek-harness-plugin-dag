# dsh-file-reference-local

- 包名: `@deepseek-ai/dsh-file-reference-local`
- 分组: G08 上下文注入
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/context/file-reference-local`

## 实现逻辑
ctx.fileReferences 的本地文件系统实现 LocalFileReferenceService，继承 dsh-file-reference 的服务基类并以 WorkspaceFileSearch 对 agent 工作目录建立可取消/可复用的模糊索引（src/index.ts:44-127、src/search.ts:84-255）。索引只含路径；目录前缀查询走实时列举，裸模糊查询共享一次有界遍历，且失效时旧索引继续应答、重建在后台进行（src/search.ts:114-130、src/search.ts:159-199）。按 agent 生命周期安装/卸载 system-prompt 的 context:file-reference 段落与搜索缓存，并在 tool/result 时使缓存失效（src/index.ts:66-102）。

## Provides
- ctx.fileReferences (@file 引用的本地文件系统候选发现实现，供 @ 补全)
- system-prompt section context:file-reference (@ 引用使用说明段落，仅在 read 工具可用时展示)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 按 agent 维护搜索索引与提示词 fiber 生命周期，并用 agent 的会话 cwd 作为搜索根
  - 证据: `src/index.ts:9 import type Agent + src/index.ts:45 static inject ['agents'] + src/index.ts:91 ctx.agents.list + src/index.ts:92-93 ctx.on('agent/created'/'agent/disposed')`
- `dsh-session` [运行时依赖] - 订阅会话事件流以在工具结果提交后失效文件索引
  - 证据: `src/index.ts:98 ctx.on('session/event', ...) + src/index.ts:100 ctx.agents.get(session.id)`
- `dsh-tools` [E1+E2] - 仅在 read 工具存在时展示 @ 提示词，并在工具结果后使工作区索引失效
  - 证据: `src/index.ts:14 type-only import + src/index.ts:73 agent.ctx.tools.get('read', agent) + src/index.ts:98 ctx.on('session/event') tool-result invalidate`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
