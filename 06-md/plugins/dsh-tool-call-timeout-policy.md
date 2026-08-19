# dsh-tool-call-timeout-policy

- 包名: `@deepseek-ai/dsh-tool-call-timeout-policy`
- 分组: G23 工具守卫
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/guard/timeout-policy`

## 为什么需要它（设计初衷）
集中式工具调用超时策略插件：作为 tools/execute waterfall 包装器，读取各工具声明的 timeoutMs，派生 per-tool 截止信号赋给 exec.signal，超时返回 TOOL_TIMEOUT。核心理念：工具作者只需转发 exec.signal，预算由部署策略决定；超时声明放在工具定义上，避免拼错名称致策略失效；零配置，位于 packages/guard。

发展史：由 2026-07-07 tool-call-timeout-policy Agent Note 定案（先提取共享 deadline/timeout 库，再插件化进 tools/execute 环绕分发扩展点）；2026-08-12 发布 0.0.1-rc.3。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/notes/implemented/architecture/2026-07-07-tool-call-timeout-policy.zh.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-tool-call-timeout-policy
- https://github.com/deepseek-ai/deepseek-harness

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
