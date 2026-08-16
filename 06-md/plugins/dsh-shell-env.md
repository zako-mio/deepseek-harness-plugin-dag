# dsh-shell-env

- 包名: `@deepseek-ai/dsh-shell-env`
- 分组: G14 Shell工具
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/shell/shell-env`

## 实现逻辑
工具无关的受信 DSH_* shell 环境注册表:ShellEnvRegistry extends Service 注册为 ctx.shellEnv,collect(execution) 重建每次调用的环境快照(内置 DSH_HOME/DSH_SHELL/DSH_SESSION_ID + 各 contributor);register(contributor) 校验键格式/保留键/重复所有权并以 ctx.effect 提供 fiber 级注销;apply() 内置 session-persistence contributor。

## Provides
- ctx.shellEnv 服务(ShellEnvRegistry)
- 内置 DSH_HOME、DSH_SHELL、DSH_SESSION_ID
- session-persistence contributor(DSH_SESSION_JSONL)

## Depends On (上游依赖)
- `dsh-session` [运行时依赖] - 会话 id 注入 DSH_SESSION_ID
  - 证据: `packages/shell/shell-env/src/index.ts:158`
- `dsh-tools` [编译依赖] - ToolExecution 类型
  - 证据: `packages/shell/shell-env/src/index.ts:16`

## Dependents (下游被依赖)
- `dsh-agent-spine-demo` - ctx.plugin(bashEnv) shell 环境
- `dsh-tool-bash` - 收集 DSH_* 环境
- `dsh-tool-pwsh` - 收集 DSH_* 环境
- `dsh-web-app` - Context merge（ctx.shellEnv）
