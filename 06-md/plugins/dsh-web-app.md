# dsh-web-app

- 包名: `@deepseek-ai/dsh-web-app`
- 分组: G25 宿主服务
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/bundle/web-app`

## 为什么需要它（设计初衷）
dsh 浏览器表面 bundle：在 base 之上插入 Web host 行与浏览器插件册，提供 web-runtime。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/bundle/web-app/README.md

## 实现逻辑
双入口合并：web-startup（@deepseek-ai/dsh-web-app/startup）解析 --host/--port/--trusted-host 后 ctx.provide webStartup 服务；web-runtime（主插件）解析前端 dist（@deepseek-ai/dsh-web-frontend），ctx.plugin(FrontendStatic) 挂 fallback 兜底，注册 app:web-surface prompt 段与 DSH_WEB_URL shell 变量，采样 LAN 信任后提供 webRuntime，Loader 就绪后打印 URL 行。

## Provides
- webStartup 服务（web-startup 入口）
- webRuntime 服务（web-runtime 入口）
- app:web-surface prompt 段
- DSH_WEB_URL bash 变量
- frontend-static fallback 兜底
- URL 就绪行

## Depends On (上游依赖)
- `dsh-client-ui-attachment` [组合依赖] - web-app装配附件UI
  - 证据: `cordis.patch.yml:212-218 ui-attachment装配`
- `dsh-client-ui-brand-official` [组合依赖] - web-app装配官方品牌
  - 证据: `cordis.patch.yml:213-214 装配`
- `dsh-client-ui-reference` [组合依赖] - web-app装配@引用UI
  - 证据: `cordis.patch.yml:253-255 装配`
- `dsh-client-ui-renderer` [组合依赖] - web-app装配渲染器
  - 证据: `cordis.patch.yml:191-192 装配`
- `dsh-file-reference` [组合依赖] - web-app装配文件引用seam
  - 证据: `cordis.patch.yml:84-86 装配`
- `dsh-file-reference-local` [组合依赖] - web-app装配文件引用本地实现
  - 证据: `cordis.patch.yml:85-86 装配`
- `dsh-host-webserver` [编译依赖] - Context merge（ctx.webServer）
  - 证据: `packages/bundle/web-app/src/index.ts:21`
- `dsh-session-reference` [组合依赖] - web-app装配会话引用
  - 证据: `cordis.patch.yml:82-83 装配`
- `dsh-shell-env` [编译依赖] - Context merge（ctx.shellEnv）
  - 证据: `packages/bundle/web-app/package.json:109; src/index.ts:23`
- `dsh-system-prompt` [编译依赖] - Context merge（ctx.systemPrompt）
  - 证据: `packages/bundle/web-app/package.json:111; src/index.ts:22`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
