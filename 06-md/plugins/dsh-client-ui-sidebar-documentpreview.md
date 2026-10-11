# dsh-client-ui-sidebar-documentpreview

- 包名: `@deepseek-ai/dsh-client-ui-sidebar-documentpreview`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-sidebar-documentpreview`

## 实现逻辑
以「扩展注册表 + 八个渲染器」实现可扩展文档预览：Host 半 src/index.ts:13-16 监听 webserver/index-inject，把经 schemastery 校验的 Config 以 __DSH_DOCUMENT_PREVIEW_CONFIG__ 注入浏览器页面；浏览器半 client/index.ts:88-130 的 apply 先 ctx.reflect.provide('documentPreviews', previews)（:91）提供注册表，再注册 text 类型（:93）与键控 sidebar.right.pane.tab / title 槽（:103-121），最后依次调用 text/markdown/html/image/pdf/office/excel/code 八个渲染器的 apply（:122-129）。document/contract.ts:48-95 声明 sidebar.right.tab.document（键控渲染器体）、.actions、.unpreviewable、.action 四个槽，渲染器各自向 ctx.documentPreviews 注册（如 html/index.ts:30）。

## Provides
- ctx.documentPreviews (按文件后缀注册文档渲染器的扩展注册表，供各格式实现注册)
- sidebarRightTabs 标签类型 text（预览宿主类型）
- 槽位 sidebar.right.tab.document / sidebar.right.tab.document.actions / sidebar.right.tab.document.unpreviewable / sidebar.right.tab.document.action

## Depends On (上游依赖)
- `dsh-api-gateway` [编译依赖] - 拉入网关客户端的 Context/类型合并以承载远程调用面
  - 证据: `src/client/index.ts:20 import type {} from '@deepseek-ai/dsh-api-gateway/client'`
- `dsh-api-remotes` [E1+E2] - 分页文本与字节读取走 Remote 载体
  - 证据: `src/client/rpc.ts:9 import type { RemoteResult } from '@deepseek-ai/dsh-api-remotes/client'; src/client/index.ts:98-99 ctx.remote / ctx.remote.workspaceFiles`
- `dsh-api-workspace-files` [E1+E2] - 按 session+path 读取工作区文件字节与文本页
  - 证据: `src/client/rpc.ts:11 import type { WorkspaceFileBytes, WorkspaceFileRange, WorkspaceFileText } from '@deepseek-ai/dsh-api-workspace-files/types'; src/client/index.ts:99 ctx.remote.workspaceFiles.readBytes`
- `dsh-client-locale` [E1+E2] - 各格式渲染器的标题与失败文案由 locale 拥有
  - 证据: `src/client/index.ts:15 import type {} from '@deepseek-ai/dsh-client-locale/client'; src/client/index.ts:94 ctx.locale.register(NS, { zh, en })`
- `dsh-client-resources` [E1+E2] - 预览把依赖文件注册为资源并按引用计数回收
  - 证据: `src/client/face.ts:25 import type { Resources } from '@deepseek-ai/dsh-client-resources/client'; src/client/index.ts:100 ctx.resources`
- `dsh-client-ui-dockkit` [编译依赖] - 标签生命周期与 TabId 身份来自 dockkit
  - 证据: `src/client/document/tab-lifetime.ts:3 import ... from '@deepseek-ai/dsh-client-ui-dockkit'`
- `dsh-client-ui-primitives` [编译依赖] - 加载指示、缩放控件等复用共享原语
  - 证据: `src/client/LoadingIndicator.tsx:4 import ... from '@deepseek-ai/dsh-client-ui-primitives'`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 服务与槽渲染由 renderer 提供
  - 证据: `src/client/index.ts:17 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-session` [编译依赖] - 拉入 uiSession 合并，预览按会话作用域
  - 证据: `src/client/index.ts:18 import type {} from '@deepseek-ai/dsh-client-ui-session/client'`
- `dsh-client-ui-settings` [E1+E2] - HTML 预览的交互开关读 settings 提供的 configForms
  - 证据: `src/client/html/index.ts:8 import type {} from '@deepseek-ai/dsh-client-ui-settings/client'; src/client/html/index.ts:35 ctx.configForms.developerTools.enabled`
- `dsh-client-ui-sidebar-right` [E1+E2] - 预览类型与键控槽均由 sidebar-right 声明
  - 证据: `src/client/document/contract.ts:3 import type {} from '@deepseek-ai/dsh-client-ui-sidebar-right/client'; src/client/index.ts:93 ctx.sidebarRightTabs.register`
- `dsh-host-webserver` [E1+E2] - Host 半把预览配置注入浏览器页面索引
  - 证据: `src/index.ts:3 import type {} from '@deepseek-ai/dsh-host-webserver'; src/index.ts:14 ctx.on('webserver/index-inject', ...)`
- `dsh-office-to-pdf` [E1+E2] - Office 文档经 Host 转换服务生成 PDF 后再预览
  - 证据: `src/client/office/cache.ts:2 import type { OfficeToPdfPriority, OfficeToPdfGeneration } from '@deepseek-ai/dsh-office-to-pdf/types'; src/client/office/index.ts:5 import ... from '@deepseek-ai/dsh-office-to-pdf/remote'`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/face.ts:21 import type { SessionId } from '@deepseek-ai/dsh-session/types'`

## Dependents (下游被依赖)
- `dsh-client-ui-chat` - 文件预览参数类型
- `dsh-client-ui-open-in-app` - 接入文档预览标签动作
