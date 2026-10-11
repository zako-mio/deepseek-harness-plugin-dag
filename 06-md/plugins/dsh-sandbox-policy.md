# dsh-sandbox-policy

- 包名: `@deepseek-ai/dsh-sandbox-policy`
- 分组: G28 沙箱
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/sandbox/sandbox-policy`

## 实现逻辑
以 default 导出的 SandboxPolicyService（extends Service，注册为 ctx.sandboxPolicy，static inject=['sessionProjections']）作为沙箱策略的唯一归属：持有部署默认 mode 与 agentless 回退 workspaceRoot，resolve() 按「显式 mode 覆盖 > 会话最后一条 sandbox/mode > 部署默认」定模式，并按「会话 header.cwd > 配置回退根」定工作区根，同时带上 sessionId (src/index.ts:110-131、src/index.ts:164-171)。会话级覆盖本身以日志为存储：sandboxMode 投影只折叠最后一条 sandbox/mode 事件，setSandboxMode 是唯一写入路径（append 一条事件），因此覆盖可重放、跨会话互不可见 (src/index.ts:133-139、src/session-mode.ts:53-55)。同时经 ctx.inject(['systemPrompt']) 注册 sandbox:policy 上下文节，把解析后的策略渲染成模型可见的一句话说明——只描述策略、不盘点能力 (src/index.ts:42-56、src/index.ts:141-152)。工作区根在构造期即解析为绝对路径，非绝对路径直接报错 (src/index.ts:36-39、src/index.ts:131)。

## Provides
- ctx.sandboxPolicy (每调用沙箱策略解析：部署默认 + 会话覆盖 + 工作区根 + sessionId)
- session projection 'sandboxMode' (最后一条 sandbox/mode 覆盖，init 为 null，stateVersion 1)
- session 事件 'sandbox/mode' (log-only 的覆盖写入词汇，唯一写入路径 setSandboxMode)
- systemPrompt 上下文节 sandbox:policy (把解析后的文件策略写入缓存安全的运行时上下文)
- 导出 SANDBOX_MODES / setSandboxMode (模式词表与覆盖写入 API，供 UI 与 enforcing 工具复用)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 提示词上下文按 agent 取会话，从而解析该 agent 的策略
  - 证据: `package.json:30 peerDep + src/index.ts:27 type import（src/index.ts:146 context.agent?.session）`
- `dsh-session` [E1+E2] - 把模式覆盖写入会话日志，并从会话 header 取不可变 cwd 作为 workspace-write 边界
  - 证据: `package.json:32 peerDep + src/index.ts:29 type import Session、src/session-mode.ts:21 type import；src/session-mode.ts:54 session.append('sandbox/mode')、src/index.ts:168 session?.header.cwd`
- `dsh-session-projection` [E1+E2] - 注册并读取 sandboxMode 投影单元，作为会话级覆盖的唯一读取口
  - 证据: `package.json:35 peerDep + src/index.ts:30 type import；src/index.ts:119 inject 'sessionProjections'、src/index.ts:133 register、src/index.ts:179 stateOf(session,'sandboxMode')`
- `dsh-system-prompt` [运行时依赖] - 注册 sandbox:policy 上下文节，使模型看到当前文件策略
  - 证据: `package.json:33 peerDep + src/index.ts:31 type import；src/index.ts:141 ctx.inject(['systemPrompt'])、src/index.ts:142 ctx.systemPrompt.context`

## Dependents (下游被依赖)
- `dsh-api-terminal-controller` - 按 Session 沙箱策略选择执行提供者
- `dsh-api-workspace-files` - 会话无 cwd 时的工作区根回退
- `dsh-bash-sandbox` - 读取部署默认沙箱模式并解析每次调用的完整策略
- `dsh-client-ui-deliverables` - 按沙箱策略校验可打开路径
- `dsh-experimental-ptc-runtime-python` - 运行时默认沙箱模式与每次运行的策略解析都来自该 seam
- `dsh-fs-sandbox` - 解析每调用会话的沙箱模式与工作区根
- `dsh-fs-ssh` - 读取默认沙箱模式并在写/编辑时解析策略
- `dsh-permission-presets` - 用规范 setter 写入沙箱模式旋钮
- `dsh-plugin-manager` - 解析当前会话沙箱档以判定所需升级
- `dsh-ptc-runtime-node` - 取得部署默认文件策略与每会话模式，作为程序直接文件访问的执行策略
- `dsh-pwsh-sandbox` - 读取部署默认沙箱模式并解析每次调用的完整策略
- `dsh-subagent` - 委托时机会式消费沙箱策略服务（ctx.get 模式）
- `dsh-terminal-bash` - 解析调用方 Session 当前生效的执行策略（mode 与围栏配置）作为启动 shell 的输入
- `dsh-tool-bash` - 每次调用需解析本会话的完整常驻沙箱策略
- `dsh-tool-fs` - 解析每会话沙箱模式；受限文件系统已挂载但策略服务缺失时 fail-loud
- `dsh-tool-pwsh` - 解析本会话的常驻沙箱策略
- `dsh-tool-str-replace-editor` - 解析每调用沙箱策略并映射拒绝错误
- `dsh-tools` - 解析调用方 session 的沙箱策略并下传给受限 PTC 运行时；缺失时响亮失败
- `dsh-workflow-ptc` - 按调用方 Session 解析执行策略，作为 PTC 子进程的文件策略输入
