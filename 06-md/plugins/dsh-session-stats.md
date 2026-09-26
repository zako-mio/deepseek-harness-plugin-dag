# dsh-session-stats

- 包名: `@deepseek-ai/dsh-session-stats`
- 分组: G33 会话核心
- 拓扑层: Layer 4
- 来源层: L2 web-app
- 源码路径: `packages/session/session-stats`

## 实现逻辑
以函数插件向 ctx.sessionProjections 注册 sessionStats 单元（src/index.ts:27-29）。该单元纯同步折叠 step/start、assistant/attempt、assistant/message、tool/call、tool/result、step/end、turn/end，产出整日志的 turns/steps 计数与 llm/tool/ttft/decode 墙钟时间（src/projection.ts:113-212）；以 step/end 而非 assistant/message 计步以正确覆盖失败/取消/超限步骤。stateVersion=1，wire 视图仅暴露会话总计（src/projection.ts:199-211）。

## Provides
- sessionStats 投影单元（经 ctx.sessionProjections 交付整会话计数与墙钟时间）

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 复用 assistantStreamFirstTokenTime 计算首 token 延迟
  - 证据: `src/projection.ts:27 import`
- `dsh-session-projection` [E1+E2] - 把 sessionStats 单元注册到投影注册表并交付客户端视图
  - 证据: `src/projection.ts:28 import + src/index.ts:20 static inject + src/index.ts:28 ctx.sessionProjections.register`

## Dependents (下游被依赖)
- `dsh-client-ui-chat` - 统计胶囊数据源
