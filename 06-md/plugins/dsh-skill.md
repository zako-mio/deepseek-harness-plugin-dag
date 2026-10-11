# dsh-skill

- 包名: `@deepseek-ai/dsh-skill`
- 分组: G35 技能
- 拓扑层: Layer 0
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

## Dependents (下游被依赖)
- `dsh-api-session-controller` - 筛选用户可调用的技能
- `dsh-skill-badge` - 向技能注册表注册 bundled provider，并复用其 BUNDLED_SKILL_RANK 与 SkillCandidate/SkillProvider 契约
- `dsh-skill-filesystem` - 技能 provider 契约、候选与排名常量由技能 seam 定义
- `dsh-skill-office` - 向技能注册表注册 office bundled provider，并复用其 BUNDLED_SKILL_RANK 与 SkillCandidate/SkillProvider 契约
- `dsh-tool-skill` - 技能查询、快照、渲染与调用策略由技能 seam 提供
