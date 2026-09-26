# dsh-client-ui-settings-subagent

- 包名: `@deepseek-ai/dsh-client-ui-settings-subagent`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-subagent`

## 实现逻辑
浏览器半把 Subagent 设置页注册进 `plugins.item`（id='subagent' order 30，src/client/index.ts:85-92），页面把委派上限控制器（绑 `subagent` 命名空间）与模型选择控制器（绑 `subagent-model-selection` 命名空间）合成一个注入面（src/client/index.ts:62-69、91）。它订阅 Host 推送的 `llm/adapters-updated` 与 `settings/document-updated` 事件刷新模型目录（src/client/index.ts:72-79），并在 `connection/reset` 时重置连接态（src/client/index.ts:80-83）。node half 为空 apply（src/index.ts:11）。

## Provides
- settings.subagent locale 命名空间字典
- plugins.item 槽位条目 id='subagent' (order 30)：子代理委派上限 + 可选模型选择设置卡片
- subagent-card-controller 合成的注入面（limits face 与 model selection face 合一，一份保存）

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 订阅 Host 推送的适配器/设置失效事件
  - 证据: `src/client/index.ts:18 type-only import + src/client/index.ts:73 ctx.remote.$on('llm/adapters-updated')`
- `dsh-client-locale` [E1+E2] - 注册并绑定本页文案
  - 证据: `src/client/index.ts:10 type-only import + src/client/index.ts:60 ctx.locale.bind(NS)`
- `dsh-client-ui-plugin-manager` [E1+E2] - Plugins 页拥有 plugins.item 槽位
  - 证据: `src/client/index.ts:15 type-only import + src/client/index.ts:86 向 plugins.item 注册`
- `dsh-client-ui-primitives` [编译依赖] - 复用共享设置字段原语
  - 证据: `src/client/SubagentLimitsFields.tsx:4 import + src/client/locales.ts:3 import`
- `dsh-client-ui-renderer` [编译依赖] - 引入 ctx.slots 合并
  - 证据: `src/client/index.ts:16 type-only import`
- `dsh-client-ui-settings` [E1+E2] - 经 configForms 取得两个命名空间的表单 scope
  - 证据: `src/client/index.ts:13 type-only import + src/client/index.ts:62-65 ctx.configForms.get(...)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
