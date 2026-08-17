# dsh-client-ui-directory-picker-native

- 包名: `@deepseek-ai/dsh-client-ui-directory-picker-native`
- 分组: G29 UI底座
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-directory-picker-native`

## 为什么需要它（设计初衷）
原生系统目录选择对话框的浏览器半边，经 ui-workspace 的 directoryFlow 洞驱动 host.pickDirectory，回报选中路径/取消/失败。

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/client/ui-directory-picker-native/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/host/directory-picker-native

## 实现逻辑
目录选择 native 前端（renderless）。NativeDirectoryFlow 以嵌套 slots.inject 事务性注册进 conversation.hero.workspace.directoryFlow 与 sidebar.workspaces.directoryFlow 两个洞；无渲染，每次 open 驱动 host 的 workspaces.pickDirectory（OS 选择器）并把唯一结果（picked path/取消/失败）回报 owner conversation。

## Provides
- conversation.hero.workspace.directoryFlow 条目(NativeDirectoryFlow, renderless)
- sidebar.workspaces.directoryFlow 条目(NativeDirectoryFlow, renderless)

## Depends On (上游依赖)
- `dsh-client-runtime` [运行时依赖] - host 原生目录选择原语（dsh-host-directory-picker-native node 半）
  - 证据: `index.ts:18 inject 'workspaces' + index.ts:27 ctx.workspaces.pickDirectory() + contract/workspaces.ts:41`
- `dsh-client-ui-slots` [编译依赖] - slot 注册 API
  - 证据: `index.ts:31-39 ctx.slots.inject/register`
- `dsh-client-ui-workspace` [编译依赖] - 消费 directoryFlow 洞声明
  - 证据: `index.ts:12 type-only ui-workspace/client + index.ts:31-39 注册两处洞 + package.json:35 dsh.client.inject`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
