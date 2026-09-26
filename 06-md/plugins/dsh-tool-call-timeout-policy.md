# dsh-tool-call-timeout-policy

- 包名: `@deepseek-ai/dsh-tool-call-timeout-policy`
- 分组: G18 工具守卫
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/guard/timeout-policy`

## 实现逻辑
包装 tools/execute 瀑布点：读取工具声明的 timeoutsMs，用 dsh-timeout 的 deadline 为调用臂上截止并临时把 exec.signal 替换为派生的截止信号（src/index.ts:56-67）。委派下游后，若本插件自己的定时器胜出（按 TOOL_TIMEOUT code 作用域判定，避免误读嵌套的外层截止），用结构化 isError 结果替换返回值，最后在 finally 中恢复上游 signal（src/index.ts:68-79, 41-48）。

## Provides
- TOOL_TIMEOUT 结构化超时结果 (在 tools/execute 层把声明 timeoutMs 的调用映射为超时错误)

## Depends On (上游依赖)
- `dsh-tools` [E1+E2] - 包装工具执行瀑布点并读取工具声明的超时预算
  - 证据: `src/index.ts:16 import ToolExecutionResult + src/index.ts:31 inject ['tools'] + src/index.ts:56-57 ctx.on('tools/execute') + ctx.tools.get`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
