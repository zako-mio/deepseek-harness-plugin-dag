# dsh-host-directory-picker-auto

- 包名: `@deepseek-ai/dsh-host-directory-picker-auto`
- 分组: G20 宿主服务
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/host/directory-picker-auto`

## 实现逻辑
在 apply() 中一次性采样宿主事实（绑定的 ctx.webServer.host、process.platform、SSH 启动、DISPLAY/WAYLAND_DISPLAY 与 Linux chooser 二进制），经 resolveDirectoryPickerBackend 纯函数判定该用 native 还是 browse 交互（src/index.ts:62-69、src/resolve.ts:49-55）。随后用 ctx.loader.create 把该交互的宿主后端包与客户端界面包作为真实 Loader 条目挂到内存根树，并按逆序 dispose 卸载（src/index.ts:70-103）。probe.ts 提供 canExecute/hasLinuxChooserBinary 探测 Linux 的 zenity/kdialog（src/probe.ts:20-44）。

## Provides
- 自适应目录选择交互装配（按宿主事实在 loader 根树挂载 native/browse 的后端+客户端条目对，src/index.ts:88-94）

## Depends On (上游依赖)
- `dsh-client-ui-directory-picker-browse` [E1+E2] - browse 交互的客户端界面条目
  - 证据: `package.json:32 peerDep + src/index.ts:52 SURFACE_PACKAGES.browse; src/index.ts:89 ctx.loader.create`
- `dsh-client-ui-directory-picker-native` [E1+E2] - native 交互的客户端界面条目
  - 证据: `package.json:33 peerDep + src/index.ts:51 SURFACE_PACKAGES.native; src/index.ts:89 ctx.loader.create`
- `dsh-host-directory-picker-browse` [E1+E2] - browse 交互的宿主后端条目
  - 证据: `package.json:34 peerDep + src/index.ts:40 BACKEND_PACKAGES.browse; src/index.ts:89 ctx.loader.create`
- `dsh-host-directory-picker-native` [E1+E2] - native 交互的宿主后端条目
  - 证据: `package.json:35 peerDep + src/index.ts:39 BACKEND_PACKAGES.native; src/index.ts:89 ctx.loader.create`
- `dsh-host-webserver` [E1+E2] - 读取生效绑定 host 作为后端判定事实
  - 证据: `package.json:36 peerDep + src/index.ts:17 type import; src/index.ts:64 ctx.webServer.host`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
