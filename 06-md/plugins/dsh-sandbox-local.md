# dsh-sandbox-local

- 包名: `@deepseek-ai/dsh-sandbox-local`
- 分组: G15 沙箱执行
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/sandbox/sandbox-local`

## 为什么需要它（设计初衷）
dsh-sandbox seam 的本地实现，自动选 bwrap/Landlock/Seatbelt/ACL 并 fail-closed 兜底。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/sandbox/sandbox-local/README.md

## 实现逻辑
本地进程沙箱 provider(LocalSandboxProvider extends SandboxProvider):按平台链选择 runner——linux 先 bwrap 后 landlock、darwin seatbelt、win32 windows-acl,功能探测仲裁;confine(argv, policy) 返回包裹 argv+enforcement+denialSignatures;windows-acl rung 拥有写授权:每 workspace 常驻 ACE+每会话私有临时目录 ACE。

## Provides
- ctx.sandbox 服务(LocalSandboxProvider: confine())
- runner 链选择/功能探测
- windows-acl 写授权物化

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - assertNever
  - 证据: `packages/sandbox/sandbox-local/src/index.ts:36`
- `dsh-session` [编译依赖] - SessionId 会话隔离键
  - 证据: `packages/sandbox/sandbox-local/src/index.ts:39`

## Dependents (下游被依赖)
- `dsh-bash-sandbox` - ctx.sandbox.confine
- `dsh-pwsh-sandbox` - ctx.sandbox.confine
