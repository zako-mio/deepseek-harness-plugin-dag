# dsh-typert-registry

- 包名: `@deepseek-ai/dsh-typert-registry`
- 分组: G45 类型契约
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/typert/registry`

## 实现逻辑
共享 Typert 运行时注册表：TypertRegistry 注册 ctx.typert（src/service.ts:456），存储生成的包反射元数据与 Zod schema，并提供 register/get/resolve/list 与 toJSONSchema 等契约（src/index.ts:17-26）。它不做 TypeScript 分析或 schema 生成（src/service.ts:1-6），web 客户端面复用同一实现（src/client/index.ts:13-15）。

## Provides
- ctx.typert（生成式反射元数据与 Zod schema 运行时注册表，host 与 client 双面）

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-api-session-controller` - Typert 注册表类型
- `dsh-typert-loader` - 向 typert 注册表写入清单
