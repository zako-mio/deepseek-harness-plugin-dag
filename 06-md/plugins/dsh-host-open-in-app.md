# dsh-host-open-in-app

- 包名: `@deepseek-ai/dsh-host-open-in-app`
- 分组: G20 宿主服务
- 拓扑层: Layer 3
- 来源层: L2 web-app
- 源码路径: `packages/host/open-in-app`

## 实现逻辑
在 webServer 上注册 apps/icon/open 三条路由：每个请求先经 connection.requestRejection 的 Host/Origin 与浏览器鉴权栅栏，open 路由再对 JSON body 做 64KiB、字段、绝对路径与目录存在性校验（src/index.ts:138-310）。catalog.ts 为纯数据表，resolver.ts 用各平台定位器链把条目解析为宿主上已核验的启动器并惰性缓存一次（src/resolver.ts:604-662、src/index.ts:154-157）。启动经 launchDetachedApp 以凭据擦洗环境分离 spawn，ENOENT 时刷新该条目并重试一次（src/resolver.ts:74-96、src/index.ts:295-303）。icons.ts 按平台抽取图标（src/icons.ts:143-161）。

## Provides
- webServer 路由 (open-in-app 应用目录/图标/启动端点，src/index.ts:193-310)

## Depends On (上游依赖)
- `dsh-client-connection` [运行时依赖] - 每条路由的信任栅栏与浏览器鉴权
  - 证据: `src/index.ts:47 inject=['webServer','connection','subprocess'] + src/index.ts:186 ctx.connection.requestRejection`
- `dsh-host-webserver` [E1+E2] - 承载 apps/icon/open 三条路由
  - 证据: `package.json:50 devDep + src/index.ts:27 type import; src/index.ts:193/206/241 ctx.webServer.register`

## Dependents (下游被依赖)
- `dsh-client-ui-open-in-app` - 复用 Host 侧共用的图标路由前缀常量
