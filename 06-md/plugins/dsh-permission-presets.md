# dsh-permission-presets

- 包名: `@deepseek-ai/dsh-permission-presets`
- 分组: G20 交互命令
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/interaction/permission-presets`

## 实现逻辑
把沙箱模式与审批策略两个独立旋钮打包成产品级「权限预设」：PermissionPresetService 以 schemastery 校验预设表与默认预设，并要求组合在带 sandboxMode 的 shell 执行器之上（否则构造即报错）(src/index.ts:180-232)。写入路径是 /permission 命令与 set()：先追加 permission/preset 事件记录用户意图，再经 setSandboxMode / setApprovalPolicy 只写发生变化的旋钮 (src/index.ts:255-276, src/index.ts:398-418)。读取路径注册 permissions 会话投影把 preset/sandbox/approval 折叠为当前值，并通过 catalog Remote 暴露进程级目录 (src/index.ts:237-244, src/index.ts:292-299)。另有 registerAuto 为 Auto 评审集成发布仅当前会话可用的固定预设与同步准入钩子 (src/index.ts:307-317)。

## Provides
- ctx.permissionPresets (PermissionPresetService：预设表、目录、当前值、写入路径)
- Session 投影 permissions（当前生效预设值 currentValue）
- Session 事件 permission/preset（仅日志的用户意图）
- Cordis 事件 permission-presets/catalog-changed（目录失效通知）
- /permission 人类命令（切换预设的唯一写入路径）

## Depends On (上游依赖)
- `dsh-commands` [E1+E2] - 注册 /permission 命令，作为 Web 客户端使用的唯一写入入口
  - 证据: `src/index.ts:19 import { CommandDefinitionId } + src/index.ts:255-256 ctx.inject(['commands']) 后 register`
- `dsh-sandbox-policy` [编译依赖] - 用规范 setter 写入沙箱模式旋钮
  - 证据: `src/index.ts:25 import { SANDBOX_MODES, setSandboxMode } + src/index.ts:410 setSandboxMode(session, ...)`
- `dsh-session` [编译依赖] - 预设选择作为可回放的用户意图写入会话日志
  - 证据: `src/index.ts:23 import type { Session, SessionEvent } + src/index.ts:416 session.append('permission/preset')`
- `dsh-session-projection` [E1+E2] - 注册 permissions 投影，供客户端读取当前生效值
  - 证据: `src/index.ts:32 import type {} from '@deepseek-ai/dsh-session-projection' + src/index.ts:237 ctx.sessionProjections.register`
- `dsh-settings` [E1+E2] - 把 defaultPreset 作为用户设置项写入 settings 命名空间
  - 证据: `src/index.ts:14 import type {} from '@deepseek-ai/dsh-settings' + src/index.ts:210 ctx.inject(['settings'])`
- `dsh-user-approval` [E1+E2] - 审批策略是预设 bundle 的另一半旋钮，并经 approval 服务切换
  - 证据: `src/index.ts:29-30 import { APPROVAL_POLICIES, setApprovalPolicy } + src/index.ts:350 ctx.approval.config.policy`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 把该业务包的 /remote 命名空间装配进 Client
- `dsh-client-ui-permission-presets` - 复用权限目录与选择契约类型
- `dsh-experimental-auto-review` - Auto 预设的定义与注册、以及卸载时的会话降级都由该 seam 拥有
- `dsh-subagent` - 子代理继承父级权限预设
