# dsh-hooks-codex

- 包名: `@deepseek-ai/dsh-hooks-codex`
- 分组: G13 实验特性
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/experimental/hooks-codex`

## 实现逻辑
以「配置解析 + 五扩展点桥接」实现：用 parseCodexConfig 解析 Codex 的 {hooks:…} 包装或裸事件表，只跑同步 command 钩子（非 command 与 async:true 记入 skipped 并 warn），支持 timeout/timeoutSec 双别名且不做命令替换 (src/config.ts:43-85)。apply 后在 agent/created、agent/pre-step、tools/pre-execute、tools/post-execute、agent/turn-stopping 五个点注册监听，runPoint 以 Codex 方言（snake_case、每事件带 model、turn 事件带 turn_id、stdin 不带尾换行）跑钩子并折叠决策 (src/index.ts:119-173, src/index.ts:188-273)。SessionStart/UserPromptSubmit 额外在无结构化上下文时把干净 stdout 当作 additionalContext (src/index.ts:155-159, src/index.ts:190, src/index.ts:209-211)。

## Provides

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 订阅 Agent 生命周期与 pre-step/turn-stopping 拦截点，注入上下文并在 Stop 钩子阻塞时 steer 续跑
  - 证据: `package.json:33 peerDep + src/index.ts:18 import Agent/PreStepDecision + src/index.ts:188/202/263 监听 agent/created、agent/pre-step、agent/turn-stopping`
- `dsh-llm` [编译依赖] - 构造带 hooks-codex 来源标记的用户消息，承载钩子产出的 additionalContext
  - 证据: `package.json:35 peerDep + src/index.ts:20 import createUserMessage + src/index.ts:28 import ContentBlock/MessageSource`
- `dsh-session` [编译依赖] - 为注入消息与钩子事件写入提供会话侧类型
  - 证据: `package.json:36 peerDep + src/index.ts:29 import UserMessage`
- `dsh-session-projection` [E1+E2] - 从 turnBoundary 投影取 lastTurn，为 turn_id 字段与 hook 事件填当前轮次
  - 证据: `package.json:39 peerDep + src/index.ts:19 type import + src/index.ts:47 inject 'sessionProjections' + src/index.ts:285 ctx.sessionProjections.stateOf`
- `dsh-tools` [E1+E2] - 把 Codex 钩子的 deny 映射为工具前置 deny 与后置 block/feedback，并附加 additionalContexts
  - 证据: `package.json:37 peerDep + src/index.ts:30 import PostToolDecision/PreToolDecision/ToolExecution + src/index.ts:228/237 监听 tools/pre-execute、tools/post-execute`
- `dsh-working-directory` [E1+E2] - 解析会话工作目录作为钩子进程 cwd 与 payload 的 cwd 字段
  - 证据: `package.json:40 peerDep + src/index.ts:14 type import + src/index.ts:47 inject 'workingDirectory' + src/index.ts:133 ctx.workingDirectory.ensure`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
