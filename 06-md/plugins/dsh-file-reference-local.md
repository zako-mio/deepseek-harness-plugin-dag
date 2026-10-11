# dsh-file-reference-local

- 包名: `@deepseek-ai/dsh-file-reference-local`
- 分组: G08 上下文注入
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/context/file-reference-local`

## 实现逻辑
以 ctx.fileReferences 的本地文件系统提供者身份实现文件引用发现：LocalFileReferenceService 继承 dsh-file-reference 的 Service Definition（src/index.ts:45），override 的 list() 先用 ctx.workingDirectory.ensure 解析 agent 的 cwd，cwd 变化时重建 WorkspaceFileSearch 有界模糊索引并按 agent 缓存（src/index.ts:116-129）。构造期对每个已存在与新建 agent 通过 agent.ctx.inject(['systemPrompt','tools']) 注册名为 'context:file-reference' 的提示段，且仅当 read 工具在该 agent 可见时才渲染正文（src/index.ts:67-79）；agent/disposed 回收索引与 prompt fiber，tool/result 使索引失效（src/index.ts:94-103）。配置上限（maxResults/maxEntries/excludedDirectories）在构造期校验（src/index.ts:132-142）。

## Provides
- ctx.fileReferences（本地文件系统文件引用候选发现实现，src/index.ts:45-129）
- WorkspaceFileSearch 有界模糊索引与默认限额常量（src/search.ts:16-48、src/search.ts:84）
- 文件引用语法与提示常量再导出（FILE_REFERENCE_PROMPT、activeAtToken、formatFileMention，src/index.ts:31-32）

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 按 agent 维度维护搜索缓存与提示 fiber，并在 agent/created、agent/disposed 上挂载与回收
  - 证据: `src/index.ts:10 import type { Agent } from '@deepseek-ai/dsh-agent' + src/index.ts:46 static inject = ['agents', 'workingDirectory']`
- `dsh-system-prompt` [运行时依赖] - 向 agent 作用域的系统提示注册文件引用说明段，并复用其 FILE_REFERENCE 中央排序位
  - 证据: `src/index.ts:70 agent.ctx.inject(['systemPrompt', 'tools'], (scope) => ...) + src/index.ts:71 scope.systemPrompt.section({ name: 'context:file-reference', ... })`
- `dsh-tools` [运行时依赖] - 查询该 agent 可见的 read 工具，仅在有读取能力时才对模型暴露文件引用提示
  - 证据: `src/index.ts:74 agent.ctx.tools.get('read', agent) === undefined ? '' : FILE_REFERENCE_PROMPT + src/index.ts:15 import type {} from '@deepseek-ai/dsh-tools'`
- `dsh-working-directory` [E1+E2] - 取 agent 的工作目录作为索引根，并据此判断缓存是否需要重建
  - 证据: `src/index.ts:7 import type {} from '@deepseek-ai/dsh-working-directory' + src/index.ts:121 this.ctx.workingDirectory.ensure(agent, signal)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
