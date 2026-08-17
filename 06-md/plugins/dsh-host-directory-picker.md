# dsh-host-directory-picker

- 包名: `@deepseek-ai/dsh-host-directory-picker`
- 分组: G37 示例与框架
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/host/directory-picker`

## 为什么需要它（设计初衷）
Web GUI host 工作区目录选择器的能力缝：抽象 DirectoryPicker 服务，capability() 返回判别联合描述操作者如何选目录——native 后端弹操作系统原生选择器、browse 后端为无法触达 OS 选择器的远程客户端提供 in-app 目录浏览/创建。消费者按 capability.kind 分支，未知 kind 则隐藏选目录功能而非失败。

发展史：2026-07-28 directory-picker capability seam 决策记录设计理由与 ctx.fs 的分离；派生出 -native/-browse/-auto（启动时自动选后端）三实现，每个还带浏览器入口注册 UI 流程插槽。

来源：
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/host/directory-picker
- https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/notes/implemented/architecture/2026-07-28-directory-picker-capability-seam.md

## 实现逻辑
目录选择能力 seam 抽象：DirectoryPicker extends Service (src/index.ts:131) 注册 ctx.directoryPicker (:133)；capability() 返回判别联合 native|browse (:17-97,:140)；DirectoryPickerError 封闭错误码 (:103-116)；DirectoryPickerCapabilities merge-extensible 注册表 (:94-100)；消费方按 kind 分支，未知 kind 默认隐藏选择入口。

## Provides
- ctx.directoryPicker 抽象服务（native|browse 判别能力）

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-host-directory-picker-browse` - seam 基座与错误词汇
- `dsh-host-directory-picker-native` - seam 基座
