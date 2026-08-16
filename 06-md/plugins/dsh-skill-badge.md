# dsh-skill-badge

- 包名: `@deepseek-ai/dsh-skill-badge`
- 分组: G18 技能
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/skill/skill-badge`

## 实现逻辑
apply() 在 ctx.skills.registerProvider 注册不可变内置 provider 'dsh-badge'：list 返回单个 CANDIDATE，get 读取 assets/dsh-badge.md。注意：交付 CLI 在 bundle/base/cordis.patch.yml:245 声明 disabled:true，启用该配置行才是显式 opt-in。

## Provides
- ctx.skills 的 'dsh-badge' bundled provider

## Depends On (上游依赖)
- `dsh-skill` [组合依赖] - provider 注册 seam
  - 证据: `packages/skill/skill-badge/src/index.ts:55,59`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
