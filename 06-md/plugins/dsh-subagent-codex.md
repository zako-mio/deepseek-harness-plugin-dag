# dsh-subagent-codex

- 包名: `@deepseek-ai/dsh-subagent-codex`
- 分组: G39 子代理
- 拓扑层: Layer 7
- 来源层: L3 其余
- 源码路径: `packages/subagent/subagent-codex`

## 实现逻辑
按 profile 命名的 Codex 一次性子代理 provider：apply 解析配置、校验 disposeGraceMs 上限后把 `CodexProvider` 注册到 `ctx.subagents`（默认名 `codex`）(src/index.ts:107-130)。provider 同样声明无 start 能力且不继承父会话上下文，start 校验 cwd 后组装 CodexRunSpec 交给 `startCodexRun`，spawn 走 `ctx.subprocess.spawn` (src/index.ts:63-99)。run.ts 以 `codexAppServerArgv()` 启动官方包内 wrapper 的 `app-server --stdio`，把请求文本转成 Codex 输入并按 stop reason 归一失败诊断 (src/run.ts:135-167、src/run.ts:225)；协议帧由 wire.ts 的 `CodexAppServerWire` 基于 sdk-protocol 的行传输实现，且只有在临时 thread 建立后才对外发布运行 (src/wire.ts:192、src/wire.ts:13)。

## Provides
- ctx.subagents 上的 `codex` provider（一次性 Codex 子代理后端，app-server --stdio 协议驱动）

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 内容块与消息类型用于构造/解析协议载荷
  - 证据: `src/run.ts:15 import from '@deepseek-ai/dsh-llm' + src/wire.ts:11 import`
- `dsh-session` [编译依赖] - 子代理运行身份使用 SessionId
  - 证据: `src/run.ts:16 import type SessionId from '@deepseek-ai/dsh-session'`
- `dsh-subagent` [E1+E2] - provider 契约、能力常量与注册入口
  - 证据: `src/index.ts:12-19 import NO_START_CAPABILITIES/assertUsableCwd + src/index.ts:31 inject ['subagents'] + src/index.ts:125 registerProvider`
- `dsh-tool-subagent` [组合依赖] - 必须与委托工具同装配，模型侧才能启动该后端
  - 证据: `cordis.patch.yml:4-5 与 tool-subagent-codex 同补丁装配；package.json:52 dependencies`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
