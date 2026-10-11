# dsh-agent-instructions

- 包名: `@deepseek-ai/dsh-agent-instructions`
- 分组: G08 上下文注入
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/context/agent-instructions`

## 实现逻辑
以「一次性基线 + 逐次增量对账」两段逻辑实现 AGENTS.md/CLAUDE.md 工作区指令注入。apply() 在 agent/pre-step 里调 compose()：先经 ctx.workingDirectory.ensure 取 cwd、findProjectRoot 定位项目根，再用 loadBaselineInstructionSet 读取 harness home、agents home 与祖先目录的指令文件（src/index.ts:127-154）；随后 reconcileInstructionContext 按文件元数据版本与 trimmed 内容摘要做候选组去重、生成 set/replace/remove 变更，渲染成 source.kind='agent-instructions' 的 user 消息折叠进本步批次（src/state.ts:251-455、src/index.ts:234-243）。tools/result 监听把 read/write/edit 触碰到的 file_path 记为待刷新项，按 step/end 边界串行排队（src/index.ts:362-378、src/index.ts:315-332）。ctx.fs 缺失时整体降级为空操作（src/index.ts:121-122）。

## Provides
- 工作区指令注入能力：agent-instructions 消息源类型与基线/增量渲染（src/state.ts:51-55、src/render.ts:414-434）
- 指令文件发现与读取 API：discoverBaselineInstructionFiles/loadBaselineInstructions/findProjectRoot（src/files.ts:232、src/files.ts:378、src/files.ts:456）
- 配置归一化与基线身份 API：resolveConfig/workspaceBaselineIdentity（src/config.ts:67、src/config.ts:88）

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 在工作区指令投影里读写 agent 的 inbox 与 pre-step 决策，指令才能折进本步消息批次
  - 证据: `src/index.ts:15 import type { Agent, PreStepDecision } + src/index.ts:334 ctx.on('agent/pre-step', ...) + src/index.ts:247 agent.inbox.nextStep`
- `dsh-llm` [编译依赖] - 构造承载指令文本的 user 角色消息，并扩展 MessageSourceMap 声明 agent-instructions 源
  - 证据: `src/index.ts:16 import { createUserMessage } + src/state.ts:8 import { createUserMessage } + src/state.ts:86 createUserMessage({`
- `dsh-session` [编译依赖] - 读取会话表面节点与事件，判断已渲染基线是否仍可见
  - 证据: `src/index.ts:17 import type { Session, UserMessage } from '@deepseek-ai/dsh-session' + src/state.ts:10 import type { Session, UserMessage }`
- `dsh-session-projection` [E1+E2] - 读取 turnBoundary 投影判断当前是否处于开放 step，决定触碰项是即时投影还是延迟排队
  - 证据: `src/index.ts:18 import type {} from '@deepseek-ai/dsh-session-projection' + src/index.ts:306 ctx.sessionProjections.stateOf(session, 'turnBoundary')`
- `dsh-tools` [E1+E2] - 订阅工具结果事件，从 read/write/edit 的参数中提取被触碰文件路径以触发指令刷新
  - 证据: `src/index.ts:19 import type { ToolExecution, ToolExecutionResult, ToolExecutionToken } + src/index.ts:362 ctx.on('tools/result', ...)`
- `dsh-working-directory` [E1+E2] - 解析每个 agent 的当前工作目录，作为指令发现与相对作用域键的基准
  - 证据: `src/index.ts:12 import type {} from '@deepseek-ai/dsh-working-directory' + src/index.ts:127 ctx.workingDirectory.ensure(agent, signal)`

## Dependents (下游被依赖)
- `dsh-experimental-auto-review` - 识别项目指令来源，把其内容作为 constraint 段而非指令段
