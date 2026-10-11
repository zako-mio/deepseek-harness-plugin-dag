# dsh-host-directory-picker-native

- 包名: `@deepseek-ai/dsh-host-directory-picker-native`
- 分组: G19 宿主服务
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/host/directory-picker-native`

## 实现逻辑
实现目录选择接缝的 native 后端：默认导出 NativeDirectoryPicker 继承 DirectoryPicker 基类（基类以 super(ctx,'directoryPicker') 完成服务注册），返回稳定的 native 能力对象，其 pick 转发到 pickNativeDirectory (src/index.ts:22-35)。pickNativeDirectory 按平台分派：darwin 走 osascript 的 choose folder（用户取消识别为 -128/User canceled），linux 先 zenity 后 kdialog（仅在 ENOENT 时降级，两者皆缺则显式报错），win32 交给 koffi 驱动的 IFileOpenDialog 子进程 (src/native-picker.ts:48-106)。所有本机命令都经 dsh-native-command 的 runNativeCommand 执行，绝不经过 shell (src/native-picker.ts:3, 53)。

## Provides
- ctx.directoryPicker 的 native 能力（kind: 'native'，pick(signal) 打开宿主 OS 目录选择器）
- pickNativeDirectory 及 DirectoryPickerInternals / DirectoryPickerRunner 类型的再导出

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-host-directory-picker-auto` - native 分支要挂载的宿主后端包（运行时按包名装配，非静态 import）
