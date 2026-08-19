# dsh-experimental-agent-team

- 包名: `@deepseek-ai/dsh-experimental-agent-team`
- 分组: G38 多智能体协作
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/experimental/agent-team`

## 为什么需要它（设计初衷）
为Profile Bundle按需安装的多智能体场景提供隐式root团队花名册、持久peer消息与共享任务DAG，使多个子代理能以协作方式共享同一工作区工作。

发展史：RC8 新增

## 实现逻辑
隐式root多智能体协作服务(私有包,opt-in)。src/index.ts:56 TeamService extends Service(agentTeams)，inject=['agents','sessions','sessionPersistence','subagents']。组合Roster(花名册/隐式root)、Mailbox(持久peer消息箱)、TaskBoard(共享任务DAG)、Journal(Lead会话日志)、Lifecycle与Activity。公开API：membership、spawnTeammate、sendMessage、createTask/getTask/listTasks/updateTask、waitForChange、interrupt。监听session/event、agent/session-start驱动mailbox/recovery。未装配bundle，按需加载。

## Provides
- ctx.agentTeams TeamService(花名册/持久邮箱/任务DAG/生命周期)
- spawnTeammate/sendMessage/waitForChange/interrupt等协作原语
- 会话恢复与运行时清理

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - 枚举live agent并判membership
  - 证据: `src/index.ts:57 inject ['agents']`
- `dsh-llm` [运行时依赖] - teammate模型推理
  - 证据: `peerDependencies @deepseek-ai/dsh-llm`
- `dsh-session` [运行时依赖] - 以Lead会话为journal基底
  - 证据: `src/index.ts:57 inject ['sessions']`
- `dsh-subagent` [运行时依赖] - teammate的continuable子代理提供者
  - 证据: `src/index.ts:57 static inject ['subagents']`

## Dependents (下游被依赖)
- `dsh-experimental-tool-agent-team` - 转发所有Team协作操作
