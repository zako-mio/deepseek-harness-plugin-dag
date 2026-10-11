# dsh-client-ui-settings-session-log

- 包名: `@deepseek-ai/dsh-client-ui-settings-session-log`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 12
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-session-log`

## 实现逻辑
会话日志上传开关的 General 设置行。apply 取 session-log-deepseek 命名空间的配置表单构造 UploadPreference，并只在 Host 仍服务该命名空间时把 UploadRow 注册进 settings.general.item（order 90）(src/client/index.ts:29-37)。写入是单飞的：busy 期间直接返回，接受与否分别发布 saved/failed 通知且不发布乐观上传态 (src/client/upload-preference.ts:30-44)。同一 mutation 状态另注册一个 shell.overlay 的 Toast，使保存结果在设置面板关闭后仍然可见 (src/client/index.ts:38-40, src/client/UploadRow.tsx:45-49)。开关在表单未 ready、不可写或写入进行中时禁用 (src/client/UploadRow.tsx:34-36)。Host 半是空 apply，仅为让 Loader 寻址本包 (src/index.ts:4)。

## Provides

## Depends On (上游依赖)
- `dsh-client-locale` [E1+E2] - 注册 settings.sessionLog 字典并作为两个槽的 locale 命名空间
  - 证据: `src/client/index.ts:3 import type {} from '@deepseek-ai/dsh-client-locale/client' + src/client/index.ts:28 ctx.locale.register(locale, { en, zh })`
- `dsh-client-ui-layout` [编译依赖] - Toast 注册进 layout 声明的 shell.overlay 槽（槽位声明依赖）
  - 证据: `src/client/index.ts:5 import type {} from '@deepseek-ai/dsh-client-ui-layout/client'`
- `dsh-client-ui-primitives` [编译依赖] - 设置行与提示复用共享的开关与 Toast 原语
  - 证据: `src/client/UploadRow.tsx:2 import Switch/Toast + package.json:52 devDependencies`
- `dsh-client-ui-renderer` [编译依赖] - 拉入 SlotRegistry 服务合并，使槽注册在此编译单元可用
  - 证据: `src/client/index.ts:6 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-settings` [E1+E2] - 上传开关的读写经共享配置表单，并以 whileServed 判定命名空间是否被服务
  - 证据: `src/client/index.ts:4 import type {} from '@deepseek-ai/dsh-client-ui-settings/client' + src/client/index.ts:29 ctx.configForms.get<UploadSettings>(namespace)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
