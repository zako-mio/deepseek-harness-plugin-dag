# dsh-agent-presets

- 包名: `@deepseek-ai/dsh-agent-presets`
- 分组: G25 宿主服务
- 拓扑层: Layer 3
- 来源层: L2 web-app
- 源码路径: `packages/preset/agent-presets`

## 为什么需要它（设计初衷）
按 preset 目录（agent.cordis.yml）做每会话 agent 组合，会话经 scope 父链加入常驻挂载，冷读也可解析。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/preset/agent-presets/README.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/notes/implemented/architecture/2026-08-03-per-session-agent-presets.md

## 实现逻辑
AgentPresets 服务（ctx.agentPresets）：discovery 扫描配置根+用户根，preset 组合文件按 preset 单飞 standing mount（standing map），mount() 经 bindScopeParent 把 agent scope 父链到挂载；settings 命名空间存默认 preset（热重载）；监听 agent/created 告警未入册 agent、转发 agent-preset/selected 事件。

## Provides
- ctx.agentPresets（list/resolve/mount/composeFrom/read/copy/roots）
- agent-preset/selected 事件
- settings 命名空间 'agent-presets'

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - Context merge（agent/created 事件）
  - 证据: `packages/preset/agent-presets/package.json:42; src/index.ts:29`
- `dsh-session` [编译依赖] - peerDependencies（session/event）
  - 证据: `packages/preset/agent-presets/package.json:47`
- `dsh-system-prompt` [编译依赖] - peerDependencies（preset 组合内 prompt 段）
  - 证据: `packages/preset/agent-presets/package.json:49`

## Dependents (下游被依赖)
- `dsh-client-ui-agent-preset` - host 名录 roster 与默认 preset 持久化
- `dsh-host-apiproxy` - resolveSessionPreset/preset 错误类型（agentPresets.* 域）
