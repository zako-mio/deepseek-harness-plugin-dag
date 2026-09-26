# dsh-api-session-controller

- 包名: `@deepseek-ai/dsh-api-session-controller`
- 分组: G02 API 网关与控制器
- 拓扑层: Layer 7
- 来源层: L2 web-app
- 源码路径: `packages/api/session-controller`

## 实现逻辑
SessionController 继承 TypertRemoteService 并以 namespace 'session' 注册，构造时装配 Agent 控制器、命令、控制态、历史与列表子模块，安装 modelSelection 投影，并挂载 SessionFileReferences/SessionMediaReferences/SessionSkillCatalog/ArchivedSessionGate 子插件 (src/index.ts:135-166)。Agent 的创建/续跑统一收敛到 ApiSessionAgentController（并发 resume 去重、子代理所有权、cwd/preset 冲突判定）(src/agent.ts:170-276, 444-495)。Remote 方法覆盖冷读（list/search/inspect/page/attachment/projections）、显式写（create/selectModel/rename/fork/prompt/updateQueue/cancel）与桌面打开（openWorkspacePath/workspacePathApplications/modelCatalog）(src/index.ts:251-522)。follow/control 两个 stream 分别提供会话日志快照+增量与 Host 级投影基线+替换帧 (src/history.ts:120+, src/control.ts:42-79)。同时监听 session/created|disposed、agent/created|disposed|status|error、session/event，对外发出 api-session/* 事件 (src/index.ts:167-198)。

## Provides
- ctx.remote.session（session 命名空间：list/search/create/selectModel/initializeDefaultModel/modelCatalog/rename/fork/prompt/attachment/updateQueue/cancel/page/follow/projections/control/openWorkspacePath/workspacePathApplications）
- sessionController（Host Session 业务 API：向其他 Host 域提供 resolveAgent / inspect）
- api-session/added|removed|status|error|activity 事件，以及客户端 Session 管理（manager/projection-store/notifier）

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - Agent 创建/续跑与模型选择安装
  - 证据: `src/agent.ts:5 import + src/agent.ts:437 ctx.agents.resume`
- `dsh-agent-default-model` [运行时依赖] - 读取/保存部署默认模型
  - 证据: `src/agent.ts:9 import type {} + src/index.ts:302 ctx.agentDefaultModel.saveSelection`
- `dsh-agent-preset-registry` [运行时依赖] - 解析并挂载 Agent 预设
  - 证据: `src/agent.ts:10 import + src/agent.ts:385 ctx.get('agentPresets')`
- `dsh-api-gateway` [E1+E2] - 客户端 Remote 载体与失败类型
  - 证据: `src/client/scope.ts:4 import + src/client/sessions/manager.ts:15 import`
- `dsh-client-connection` [编译依赖] - 媒体引用与客户端连接
  - 证据: `src/media-references.ts:10 import + src/client/index.ts:5 import`
- `dsh-client-file-upload` [E1+E2] - 上传收据解析与 Agent 解析登记
  - 证据: `src/index.ts:10 import + src/index.ts:140 ctx.fileUploads.registerAgentResolver`
- `dsh-commands` [E1+E2] - 命令注册表会话侧表面
  - 证据: `src/commands.ts + src/client/sessions/remotes.ts:9 import types`
- `dsh-llm` [E1+E2] - 消息构造、assistant 流与模型目录
  - 证据: `src/commands.ts:17 import + src/catalog.ts:24 ctx.llm.listProviders`
- `dsh-scope` [编译依赖] - 作用域工具
  - 证据: `src/skill-catalog.ts:7 import`
- `dsh-session` [E1+E2] - 会话身份、事件与 fork 种子
  - 证据: `src/agent.ts:12 import + src/agent.ts:189 ctx.sessions.get`
- `dsh-session-projection` [E1+E2] - 会话投影状态与增量
  - 证据: `src/agent.ts:286 ctx.sessionProjections.stateOf + src/control.ts:22 onChanged`
- `dsh-session-projection-cache` [编译依赖] - 投影缓存类型面
  - 证据: `src/list.ts:8 import type {}`
- `dsh-session-title` [E1+E2] - 会话标题命令与客户端投影
  - 证据: `src/commands.ts:22 import + src/client/sessions/manager.ts:23`
- `dsh-settings` [运行时依赖] - 设置域参与模型/凭证表面
  - 证据: `src/catalog.ts:5 import type {} + package.json peerDependencies dsh-settings(optional)`
- `dsh-skill` [编译依赖] - 会话技能目录
  - 证据: `src/skill-catalog.ts:6 import`
- `dsh-subagent` [E1+E2] - 子代理所有权与客户端地址类型
  - 证据: `src/history.ts:19 import + src/client/sessions/manager.ts:3 import`
- `dsh-typert-registry` [编译依赖] - Typert 注册表类型
  - 证据: `src/agent.ts:16 import type {}`
- `dsh-workspace` [E1+E2] - 工作区注册表与归档会话门控
  - 证据: `src/archived-session-gate.ts:13 import + src/index.ts:111 inject 'workspaceRegistry'`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配 session 命名空间与事件类型声明
- `dsh-client-ui-agent-preset` - 按会话解析 binding 与保留态以决定 seat 归属
- `dsh-client-ui-approval` - 把 Remote 监听者 owner 解析成会话 id
- `dsh-client-ui-chat` - 按会话解析 binding 与事件源
- `dsh-client-ui-commands` - 按会话解析 scope 与 using
- `dsh-client-ui-conversation` - 按会话解析 scope 与 conversation 服务
- `dsh-client-ui-deliverables` - 解析会话与其工作目录以做原生打开
- `dsh-client-ui-goal` - 保留会话并在初始历史打开后访问 Host
- `dsh-client-ui-input-trigger` - 把槽 frame 的 sessionId 解析成会话作用域
- `dsh-client-ui-model-selection` - Session 绑定/投影与 session Remote 控制器面
- `dsh-client-ui-open-in-app` - 调用 session Remote 打开工作区路径/查询关联应用
- `dsh-client-ui-permission-presets` - Session 外观与命令执行类型
- `dsh-client-ui-plan` - Session 地址与投影类型
- `dsh-client-ui-reference` - retain 会话并用 using() 挂参考候选数据源
- `dsh-client-ui-schedule` - 会话定位与打开状态判定
- `dsh-client-ui-session` - 消费 Session Controller 的列表/绑定/快照与投影接口
- `dsh-client-ui-sidebar-right` - 会话视图类型（SidebarSessionViews 消费 SessionManager）
- `dsh-client-ui-skill` - 按 session 保留引用，等待初始历史就绪后取目录
- `dsh-client-ui-trajectory` - 读取会话 binding 与分页 loadOlder
- `dsh-client-ui-user-questions` - 把请求归属到具体会话作用域
- `dsh-client-ui-workflow-run` - 读取会话列表状态与导航目标类型
- `dsh-client-ui-workspace` - 会话列表、rename、search 与引用保留
- `dsh-experimental-client-ui-agent-team` - 读取会话绑定与保留信息定位 Lead/子会话
- `dsh-schedule` - 在到期投递时恢复/激活目标会话
