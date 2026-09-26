# dsh-typert-loader

- 包名: `@deepseek-ai/dsh-typert-loader`
- 分组: G45 类型契约
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/typert/loader`

## 实现逻辑
Loader 集成：当 Loader entry 挂载时解析其 package.json，若导出 ./typert 则导入 host 面并把 TYPERT 清单注册进 ctx.typert，entry 卸载时撤下注册（src/index.ts:1-26）。扫描按 entry 名增量进行：internal/plugin 标脏后经微任务 flush 对账实时 entries（src/index.ts:435-463）。

## Provides
- 自动注册挂载插件包的 ./typert 清单到 ctx.typert（src/index.ts:410）

## Depends On (上游依赖)
- `cordis-plugin-loader` [E1+E2] - 观察 Loader entry 生命周期并定位包
  - 证据: `package.json:30 peerDep + src/index.ts:34 type-only import + src/index.ts:45 inject ['loader']`
- `dsh-typert-registry` [E1+E2] - 向 typert 注册表写入清单
  - 证据: `package.json:31 peerDep + src/index.ts:36-37 import + src/index.ts:410 ctx.typert.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
