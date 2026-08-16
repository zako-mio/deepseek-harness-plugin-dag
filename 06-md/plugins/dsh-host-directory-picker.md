# dsh-host-directory-picker

- 包名: `@deepseek-ai/dsh-host-directory-picker`
- 分组: G37 示例与框架
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/host/directory-picker`

## 实现逻辑
目录选择能力 seam 抽象：DirectoryPicker extends Service (src/index.ts:131) 注册 ctx.directoryPicker (:133)；capability() 返回判别联合 native|browse (:17-97,:140)；DirectoryPickerError 封闭错误码 (:103-116)；DirectoryPickerCapabilities merge-extensible 注册表 (:94-100)；消费方按 kind 分支，未知 kind 默认隐藏选择入口。

## Provides
- ctx.directoryPicker 抽象服务（native|browse 判别能力）

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-host-directory-picker-browse` - seam 基座与错误词汇
- `dsh-host-directory-picker-native` - seam 基座
