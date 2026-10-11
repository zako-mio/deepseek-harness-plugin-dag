# dsh-agent-preset-registry

- 包名: `@deepseek-ai/dsh-agent-preset-registry`
- 分组: G26 Agent 预设
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/preset/agent-preset-registry`

## 实现逻辑
以 default 导出的 AgentPresetRegistry（extends TypertRemoteService，static inject=['loader','sessionProjections']）把 YAML 声明的 preset 变成可在隔离 scope 中挂载的 Cordis 插件树：register() 先做 entryListProblem 校验，再经 createScope + mountPreset 装配并保留该修订（generations/引用计数）；子树入口列表由 dsh-app-boot 的 prepareProfileEntries 按 profile 兼容策略准备，但该包属装配框架、不计入 DAG 边 (src/index.ts:81-122、src/mount.ts:204-215、src/mount.ts:209)。PresetTree 覆写 write() 为空以免内存树落盘，挂载后 auditRows 逐行审计失败与缺服务行，leakedServices 若发现子树向 root realm 泄漏服务即拒绝挂载 (src/mount.ts:9-24、src/mount.ts:211-214)。Agent 通过 bind/join 把自身 scope 的父级绑定到修订，recompose/select 只在会话尚未开始首轮时切换并写入 agent-preset/selected 事件；配套的 agentPreset 投影从 header 初始化、由该事件推进 (src/index.ts:250-274、src/index.ts:346-362、src/session.ts:35-44)。对外以 @Remote 暴露 list/read/select，并给出 compositionInventory 与 inspectCompositions 供 UI 与隔离诊断读取 (src/index.ts:194-230、src/index.ts:164-172、src/index.ts:382-392)。

## Provides
- ctx.agentPresets (AgentPresetRegistry：声明式 preset 的注册、挂载、修订保留、选择与绑定)
- session projection 'agentPreset' (会话实际运行的 preset，从创建 header 初始化并由选择事件推进)
- 事件 'agent-preset/selected'(sessionId, agentPreset) (会话已提交新 preset 的持久化通知)
- Typert Remote 方法 list/read/select (远端读取名册、声明 YAML 与提交选择)
- display 出口 presetDisplayText/isBuiltInPreset (内置 preset 走 locale 字典、用户自定义元数据不翻译)

## Depends On (上游依赖)
- `cordis-plugin-include` [编译依赖] - 以 Loader 自身的 entry-list YAML 方言导出声明，使 !!js 条件按声明原样呈现
  - 证据: `package.json:51 peerDep + src/index.ts:6 import entryListSchema`
- `cordis-plugin-loader` [编译依赖] - 复用 Loader 的入口树与入口类型来装配并审计 preset 子树
  - 证据: `package.json:52 peerDep + src/index.ts:3 与 src/mount.ts:3 import EntryTree/EntryOptions、src/definition.ts:2 type import、src/composition-inventory.ts:3 import isJsExpr`
- `dsh-agent` [编译依赖] - 把 preset 选择与绑定作用到具体 Agent 的上下文与会话
  - 证据: `package.json:53 peerDep + src/index.ts:8 type import Agent；src/index.ts:347 select(agent: Agent)`
- `dsh-session` [E1+E2] - 把 preset 选择声明为会话日志事件并实际追加，满足「模型可见即已记录」
  - 证据: `package.json:55 peerDep + src/types.ts:2 type import SessionId、src/session.ts:20 declare module '@deepseek-ai/dsh-session/types'；src/index.ts:354 session.append('agent-preset/selected')`
- `dsh-session-projection` [E1+E2] - 注册 agentPreset 投影并读取 turnBoundary 以判定会话是否已开始
  - 证据: `package.json:56 peerDep + src/session.ts:17 type import ProjectionDefinition；src/index.ts:53 inject 'sessionProjections'、src/index.ts:67 register、src/index.ts:349 stateOf('turnBoundary')`
- `dsh-settings` [运行时依赖] - 把 preset 定义排除在自动设置持久化之外
  - 证据: `package.json:57 peerDep + src/index.ts:10 type import；src/index.ts:68 ctx.inject(['settings']) → child.settings.configure({auto:false})`
- `dsh-system-prompt` [编译依赖] - 编译期契约对齐：preset 子树装配的提示词插件共用同一 systemPrompt 基线；仅声明式依赖
  - 证据: `package.json:58 peerDep + packages/preset/agent-preset-registry/tsconfig.json:42 项目引用（源码无直接 import）`
- `dsh-tools` [E1+E2] - preset 重新挂载后通知工具目录变更
  - 证据: `package.json:59 peerDep + src/index.ts:11 type import、packages/preset/agent-preset-registry/tsconfig.json:45 项目引用；src/index.ts:336 owner.emit('tools/change')`

## Dependents (下游被依赖)
- `dsh-agent-preset` - 把本行声明的预设定义提交给注册表激活
- `dsh-api-remotes` - 把该业务包的 /remote 命名空间装配进 Client
- `dsh-api-session-controller` - 解析 Session 行展示所需的 Agent 预设元数据
- `dsh-client-ui-agent-preset` - 读取 preset 名册与展示信息
- `dsh-client-ui-settings-plugin-inventory` - 预置显示名解析复用 registry 的 display 折叠，避免在本包另建一份映射
- `dsh-host-plugin-inventory` - 读取 agent preset 组合清单并投影其行
- `dsh-plugin-package-inventory-deepseek` - 可选地把请求 agent 的 preset 组合模块并入插件包清单
- `dsh-subagent` - 子代理机会式继承父级预设组合（ctx.get('agentPresets')）
