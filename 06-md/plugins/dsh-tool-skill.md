# dsh-tool-skill

- 包名: `@deepseek-ai/dsh-tool-skill`
- 分组: G37 技能
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/skill/tool-skill`

## 实现逻辑
注册面向模型的 skill 加载工具与持久化技能目录：defineTool 'skill' 经 ctx.skills 按 agent scope 查找并加载技能，正文渲染为 <skill_content> 块 (src/index.ts:81-161)。两个 agent/pre-step 监听器在决策后分别追加用户显式 /name 手势对应的技能注入（仅 user 来源消息可触发，src/index.ts:177-204），以及在工具对当前 agent 可见时，按目录条目摘要（sha256 digest 判重）发布或替换 session 技能目录消息 (src/index.ts:213-251, src/index.ts:328-378)。

## Provides
- skill 工具 (模型侧技能加载入口，加载完整技能指令)
- session 技能目录消息 (skill-catalog 来源的持久化目录，随技能变化发布/替换)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 订阅 agent/pre-step 注入技能正文与技能目录，并读取 agent.session 的 cwd 与事件序列
  - 证据: `package.json:30 peerDep + src/index.ts:10 import type + src/index.ts:177,213 agent/pre-step`
- `dsh-llm` [编译依赖] - 用 createUserMessage 构造带 source 的目录/注入消息，并注册 'skill-catalog' 消息来源类型
  - 证据: `package.json:31 peerDep + src/index.ts:12 import + src/index.ts:43-47 declare module`
- `dsh-session` [编译依赖] - 用 SessionSeq 回溯 session 事件序列以构造既有目录历史 (src/index.ts:361-378)
  - 证据: `package.json:44 devDep + src/index.ts:13 import`
- `dsh-skill` [E1+E2] - 解析并加载技能、渲染正文块，并读取目录快照用于计算 digest 与发布
  - 证据: `package.json:32 peerDep + src/index.ts:14-22 import + src/index.ts:25 inject['skills'] + src/index.ts:134,141,189,222 ctx.skills.list/get/snapshot`
- `dsh-tools` [E1+E2] - 注册 skill 工具并据其在当前 agent 的可见性决定是否发布技能目录
  - 证据: `package.json:33 peerDep + src/index.ts:11 import + src/index.ts:25 inject['tools'] + src/index.ts:161 ctx.tools.register + src/index.ts:220 ctx.tools.get`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
