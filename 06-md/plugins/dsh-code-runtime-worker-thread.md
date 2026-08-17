# dsh-code-runtime-worker-thread

- 包名: `@deepseek-ai/dsh-code-runtime-worker-thread`
- 分组: G25 宿主服务
- 拓扑层: Layer 2
- 来源层: L2 web-app
- 源码路径: `packages/code-runtime/code-runtime-worker-thread`

## 为什么需要它（设计初衷）
code-runtime seam 的 worker 线程实现：每次运行全新 Worker，隔离非安全边界，含 computeMs/maxWallMs 双预算与 JSON 边界验证。

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/code-runtime/code-runtime-worker-thread/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/code-runtime

## 实现逻辑
worker_threads 实现 CodeRuntime 抽象：run() 用 stripTypeScriptTypes 剥类型后为每个程序 spawn 全新 worker（空 env、无 execArgv、resourceLimits 堆上限），绑定函数与 JSON 值经 message port 桥接（decode/encodeWorkerJson）；ELU 轮询 busy-time + wall-time 双预算、输出字节账本 OutputLedger、abort/exit/timeout 收敛到静止后 dispose。提供 ctx.codeRuntime 服务。

## Provides
- ctx.codeRuntime（CodeRuntime 后端，language=typescript, isolation=worker-thread）

## Depends On (上游依赖)
- `dsh-session` [编译依赖] - snapshotJsonValue 将绑定解析结果快照为无损耗 JSON
  - 证据: `packages/code-runtime/code-runtime-worker-thread/package.json:41; src/index.ts:18`

## Dependents (下游被依赖)
- `dsh-agent-tool-presentation` - code 模式所需的宿主平面 TypeScript 运行时
- `dsh-tools` - Code Mode 工具经 ctx.get('codeRuntime') 解析运行时, 缺失 loud 报错
