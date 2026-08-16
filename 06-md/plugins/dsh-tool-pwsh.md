# dsh-tool-pwsh

- 包名: `@deepseek-ai/dsh-tool-pwsh`
- 分组: G14 Shell工具
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/shell/tool-pwsh`

## 实现逻辑
tool-bash 的 PowerShell 对偶:注册 pwsh 工具,逐调用镜像 bash 的 validate/escalation/standingPolicy/resolveWorkdir/shellEnv 收集/前台后台执行;升级经 ctx.get('approval'),后台经 ctx.jobs.start(kind:'pwsh');额外 declare module 扩展 dsh-jobs 的 JobKindMap 增加 pwsh kind。

## Provides
- ctx.tools 注册 pwsh
- dsh-jobs 模块声明扩展(JobKindMap.pwsh)
- ctx.jobs 后台任务(kind: 'pwsh')
- ctx.systemPrompt section: tool:pwsh

## Depends On (上游依赖)
- `dsh-sandbox-policy` [运行时依赖] - standing policy
  - 证据: `packages/shell/tool-pwsh/src/index.ts:200,207`
- `dsh-shell-env` [运行时依赖] - 收集 DSH_* 环境
  - 证据: `packages/shell/tool-pwsh/src/index.ts:49,363`
- `dsh-tools` [运行时依赖] - 工具注册管线
  - 证据: `packages/shell/tool-pwsh/src/index.ts:49,252`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
