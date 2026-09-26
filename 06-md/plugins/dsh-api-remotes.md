# dsh-api-remotes

- 包名: `@deepseek-ai/dsh-api-remotes`
- 分组: G02 API 网关与控制器
- 拓扑层: Layer 9
- 来源层: L2 web-app
- 源码路径: `packages/api/remotes`

## 实现逻辑
Host 侧 apply() 把 remoteEventSource(ctx) 注册进 ctx.typertGateway.registerRemoteEvents，并用 ctx.effect 绑定其生命周期 (src/index.ts:40-45)。remoteEventSource 按 API_REMOTE_FORWARDED_EVENTS 白名单逐条挂 Cordis 监听：emit 型把参数经 assertJsonArgs 校验后入队，waterfall 型先校验请求携带的 Agent 与 carrierKeyOf(this) 一致，再经 forwardWaterfall 把 settle 交给 Gateway 关联 (src/index.ts:48-81, 134-158)。该白名单是唯一真相源，被 Host 转发循环与消费端 ctx.remote.$on 键面共同读取 (src/remote-events.ts:20-48)。client/index.ts 作为平台无关装配点，导入全部 Remote 命名空间并导出其类型面 (src/client/index.ts:3-100)。

## Provides
- ctx.remote 的命名空间装配（应用级远程 BFF 入口）
- API_REMOTE_FORWARDED_EVENTS 转发事件白名单（emit/waterfall 模式）与对应的 Host 事件源

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - waterfall 请求携带的 Agent 类型
  - 证据: `src/index.ts:5 import type Agent`
- `dsh-agent-preset-registry` [编译依赖] - 装配 agent preset registry 命名空间
  - 证据: `src/client/index.ts:4 import remote + src/client/index.ts:75 import types`
- `dsh-api-account-controller` [编译依赖] - 装配 account 命名空间
  - 证据: `src/client/index.ts:6 import remote`
- `dsh-api-gateway` [E1+E2] - 注册转发事件源并使用客户端 Remote 载体
  - 证据: `src/index.ts:6 import type + src/index.ts:42 ctx.typertGateway.registerRemoteEvents`
- `dsh-api-job-controller` [编译依赖] - 装配 job 命名空间
  - 证据: `src/client/index.ts:23 import remote`
- `dsh-api-session-controller` [编译依赖] - 装配 session 命名空间与事件类型声明
  - 证据: `src/client/index.ts:22 import remote + src/remote-events.ts:9 import remote-events`
- `dsh-api-settings-controller` [编译依赖] - 装配 settings/credentials 命名空间
  - 证据: `src/client/index.ts:7 import remote`
- `dsh-api-terminal-controller` [编译依赖] - 装配 terminal 命名空间
  - 证据: `src/client/index.ts:25 import remote`
- `dsh-api-workspace-controller` [编译依赖] - 装配 workspace 命名空间
  - 证据: `src/client/index.ts:24 import remote`
- `dsh-api-workspace-files` [编译依赖] - 装配 workspaceFiles 命名空间
  - 证据: `src/client/index.ts:26 import remote`
- `dsh-client-connection` [编译依赖] - 客户端连接类型再导出
  - 证据: `src/client/index.ts:88 import types`
- `dsh-client-file-upload` [编译依赖] - 装配文件上传命名空间
  - 证据: `src/client/index.ts:19 import remote + src/client/index.ts:51 import remote`
- `dsh-client-ui-plugin-manager` [编译依赖] - 装配插件管理 UI 探针命名空间
  - 证据: `src/client/index.ts:14 import remote + src/client/index.ts:37 import remote`
- `dsh-command-feedback` [编译依赖] - 装配命令反馈命名空间
  - 证据: `src/client/index.ts:18 import remote + src/client/index.ts:50 import remote`
- `dsh-commands` [编译依赖] - 装配 commands 命名空间与事件签名
  - 证据: `src/client/index.ts:5 import remote + src/client/index.ts:71 import types`
- `dsh-cordis-host-runner` [编译依赖] - 装配动态包运行器命名空间
  - 证据: `src/client/index.ts:12 import remote + src/client/index.ts:94 import remote`
- `dsh-goal` [编译依赖] - 装配 goal 命名空间
  - 证据: `src/client/index.ts:9 import remote + src/client/index.ts:43 import remote`
- `dsh-host-plugin-inventory` [编译依赖] - 装配插件清单命名空间
  - 证据: `src/client/index.ts:15 import remote + src/client/index.ts:38 import types`
- `dsh-llm` [编译依赖] - 装配 llm 命名空间
  - 证据: `src/client/index.ts:11 import remote + src/client/index.ts:74 import types`
- `dsh-message-feedback` [编译依赖] - 装配消息反馈命名空间
  - 证据: `src/client/index.ts:16 import remote + src/client/index.ts:48 import remote`
