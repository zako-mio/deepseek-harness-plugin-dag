# dsh-client-ui-settings-subagent

- 包名: `@deepseek-ai/dsh-client-ui-settings-subagent`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-subagent`

## 实现逻辑
Subagent 设置页（浏览器半）。apply 同时为 subagent（递归深度与并行容量）与 subagent-model-selection-settings（可选子模型白名单）两个命名空间建控制器，任一被服务即把 subagent 页注册进 plugins.item（order 10），并用 subagentCardFace 把两个 face 合成一个注入面 (src/client/index.ts:59-92)。模型目录不属任何 settings 段，因此额外订阅 llm/adapters-updated、settings/document-updated 与 connection/reset 来刷新目录或重置连接代际 (src/client/index.ts:72-83)。模型选择控制器把适配器目录与已存路由做 join，逐行标记 available/selected 并处理 revision 冲突 (src/client/subagent-model-selection-card-controller.ts:26-51)。Host 半是空 apply，两个命名空间分别由委派类插件注册 (src/index.ts:10)。

## Provides

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 模型目录读取与三类推送失效订阅都经 Remote 事件面
  - 证据: `src/client/index.ts:18 import type {} from '@deepseek-ai/dsh-api-remotes/client' + src/client/index.ts:73 ctx.remote.$on('llm/adapters-updated', ...)`
- `dsh-client-locale` [E1+E2] - 注册 settings.subagent 字典并按命名空间绑定翻译
  - 证据: `src/client/index.ts:10 import type {} from '@deepseek-ai/dsh-client-locale/client' + src/client/index.ts:60-61 ctx.locale.bind(NS) / ctx.locale.register(NS, { zh, en })`
- `dsh-client-ui-plugin-manager` [E1+E2] - 页面必须注册进 Plugins 页声明的 plugins.item 槽
  - 证据: `src/client/SubagentCard.tsx:5 import type {} from '@deepseek-ai/dsh-client-ui-plugin-manager/client' + src/client/index.ts:85 ctx.slots.inject('plugins.item', ...)`
- `dsh-client-ui-primitives` [编译依赖] - 设置页与字段复用共享表单控件及其暂存模型类型
  - 证据: `src/client/SubagentCard.tsx:6 import SettingsForm + src/client/subagent-model-selection-card-controller.ts:6 import SettingsFormScope/SettingsFormShell + package.json:54 devDependencies`
- `dsh-client-ui-renderer` [编译依赖] - 拉入 SlotRegistry 服务合并，使槽注册与 slots.inject 在此编译单元可用
  - 证据: `src/client/index.ts:16 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-settings` [E1+E2] - 两个命名空间的共享配置表单读写与 whileServed 判定都经该服务
  - 证据: `src/client/index.ts:13 import type {} from '@deepseek-ai/dsh-client-ui-settings/client' + src/client/index.ts:62 ctx.configForms.get(SUBAGENT_NS)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
