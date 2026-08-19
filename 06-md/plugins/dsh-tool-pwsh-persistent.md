# dsh-tool-pwsh-persistent

- 包名: `@deepseek-ai/dsh-tool-pwsh-persistent`
- 分组: G14 Shell工具
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/shell/tool-pwsh-persistent`

## 为什么需要它（设计初衷）
为Windows提供持久PTY PowerShell会话工具(镜像bash-persistent)，使模型跨调用保持PowerShell状态，解决一次性pwsh无法保留工作目录/环境变量的问题。

发展史：RC8 新增

## 实现逻辑
面向模型的owner-scoped持久PowerShell工具，基于Harness PTY服务(与tool-bash-persistent镜像)。src/index.ts:425 registerPersistentPwsh 注册 name='pwsh' 工具，execute 按owner串行执行；persistentShells 维护 owner→TerminalSessionId 注册表，get 懒spawn PTY并注入PWSH_PROMPT_SETUP 设置OSC状态提示；executeCommand 用deadline限制超时，wrapCommand 将命令包进单行带START/END nonce的PowerShell包装精确捕获退出码，retainedScrollback 分页重组回滚缓冲。inject=['tools','terminals']。未装配进bundle(Windows按需)。

## Provides
- 模型面向持久'pwsh'工具(跨调用保留cwd/env)
- owner-scoped PTY会话注册表(懒spawn/重置/清理)
- 命令nonce包装精确捕获退出码+滚动缓冲重组

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - owner作用域隔离shell会话
  - 证据: `src/index.ts:457 exec.agent作为owner`
- `dsh-tools` [运行时依赖] - 工具注册
  - 证据: `src/index.ts:441 ctx.tools.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
