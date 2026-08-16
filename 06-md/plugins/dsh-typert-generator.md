# dsh-typert-generator

- 包名: `@deepseek-ai/dsh-typert-generator`
- 分组: G37 示例与框架
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/typert/generator`

## 实现逻辑
Typert 生成工具链：WorkspaceAnalyzer(analyzer.ts) 基于 typescript 编译器做 workspace 级程序分析，产出 compiler-independent Typert 模型(model.ts)；FaceModelEmitter(emitter.ts) 用 @jridgewell/gen-mapping 生成 sourcemap 感知的 host/client 面反射工件；TypeGraphRenderer(renderer.ts) 渲染类型图；WorkspaceTypertGenerator(workspace.ts) 组合 discover→analyze→emit 并校验 package.json exports/files 契约(./typert、./client/typert、./remote)；cordis-catalog.ts 做 Cordis 目录投影与 type-link 违规门控。tsdown-plugin.ts 暴露 typertPlugin(transform 降级装饰器 + writeBundle 生成工件)，供根 tsdown.config.ts 以 workspace 模式接入构建。

## Provides
- WorkspaceAnalyzer/WorkspaceCaches(TS 项目分析)
- FaceModelEmitter(model 驱动工件发射)
- TypeGraphRenderer(类型图渲染)
- WorkspaceTypertGenerator(workspace 级发现+生成)
- cordis-catalog 投影与 type-link 门控
- typertPlugin(tsdown/rolldown 插件面)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
