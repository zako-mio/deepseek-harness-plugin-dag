# dsh-host-frontend-static

- 包名: `@deepseek-ai/dsh-host-frontend-static`
- 分组: G20 宿主服务
- 拓扑层: Layer 3
- 来源层: L3 其余
- 源码路径: `packages/host/frontend-static`

## 实现逻辑
在 webServer 的 fallback 座位注册 SPA 静态服务：非 GET/HEAD 返回 405，解析后越出 distRoot 返回 403，index 与非 index 资产分别处理（src/index.ts:113-139、71-106）。index 响应先经 Connection 的 authorizeIndex 浏览器鉴权，再由 ctx.webServer.renderIndex 注入并加 <base href="./">（src/index.ts:117-120、136）。未知扩展名以 octet-stream 下发，缺失文件返回 404（src/index.ts:94、99-101）。

## Provides
- webServer 回退座位 (SPA dist 静态托管：index 鉴权+注入、资产 MIME 服务，src/index.ts:121-139)

## Depends On (上游依赖)
- `dsh-client-connection` [E1+E2] - 对 index 响应执行浏览器鉴权
  - 证据: `package.json:31 peerDep + src/index.ts:20 type import; src/index.ts:136 ctx.connection.authorizeIndex`
- `dsh-host-webserver` [E1+E2] - 占用其 fallback 座位并渲染 index 注入
  - 证据: `package.json:30 peerDep + src/index.ts:21 type import; src/index.ts:118 ctx.webServer.renderIndex、:121 registerFallback`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
