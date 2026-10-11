# dsh-subprocess-local

- 包名: `@deepseek-ai/dsh-subprocess-local`
- 分组: G40 子进程
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/subprocess/subprocess-local`

## 实现逻辑
以 LocalSubprocessRuntime extends SubprocessRuntime 的方式实现 ctx.subprocess 的本地 provider：构造函数用 ctx.effect 挂 process 'exit' 同步兜底终止，正常销毁时先 SIGTERM 再按 graceMs 升级 SIGKILL，并等待整个受管进程范围退出而非仅直接子进程 (src/index.ts:59-85, src/index.ts:107-138)。spawn() 先 validateSubprocessSpec，再按平台探测结果在 linux-scope / windows-job / fallback 三种收容模式中择一，绑定 stdio 处置、spill 采集与取消/超时生命周期 (src/index.ts:182-232, src/spawn.ts:267-446)。spawnTerminal() 通过懒加载的 node-pty 分配 PTY，并在 Linux 下把终端套进 scope 所有者；fallback 路径用 detached PGID + taskkill 做弱收容 (src/index.ts:264-335, src/spawn.ts:454-492)。resolveExecutable 按 PATH/PATHEXT 逐候选 stat + X_OK 校验，失败抛 SubprocessExecutableNotFoundError (src/index.ts:140-180)。

## Provides
- ctx.subprocess (子进程 seam 的本地实现：平台选择的托管进程范围收容、stdio 处置与 spill 采集、PTY 终端分配、可执行文件解析)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-subprocess-ssh` - 复用本地输出收集器实现远程收集快照
