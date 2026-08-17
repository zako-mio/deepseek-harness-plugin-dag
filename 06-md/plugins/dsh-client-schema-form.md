# dsh-client-schema-form

- 包名: `@deepseek-ai/dsh-client-schema-form`
- 分组: G29 UI底座
- 拓扑层: Layer 0
- 来源层: L2 web-app
- 源码路径: `packages/client/schema-form`

## 为什么需要它（设计初衷）
设置编辑器提供 schema/draft 模型层，rehydrate 服务端 schema 做客户端校验，避免校验漂移。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/schema-form/README.md

## 实现逻辑
schema/draft 模型层（零 cordis 运行时）。rehydrateSchema 从 wire 的反序列化 schemastery 信封重建 schema，nodeAtPath/getPath/setPath/deletePath 按 settings 路径不可变编辑 draft，validateDraft 校验 draft。被 settings 编辑器（ui-settings-* 各页）作为纯工具 import，不注册任何 slot/service。

## Provides
- rehydrateSchema/nodeAtPath/getPath/setPath/deletePath/hasPath/validateDraft
- SchemaNode 类型

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
