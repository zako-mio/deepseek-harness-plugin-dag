# dsh-host-directory-picker-browse

- 包名: `@deepseek-ai/dsh-host-directory-picker-browse`
- 分组: G20 宿主服务
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/host/directory-picker-browse`

## 实现逻辑
实现 dsh-host-directory-picker 定义的 DirectoryPicker 服务，向 ctx.directoryPicker 注册 kind:'browse' 能力（src/index.ts:187-215）。list() 用 opendir 流式扫描目标目录，以 maxEntries+1 的有界保序窗口截断并用 raceAbort 让文件系统等待可被调用方中止，返回 crumbs 面包屑与 entries（src/index.ts:217-297）。createDirectory() 校验父路径全限定与单段名后非递归 mkdir（src/index.ts:299-323）。

## Provides
- ctx.directoryPicker (browse 能力实现：一层目录列举 + 子目录创建，src/index.ts:199-203)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-host-directory-picker-auto` - browse 交互的宿主后端条目
