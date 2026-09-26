# dsh-host-directory-picker-native

- 包名: `@deepseek-ai/dsh-host-directory-picker-native`
- 分组: G20 宿主服务
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/host/directory-picker-native`

## 实现逻辑
实现 dsh-host-directory-picker 的 DirectoryPicker 服务，注册 kind:'native' 能力，pick 委托 pickNativeDirectory（src/index.ts:22-35）。native-picker.ts 按平台分派：darwin 调 osascript、linux 依次调 zenity/kdialog、win32 走 koffi 驱动的 IFileOpenDialog 子进程（src/native-picker.ts:48-107）。命令一律经 dsh-native-command 的 runNativeCommand 以 argv 执行，绝不经过 shell（src/native-picker.ts:3、53）。

## Provides
- ctx.directoryPicker (native 能力实现：调用宿主 OS 原生目录选择对话框，src/index.ts:23-27)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-host-directory-picker-auto` - native 交互的宿主后端条目
