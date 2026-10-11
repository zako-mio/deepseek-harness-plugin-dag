# dsh-experimental-webworker-runtime

- 包名: `@deepseek-ai/dsh-experimental-webworker-runtime`
- 分组: G13 实验特性
- 拓扑层: Layer 3
- 来源层: L3 其余
- 源码路径: `packages/experimental/webworker-runtime`

## 实现逻辑
浏览器专用宿主运行时：createWorkerHost/startWorkerHost 在一个 dedicated Web Worker 内装配完整 harness Cordis 树——挂载内存 VFS 镜像与数据叠加层、校验镜像 lowering 版本、建立 WorkerModuleLoader 与 Node 兼容层，然后经镜像内的 dsh-app-boot 启动 profile，把 connection 与 typertGateway 接到 postMessage 隧道上 (src/worker-host.ts:169-302, src/worker-host.ts:355-367)。隧道负责把页面的 fetch/流请求转成树内请求，并在启动前排队、启动后服务、失败时以 503 拒绝 (src/worker-host.ts:273-286)。浏览器半边（pre-Cordis glue，不是 client plugin）安装 __DSH_TRANSPORT__/__DSH_FILE_UPLOAD__ 全局并按表执行 boot 注入，以 __DSH_BOOT_READY__ 作启动屏障 (src/client/index.ts:145-175)。包同时导出 Node 内置模块/外部包代理、模块转换与加载、内存 VFS 与 tar/gzip、shell 解释器等兼容层 (src/index.ts:5-52)。

## Provides
- createWorkerHost / startWorkerHost (Web Worker 内运行完整 harness Cordis 树的装配入口)
- 浏览器侧 connectWorkerHost / chooseWorkerHostSource (postMessage 隧道、boot 注入表执行、__DSH_TRANSPORT__ 与 __DSH_FILE_UPLOAD__ 全局)
- Node 兼容层：node:* 内置模块与外部包代理、模块加载与转换、内存 VFS、tar/gzip、shell 解释器

## Depends On (上游依赖)
- `dsh-api-gateway` [E1+E2] - 隧道上的流式请求由网关的 wireStream 承载
  - 证据: `src/worker-host.ts:26 import type { TypertGateway } from '@deepseek-ai/dsh-api-gateway' + src/worker-host.ts:265 ctx.get('typertGateway') + src/worker-host.ts:278 typertGateway.wireStream.open(...) + package.json:50 devDep`
- `dsh-client-connection` [E1+E2] - 树内 HTTP 请求的统一入口与共享 fetch handler 来自连接层
  - 证据: `src/worker-host.ts:27 import type { HostConnectionHandle } from '@deepseek-ai/dsh-client-connection' + src/worker-host.ts:263 ctx.get('connection') + src/worker-host.ts:269 connection.createSharedFetchHandler('/api') + package.json:43 peerDep`
- `dsh-client-file-upload` [编译依赖] - 页面侧文件上传钩子被替换为走 worker 隧道
  - 证据: `src/client/index.ts:12 import type { ClientFileUploadHooks } from '@deepseek-ai/dsh-client-file-upload/types' + src/client/index.ts:165 globalThis.__DSH_FILE_UPLOAD__ 赋值 + package.json:54 devDep`
- `dsh-client-modules` [编译依赖] - 浏览器模块装载的声明依赖，保证组合中存在同一份实现
  - 证据: `package.json:44 peerDep`
- `dsh-client-web` [编译依赖] - boot 注入表（__ModuleLoader__、__DSH_BOOT__、主题引导）的执行器由 client-web 提供
  - 证据: `src/client/apply-injections.ts:2 export { applyIndexInjections } from '@deepseek-ai/dsh-client-web/injections' + package.json:38 dependencies`
- `dsh-host-webserver` [E1+E2] - 页面 boot 所需的 index 注入表由树内 webserver 收集
  - 证据: `src/client/client.ts:9 import type { IndexInjection } from '@deepseek-ai/dsh-host-webserver' + src/worker-host.ts:446 ctx.get('webServer') + src/worker-host.ts:450 webServer.collectIndexInjections() + package.json:45 peerDep`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
