# dsh-client-ui-skill

- 包名: `@deepseek-ai/dsh-client-ui-skill`
- 分组: G28 设置输入UI
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-skill`

## 为什么需要它（设计初衷）
Web 端 skill 引用与专用 skill 工具行，让用户查看/调用 Agent 技能。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-skill/package.json

## 实现逻辑
技能引用源：注册 '/' source name=skill order=2（index.ts:133-178,185），候选来自 skill.list RPC 按会话缓存（session-keyed catalog fetch，单 flight，:70-115），pick 落字面 /name （plain-text-reference）。注册 tool.call.toolview keyed 'skill' 的 SkillRow（:65-68）。agent-preset/selected 失效单键、connection/reset 全清（:182-183）。

## Provides
- '/' source 'skill' (InputTriggerSource)
- tool.call.toolview key='skill' 工具行 (SkillRow)
- skill 字典 + 会话键控目录缓存

## Depends On (上游依赖)
- `dsh-client-ui-input-trigger` [编译依赖] - 注册 '/' 引用源并消费 lexicon/subscribeLexicon 契约
  - 证据: `packages/client/ui-skill/src/client/index.ts:35,57,185 (类型 import + inject inputTriggers + registerSource)`
- `dsh-client-ui-tool` [编译依赖] - keyed 工具行槽声明
  - 证据: `packages/client/ui-skill/src/client/index.ts:65 (slots.inject('tool.call.toolview'))`
- `dsh-session` [运行时依赖] - 会话身份判定与键控缓存
  - 证据: `packages/client/ui-skill/src/client/index.ts:92 (sessions.subagentAddress 判定代理子会话跳过)`
- `dsh-skill` [运行时依赖] - 技能目录 Remote 列表
  - 证据: `packages/client/ui-skill/src/client/index.ts:70,97 (connection.api.skills.list RPC)`
- `dsh-tool-skill` [运行时依赖] - host 侧技能加载器消费 pick 字面
  - 证据: `packages/client/ui-skill/src/client/index.ts:9-12 (注释：host pre-step 边界识别 /name 注入渲染 body)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
