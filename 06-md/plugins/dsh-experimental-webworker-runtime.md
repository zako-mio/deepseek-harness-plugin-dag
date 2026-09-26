# dsh-experimental-webworker-runtime

- 包名: `@deepseek-ai/dsh-experimental-webworker-runtime`
- 分组: G13 实验特性
- 拓扑层: Layer 3
- 来源层: L3 其余
- 源码路径: `packages/experimental/webworker-runtime`

## 实现逻辑
浏览器专用 host runtime：在专用 Web Worker 内跑整套 harness Cordis 树。`createWorkerHost` 同步构造（先装消息处理器以便启动期排队），`start()` 挂载 VFS 镜像/overlay、安装 Worker 模块加载器与 process shim，再从镜像 require `boot()`/cmdline 启动 preview profile 并让 TunnelServer 开始服务（src/worker-host.ts:169-271）。包同时导出 ModuleLoader、node builtin/external 代理与 mock、shell 解释器、storage(VFS/tar/gzip)、transport(tunnel/synthetic-http)、async-context polyfill 等浏览器运行时基建（src/index.ts:5-52）。

## Provides
- createWorkerHost/startWorkerHost (在 Web Worker 内组装并启动完整 harness Cordis 树)
- 浏览器运行时基建 (WorkerModuleLoader / MemoryVfs / TunnelServer / shell / node builtin 代理)

## Depends On (上游依赖)
- `dsh-api-gateway` [编译依赖] - 把 typert 流经 tunnel 转发到页面
  - 证据: `src/worker-host.ts:26 import type { TypertGateway }`
- `dsh-client-connection` [编译依赖] - 从树中取得共享 fetch handler 供 tunnel 直连
  - 证据: `src/worker-host.ts:27 import type { HostConnectionHandle }`
- `dsh-client-file-upload` [编译依赖] - 复用文件上传类型于 Worker 传输层
  - 证据: `src/client/index.ts:12 import '@deepseek-ai/dsh-client-file-upload/types'`
- `dsh-client-web` [编译依赖] - 复用 Client web 侧的 index injection 定义
  - 证据: `src/client/apply-injections.ts:2 import '@deepseek-ai/dsh-client-web/injections'`
- `dsh-host-webserver` [编译依赖] - 使用 webserver 采集 index injections 作为 boot payload
  - 证据: `src/client/client.ts:8 import '@deepseek-ai/dsh-host-webserver'`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
