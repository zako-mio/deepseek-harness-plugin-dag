# dsh-tool-call-timeout-policy

- 包名: `@deepseek-ai/dsh-tool-call-timeout-policy`
- 分组: G23 工具守卫
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/guard/timeout-policy`

## 实现逻辑
工具调用超时 guard：apply 在 'tools/execute' 事件链上包装。读取 ctx.tools.get(exec.name, exec.agent)?.timeoutMs，用 dsh-timeout 的 deadline 派生 deadline 信号临时替换 exec.signal 后委托 next()，超时则以 toolTimeoutResult 生成 TOOL_TIMEOUT 错误结果替换，finally 恢复上游信号。

## Provides
- tools/execute 包装(per-tool deadline + TOOL_TIMEOUT)
- 常量 TOOL_TIMEOUT

## Depends On (上游依赖)
- `dsh-llm` [组合依赖] - ToolExecutionResult 类型
  - 证据: `packages/guard/timeout-policy/package.json:36`
- `dsh-tools` [运行时依赖] - inject tools; 监听 tools/execute
  - 证据: `packages/guard/timeout-policy/src/index.ts:31,56-57`

## Dependents (下游被依赖)
- `dsh-tool-web` - timeoutMs 交策略强制
