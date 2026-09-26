# dsh-client-ui-skill

- 包名: `@deepseek-ai/dsh-client-ui-skill`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-skill`

## 实现逻辑
在输入触发菜单注册 '/' 的 skill 引用源：构造 InputTriggerSource（trigger='/'、name='skill'、order=2），实现 candidates/warm/lexicon/openReference/onPick（src/client/index.ts:159-226）。目录按 session 单飞缓存并调用 ctx.remote.skills.list RPC，先等待会话初始历史 open 成功（src/client/index.ts:107-141）。同时注册 'tool.call.toolview' 的 'skill' 键 toolview 与 'skill' 字典（src/client/index.ts:80-84），并在 agent-preset/selected 与 connection/reset 时失效缓存（src/client/index.ts:230-231）。

## Provides
- inputTriggers 源：trigger '/'，name 'skill'（候选/预热/词典/打开引用/选中回填）
- slot tool.call.toolview key='skill' 的 SkillRow 专用渲染
- locale 命名空间 'skill' 字典

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 调用 skills/list 与订阅 agent-preset/selected
  - 证据: `src/client/index.ts:37 import + src/client/index.ts:86 ctx.remote.skills`
- `dsh-api-session-controller` [E1+E2] - 按 session 保留引用，等待初始历史就绪后取目录
  - 证据: `src/client/index.ts:38 import + src/client/index.ts:115 sessions.using`
- `dsh-client-locale` [E1+E2] - 注册 skill 字典
  - 证据: `src/client/index.ts:44 + src/client/index.ts:80 ctx.locale.register`
- `dsh-client-ui-input-trigger` [E1+E2] - 注册斜杠菜单的 skill 候选源
  - 证据: `src/client/index.ts:40 import type + src/client/index.ts:227-238 registerSource`
- `dsh-client-ui-primitives` [编译依赖] - 候选按名称排序（与命令组一致）
  - 证据: `src/client/index.ts:42 rankByName`
- `dsh-client-ui-renderer` [编译依赖] - 拉入 SlotRegistry 服务合并类型
  - 证据: `src/client/index.ts:46 import type`
- `dsh-client-ui-sidebar-right` [E1+E2] - 点击 skill 引用时在侧栏打开其文件资源
  - 证据: `src/client/index.ts:35 import type + src/client/index.ts:203 ctx.sidebarRight.openResource`
- `dsh-client-ui-tool` [编译依赖] - 复用 tool.call.toolview 的 props 类型契约
  - 证据: `src/client/SkillRow.tsx:5 ToolCallViewProps`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/index.ts:39 SessionId`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
