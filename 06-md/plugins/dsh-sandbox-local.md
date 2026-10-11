# dsh-sandbox-local

- 包名: `@deepseek-ai/dsh-sandbox-local`
- 分组: G28 沙箱
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/sandbox/sandbox-local`

## 实现逻辑
以 default 导出的 LocalSandboxProvider（extends SandboxProvider，注册为 ctx.sandbox）实现本地进程沙箱 provider：先按平台选 runner 链（linux: bwrap→landlock、darwin: seatbelt、win32: windows-acl），单候选直接选定、多候选才用功能性探测仲裁，链为空或全部不可用即抛 SandboxUnavailableError 失败关闭 (src/index.ts:160-167、src/index.ts:503-551)。confine() 把调用方 argv 包进所选 runner 的 profile 参数，并随结果附带 enforcement、denialSignatures 与结构化 runner 失败规则（含 Landlock 的 exit 125 与 windows-acl 的 exit 127） (src/index.ts:325-344、src/index.ts:207-242)。profile 构造集中在本包的 profiles.ts：bwrap 用 ro-bind/tmpfs、landlock 用 grantArgs 白名单、seatbelt 用 SBPL 文本且可写根取自 dsh-sandbox 的 writableRoots 以避免与 fs 围栏漂移 (src/profiles.ts:16-57)。windows-acl 档额外拥有写授权：每工作区一份常驻 AclWriteGrant 复用缓存、每会话随机私有临时目录一份可撤销授权，provider dispose 时撤销临时授权并删除临时目录 (src/index.ts:403-454、src/index.ts:465-494)。

## Provides
- ctx.sandbox (本地进程沙箱 provider：平台 runner 链、功能性探测、fail-closed 的 argv 包裹与失败分类事实)
- 每平台 runner 的 denialSignatures 与 RunnerFailureRule 词表 (供调用方区分「命令没跑」与「命令被拒」)
- Windows 受限令牌档的写授权生命周期 (每工作区常驻 ACE + 每会话随机私有临时目录的可撤销 ACE)

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 编译期依赖基线对齐（沙箱 provider 与工具/llm 层共用同一工作区依赖图）；仅声明式依赖
  - 证据: `package.json:31 peerDep + packages/sandbox/sandbox-local/tsconfig.json:24 项目引用（源码无直接 import）`
- `dsh-session` [编译依赖] - 以 SessionId 作为每会话私有临时目录写授权的键，隔离同工作区的不同会话
  - 证据: `package.json:33 peerDep + src/index.ts:39 type import SessionId、packages/sandbox/sandbox-local/tsconfig.json:33 项目引用；src/index.ts:403 materializeAclGrant(sessionId, workspaceRoot)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
