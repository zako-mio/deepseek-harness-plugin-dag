# dsh-skill-filesystem

- 包名: `@deepseek-ai/dsh-skill-filesystem`
- 分组: G18 技能
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/skill/skill-filesystem`

## 实现逻辑
apply() 在 ctx.skills.registerProvider 注册 filesystem provider；list() 扫描 project(.dsh/skills,.agents/skills)/custom/user/bundled 根，按 source rank 排序；get() 解析 frontmatter 并经 ctx.fs 读正文；SkillWatchManager 以 chokidar 监控根目录并调 control.invalidate；ctx.on('fs/observed') 监听模型写后失效。

## Provides
- ctx.skills 的 filesystem provider
- project/custom/user/bundled skill 发现
- frontmatter 解析与 watch 失效

## Depends On (上游依赖)
- `dsh-skill` [组合依赖] - provider 注册 seam
  - 证据: `packages/skill/skill-filesystem/src/index.ts:46,132`

## Dependents (下游被依赖)
- `dsh-agent-spine-demo` - ctx.plugin(SkillFileSystem) 本地技能提供者
