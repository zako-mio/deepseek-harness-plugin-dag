# dsh-tool-lsp

- 包名: `@deepseek-ai/dsh-tool-lsp`
- 分组: G32 LSP集成
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/lsp/tool-lsp`

## 实现逻辑
模型可见的 lsp 工具（基于 ctx.lsp seam）：一个只读工具带 4 操作(goToDefinition/findReferences/goToImplementation/hover)；模型端 one-based UTF-16 光标坐标转 seam zero-based 位置，要求 session workspace 无回退，截断渲染结果(MAX_LOCATIONS/MAX_RESULT_CHARS)，附加可配置超时预算(DEFAULT_LSP_TOOL_TIMEOUT_MS)交 dsh-tool-call-timeout-policy 执行。运行时仅注入 tools/lsp/systemPrompt，不 import 任何 provider。

## Provides
- 模型工具 'lsp'(4 只读操作)
- LSP_PROMPT_TEXT 系统提示词指引
- render.ts 渲染/归一化工具导出(parseLspArgs/presentLspCall)

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - assertNever
  - 证据: `packages/lsp/tool-lsp/src/index.ts:16`
- `dsh-system-prompt` [运行时依赖] - inject ['systemPrompt'] 注册指引 section；type-only 模块增强(E1)
  - 证据: `packages/lsp/tool-lsp/src/index.ts:19,48`
- `dsh-tools` [运行时依赖] - inject ['tools'] 注册工具；defineTool/GenericCallView/ToolExecution 类型(E1)
  - 证据: `packages/lsp/tool-lsp/src/index.ts:15,48, packages/lsp/tool-lsp/src/render.ts:9, packages/lsp/tool-lsp/src/session-cwd.ts:10`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
