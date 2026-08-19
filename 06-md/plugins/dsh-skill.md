# dsh-skill

- 包名: `@deepseek-ai/dsh-skill`
- 分组: G18 技能
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/skill/skill`

## 为什么需要它（设计初衷）
纯 agent skill 提供方注册表（ctx.skills）：宿主+按 scope 分层结构，不感知来源（本地/嵌入式/HTTP），提供方经 registerProvider 注册；按 modelInvocable/userInvocable 策略区分目录。为 harness 提供可插拔的技能发现/加载能力，是 skill 能力族的注册中心。

发展史：位于 packages/skill/skill，2026-08-10 首批发布，0.1.0-rc.6 转公开。本地实现为 dsh-skill-filesystem；面向模型的 skill 工具由 dsh-tool-skill 消费，注册表本身不渲染模型指引。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/skill/README.zh.md
- https://registry.npmjs.org/@deepseek-ai/dsh-skill

## 实现逻辑
Agent skill provider 注册表(能力接缝的 Service Definition 角色)。SkillRegistry(ctx.skills) 用 ScopedLayers 维护 global + per-scope 分层：registerProvider 分层注册，register 接收运行时 skill。读取面 list()/snapshot()/get()：collect 以 (cwd, scopeChain, revision) 为缓存键合并各层，就近层同名胜出；变更经 'skills/change' 事件通知。renderSkillContent 渲染成统一 <skill_content> 模型块。

## Provides
- ctx.skills(registerProvider/register/list/snapshot/get)
- skills/change 事件
- SkillProvider 契约
- renderSkillContent/escapeText + skill-invocation MessageSourceMap

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - assertNever + MessageSourceMap 注入
  - 证据: `packages/skill/skill/src/index.ts:14,155-160`

## Dependents (下游被依赖)
- `dsh-agent-spine-demo` - ctx.plugin(SkillRegistry) 技能注册表(可选)
- `dsh-client-ui-skill` - 技能目录 Remote 列表
- `dsh-host-apiproxy` - isUserInvocable（skills 域）
- `dsh-skill-badge` - provider 注册 seam
- `dsh-skill-filesystem` - provider 注册 seam
- `dsh-tool-skill` - 技能目录与正文加载
