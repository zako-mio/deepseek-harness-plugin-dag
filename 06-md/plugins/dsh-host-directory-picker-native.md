# dsh-host-directory-picker-native

- 包名: `@deepseek-ai/dsh-host-directory-picker-native`
- 分组: G37 示例与框架
- 拓扑层: Layer 1
- 来源层: L3 其余
- 源码路径: `packages/host/directory-picker-native`

## 为什么需要它（设计初衷）
directory-picker seam 的原生 OS 选择器后端（macOS osascript / Linux Zenity / Windows IFileOpenDialog）。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/host/directory-picker-native/README.md

## 实现逻辑
NativeDirectoryPicker extends DirectoryPicker (src/index.ts:20)，native capability pick→pickNativeDirectory (:21-25)；打开系统级目录选择器：macOS osascript、Linux Zenity+KDialog 回退、Windows 经 koffi 驱动 IFileOpenDialog 于 spawn 子进程 COM 对话（头注释 :1-10）；native-picker.ts + win32-dialog-* 多文件实现 worker 隔离。

## Provides
- ctx.directoryPicker（native capability: pick）

## Depends On (上游依赖)
- `dsh-host-directory-picker` [E1+E2] - seam 基座
  - 证据: `package.json:40 deps + src/index.ts:12-13 import { DirectoryPicker }；E2: :20 extends DirectoryPicker`
- `dsh-native-command` [编译依赖] - osascript/zenity 原生命令执行
  - 证据: `package.json:41 deps`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
