# dsh-client-ui-open-in-app

- 包名: `@deepseek-ai/dsh-client-ui-open-in-app`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-open-in-app`

## 实现逻辑
浏览器半把「用本机应用打开」的统一控件挂到多个位置：会话头的 utilities、右侧栏 files/document 标签动作、deliverables 与 review 的文件动作（src/client/index.ts:102-134）。它维护应用列表与当前选择（OpenInAppController）、桌面文件应用查询与打开（OpenInAppPathController 经 ctx.remote），并注册 workspace.openLocal 快捷键按当前布局与会话解析目标（src/client/index.ts:51-83）。

## Provides

## Depends On (上游依赖)
- `dsh-api-gateway` [编译依赖] - 网关 Remote 类型
  - 证据: `src/client/index.ts:18 import type`
- `dsh-api-remotes` [E1+E2] - 查询可用应用并执行原生打开
  - 证据: `src/client/index.ts:19 import type + src/client/index.ts:53 ctx.remote`
- `dsh-api-session-controller` [编译依赖] - 会话与远程调用类型
  - 证据: `src/client/index.ts:20 import type + src/client/open-path.ts:7 import`
- `dsh-client-locale` [E1+E2] - 注册 open-in-app 字典
  - 证据: `src/client/index.ts:11 import + src/client/index.ts:54 ctx.locale.register(NS)`
- `dsh-client-shortcuts` [E1+E2] - 注册打开工作区快捷键
  - 证据: `src/client/OpenInAppAction.tsx:5 import + src/client/index.ts:63 ctx.shortcuts.register`
- `dsh-client-ui-conversation` [编译依赖] - 占用会话头槽位声明
  - 证据: `src/client/index.ts:15 import type`
- `dsh-client-ui-deliverables` [编译依赖] - 接入交付文件动作槽位
  - 证据: `src/client/FileRouteAction.tsx:3 import`
- `dsh-client-ui-layout` [E1+E2] - 按当前主面板判断是否可打开
  - 证据: `src/client/index.ts:13 import type + src/client/index.ts:57 ctx.layout.panelInfo`
- `dsh-client-ui-primitives` [编译依赖] - 失败提示控件
  - 证据: `src/client/open-failure-toast.tsx:4 import`
- `dsh-client-ui-renderer` [编译依赖] - 渲染器槽位服务类型
  - 证据: `src/client/index.ts:12 import type`
- `dsh-client-ui-session` [编译依赖] - 会话标准 seat 类型
  - 证据: `src/client/index.ts:14 import type`
- `dsh-client-ui-sidebar-documentpreview` [编译依赖] - 接入文档预览标签动作
  - 证据: `src/client/OpenPathAction.tsx:7 import + src/client/index.ts:16 import type`
- `dsh-client-ui-sidebar-files` [编译依赖] - 占用文件标签动作槽位声明
  - 证据: `src/client/index.ts:17 import type`
- `dsh-host-open-in-app` [编译依赖] - 复用应用图标路由常量
  - 证据: `src/client/index.ts:21 import`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
