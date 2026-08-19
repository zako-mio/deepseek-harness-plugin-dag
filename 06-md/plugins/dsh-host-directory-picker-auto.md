# dsh-host-directory-picker-auto

- 包名: `@deepseek-ai/dsh-host-directory-picker-auto`
- 分组: G25 宿主服务
- 拓扑层: Layer 1
- 来源层: L2 web-app
- 源码路径: `packages/host/directory-picker-auto`

## 为什么需要它（设计初衷）
目录选择 seam 的自适应选择器：启动时一次采样判定 native/browse 后端并动态挂载，保证交互一致性。

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/host/directory-picker-auto/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/notes/implemented/architecture/2026-07-28-directory-picker-capability-seam.md

## 实现逻辑
启动一次采样 bind host/平台/display/Linux chooser 解析交互类型（native|browse），经 ctx.loader.create 把对应后端包（BACKEND_PACKAGES）+客户端 UI 包（SURFACE_PACKAGES）作为真实 Loader 条目挂入内存根树，卸载时按逆序 remove；不动配置树。

## Provides
- 挂载 directoryPicker 后端（native|browse）+ 对应客户端 surface 为 Loader 条目

## Depends On (上游依赖)
- `dsh-host-webserver` [编译依赖] - Context merge（ctx.webServer）
  - 证据: `packages/host/directory-picker-auto/package.json:41; src/index.ts:17`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
