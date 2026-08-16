# dsh-settings-file

- 包名: `@deepseek-ai/dsh-settings-file`
- 分组: G11 凭据设置
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/settings/settings-file`

## 实现逻辑
实现 SettingsProvider 抽象(默认导出)，单个 YAML/JSON 文档($DSH_HOME/settings.yaml)承载所有 namespace section。load() 解析并 publish，persist() 经操作链+withFileLock 读-改-写，renderYaml 用 patchNode 做注释保留的 leaf-level diff。chokidar watch 热发布外部编辑，reconcileFromDisk 抑制 self-write。

## Provides
- ctx.settings(FileSettingsProvider)
- documentPath/prepareDocument
- settings/update→persist 实现

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
