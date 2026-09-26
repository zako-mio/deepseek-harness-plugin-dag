# dsh-tool-lsp

- 包名: `@deepseek-ai/dsh-tool-lsp`
- 分组: G24 LSP 集成
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/lsp/tool-lsp`

## 实现逻辑
面向模型的 `lsp` 工具：apply() 校验配置后注册 systemPrompt 的 tool:lsp 指导段，并用 ctx.tools.register 注册一个含四种只读操作（goToDefinition/findReferences/goToImplementation/hover）的工具（src/index.ts:97-232）。execute() 经 parseLspArgs 把模型的一基 UTF-16 坐标转成 seam 的零基位置（src/render.ts:46-59），强制要求会话工作区 cwd 否则抛 LSP_WORKSPACE_REQUIRED（src/session-cwd.ts:15-16、src/index.ts:185-188），并调用 ctx.lsp.query 等待结果（src/index.ts:189-194）。render.ts 纯函数把结果按文件分组渲染、按 maxLocations/maxResultChars 截断，并把 file: URI 解析为工作区相对路径（src/render.ts:85-164）。

## Provides
- ctx.tools 的 `lsp` 工具（四操作精确代码导航，含一基/零基坐标换算与结果截断，src/index.ts:109-231）
- systemPrompt `tool:lsp` 段（何时用 lsp 而非文本检索的定位指导，src/index.ts:103-107）

## Depends On (上游依赖)
- `dsh-system-prompt` [运行时依赖] - 注入 lsp 工具的模型可见使用指导段落
  - 证据: `src/index.ts:47 inject 'systemPrompt' + src/index.ts:103 ctx.systemPrompt.section`
- `dsh-tools` [E1+E2] - 定义并注册 lsp 工具与其输出 schema/渲染
  - 证据: `src/index.ts:15 import defineTool + src/index.ts:47 inject 'tools' + src/index.ts:109 ctx.tools.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
