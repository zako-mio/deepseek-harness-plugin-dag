# dsh-experimental-auto-review

- 包名: `@deepseek-ai/dsh-experimental-auto-review`
- 分组: G13 实验特性
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/experimental/auto-review`

## 实现逻辑
在 tools/pre-execute 前置挂一个 LLM 授权闸门：仅当会话处于 Auto 权限预设时，把待执行调用连同会话全部动作历史冻结成五段（策略+环境+项目指令+过滤历史+待执行动作）快照，交 ctx.llm.stream 以 temperature 0 判定风险与允许/拒绝 (src/index.ts:615-636, src/index.ts:362-520)。审查输出被严格解析为 {risk, decision[, reason]} 封闭协议，且要求零或多个 reasoning 块后恰好一个 text 块并以 stop 收尾，任何偏差都算审查失败而非放行 (src/index.ts:558-612)。拒绝时若审批策略为 never 则直接 deny，否则把决定交回用户询问 (ask) (src/index.ts:675-719)。注册 Auto 预设，并在卸载时把仍处于 Auto 的会话降级为 danger-full-access、中止在飞审查 (src/index.ts:721-736)。

## Provides
- Auto 权限预设的 LLM 审查闸门 (tools/pre-execute 前置判定，deny/ask)
- AUTO_REVIEW_DENIED 结构化拒绝错误 (AutoReviewDeniedError)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 审查绑定与 agent 作用域类型来自 agent 包
  - 证据: `src/index.ts:13 import type { Agent } from '@deepseek-ai/dsh-agent' + package.json:33 peerDep`
- `dsh-agent-instructions` [编译依赖] - 识别项目指令来源，把其内容作为 constraint 段而非指令段
  - 证据: `src/index.ts:14 import type {} from '@deepseek-ai/dsh-agent-instructions' + src/index.ts:186 source.kind === 'agent-instructions' 判定 + package.json:34 peerDep`
- `dsh-llm` [E1+E2] - 审查请求经 llm seam 以会话当前 provider/model 路由发出，流式结果由 BlockAssembler 解析
  - 证据: `src/index.ts:15-23 import { BlockAssembler, type GenerateOptions, ... } from '@deepseek-ai/dsh-llm' + src/index.ts:127 export const inject = ['approval', 'llm', 'permissionPresets', 'sessions', 'tools', 'workingDirectory'] + src/index.ts:635 ctx.llm.stream(options) + package.json:35 peerDep`
- `dsh-permission-presets` [E1+E2] - Auto 预设的定义与注册、以及卸载时的会话降级都由该 seam 拥有
  - 证据: `src/index.ts:25 import { AUTO_PRESET } from '@deepseek-ai/dsh-permission-presets' + src/index.ts:689 permissionPresets.current(agent.session) !== AUTO_PRESET + src/index.ts:721 permissionPresets.registerAuto(...) + package.json:36 peerDep`
- `dsh-session` [E1+E2] - 审查输入取自会话日志与 surface 节点，卸载时遍历所有会话
  - 证据: `src/index.ts:26 import type { SessionEvent } from '@deepseek-ai/dsh-session' + src/index.ts:369 session.snapshotEvents() + src/index.ts:728 ctx.sessions.list() + package.json:37 peerDep`
- `dsh-subagent` [编译依赖] - 类型面需要 subagent 的 Context 声明以读取 in-process 子代理的父会话信息
  - 证据: `src/index.ts:27 import type {} from '@deepseek-ai/dsh-subagent' + package.json:66 devDep`
- `dsh-tools` [E1+E2] - 以工具预执行为唯一拦截点，决定放行/拒绝/询问，并排除 run_code 外层传输
  - 证据: `src/index.ts:29-33 import { RUN_CODE_NAME, type PreToolDecision, type ToolExecution } + src/index.ts:684 ctx.on('tools/pre-execute', ...) + package.json:38 peerDep`
- `dsh-user-approval` [E1+E2] - 按当前审批策略决定拒绝是终局还是转交用户询问
  - 证据: `src/index.ts:28 import type {} from '@deepseek-ai/dsh-user-approval' + src/index.ts:708 ctx.approval.overrideOf(agent.session) === 'never' + src/index.ts:127 inject 'approval' + package.json:73 devDep`
- `dsh-working-directory` [E1+E2] - 审查快照的 ENVIRONMENT 段需要会话工作目录
  - 证据: `src/index.ts:11 import type {} from '@deepseek-ai/dsh-working-directory' + src/index.ts:621 ctx.workingDirectory.ensure(agent, signal) + package.json:40 peerDep`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
