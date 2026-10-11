# dsh-workflow-ptc

- 包名: `@deepseek-ai/dsh-workflow-ptc`
- 分组: G47 工作流
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/workflow/workflow-ptc`

## 实现逻辑
PtcWorkflowEngine extends WorkflowEngine 并 static inject ['subagents','ptcRuntime','sandboxPolicy','workingDirectory']，构造时要求 ctx.ptcRuntime.language 为 typescript，否则直接拒绝启动 (src/index.ts:103-122)。start() 先 validateMeta 校验调用方数据形状（未知字段、缺失/错型 name/description、phases 结构），再用宿主侧 vm.Script 只解析不执行地预检脚本体，并把并发/总量/单次条目/同步超时等上限解析进 WorkerLimits (src/index.ts:134-154, src/meta.ts:76-81, src/index.ts:55-65)。执行交给 PtcWorkflowRun：它在共享沙箱 Node PTC 进程里以 data:URL 导入 guest 源码运行脚本，自身负责子 agent 所有权、取消时中止并回收子 agent、以及等待受管进程与全部子启动/销毁后结算 (src/host.ts:113-145, src/host.ts:26-27, src/host.ts:151-156)。进度经 observer 回调发出 workflow/phase|log|agent-start|agent-end，结束发 workflow/end（只带结果数据，值留在 holder）(src/index.ts:169-186)。返回值从 vm realm 物化成纯 JSON，非 JSON 值（bigint/函数/环/稀疏数组/奇异原型）按路径报错 (src/realm.ts:62-72)。

## Provides
- ctx.workflowEngine (在共享沙箱 Node PTC 运行时里执行 workflow 脚本的引擎实现)
- workflow/start|phase|log|agent-start|agent-end|end 事件 (运行生命周期与进度广播)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 运行以父 Agent 为归属，子 agent 与工作目录均挂在该 Agent 上
  - 证据: `package.json:31 peerDep + src/host.ts:3 import type { Agent }`
- `dsh-llm` [编译依赖] - 无 schema 的 agent() 结果需要把子 agent 的 llm 内容块压平成文本
  - 证据: `package.json:32 peerDep + src/types.ts:7 import type { ContentBlock } + src/runtime.ts:10 import type { ContentBlock }`
- `dsh-sandbox-policy` [运行时依赖] - 按调用方 Session 解析执行策略，作为 PTC 子进程的文件策略输入
  - 证据: `package.json:39 peerDep + src/index.ts:12 import type {} + src/index.ts:167 ctx.sandboxPolicy.resolve({ session: request.parent.session })`
- `dsh-session` [编译依赖] - 子 agent 的会话身份（childId）按 SessionId 品牌传递与校验
  - 证据: `package.json:33 peerDep + src/host.ts:7 import { SessionId } + src/runtime.ts:11 import type { SessionId }`
- `dsh-subagent` [运行时依赖] - agent() 钩子通过 subagents seam 的 provider 启动/销毁子 agent，并把结果映射成 ChildResult
  - 证据: `package.json:34 peerDep + src/host.ts:8 import type SubagentRuntime + src/index.ts:76 ctx.subagents.getProvider(provider)`
- `dsh-tools` [编译依赖] - 校验脚本传入的 structured-output schema 属于受支持的 object-rooted JSON Schema 子集
  - 证据: `package.json:35 peerDep + src/host.ts:10-11 import { assertObjectJsonSchema } + src/runtime.ts:12 import { JsonSchemaError }`
- `dsh-working-directory` [运行时依赖] - 为运行解析父 Agent 的工作目录，作为沙箱进程 cwd 依据
  - 证据: `package.json:40 peerDep + src/index.ts:13 import type {} + src/host.ts:142 ctx.workingDirectory.ensure(parent, signal)`

## Dependents (下游被依赖)
- `dsh-tool-ralph` - base bundle 中 workflow-ptc 先行装配以提供 ctx.workflowEngine，tool-ralph 随后装配使用该服务
