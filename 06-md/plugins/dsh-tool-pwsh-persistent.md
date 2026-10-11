# dsh-tool-pwsh-persistent

- 包名: `@deepseek-ai/dsh-tool-pwsh-persistent`
- 分组: G34 Shell 执行
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/shell/tool-pwsh-persistent`

## 实现逻辑
持久 `pwsh` 工具，与 `dsh-tool-bash-persistent` 共用会话注册表、轮询与 reset 契约（文件头明示为刻意镜像）(src/index.ts:1-2)。命令经 `quoteForPwsh` 做反引号转义后包进 `Write-Output`/`Invoke-Expression` wrapper，以 `$LASTEXITCODE`/`$?` 归一退出码，并保持 wrapper 在单一物理行以免 PSReadLine 回显破坏提取 (src/index.ts:82-100)。轮询 scrollback 时用真实标记锚定并剥离回显的 wrapper 源码，仅非零退出才追加 `[exit code: N]` 标记 (src/index.ts:106-129、src/index.ts:187-196)；超时/中止/会话退出同样 reset 并提示下次全新开始 (src/index.ts:216-245、src/index.ts:363-381)。

## Provides
- ctx.tools 上的 `pwsh` 工具定义（owner 隔离的持久 PowerShell PTY 会话）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 以 Agent 作为会话所有者
  - 证据: `package.json:29 peerDependencies '@deepseek-ai/dsh-agent' + src/index.ts:12 type Agent`
- `dsh-terminal` [E1+E2] - 持久会话的 spawn/发送/读取/kill 由终端 seam 提供
  - 证据: `src/index.ts:14 type TerminalSessionId + src/index.ts:281 ctx.terminals.spawn + src/index.ts:347 ctx.terminals.startSend`
- `dsh-terminal-bash` [组合依赖] - Windows 侧持久会话依赖该 PTY 后端注册
  - 证据: `src/index.ts:471 backendType 默认 'shell'；packages/bundle/sdk-minimal/cordis.patch.yml:68-73 terminal-pwsh 后端由 dsh-terminal-bash 以 shellDialect: pwsh 提供`
- `dsh-tools` [E1+E2] - 工具必须注册进工具注册表
  - 证据: `src/index.ts:16 import defineTool + src/index.ts:455 inject 'tools' + src/index.ts:427 ctx.tools.register`
- `dsh-working-directory` [运行时依赖] - 会话初始 cwd 取自 owner 工作区
  - 证据: `src/index.ts:8 type import + src/index.ts:280 ctx.workingDirectory.ensure(owner, combinedSignal)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