- `dsh-office-to-pdf` [编译依赖] - 装配 office-to-pdf 命名空间
  - 证据: `src/client/index.ts:8 import remote + src/client/index.ts:45 import remote`
- `dsh-permission-presets` [编译依赖] - 装配权限预设命名空间与事件
  - 证据: `src/client/index.ts:17 import remote + src/remote-events.ts:11 import types`
- `dsh-plugin-manager` [编译依赖] - 装配插件管理命名空间与事件
  - 证据: `src/client/index.ts:13 import remote + src/remote-events.ts:12 import types`
- `dsh-schedule` [编译依赖] - 装配 schedule 命名空间
  - 证据: `src/client/index.ts:10 import remote + src/client/index.ts:44 import remote`
- `dsh-scope` [E1+E2] - 从 waterfall 的 this 提取 carrier Agent 作用域
  - 证据: `src/index.ts:13 import carrierKeyOf + package.json peerDependencies dsh-scope`
- `dsh-session-reference` [编译依赖] - 装配会话引用命名空间
  - 证据: `src/client/index.ts:20 import remote + src/client/index.ts:52 import remote`
- `dsh-settings` [编译依赖] - 设置事件类型声明
  - 证据: `src/index.ts:28 import types`
- `dsh-subagent` [编译依赖] - 装配 subagent 命名空间与客户端类型
  - 证据: `src/client/index.ts:21 import remote + src/client/index.ts:53 import remote`
- `dsh-user-approval` [编译依赖] - 审批 waterfall 事件签名
  - 证据: `src/index.ts:29 import type {}`
- `dsh-user-questions` [编译依赖] - 用户提问 waterfall 事件签名
  - 证据: `src/index.ts:30 import type {}`

## Dependents (下游被依赖)
- `dsh-client-ui-agent-preset` - 读取 preset 名册并订阅设置文档变更
- `dsh-client-ui-approval` - 订阅审批请求瀑布
- `dsh-client-ui-chat` - 引入 ctx.remote 与转发事件声明
- `dsh-client-ui-commands` - 拉取 Host 命令目录并订阅变更
- `dsh-client-ui-cordis` - 经 Remote 命名空间同步宿主侧 cordis 事件与库存
- `dsh-client-ui-deliverables` - 引入 ctx.remote 与事件声明
- `dsh-client-ui-directory-picker-browse` - 目录列举结果类型
- `dsh-client-ui-goal` - 目标 Remote 读取与 CAS 改动
- `dsh-client-ui-message-feedback` - 调用 messageFeedback/sessionFeedback Remote 记录反馈
- `dsh-client-ui-model-selection` - 读模型目录 Remote 与转发事件
- `dsh-client-ui-open-in-app` - ctx.remote 与 Remote 结果类型
- `dsh-client-ui-permission-presets` - 写 defaultPreset 与读 Session 投影
- `dsh-client-ui-plan` - ctx.remote 与 Remote 转发事件面
- `dsh-client-ui-plugin-manager` - 调用 pluginManager 等 Remote 并订阅 Host 事件
- `dsh-client-ui-reference` - 文件与会话候选的 Remote 查询
- `dsh-client-ui-schedule` - ctx.remote 与 Remote 事件面
- `dsh-client-ui-session` - ctx.remote 声明合并
- `dsh-client-ui-settings` - 读配置 describe 与写 settings 命名空间
- `dsh-client-ui-settings-account` - 调用 account/session Remote 与订阅转发事件
- `dsh-client-ui-settings-general` - 判断 loopback 以决定是否注册本地设置文档动作
- `dsh-client-ui-settings-models` - 订阅 Host 推送的设置/凭据/适配器失效事件
- `dsh-client-ui-settings-plugin-inventory` - 获取 Host 插件清单快照
- `dsh-client-ui-settings-subagent` - 订阅 Host 推送的适配器/设置失效事件
- `dsh-client-ui-settings-web-search` - 订阅 Host 推送的凭据失效事件以刷新密钥态
- `dsh-client-ui-sidebar-documentpreview` - 经 remote 面读取工作区文件字节与分页文本
- `dsh-client-ui-sidebar-files` - 经 remote 面列目录/订阅文件变更
- `dsh-client-ui-skill` - 调用 skills/list 与订阅 agent-preset/selected
- `dsh-client-ui-tool` - 提供 Host home 事实用于 POSIX ~ 显示
- `dsh-client-ui-user-questions` - 订阅 Host 的 user-questions/request waterfall
- `dsh-client-ui-workspace` - Host 目录选择器与 $host 事实
- `dsh-cordis-client-runner` - 跨平面调用宿主半运行、获取客户端代码与上报失败
- `dsh-experimental-client-ui-voice-input` - 在 Client 注册实验 Remote 贡献
