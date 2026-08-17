# dsh-tool-skill

- 包名: `@deepseek-ai/dsh-tool-skill`
- 分组: G18 技能
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/skill/tool-skill`

## 为什么需要它（设计初衷）
DeepSeek Harness 的模型侧技能加载工具，让模型按需加载 skill 能力（提供方注册表 + 本地提供方 + 目录/loader）。

来源：
- https://registry.npmjs.org/@deepseek-ai/dsh-tool-skill
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/tool-skill/README.zh.md

## 实现逻辑
apply() 注册 'skill' 模型工具(ctx.skills.list 查名、isModelInvocable 校验、ctx.skills.get 加载、renderSkillContent 渲染)。两个 agent/pre-step 监听：(1) 扫描 claimed user 消息首行 /<name> 的显式技能调用；(2) 按工具可见性发布/替换 'skill-catalog' catalog 目录消息。

## Provides
- ctx.tools: skill
- skill-catalog catalog 消息注入
- user 显式 /<skill> 调用注入

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - pre-step 注入钩子
  - 证据: `packages/skill/tool-skill/src/index.ts:10,177,213`
- `dsh-llm` [编译依赖] - createUserMessage + MessageSourceMap
  - 证据: `packages/skill/tool-skill/src/index.ts:12,197`
- `dsh-skill` [运行时依赖] - 技能目录与正文加载
  - 证据: `packages/skill/tool-skill/src/index.ts:15-22,134,141,222`
- `dsh-tools` [组合依赖] - 工具注册
  - 证据: `packages/skill/tool-skill/src/index.ts:11,161`

## Dependents (下游被依赖)
- `dsh-agent-spine-demo` - 可选 ctx.plugin(toolSkill) 模型面技能目录
- `dsh-client-ui-skill` - host 侧技能加载器消费 pick 字面
