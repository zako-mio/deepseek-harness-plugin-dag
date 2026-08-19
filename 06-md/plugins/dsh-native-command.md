# dsh-native-command

- 包名: `@deepseek-ai/dsh-native-command`
- 分组: G37 示例与框架
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/util/native-command`

## 为什么需要它（设计初衷）
零依赖无 shell 的 execFile 运行器，支持 utf8 捕获、abort 传播与 Windows 隐藏窗口，用于宿主原生 OS 集成。

来源：
- https://registry.npmjs.org/@deepseek-ai/dsh-native-command
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/util/native-command

## 实现逻辑
零依赖无 shell 的 execFile 运行器（库而非插件，无 ctx/state/events；与 R5 stage-01-l3-r5.json 同条记录一致）。runNativeCommand(command, args, signal) 直接 execFile 执行可执行文件路径/PATH 名，不做 shell 字符串解释；utf8 stdio 捕获（exit 0 resolve，非零带 code/stdout/stderr reject）、AbortSignal 中止传播、windowsHide 隐藏 Windows 控制台。invariant.ts 提供包属 invariant 伴随插件。服务宿主原生 OS 集成（native 目录选择器、默认应用打开）。

## Provides
- runNativeCommand(execFile runner)
- NativeCommandRunner 可测试边界类型
- native-command-invariant 伴随插件

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-host-directory-picker-native` - osascript/zenity 原生命令执行
