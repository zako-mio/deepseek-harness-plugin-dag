# cordis-plugin-group

- 包名: `@deepseek-ai/cordis-plugin-group`
- 分组: G46 框架 vendor
- 拓扑层: Layer 1
- 来源层: L3 其余
- 源码路径: `vendor/group`

## 实现逻辑
把 Loader 的 Group 类作为默认导出暴露为独立插件包（src/index.ts:1-3），用于在 cordis 配置中声明嵌套插件组。

## Provides
- Group 插件（嵌套插件组的默认导出，src/index.ts:1-3）

## Depends On (上游依赖)
- `cordis-plugin-loader` [编译依赖] - 复用 Loader 的 Group 实现
  - 证据: `package.json:33 peerDep + src/index.ts:1 import Group`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
