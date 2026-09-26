# dsh-skill

- 包名: `@deepseek-ai/dsh-skill`
- 分组: G37 技能
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/skill/skill`

## 实现逻辑
技能能力 seam 的 Service Definition：实现分层技能注册表 SkillRegistry（以 'skills' 名注册 ctx 服务），按调用上下文 scope 把 provider 与运行时技能分入 global 层与各 scope 层，读取时合并 global 与 scope 链、同层内按 rank 解析同名胜出者，并按 revision+cwd+scope 链做目录缓存 (src/index.ts:356-660)。对外暴露 list/snapshot/get 读取目录与技能正文，registerProvider/register 供 provider 与运行时贡献注册，变更时提升 revision 并使缓存失效、向 skills/change 事件广播 (src/index.ts:390-517, src/index.ts:621-659)。

## Provides
- ctx.skills (技能注册表 seam：合并多渠道 provider 目录、按 scope 分层与 rank 解析唯一胜出技能，暴露 list/snapshot/get)
- skills/change 事件 (技能目录失效通知，订阅者据此重新拉取目录)

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 声明合并 dsh-llm 的 MessageSourceMap 以注册 'skill-invocation' 消息来源类型 (src/index.ts:154-159)
  - 证据: `package.json:31 peerDep + src/index.ts:14 import type`
- `dsh-scope` [编译依赖] - 复用 ScopedLayers/NamedEntries/scopeOf/scopeChainOf 实现按 agent scope 分层的注册表与缓存键 (src/index.ts:362-371)
  - 证据: `package.json:32 peerDep + src/index.ts:16-17 import`

## Dependents (下游被依赖)
- `dsh-api-session-controller` - 会话技能目录
- `dsh-skill-badge` - 向技能注册表注册 bundled provider，并复用其 BUNDLED_SKILL_RANK 与 SkillCandidate/SkillProvider 契约
- `dsh-skill-filesystem` - 实现并注册文件系统技能提供者，复用其 rank 常量、候选/定义与观察结果类型契约
- `dsh-skill-office` - 向技能注册表注册 office bundled provider，并复用其 BUNDLED_SKILL_RANK 与 SkillCandidate/SkillProvider 契约
- `dsh-tool-skill` - 解析并加载技能、渲染正文块，并读取目录快照用于计算 digest 与发布
