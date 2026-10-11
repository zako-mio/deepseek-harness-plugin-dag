# dsh-tool-skill

- 包名: `@deepseek-ai/dsh-tool-skill`
- 分组: G35 技能
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/skill/tool-skill`

## 实现逻辑
同时提供模型侧 `skill` 加载工具与会话级技能目录：工具 execute 按调用 Agent 作为 scope 解析分层注册表，校验名称与 model-invocable 后返回技能正文与资源基址 (src/index.ts:82-163)。第二个 `agent/pre-step` 监听器在工具对本 Agent 可见时快照技能列表，用条目的 sha256 摘要比对已发布目录，决定追加、替换还是删除 `<available_skills>` 消息，并把条目写入 `skill-catalog` form 的 durable source (src/index.ts:215-253、src/index.ts:330-380)。另一个 pre-step 监听器扫描 source.kind === 'user' 消息中的 `/name` 手势，把 user-invocable 技能正文作为 instructions 注入，这也是 `disable-model-invocation` 技能的唯一入口 (src/index.ts:179-206、src/index.ts:411-433)。

## Provides
- ctx.tools 上的 `skill` 工具定义（按名称加载技能完整说明）
- 会话级技能目录注入（`<available_skills>` 消息 + 可重建的 `skill-catalog` durable source）
- `/name` 用户显式技能调用手势的注入通道

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 以 Agent 为 scope 键做分层查找并挂载 pre-step 注入
  - 证据: `src/index.ts:11 import type { Agent, PreStepDecision } + src/index.ts:135 scope: exec.agent + src/index.ts:179 ctx.on('agent/pre-step')`
- `dsh-llm` [编译依赖] - 目录与注入消息需要 LLM 消息源类型扩展
  - 证据: `src/index.ts:13 import { createUserMessage } from '@deepseek-ai/dsh-llm' + src/index.ts:44-48 声明 MessageSourceMap`
- `dsh-session` [编译依赖] - 从会话事件历史判定目录是否已发布/可见
  - 证据: `src/index.ts:14 import { SessionSeq, type UserMessage } + src/index.ts:364 agent.session.surface.nodes`
- `dsh-skill` [E1+E2] - 技能查询、快照、渲染与调用策略由技能 seam 提供
  - 证据: `src/index.ts:15-23 import renderSkillContent/isModelInvocable/isUserInvocable + src/index.ts:136 ctx.skills.list / src/index.ts:143 get / src/index.ts:224 snapshot`
- `dsh-tools` [E1+E2] - 注册模型可见工具，并以定义身份判定目录可见性
  - 证据: `src/index.ts:12 import defineTool + src/index.ts:26 inject 'tools' + src/index.ts:163 ctx.tools.register`
- `dsh-working-directory` [运行时依赖] - 技能查找需要 cwd 以选择项目根
  - 证据: `src/index.ts:7 type import + src/index.ts:134 ctx.workingDirectory.ensure(exec.agent, exec.signal)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
