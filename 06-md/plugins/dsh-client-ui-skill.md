# dsh-client-ui-skill

- 包名: `@deepseek-ai/dsh-client-ui-skill`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-skill`

## 实现逻辑
提供斜杠命令的 skill 引用源并接管 skill 工具行：client/index.ts:159-226 构造 InputTriggerSource（trigger '/'、order 2），candidates 经按会话单飞的 fetchCatalog（:107-141）调用 ctx.remote.skills.list 的 skills/list RPC，再用 rankByName 做大小写无关的有序子序列排序（:170）；选中项只落纯文本 `/name `（:216-225），确定性判定留在 Host 的 dsh-tool-skill 前置边界。目录缓存按 session 键控，preset 切换时失效（:230）、connection/reset 时全清（:231），lexicon/subscribeLexicon 驱动草稿芯片（:184-196）。同时把 SkillRow 注册到键控 tool.call.toolview 的 'skill' 键（:81-84），并在 :232-238 用 effect 绑定源注册与清理。

## Provides
- InputTriggerSource '/' 的 skill 目录源（candidates/warm/lexicon/subscribeLexicon/openReference/onPick）
- 槽位贡献 tool.call.toolview 的 'skill' 键视图（SkillRow）

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - skill 目录与 skills/list 调用来自 Remote 的 skills 命名空间
  - 证据: `src/client/index.ts:37 import type { SkillEntry } from '@deepseek-ai/dsh-api-remotes/client'; src/client/index.ts:86 const skills = ctx.remote.skills`
- `dsh-api-session-controller` [E1+E2] - 取回目录前需等待会话初次历史打开成功
  - 证据: `src/client/index.ts:38 import type {} from '@deepseek-ai/dsh-api-session-controller/client'; src/client/index.ts:115 sessions.using(sessionId, { source: 'skillCatalog', ... })`
- `dsh-client-locale` [E1+E2] - 菜单与工具行文案本地化
  - 证据: `src/client/index.ts:44 import type {} from '@deepseek-ai/dsh-client-locale/client'; src/client/index.ts:80 ctx.locale.register(NS, { zh, en })`
- `dsh-client-ui-input-trigger` [E1+E2] - 斜杠触发源的注册契约由 input-trigger 定义
  - 证据: `src/client/index.ts:40 import type { InputTriggerServiceContract, InputTriggerSource } from '@deepseek-ai/dsh-client-ui-input-trigger/client'; src/client/index.ts:227 ctx.get('inputTriggers')`
- `dsh-client-ui-primitives` [编译依赖] - 候选排序复用共享的按名排序实现
  - 证据: `src/client/index.ts:42 import { rankByName } from '@deepseek-ai/dsh-client-ui-primitives'`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 服务由 renderer 提供
  - 证据: `src/client/index.ts:46 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-sidebar-right` [E1+E2] - 引用预览在右侧边栏打开 skill 文件资源
  - 证据: `src/client/index.ts:35 import type {} from '@deepseek-ai/dsh-client-ui-sidebar-right/client'; src/client/index.ts:203 ctx.sidebarRight.openResource(fileAddressFor(...))`
- `dsh-client-ui-tool` [编译依赖] - tool.call.toolview 槽由 ui-tool 声明，skill 行按其视图契约实现
  - 证据: `src/client/SkillRow.tsx:5 import ... from '@deepseek-ai/dsh-client-ui-tool/client'; src/client/index.ts:81 ctx.slots.inject('tool.call.toolview', ...)`
- `dsh-session` [编译依赖] - 目录缓存以 SessionId 为键
  - 证据: `src/client/index.ts:39 import type { SessionId } from '@deepseek-ai/dsh-session/types'`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
