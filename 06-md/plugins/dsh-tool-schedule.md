# dsh-tool-schedule

- 包名: `@deepseek-ai/dsh-tool-schedule`
- 分组: G29 定时调度
- 拓扑层: Layer 9
- 来源层: L3 其余
- 源码路径: `packages/schedule/tool-schedule`

## 实现逻辑
函数式插件（具名导出 name/inject/apply，无 default 导出）：apply 经 ctx.inject(['schedule']) 在解析到 Schedule 服务的 scope 内注册四个模型工具 schedule_create/schedule_list/schedule_delete/schedule_update，因此由 preset 决定哪些 agent 拿到它们 (src/index.ts:29、src/index.ts:435-437、src/index.ts:444-581)。每个工具先做「调用者必须存在、且不得是委派子 agent」的前置拒绝，再把输入收敛成规范词表：六种 timing 视图 schema、九种稳定错误码与 update 的 not-found/ended/conflict 结果 (src/index.ts:31-181、src/index.ts:227-230)。参数层校验开放根无法表达的约束（恰好一个 timing 选择子、title/prompt 非空且不超 120 字、every_seconds 下限），错误一律翻译成稳定 code，内部存储失败则归约为 internal_error 而不泄漏细节 (src/index.ts:248-292、src/index.ts:294-345、src/index.ts:211-218)。执行体全部走 ctx.schedule 并保持会话作用域：create 用 agent.session.id，update 先 list 出 expected 再比较更新，未命中时查 catalog 区分已结束与不存在 (src/index.ts:466-479、src/index.ts:546-578)。

## Provides
- tools.schedule_create / schedule_list / schedule_delete / schedule_update (四个模型可见的提醒管理工具，注册在解析到 schedule 服务的 scope)
- 工具输出 schema 词表 (六种 timing 视图 + 九种稳定错误码 + delete/update 的非变更结果)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 以 Agent 类型标注调用者参数；仅编译期类型依赖，运行期经 exec.agent 取得
  - 证据: `src/index.ts:10 type import Agent + package.json:38 devDependencies（peer 未声明）`
- `dsh-llm` [编译依赖] - 工具结果渲染函数返回 llm 内容块，保证输出形状与其它工具一致
  - 证据: `package.json:31 peerDep + src/index.ts:11 type import ContentBlock；src/index.ts:199-203 renderValue 返回 ContentBlock[]`
- `dsh-schedule` [E1+E2+E3] - 复用提醒服务的规范词表与视图，并把工具注册在能解析到该服务的 scope（由 preset 装配决定）
  - 证据: `package.json:32 peerDep + src/index.ts:15-17 import MAX_TITLE_LENGTH/MIN_EVERY_INTERVAL_SECONDS/REQUIRED_TITLE_MESSAGE/ScheduleId/ScheduleInputError/scheduleView、src/index.ts:18-21 type import；src/index.ts:436 ctx.inject(['schedule'])、src/index.ts:475 与 :522 与 :557 ctx.schedule.*；packages/bundle/web-app/presets/standard.patch.yml:35-36 装配位置`
- `dsh-subagent` [编译依赖] - 在 dispatch 前拒绝委派子 agent 使用提醒工具，而不只依赖 preset 的工具过滤
  - 证据: `package.json:33 peerDep + src/index.ts:12 import delegationDepthOf；src/index.ts:228 delegationDepthOf(agent) === 0`
- `dsh-tools` [E1+E2] - 以 defineTool 定义四个工具并注册进工具注册表
  - 证据: `package.json:34 peerDep + src/index.ts:13 import defineTool、src/index.ts:14 type import GenericCallView；src/index.ts:29 inject 'tools'、src/index.ts:445 ctx.tools.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
