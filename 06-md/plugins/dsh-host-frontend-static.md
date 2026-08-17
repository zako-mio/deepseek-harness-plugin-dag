# dsh-host-frontend-static

- 包名: `@deepseek-ai/dsh-host-frontend-static`
- 分组: G37 示例与框架
- 拓扑层: Layer 1
- 来源层: L3 其余
- 源码路径: `packages/host/frontend-static`

## 为什么需要它（设计初衷）
Web shell 的 SPA dist 静态服务器：占用 webserver 单 fallback seat，带 index-tap 注入、越界 403、SPA 路由回退。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/host/frontend-static/README.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-host-frontend-static

## 实现逻辑
SPA dist 静态服务器：apply 经 ctx.webServer.registerFallback 认领 fallback seat (src/index.ts:98-109)；serveStatic (:56-86) 目录穿越 403 (:64-67)、miss 回退 index.html 200 (SPA 路由 :82-85)、MIME 表 (:37-45)、非 GET/HEAD 405 (:101-105)；renderIndex 经 webServer.applyIndexTaps 注入 boot-manifest (:96-97)；inject ['webServer'] (:25)；distIndex 为装配知识 (:28-35)。

## Provides
- webserver fallback seat（SPA dist 静态托管 + index tap 注入）

## Depends On (上游依赖)
- `dsh-host-webserver` [E1+E2] - HTTP 服务器与 index taps 注册
  - 证据: `package.json:35 peerDep + src/index.ts:19 import type {}（side-effect merge）；E2: :25 inject=['webServer']、:97 ctx.webServer.applyIndexTaps、:98 ctx.webServer.registerFallback`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
