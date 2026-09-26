# dsh-bash-local

- 包名: `@deepseek-ai/dsh-bash-local`
- 分组: G36 Shell 执行
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/shell/bash-local`

## 实现逻辑
实现 shell 能力 seam 的本地 bash 执行器 ctx.shell：resolve() 用配置补齐 workdir/timeout/输出上限并夹取超时，spawnSpec() 组装带 ENV_OVERRIDES 的 subprocess spawn 规格 (src/index.ts:120-174)。execute() 以 bash -c 运行，executeArgv() 负责 deadline/取消分类（'kill' 与 'none' 两臂）、输出读取、stdout/stderr 模型友好合并、kill 与 result 投影 (src/index.ts:187-389)。实际进程经 ctx.subprocess 管理、输出有界并可溢出到 spill 文件，替身未产出进程时以 settled-killed 形态收敛 (src/index.ts:97-107, 156-185, 251-341)。

## Provides
- ctx.shell (本地 bash 执行器实现，经 ctx.subprocess 以 bash -c 运行命令)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-bash-sandbox` - 复用本地 bash 的执行生命周期、输出与 deadline 机制
