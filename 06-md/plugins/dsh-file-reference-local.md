# dsh-file-reference-local

- 包名: `@deepseek-ai/dsh-file-reference-local`
- 分组: G21 上下文治理
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/context/file-reference-local`

## 为什么需要它（设计初衷）
为@file引用seam提供本地文件系统实现，以有界索引保证性能与可取消性，同时按agent注入引用指引，使Web端@菜单能实时补全工作区路径。

发展史：RC8 新增

## 实现逻辑
ctx.fileReferences 的本地文件系统实现。src/index.ts:45 LocalFileReferenceService extends FileReferenceService(seam)，list 按agent懒建 WorkspaceFileSearch(以agent cwd为root)；构造函数为每个agent安装FILE_REFERENCE_PROMPT的systemPrompt section(仅在read工具存在时)，并监听agent/created、tool/result事件维护搜索缓存与失效。search.ts:49 WorkspaceFileSearch 提供可取消可复用的有界模糊索引(默认maxEntries=10000)。装配于 cordis.patch.yml:85-86(E3)。

## Provides
- ctx.fileReferences 本地实现(LocalFileReferenceService)
- 有界可取消WorkspaceFileSearch模糊索引
- 按agent的@file系统提示注入

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - 枚举agent并安装提示
  - 证据: `src/index.ts:46 static inject=['agents']`
- `dsh-file-reference` [编译依赖] - 实现seam抽象list契约
  - 证据: `src/index.ts:10-13 extends FileReferenceService`
- `dsh-system-prompt` [运行时依赖] - 注入@file模型指引
  - 证据: `src/index.ts:69-74 scope.systemPrompt.section`
- `dsh-tools` [运行时依赖] - 检测read工具决定是否注入提示
  - 证据: `src/index.ts:73 agent.ctx.tools.get('read')`

## Dependents (下游被依赖)
- `dsh-web-app` - web-app装配文件引用本地实现
