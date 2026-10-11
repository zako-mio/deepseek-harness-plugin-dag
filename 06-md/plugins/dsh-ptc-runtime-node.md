# dsh-ptc-runtime-node

- 包名: `@deepseek-ai/dsh-ptc-runtime-node`
- 分组: G27 代码执行运行时
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/ptc-runtime/ptc-runtime-node`

## 实现逻辑
以 default 导出的 NodePtcRuntime（extends PtcRuntime，注册为 ctx.ptcRuntime；static inject=['fs','subprocess','sandbox','sandboxPolicy']）实现 PTC 执行 seam 的 Node 进程后端，语言为 typescript、隔离级别为 process (src/index.ts:55-71)。resolve() 补齐 cwd 与沙箱策略并按配置上下限钳制时间预算，run() 校验绑定后为每次执行登记一个 AbortController 以便 dispose 时终止 (src/index.ts:111-144)。执行时先把程序用 stripTypeScriptTypes 剥成纯 JS 装入 async function 包装，再经 ctx.subprocess.resolveExecutable/spawn 启动受管子进程，控制通道走长度前缀 JSON 帧（JsonChannel），绑定调用以 id 关联并受 maxPendingCalls/maxMessageBytes 限制 (src/index.ts:209-227、src/index.ts:240、src/channel.ts:51-121)。输出经 OutputLedger 与进程侧 LogBuffer 双层按字节计账，超限统一归约为 output-limit 失败；子进程侧 bootstrap 捕获 console 与 stdout/stderr 写入、以 null-prototype 命名空间对象桥接宿主绑定、并只把无损 JSON 值送回 (src/index.ts:152-197、src/output-ledger.ts:12-65、src/bootstrap.ts:110-148、src/bootstrap.ts:313-357)。

## Provides
- ctx.ptcRuntime (PTC 执行能力 seam 的 Node 进程 provider：resolve/run 一个模型编写的 TypeScript 程序)
- 子进程私有入口 ./process (process.js/process.ts：经继承控制通道运行程序，不加载任何 Harness 服务)
- 有界输出账本与失败归约词表 (logs/value 或 exception/invalid-output/output-limit/worker-exit/sandbox-unavailable)

## Depends On (上游依赖)
- `dsh-sandbox-policy` [运行时依赖] - 取得部署默认文件策略与每会话模式，作为程序直接文件访问的执行策略
  - 证据: `package.json:41 peerDep + src/index.ts:12 type import；src/index.ts:56 inject 'sandboxPolicy'、src/index.ts:100 sandboxMode、src/index.ts:113 sandboxPolicy.resolve`
- `dsh-session` [编译依赖] - 编译期会话作用域契约对齐（PTC 运行于会话边界内）；仅声明式依赖
  - 证据: `package.json:36 peerDep + packages/ptc-runtime/ptc-runtime-node/tsconfig.json:12 项目引用（源码无直接 import）`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
