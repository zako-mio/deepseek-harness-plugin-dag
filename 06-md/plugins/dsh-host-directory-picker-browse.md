# dsh-host-directory-picker-browse

- 包名: `@deepseek-ai/dsh-host-directory-picker-browse`
- 分组: G37 示例与框架
- 拓扑层: Layer 1
- 来源层: L3 其余
- 源码路径: `packages/host/directory-picker-browse`

## 为什么需要它（设计初衷）
目录选择 seam 的应用内浏览后端：Node 标准库单层列举+子目录创建，无本地对话框，可服务远程客户端。

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/host/directory-picker-browse/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/host/directory-picker

## 实现逻辑
BrowseDirectoryPicker extends DirectoryPicker (src/index.ts:187)，capability() 返回稳定 browse 能力 (:199-215)；list 以 opendir 流式读入 name 排序有界窗口（O(keep) 内存，:76-96），raceAbort 竞速 caller signal (:108-134)，fullyQualified 全限定围栏 (:50-54)，ancestryCrumbs 面包屑 (:28-38)；createDirectory 单段校验+EEXIST 映射 (:299-323)；maxEntries 默认 1000 (:195-197)。

## Provides
- ctx.directoryPicker（browse capability: list/createDirectory）

## Depends On (上游依赖)
- `dsh-host-directory-picker` [E1+E2] - seam 基座与错误词汇
  - 证据: `package.json:35 deps + src/index.ts:18-19 import { DirectoryPicker, DirectoryPickerError }；E2: :187 extends DirectoryPicker、:206 super(ctx)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
