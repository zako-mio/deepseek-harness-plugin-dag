# dsh-office-to-pdf

- 包名: `@deepseek-ai/dsh-office-to-pdf`
- 分组: G12 文档处理
- 拓扑层: Layer 6
- 来源层: L2 web-app
- 源码路径: `packages/document/office-to-pdf`

## 实现逻辑
`OfficeToPdf` 继承 `TypertRemoteService`（服务名 officeToPdf），用 LibreOffice kit 把 Office 文档转 PDF：私有临时目录写入输入、`createConverter` 渲染，并对输出做大小上限与 `%PDF`/`%%EOF` 结构校验（src/index.ts:233-277、src/output.ts:13-39）。`ConversionQueue` 做有界准入、按内容 sha256 去重与 LRU 缓存、foreground/background 优先级、reader 取消与源字节预留（src/queue.ts:51-232）。`@Remote render()` 经 `workspaceFiles` 授权读取源文件、以 version 校验源未变，并把失败映射为稳定的 RemoteError（src/index.ts:159-231）。

## Provides
- ctx.officeToPdf (Office→PDF 转换与授权工作区文件渲染服务)
- Remote 域 officeToPdf (render/generation)

## Depends On (上游依赖)
- `dsh-api-workspace-files` [E1+E2] - 按 Session 授权读取/校验源文件元数据
  - 证据: `src/types.ts:2 import WorkspaceFileBytes + src/index.ts:9 import + src/index.ts:187 ctx.get('workspaceFiles')`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配 office-to-pdf 命名空间
- `dsh-client-ui-sidebar-documentpreview` - office 文档转 PDF 渲染
