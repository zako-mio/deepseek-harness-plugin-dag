# dsh-session-projection

- 包名: `@deepseek-ai/dsh-session-projection`
- 分组: G08 会话展示
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/session/session-projection`

## 为什么需要它（设计初衷）
会话投影 seam：拥有合并可扩展的投影类型表、provider 契约与 ctx.sessionProjections 注册表，将已提交的会话事件驱动到每个注册投影单元（init/apply/view 三个纯函数）并输出完整当前值，供 api-proxy 历史尾页与 session/projection push 帧消费。领域注册纯数学，框架负责驱动，事件日志为唯一真源，UI 读模型由此派生。

发展史：由 2026-07-27 session-projection RFC 定案设计（框架驱动/领域计算、同引用即无工作、全量值规则）；2026-08-10 发布 0.0.1-rc.1。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/session/session-projection/README.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/notes/proposed/architecture/2026-07-27-session-projection-and-command-log.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-session-projection

## 实现逻辑
会话投影能力接缝：SessionProjectionRegistry(ctx.sessionProjections) 管理 merge 可扩展的 SessionProjectionMap 类型表与投影单元注册。服务构造时订阅 'session/event' 一次驱动所有注册单元，仅当 apply 返回新引用才触发 onChanged。注册是 effect，同 key 多注册者共享单元并 refs 计数。读取面：snapshot()/checkpoint()/restoreFloor()/viewCheckpoint()/restore()。

## Provides
- ctx.sessionProjections
- SessionProjectionMap 类型表
- ProjectionDefinition 纯同步单元契约
- ProjectionChangeListener

## Depends On (上游依赖)
- `dsh-session` [运行时依赖] - 订阅 session/event 驱动投影
  - 证据: `packages/session/session-projection/src/index.ts:22,181`

## Dependents (下游被依赖)
- `dsh-client-runtime` - projection 值类型（projectionValues）
- `dsh-client-ui-conversation` - 会话投影数据源：plan/goal/permissions/tokenUsage/sessionStats 渲染输入
- `dsh-client-ui-goal` - goal 会话投影读取（CAS ref 来源）
- `dsh-client-ui-workflow-run` - 会话数据源
- `dsh-goal` - goal 投影单元
- `dsh-host-apiproxy` - Context merge（ctx.sessionProjections）
- `dsh-plan-mode` - plan 投影单元
- `dsh-session-projection-cache` - ProjectionCheckpoint/Snapshot 类型
- `dsh-session-stats` - ProjectionDefinition 类型
- `dsh-session-title` - 注册 title 纯折单元
- `dsh-token-meter` - ctx.inject(['sessionProjections']) 注册投影
- `dsh-tool-todo` - todos 投影单元
