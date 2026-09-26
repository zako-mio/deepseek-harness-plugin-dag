# dsh-sandbox-local

- 包名: `@deepseek-ai/dsh-sandbox-local`
- 分组: G30 沙箱
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/sandbox/sandbox-local`

## 实现逻辑
LocalSandboxProvider 继承 SandboxProvider（注册 ctx.sandbox），按平台先选 runner 链（Linux bwrap→Landlock、darwin seatbelt、win32 windows-acl），仅当链有多候选时按序做功能探测，全部不可用则 fail-closed 抛 SandboxUnavailableError（src/index.ts:160-167,497-545）。confine() 把调用方 argv 包装为所选 runner 的 profile 参数，并附带 enforcement、denial签名与结构化 runner 失败规则（src/index.ts:319-338）；profiles.ts 生成 bwrap/landlock/seatbelt 三套 profile 参数（src/profiles.ts:16-57）。windows-acl rung 额外管理工作区级长期写授权与每会话私有临时写授权，并在 provider dispose 时撤销临时授权（src/index.ts:363-482）。

## Provides
- ctx.sandbox (本地进程沙箱后端：平台 runner 选择、confine 包装与写授权管理)

## Depends On (上游依赖)
- `dsh-session` [编译依赖] - 引用 SessionId 品牌以按会话/工作区对标记临时授权
  - 证据: `src/index.ts:39 type import`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
