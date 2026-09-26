# dsh-permission-presets

- 包名: `@deepseek-ai/dsh-permission-presets`
- 分组: G21 交互命令
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/interaction/permission-presets`

## 实现逻辑
实现 ctx.permissionPresets 服务：以预设名→(sandbox 模式, approval 策略) 表把用户选择写穿到各自的规范 setter（src/index.ts:398-418）。注册 permissions Session 投影以折叠三个整值 knob 事件并派生当前预设（custom 兜底）（src/index.ts:237-244、348-361），/permission 命令是 Web 客户端的唯一写路径（src/index.ts:255-276）。会话创建时 pinInitialPermission 补齐缺失权限事实（src/index.ts:428-456），并支持 Auto 评审集成的 registerAuto 同步准入（src/index.ts:307-317）。

## Provides
- ctx.permissionPresets (权限预设服务：sandbox/approval 绑定切换 + permissions 投影 + /permission 命令，src/index.ts:180-479)

## Depends On (上游依赖)
- `dsh-commands` [E1+E2] - 以 /permission 命令暴露唯一写路径
  - 证据: `package.json:57 peerDep + src/index.ts:19、:33 import; src/index.ts:255 ctx.inject(['commands'])、:256 commands.register`
- `dsh-invariants` [E1+E2] - 注册 preset 事件可解析性不变量
  - 证据: `package.json:58 peerDep + src/invariant.ts:5 import; src/invariant.ts:43 ctx.invariants.register`
- `dsh-sandbox-policy` [E1+E2] - 按预设写穿 sandbox/mode 规范 setter
  - 证据: `package.json:60 peerDep + src/index.ts:25 import setSandboxMode/SANDBOX_MODES; src/index.ts:410 setSandboxMode`
- `dsh-session` [E1+E2] - 记录预设选择与会话权限覆盖
  - 证据: `package.json:61 peerDep + src/index.ts:23 import Session; src/index.ts:416 session.append('permission/preset')`
- `dsh-session-projection` [E1+E2] - 注册 permissions 会话投影
  - 证据: `package.json:62 peerDep + src/index.ts:32 type import; src/index.ts:237 ctx.sessionProjections.register`
- `dsh-settings` [E1+E2] - 为 defaultPreset 提供用户设置默认值
  - 证据: `package.json:82 devDep + src/index.ts:14 type import; src/index.ts:210 ctx.inject(['settings']) 配置 auto 默认`
- `dsh-user-approval` [E1+E2] - 按预设写穿 approval 策略
  - 证据: `package.json:64 peerDep + src/index.ts:29-30 import setApprovalPolicy/APPROVAL_POLICIES; src/index.ts:272 ctx.approval.setPolicy、:399 setApprovalPolicy`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配权限预设命名空间与事件
- `dsh-client-ui-permission-presets` - 权限目录/选项与预设协议（Host client 面）
- `dsh-experimental-auto-review` - 注册 Auto 预设并读取/设置当前 session 预设
- `dsh-subagent` - 继承 auto/full-access 权限预设身份
