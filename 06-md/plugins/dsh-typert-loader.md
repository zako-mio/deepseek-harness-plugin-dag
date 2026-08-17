# dsh-typert-loader

- 包名: `@deepseek-ai/dsh-typert-loader`
- 分组: G02 类型契约
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/typert/loader`

## 为什么需要它（设计初衷）
Typert Loader 集成：扫描 Loader 条目并注册生成的主机类型产物进运行时 registry，喂给 typert 类型图（ctx.typert）。

来源：
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/typert/loader
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/typert

## 实现逻辑
Typert 构建产物的自动注册集成。apply(ctx) 扫描 loader entries 与显式配置 packages，对每个 entry 解析其 package.json 的 './typert' export，动态 import 后经 validateTypertManifest 严格校验，通过 ctx.typert.register(manifest) 注册。监听 'internal/plugin' 事件把 fiber entry 标记 dirty，microtask 批量 flush 增量 reconcile；unmount 时撤下注册。

## Provides
- typert manifest 自动注册/撤销能力
- inject=['typert','loader'] 插件入口
- validateTypertManifest/TYPERT_HOST_EXPORT

## Depends On (上游依赖)
- `dsh-typert-registry` [运行时依赖] - ctx.typert.register
  - 证据: `packages/typert/loader/src/index.ts:35,383`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
