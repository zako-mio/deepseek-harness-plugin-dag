# dsh-api-session-controller

- 包名: `@deepseek-ai/dsh-api-session-controller`
- 分组: G02 API 网关与控制器
- 拓扑层: Layer 7
- 来源层: L2 web-app
- 源码路径: `packages/api/session-controller`

## 实现逻辑
实现 Host 侧 Session 业务 API：SessionController 继承 TypertRemoteService 并以 namespace 'session' 注册 ctx.sessionController(src/index.ts:105,143)，静态注入 agents/sessions/sessionProjections/sessionQuery/workspaceRegistry 等服务(src/index.ts:106-118)。它把 list/search/create/rename/fork/prompt/cancel/page/follow/control/projections 等 Remote 方法委托给 agent/commands/history/control/list 子控制器(src/index.ts:259-560)，并由子插件提供文件引用、媒体引用、技能目录与归档门控(src/index.ts:167-173)。同时订阅 session/agent 生命周期事件向外广播 api-session/* 增量(src/index.ts:175-206)。

## Provides
- ctx.sessionController(Host Session 业务 API 与 ctx.remote.session 命名空间所有者，src/index.ts:72-105)
- ctx.remote.session 远程方法集 list/search/create/rename/fork/prompt/cancel/page/follow/control/projections 等(src/index.ts:259-560)
- Host 事件 api-session/added|removed|status|error|activity(src/index.ts:175-206)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 激活/恢复 Session 的 Agent 并读取其状态
  - 证据: `package.json:80 peerDep + src/agent.ts:5 import + src/index.ts:106 inject 'agents' + src/index.ts:196 ctx.agents.get`
- `dsh-agent-default-model` [E1+E2] - 读写默认模型选择
  - 证据: `package.json:81 peerDep + src/agent.ts:9 import + src/index.ts:107 inject 'agentDefaultModel' + src/index.ts:310 ctx.agentDefaultModel.saveSelection`
- `dsh-agent-preset-registry` [编译依赖] - 解析 Session 行展示所需的 Agent 预设元数据
  - 证据: `package.json:82 peerDep + src/agent.ts:10 import + src/list.ts:6 import`
- `dsh-api-gateway` [E1+E2] - Client 面通过 Gateway 的 ctx.remote 调用本命名空间
  - 证据: `package.json:83 peerDep + src/client/scope.ts:4 import '@deepseek-ai/dsh-api-gateway/client' + src/client/sessions/manager.ts:15 同源导入`
- `dsh-client-connection` [E1+E2] - 媒体引用 HTTP 端点复用连接层的请求鉴权
  - 证据: `package.json:85 peerDep + src/media-references.ts:10 import + src/media-references.ts:67 inject 'connection'`
- `dsh-client-file-upload` [E1+E2] - 为上传文件注册 Session→Agent 解析器
  - 证据: `package.json:86 peerDep + src/commands.ts:12-13 import + src/index.ts:148 ctx.fileUploads.registerAgentResolver`
- `dsh-commands` [编译依赖] - 复用命令目录词汇与 Client 契约
  - 证据: `package.json:87 peerDep + src/client/sessions/remotes.ts:9 import '@deepseek-ai/dsh-commands/types'`
- `dsh-llm` [E1+E2] - 构建模型目录与推理档选项
  - 证据: `package.json:91 peerDep + src/agent.ts:11 import + src/index.ts:112 inject 'llm' + src/catalog.ts:24 ctx.llm`
- `dsh-session` [E1+E2] - 读写 Session 事件日志与当前附着状态
  - 证据: `package.json:94 peerDep + src/index.ts:12 import + src/index.ts:113 inject 'sessions' + src/index.ts:241 ctx.sessions.get`
- `dsh-session-projection` [E1+E2] - 定义并读取会话投影(含模型选择投影)
  - 证据: `package.json:96 peerDep + src/model-selection-projection.ts:5 import + src/index.ts:114 inject 'sessionProjections'`
- `dsh-session-projection-cache` [E1+E2] - 迁移待完成时返回缓存投影提示
  - 证据: `package.json:97 peerDep(optional) + src/index.ts:14 import + src/index.ts:522 ctx.get('sessionProjectionCache')`
- `dsh-session-title` [编译依赖] - 重命名会话时生成/校验标题
  - 证据: `package.json:99 peerDep + src/commands.ts:22 import + src/client/sessions/manager.ts:23 import '/client'`
- `dsh-settings` [编译依赖] - 读取模型目录相关设置声明
  - 证据: `package.json:100 peerDep(optional) + src/catalog.ts:5 import type {}`
- `dsh-skill` [编译依赖] - 筛选用户可调用的技能
  - 证据: `package.json:101 peerDep + src/skill-catalog.ts:6 import isUserInvocable`
- `dsh-subagent` [编译依赖] - 在会话谱系与快照中标注子 Agent 后代
  - 证据: `package.json:102 peerDep + src/history.ts:19 import + src/client/contract/sessions.ts:8 import '/client'`
- `dsh-typert-registry` [运行时依赖] - 把本服务的 Remote 定义注册进 Typert registry
  - 证据: `package.json:104 peerDep + src/agent.ts:16 import '@deepseek-ai/dsh-typert-registry'`
- `dsh-working-directory` [E1+E2] - 解析会话当前工作目录
  - 证据: `package.json:109 peerDep + src/skill-catalog.ts:7 import + src/skill-catalog.ts:21 inject 'workingDirectory'`
- `dsh-workspace` [E1+E2] - 按工作区登记会话并实现归档准入
  - 证据: `package.json:108 peerDep + src/commands.ts:26 import + src/index.ts:117 inject 'workspaceRegistry' + src/archived-session-gate.ts:44 ctx.workspaceRegistry`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 把该业务包的 /remote 命名空间装配进 Client
- `dsh-client-ui-agent-preset` - 按会话绑定解析 preset 状态
- `dsh-client-ui-approval` - 把 Remote 监听者 owner 解析成会话 id
- `dsh-client-ui-chat` - 会话绑定、事件流与分叉
- `dsh-client-ui-commands` - 按会话作用域解析 popup 控制器
- `dsh-client-ui-conversation` - 会话绑定、作用域与事件流
- `dsh-client-ui-deliverables` - 会话控制器类型
- `dsh-client-ui-goal` - 按会话取投影并用 using 保留引用
- `dsh-client-ui-input-trigger` - 把槽 frame 的 sessionId 解析成会话作用域
- `dsh-client-ui-model-selection` - 按会话寻址目录并判断 subagent
- `dsh-client-ui-open-in-app` - 会话与远程调用类型
- `dsh-client-ui-permission-presets` - 按会话读取 permissions 投影
- `dsh-client-ui-plan` - 按会话绑定与 subagent 寻址
- `dsh-client-ui-reference` - retain 会话并用 using() 挂参考候选数据源
- `dsh-client-ui-schedule` - 判断任务所属会话是否仍可打开（可用性判定读会话列表快照）
- `dsh-client-ui-session` - 消费 Session Controller 的列表/绑定/快照与投影接口
- `dsh-client-ui-sidebar-right` - 保留已打开会话的视图，标签按会话作用域存活
- `dsh-client-ui-skill` - 取回目录前需等待会话初次历史打开成功
- `dsh-client-ui-subagent` - 子 Agent 目录来自会话投影，刷新经 sessions 服务
- `dsh-client-ui-trajectory` - 取会话绑定以读取快照并翻页加载更早历史
- `dsh-client-ui-workflow-run` - 会话目标与绑定类型由会话控制器定义
- `dsh-client-ui-workspace` - 会话检索、fork 与归档动作走会话控制器
- `dsh-experimental-client-ui-agent-team` - 读取会话绑定与保留信息定位 Lead/子会话
- `dsh-experimental-client-ui-claude-code-mods` - 客户端类型面需要会话控制器声明以取得会话身份
- `dsh-experimental-client-ui-cot-translation` - 未激活会话需要先走 GUI 激活流程才能翻译
- `dsh-experimental-client-ui-voice-input` - 客户端会话控制器的声明依赖，保证组合中存在同一份实现
- `dsh-experimental-session-inspector` - 会话绑定类型与事件源由会话控制器提供
- `dsh-schedule` - 到期时经既有控制器恢复原会话的 Agent，保证 preset 组合与并发激活只有一个所有者
