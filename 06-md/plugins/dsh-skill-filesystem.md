# dsh-skill-filesystem

- 包名: `@deepseek-ai/dsh-skill-filesystem`
- 分组: G18 技能
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/skill/skill-filesystem`

## 为什么需要它（设计初衷）
ctx.skills 注册表的本地文件系统提供方：扫描项目/.dsh/用户级多个 skill 根目录，解析 SKILL.md 或平铺 Markdown 并注册，Chokidar 热监视目录变化实现动态发现，解决 skill 跨项目共享、编辑即生效、多根 rank 合并的问题。

发展史：与 dsh-skill（注册表）、dsh-tool-skill（模型加载工具）分层：本包只做发现与解析；项目根以最近 .git 祖先界定，限定一层发现深度，monorepo 子项目选择暂缓。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/skill-filesystem/README.zh.md

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
