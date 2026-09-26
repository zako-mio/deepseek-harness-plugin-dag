# dsh-client-ui-directory-picker-native

- 包名: `@deepseek-ai/dsh-client-ui-directory-picker-native`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L3 其余
- 源码路径: `packages/client/ui-directory-picker-native`

## 实现逻辑
无渲染的原生目录流占位：apply 先读全局 globalThis.__DSH_DIRECTORY_PICKER__（Desktop preload 桥），存在则用 desktop.pick()，否则退回 ctx.uiWorkspace.pickDirectory() (src/client/index.ts:21-25)，再以 generator 事务式把 NativeDirectoryFlow 同时注册进 ui-workspace 的两个 directory-flow 洞 (src/client/index.ts:29-37)。组件本身返回 null，用 useRef 的 armed/alive 保证每次 open 上升沿只发起一次选取、只报告一次结果，卸载即整体丢弃结果 (src/client/flow.ts:25-64)。

## Provides
- slot: conversation.hero.workspace.directoryFlow (NativeDirectoryFlow 无渲染原生选择器占用)
- slot: sidebar.workspaces.directoryFlow (同上的侧边栏占位)
- 组件 NativeDirectoryFlow (每次 open 恰发起一次原生/Host 目录选取)

## Depends On (上游依赖)
- `dsh-client-ui-renderer` [运行时依赖] - 注册槽位占用
  - 证据: `src/client/index.ts:6 merge + src/client/index.ts:29 ctx.slots.inject`
- `dsh-client-ui-workspace` [E1+E2] - 占据目录流洞并驱动 Host OS 选择器
  - 证据: `src/client/flow.ts:9 DirectoryFlowOwnerProps + src/client/index.ts:24 ctx.uiWorkspace.pickDirectory`

## Dependents (下游被依赖)
- `dsh-host-directory-picker-auto` - native 交互的客户端界面条目
