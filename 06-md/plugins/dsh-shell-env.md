# dsh-shell-env

- 包名: `@deepseek-ai/dsh-shell-env`
- 分组: G14 Shell工具
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/shell/shell-env`

## 为什么需要它（设计初衷）
解决模型可见 shell 工具缺乏可信、受管环境的问题：拥有 ctx.shellEnv 注册表，为每次 shell 调用收集可信 DSH_* 变量（DSH_HOME/DSH_SHELL/DSH_SESSION_ID 等），内置键归自身、其他插件可注册贡献。其核心价值是让 bash/pwsh 工具拿到经过身份标注、防嵌套 harness 身份泄漏的一致环境快照，且永不修改 process.env，成为 shell 执行器的环境事实来源。

发展史：位于 packages/shell/shell-env，作为工具无关的 shell 环境层与 dsh-tool-bash/pwsh 强耦合，属 shell 子系统基础件；随持久化 seam 演进新增 DSH_SESSION_JSONL 等动态键，保持注册表单点管理。

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/shell/shell-env/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness

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
