# dsh-shell-env

- 包名: `@deepseek-ai/dsh-shell-env`
- 分组: G36 Shell 执行
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/shell/shell-env`

## 实现逻辑
提供与具体 shell 工具无关的 ctx.shellEnv 注册表，管理每次执行注入的受信任 DSH_* 变量 (src/index.ts:93-201)。内置变量（DSH_HOME/DSH_SHELL/DSH_SESSION_ID/DSH_PROFILE/DSH_PROFILE_DIR）由注册表自身持有，插件可经 register() 声明并贡献额外可枚举变量（名称/键唯一、保留键与命名校验、随 fiber 处置）(src/index.ts:72-82, 114-149)。collect() 为一次工具执行生成按名排序的冻结环境快照，list() 供诊断枚举 (src/index.ts:156-201)。

## Provides
- ctx.shellEnv (受信任的 DSH_* 环境变量注册表，供 shell 工具每次执行时收集与插件注册贡献)

## Depends On (上游依赖)
- `dsh-tools` [编译依赖] - 按一次工具执行上下文解析并贡献环境变量
  - 证据: `src/index.ts:16 import type { ToolExecution }; package.json:34 peerDep`

## Dependents (下游被依赖)
- `dsh-tool-bash` - 为每次执行收集受信任 DSH_* 环境变量
- `dsh-tool-pwsh` - 为每次执行收集受信任 DSH_* 环境变量
