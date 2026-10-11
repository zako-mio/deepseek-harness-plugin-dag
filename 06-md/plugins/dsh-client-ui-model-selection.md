# dsh-client-ui-model-selection

- 包名: `@deepseek-ai/dsh-client-ui-model-selection`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-model-selection`

## 实现逻辑
浏览器半围绕每会话一份的模型目录（ModelDirectoryResolver，ctx.modelDirectories）挂两个入口：/model 的 popupSelect 贡献与 composer 的 conversation.input.model 座位，两者共用同一份 session/modelCatalog 目录与 Session 的模型选择投影（src/client/index.ts:122-190、src/client/service.ts:47）。目录在 connection/reset 时失效（src/client/service.ts:50），选择经目录提交到 session.selectModel，并对 addressed subagent 会话隐藏两个入口（src/client/index.ts:134、src/client/index.ts:177）。

## Provides
- ctx.modelDirectories (每会话模型目录解析与选择提交) (src/client/service.ts:47)

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 拉取模型目录并提交选择
  - 证据: `src/client/directory.ts:11 import + src/client/catalog.ts:56 ctx.remote`
- `dsh-api-session-controller` [E1+E2] - 按会话寻址目录并判断 subagent
  - 证据: `src/client/index.ts:14 import type + src/client/service.ts:68 ctx.sessions`
- `dsh-client-locale` [E1+E2] - 注册 model 字典
  - 证据: `src/client/index.ts:21 import type + src/client/index.ts:116 ctx.locale.register(NS)`
- `dsh-client-product-analytics` [E1+E2] - 模型切换埋点
  - 证据: `src/client/directory.ts:7 import + src/client/service.ts:15 import`
- `dsh-client-ui-commands` [E1+E2] - 注册 /model 的 popupSelect 贡献
  - 证据: `src/client/index.ts:17 import type + src/client/index.ts:129 command.register({ name: 'model' … })`
- `dsh-client-ui-conversation` [编译依赖] - 占用 conversation.input.model 槽位声明
  - 证据: `src/client/index.ts:19 import type`
- `dsh-client-ui-primitives` [编译依赖] - 复用图标与基础控件
  - 证据: `src/client/index.ts:25 import + src/client/ModelSelect.tsx:28 import`
- `dsh-client-ui-renderer` [编译依赖] - 渲染器槽位服务类型
  - 证据: `src/client/index.ts:22 import type`
- `dsh-client-ui-session` [编译依赖] - 会话标准 seat 类型
  - 证据: `src/client/index.ts:23 import type`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/service.ts:19 import`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
