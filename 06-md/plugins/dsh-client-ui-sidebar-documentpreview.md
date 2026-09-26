# dsh-client-ui-sidebar-documentpreview

- 包名: `@deepseek-ai/dsh-client-ui-sidebar-documentpreview`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-sidebar-documentpreview`

## 实现逻辑
浏览器半把 `text` tab 类型注册进 `ctx.sidebarRightTabs`（src/client/index.ts:93），并新建 DocumentPreviewRegistry 经 `ctx.reflect.provide('documentPreviews', ...)` 暴露为扩展点 seam（src/client/index.ts:90-92、54-58）。主体经键控槽 `sidebar.right.pane.tab` 注册 TextPreview 并声明 document 系列子槽（src/client/index.ts:103-117），标题经 `sidebar.right.pane.tab.title` 注册 TextTitle（src/client/index.ts:118-121）。随后依次装配 text/markdown/html/image/pdf/office/excel/code 八类渲染器（src/client/index.ts:122-129），每类都把定义注册进 documentPreviews 并注册 keyed 文档主体（如 src/client/code/index.ts:15-25）。node half 在 `webserver/index-inject` 时把校验过的预览配置注入页面全局（src/index.ts:14-16）。

## Provides
- sidebarDocumentPreview locale 命名空间字典
- ctx.documentPreviews（文件扩展名 → 文档渲染器定义注册表 seam，供各内建/外部预览类型注册）
- sidebarRightTabs 注册 'text' tab 类型定义（并扩展 SidebarRightResourceParamsMap.file 参数，src/client/index.ts:64-69）
- sidebar.right.pane.tab 键控条目 key=TEXTPREVIEW_ID：文档预览 body，声明 sidebar.right.tab.document / document.actions / document.unpreviewable / document.action 子槽
- sidebar.right.pane.tab.title 键控条目 key=TEXTPREVIEW_ID：预览标签标题
- 内建 8 类文档渲染器（text / markdown / html / image / pdf / office / excel / code）
- Host 侧页面全局 __DSH_DOCUMENT_PREVIEW_CONFIG__（预览缓存配置）

## Depends On (上游依赖)
- `dsh-api-gateway` [编译依赖] - 引入网关客户端面与其类型合并
  - 证据: `src/client/index.ts:20 import (client)`
- `dsh-api-remotes` [E1+E2] - 经 remote 面读取工作区文件字节与分页文本
  - 证据: `src/client/failure-line.ts:8 import (client) + src/client/index.ts:98 ctx.remote`
- `dsh-api-workspace-files` [编译依赖] - 工作区文件读取的类型与 remote 调用签名
  - 证据: `src/client/index.ts:21-22 import (/remote, /client) + src/client/document/resource-group.ts:3 import (/types)`
- `dsh-client-locale` [E1+E2] - 注册并绑定预览文案
  - 证据: `src/client/failure-line.ts:9 import + src/client/index.ts:94 ctx.locale.register`
- `dsh-client-resources` [E1+E2] - 借用资源模型登记/固定被预览的文件资源
  - 证据: `src/client/document/resource-group.ts:2 import (client) + src/client/index.ts:100 ctx.resources`
- `dsh-client-ui-dockkit` [编译依赖] - 标签生命周期与 dock 原语
  - 证据: `src/client/document/tab-lifetime.ts:3 import`
- `dsh-client-ui-primitives` [编译依赖] - 复用加载指示与代码高亮扩展名等共享原语
  - 证据: `src/client/LoadingIndicator.tsx:4 import + src/client/code/index.ts:3 import`
- `dsh-client-ui-renderer` [编译依赖] - 引入 ctx.slots 合并
  - 证据: `src/client/index.ts:17 type-only import`
- `dsh-client-ui-session` [编译依赖] - 引入会话标准 props 合并
  - 证据: `src/client/index.ts:18 type-only import`
- `dsh-client-ui-settings` [E1+E2] - html 预览经设置服务注册其配置表单
  - 证据: `src/client/html/index.ts:8 import (client) + src/client/html/index.ts:35 ctx.configForms`
- `dsh-client-ui-sidebar-right` [E1+E2] - 经两级公共路径把预览类型、body 与标题注册进右侧边栏
  - 证据: `src/client/definition.ts:11 import (client) + src/client/index.ts:93 ctx.sidebarRightTabs.register`
- `dsh-host-webserver` [E1+E2] - Host 侧向浏览器页面注入预览配置全局
  - 证据: `src/index.ts:3 type-only import + src/index.ts:14 ctx.on('webserver/index-inject')`
- `dsh-office-to-pdf` [编译依赖] - office 文档转 PDF 渲染
  - 证据: `src/client/office/cache.ts:2 import (/types) + src/client/office/index.ts:5 import (/remote)`
- `dsh-session` [编译依赖] - 会话 id 等类型
  - 证据: `src/client/face.ts:21 import (/types)`

## Dependents (下游被依赖)
- `dsh-client-ui-chat` - 文件行号导航参数类型
- `dsh-client-ui-open-in-app` - 使用文档预览声明的路径动作槽
