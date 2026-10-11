# dsh-skill-filesystem

- 包名: `@deepseek-ai/dsh-skill-filesystem`
- 分组: G35 技能
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/skill/skill-filesystem`

## 实现逻辑
作为 `ctx.skills` provider 注册表的一个实现，把项目、自定义与用户技能根映射为技能候选：apply 通过 `ctx.skills.registerProvider` 建立 `FileSystemSkillProvider` 并挂载 dispose 效应 (src/index.ts:133-146)。roots() 按固定 rank 组装 `.dsh/skills`、`.agents/skills`、customSkillDirs、用户 home 与 bundled 根，findProjectRoot 自 cwd 向上找 `.git` (src/index.ts:244-264、src/index.ts:952-962)。发现阶段读目录并用 YAML frontmatter 解析 name/description/invocation（旧字段名显式拒绝），读取优先走 `ctx.get('fs')` 并回退 Node fs，缺失/非文本文件按不可用处理 (src/index.ts:730-847、src/index.ts:1007-1043)。SkillWatchManager 用 chokidar 或祖先 `watchFile` 观测根目录变化，按项目数上限淘汰并以 microtask 合并失效通知；同时订阅 `fs/observed` 在 edit/write 后立即失效 (src/index.ts:287-340、src/index.ts:142-145)。

## Provides
- ctx.skills 上的 `filesystem` 技能提供者（项目/自定义/用户/bundled 根的发现、frontmatter 解析与宿主变更监听）

## Depends On (上游依赖)
- `dsh-skill` [E1+E2] - 技能 provider 契约、候选与排名常量由技能 seam 定义
  - 证据: `src/index.ts:22-33 import SkillProvider/SkillCandidate/isSkillName/BUNDLED_SKILL_RANK + src/index.ts:45 inject ['skills'] + src/index.ts:135 ctx.skills.registerProvider`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
