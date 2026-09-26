# dsh-client-ui-directory-picker-browse

- 包名: `@deepseek-ai/dsh-client-ui-directory-picker-browse`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L3 其余
- 源码路径: `packages/client/ui-directory-picker-browse`

## 实现逻辑
浏览器半把应用内「选择工作区目录」对话框装进 ui-workspace 的两个 directory-flow 洞：apply 先事务式注册 zh/en 两份 directory-browser 字典（第二份失败则回滚第一份）(src/client/index.ts:32-76)，再用嵌套 slots.inject 加 generator 同时向 'conversation.hero.workspace.directoryFlow' 与 'sidebar.workspaces.directoryFlow' 注册同一个 BrowseDirectoryFlow (src/client/index.ts:86-94)。注入面把洞的 owner 会话适配到对话框：确认目录即 onPicked、关闭即 onCancel，listDirectory/createDirectory 转发 ctx.uiWorkspace (src/client/flow.ts:24-43, src/client/index.ts:78-82)。

## Provides
- slot: conversation.hero.workspace.directoryFlow (BrowseDirectoryFlow 应用内目录浏览对话框)
- slot: sidebar.workspaces.directoryFlow (同一对话框在侧边栏工作区流的占位)
- Locale 命名空间 directory-browser (zh/en 字典)
- 组件 DirectoryBrowser (应用内目录浏览/新建文件夹对话框)

## Depends On (上游依赖)
- `dsh-api-remotes` [编译依赖] - 目录列举结果类型
  - 证据: `src/client/DirectoryBrowser.tsx:43 import DirectoryListing from @deepseek-ai/dsh-api-remotes/client + src/client/flow.ts:8`
- `dsh-client-locale` [运行时依赖] - 注册并绑定对话框字典
  - 证据: `src/client/DirectoryBrowser.tsx:44 Translate + src/client/index.ts:70 ctx.locale.register`
- `dsh-client-ui-renderer` [运行时依赖] - 注册槽位占用
  - 证据: `src/client/index.ts:15 merge + src/client/index.ts:86 ctx.slots.inject`
- `dsh-client-ui-workspace` [E1+E2] - 占据目录流洞并驱动枚举/创建原语
  - 证据: `src/client/flow.ts:11 DirectoryFlowOwnerProps + src/client/index.ts:79-80 ctx.uiWorkspace.listDirectory/createDirectory`

## Dependents (下游被依赖)
- `dsh-host-directory-picker-auto` - browse 交互的客户端界面条目
