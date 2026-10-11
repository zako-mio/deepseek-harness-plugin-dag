# dsh-host-directory-picker-auto

- 包名: `@deepseek-ai/dsh-host-directory-picker-auto`
- 分组: G19 宿主服务
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/host/directory-picker-auto`

## 实现逻辑
在启动时一次性采样宿主事实，据此把目录选择接缝的一个交互（host backend 加 client surface 一对）作为真实 Loader 条目挂入内存根树 (src/index.ts:69-111)。resolveDirectoryPickerBackend 是纯函数：只要允许远程权威、绑定非 loopback、经 SSH 启动、或平台不是 darwin/win32 且缺少 Linux chooser 二进制或显示会话，就退化为 browse，其余为 native (src/resolve.ts:55-60)；probe.ts 用 accessSync(X_OK) 扫描 PATH 上的 zenity/kdialog (src/probe.ts:36-43)。挂载顺序为先 backend 后 surface，任一步失败即逆序卸载已建条目，effect 的 disposer 连同其 fiber 一并拆除 (src/index.ts:78-111)。

## Provides
- 启动期目录选择交互的自动装配（按宿主事实挂载 native 或 browse 的 host backend 与 client surface 条目）
- BACKEND_PACKAGES / SURFACE_PACKAGES 常量（供 verify-cordis-config 静态校验组合依赖）
- resolveDirectoryPickerBackend / canExecute / hasLinuxChooserBinary 的再导出

## Depends On (上游依赖)
- `cordis-plugin-loader` [E1+E2] - 把选中的交互以真实 Loader 条目挂载，使客户端界面按普通配置行被发现
  - 证据: `src/index.ts:18 import type {} from '@deepseek-ai/cordis-plugin-loader' + src/index.ts:97 ctx.loader.create({ name })`
- `dsh-client-connection` [E1+E2] - 信任策略允许非 loopback 权威时，远程浏览器无法到达宿主 OS 选择器，必须走 browse
  - 证据: `src/index.ts:19 import type {} from '@deepseek-ai/dsh-client-connection' + src/index.ts:72 ctx.connection.allowsRemoteAuthorities`
- `dsh-client-ui-directory-picker-browse` [E1+E3] - 与 browse 后端配对挂载的客户端界面包
  - 证据: `src/index.ts:59 SURFACE_PACKAGES.browse + package.json:33 peerDependencies`
- `dsh-client-ui-directory-picker-native` [E1+E3] - 与 native 后端配对挂载的客户端界面包，保证一个选择同时换掉两面
  - 证据: `src/index.ts:58 SURFACE_PACKAGES.native + package.json:34 peerDependencies`
- `dsh-host-directory-picker-browse` [E1+E3] - browse 分支要挂载的宿主后端包
  - 证据: `src/index.ts:47 BACKEND_PACKAGES.browse + package.json:35 peerDependencies`
- `dsh-host-directory-picker-native` [E1+E3] - native 分支要挂载的宿主后端包（运行时按包名装配，非静态 import）
  - 证据: `src/index.ts:46 BACKEND_PACKAGES.native + package.json:36 peerDependencies + src/index.ts:97 ctx.loader.create({ name })`
- `dsh-host-webserver` [E1+E2] - 读取生效的绑定地址，并用 loopback 判定决定是否可能使用 native 选择器
  - 证据: `src/index.ts:20 import type {} from '@deepseek-ai/dsh-host-webserver' + src/resolve.ts:9 import isLoopbackHost + src/index.ts:71 ctx.webServer.host`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
