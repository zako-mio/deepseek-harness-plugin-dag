# dsh-subprocess-local

- 包名: `@deepseek-ai/dsh-subprocess-local`
- 分组: G15 沙箱执行
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/subprocess/subprocess-local`

## 为什么需要它（设计初衷）
subprocess seam 的本地 Service Provider，spawn 进程树/PTY 终端、升级式终止、有界 spill 输出与凭据清除。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/subprocess/subprocess-local/README.zh.md

## 实现逻辑
子进程 seam 的本地实现(LocalSubprocessRuntime extends SubprocessRuntime):spawn() 创建 detached 进程树(Windows 经 taskkill /T),OutputCollector 做每流内存尾部保留+溢出 spill 文件,childEnv 清洗父环境,spawnTerminal 经 node-pty 提供 PTY 句柄。

## Provides
- ctx.subprocess 服务
- 输出采集(spill 文件)/环境清洗/进程树终止

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
