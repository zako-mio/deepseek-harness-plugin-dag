# dsh-ptc-runtime-node

- 包名: `@deepseek-ai/dsh-ptc-runtime-node`
- 分组: G28 代码执行运行时
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/ptc-runtime/ptc-runtime-node`

## 实现逻辑
NodePtcRuntime 继承 PtcRuntime（注册 ctx.ptcRuntime），resolve() 解析 cwd 与超时预算并做上限夹取（src/index.ts:108-119），run()/execute() 用 stripTypeScriptTypes 剥离 TS 后在受限子进程中执行程序：经 ctx.sandbox.confine 包装 argv、经 ctx.subprocess.spawn 启动、经 JsonChannel 长度前缀控制帧做 boot/日志/绑定调用/完成握手，并由 OutputLedger 做合并字节上限（src/index.ts:126-354）。宿主绑定名先经 validateBindings 校验、去重并拒绝保留名（src/bindings.ts:10-51），控制帧的损失 JSON 快照与编解码在 json-wire.ts（src/json-wire.ts:150-419）与 channel.ts（src/channel.ts:16-140）。启动 bootstrap 参数由 launch.ts 依 dsh-fs 映射到执行世界（src/launch.ts:21-38），子进程入口 process-entry.ts 走 dsh-subprocess/control（src/process-entry.ts:2-5）。

## Provides
- ctx.ptcRuntime (PTC 代码执行运行时 seam 的 Node 进程实现)

## Depends On (上游依赖)
- `dsh-sandbox-policy` [运行时依赖] - 读取部署/会话沙箱策略作为执行的文件效应边界
  - 证据: `src/index.ts:12 type import + src/index.ts:53 static inject + src/index.ts:97,110 ctx.sandboxPolicy`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
