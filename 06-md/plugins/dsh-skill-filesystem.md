# dsh-skill-filesystem

- 包名: `@deepseek-ai/dsh-skill-filesystem`
- 分组: G37 技能
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/skill/skill-filesystem`

## 实现逻辑
本地文件系统技能提供者：按 project(.dsh/.agents skill 根)/custom/user/bundled 有序根（各带 rank）发现目录式 SKILL.md 与扁平 .md 技能，解析 YAML frontmatter 与 invocation 策略后产出候选；技能正文优先经 ctx.fs 读取，无 fs 服务时退回 node fs (src/index.ts:134-266, src/index.ts:723-840)。内置 SkillWatchManager 以 chokidar/watchFile 监听技能根，并在 fs/observed 的一手写改后同步失效目录，dispose 时收敛全部 watcher (src/index.ts:288-601, src/index.ts:143-146)。

## Provides
- filesystem 技能提供者 (从项目/自定义/用户/bundled 根发现并加载本地技能注册进 ctx.skills)

## Depends On (上游依赖)
- `dsh-skill` [E1+E2] - 实现并注册文件系统技能提供者，复用其 rank 常量、候选/定义与观察结果类型契约
  - 证据: `package.json:32 peerDep + src/index.ts:23-34 import + src/index.ts:46 inject['skills'] + src/index.ts:136 ctx.skills.registerProvider`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
