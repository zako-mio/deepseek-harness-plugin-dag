# dsh-permission-presets

- 包名: `@deepseek-ai/dsh-permission-presets`
- 分组: G09 审批权限
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/interaction/permission-presets`

## 实现逻辑
定义 ctx.permissionPresets 服务，把 sandbox 模式与 approval policy 两个旋钮捆绑成产品级 preset 表(read-only/workspace-write/danger-full-access)。set()/apply() 先 append 'permission/preset' 事件再经 setSandboxMode/setApprovalPolicy 写各旋钮；pinInitialPermission 在 session/created 时补齐缺省旋钮。经 installSettingsSection 注册 'permission' 默认 preset 设置，注册 'permissions' 投影单元与 /permission 命令。

## Provides
- ctx.permissionPresets
- session 事件 permission/preset
- permissions 投影单元
- /permission 命令
- permission settings 命名空间

## Depends On (上游依赖)
- `dsh-commands` [组合依赖] - /permission 命令注册
  - 证据: `packages/interaction/permission-presets/src/index.ts:257`
- `dsh-sandbox-policy` [运行时依赖] - sandbox 旋钮写穿
  - 证据: `packages/interaction/permission-presets/src/index.ts:18,387`
- `dsh-user-approval` [运行时依赖] - approval 旋钮写穿
  - 证据: `packages/interaction/permission-presets/src/index.ts:23,376,389`

## Dependents (下游被依赖)
- `dsh-client-ui-conversation` - permissions 投影与 PermissionSelect 值类型
- `dsh-client-ui-permission-presets` - permissions 会话投影提供选项/当前值
