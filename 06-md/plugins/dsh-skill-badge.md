# dsh-skill-badge

- 包名: `@deepseek-ai/dsh-skill-badge`
- 分组: G37 技能
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/skill/skill-badge`

## 实现逻辑
内置技能提供者插件：构造单个 dsh-badge 技能候选（bundled 来源、BUNDLED_SKILL_RANK 优先级、资源基目录指向 ../assets/），list 返回静态候选、get 读取 assets/dsh-badge.md 正文 (src/index.ts:25-50)。apply 时经 ctx.skills.registerProvider 注册名为 'dsh-badge' 的 provider (src/index.ts:57-60)。

## Provides
- dsh-badge 技能 (bundled 提供者：向 ctx.skills 注册官方 powered-by-dsh 徽章技能)

## Depends On (上游依赖)
- `dsh-skill` [E1+E2] - 向技能注册表注册 bundled provider，并复用其 BUNDLED_SKILL_RANK 与 SkillCandidate/SkillProvider 契约
  - 证据: `package.json:30 peerDep + src/index.ts:10-15 import + src/index.ts:55 inject['skills'] + src/index.ts:59 ctx.skills.registerProvider`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
