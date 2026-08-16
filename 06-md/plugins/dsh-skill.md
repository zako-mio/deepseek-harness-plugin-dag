# dsh-skill

- 包名: `@deepseek-ai/dsh-skill`
- 分组: G18 技能
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/skill/skill`

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
