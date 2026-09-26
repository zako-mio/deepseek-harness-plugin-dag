# dsh-pwsh-local

- 包名: `@deepseek-ai/dsh-pwsh-local`
- 分组: G36 Shell 执行
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/shell/pwsh-local`

## 实现逻辑
实现 shell 能力 seam 的本地 PowerShell 执行器 ctx.shell：以 pwsh -NoLogo -NoProfile -NonInteractive -Command 运行命令作为单个 argv 元素，并前置 UTF-8 编码前言避免老版 PowerShell 控制台码页乱码 (src/index.ts:193-195, 40-49)。executeArgv() 复用与 bash-local 相同的 deadline 分类、输出合并、kill/result 投影与 provider 失败收敛机制 (src/index.ts:245-433)。resolve.ts 以纯函数按「显式配置 > Windows 已知安装位置 > PATH」解析 pwsh 可执行文件 (src/resolve.ts:21-78)。

## Provides
- ctx.shell (本地 PowerShell 执行器实现，经 ctx.subprocess 以 pwsh -Command 运行命令)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-pwsh-sandbox` - 复用本地 pwsh 的 argv、执行生命周期与输出机制
- `dsh-terminal-bash` - pwsh 方言的可执行路径解析与 UTF-8 前置
