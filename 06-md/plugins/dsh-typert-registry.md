# dsh-typert-registry

- 包名: `@deepseek-ai/dsh-typert-registry`
- 分组: G02 类型契约
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/typert/registry`

## 为什么需要它（设计初衷）
Typert 生成产物的运行时注册中心：贡献者携带一个包面的业务反射与可选实时 Zod schema，ctx.typert 原子注册并在 fiber 卸载时撤回。按 <包>#<面> 键控包反射、按 <包>#<名> 键控 schema，JSON Schema 在消费端按需计算，为 host/client 跨进程类型安全 Remote 通信提供运行时支撑。

发展史：2026-08-10 发布 0.0.1-rc.1；与 typert 生成器/loader/协议组包，构成 harness 类型反射与 Remote 通信机制的可替换组件。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/typert/registry/README.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-typert-registry

## 实现逻辑
Typert 运行时注册表(ctx.typert)。TypertRegistry 服务注册生成的包反射/Zod schema(register 原子提交)、local/remote Invocation 描述符、host 对象查找器与 host Context 提供者；typertKey/typertEndpoint 构成全局键；lookups/contexts/remotes/local 各视图暴露给依赖方；纯运行时反射仓库。

## Provides
- ctx.typert(TypertRegistry)
- register()/get()/resolve()/list()/toJSONSchema()
- typert.lookups/contexts/remotes/local 视图
- typertKey/typertEndpoint
- 变更订阅(ChangeSource)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-agent` - ctx.inject(['typert']) 注册 agent 查找器
- `dsh-api-gateway` - descriptor 权威来源
- `dsh-api-remotes` - 配置 Agent/Session Typert lookups
- `dsh-client-runtime` - 注册 client Agent scope identity
- `dsh-session` - ctx.inject(['typert']) 注册 session 查找器(typert.lookups.register)
- `dsh-typert-loader` - ctx.typert.register
