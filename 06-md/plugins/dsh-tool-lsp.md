# dsh-tool-lsp

- 包名: `@deepseek-ai/dsh-tool-lsp`
- 分组: G23 LSP 集成
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/lsp/tool-lsp`

## 实现逻辑
函数式插件（具名导出 name/inject/Config/apply，无 default 导出）：在 ctx.tools 上注册唯一的只读工具 `lsp`，把 goToDefinition/findReferences/goToImplementation/hover 四种操作作为枚举暴露给模型 (src/index.ts:108-231、src/render.ts:15)。参数校验把模型的一基 UTF-16 行列坐标换算为 seam 的零基位置，操作名与坐标非法即报错 (src/render.ts:46-59、src/render.ts:62-72)。执行时要求会话工作区（无则抛 LSP_WORKSPACE_REQUIRED），经 ctx.lsp.query 查询后按文件分组渲染为一基 path:line:character，并对 locations 与 hover 分别做条数截断与整体字符截断 (src/index.ts:182-193、src/render.ts:85-128)。另在 ctx.systemPrompt 注册 tool:lsp 指引节，声明式地把 LSP 定位为 search/read 之外的精确导航补充 (src/index.ts:52-53、src/index.ts:102-106)；maxLocations/maxResultChars/timeoutMs 在加载期强校验，误配即失败 (src/index.ts:65-69、src/index.ts:233-244)。

## Provides
- tools.lsp (模型可见的只读代码导航工具：四种 LSP 操作、一基 UTF-16 光标坐标、有界结果渲染)
- systemPrompt 章节 tool:lsp (把 LSP 定位为文本匹配含糊或改动前需要精确符号关系时的补充手段)

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 编译期契约对齐：工具结果经 dsh-tools 呈现时与 llm 内容类型同一基线；仅声明式依赖
  - 证据: `package.json:31 peerDep + packages/lsp/tool-lsp/tsconfig.json:21 项目引用（源码无直接 import）`
- `dsh-system-prompt` [运行时依赖] - 注册 tool:lsp 指引节，使工具策略进入稳定系统提示词
  - 证据: `package.json:33 peerDep + src/index.ts:46 inject 'systemPrompt'；src/index.ts:102 ctx.systemPrompt.section`
- `dsh-tools` [E1+E2] - 定义并注册 lsp 工具到工具注册表，复用其 schema/render/presentCall 契约
  - 证据: `package.json:35 peerDep + src/index.ts:16 import defineTool；src/index.ts:46 inject 'tools'、src/index.ts:108 ctx.tools.register`
- `dsh-working-directory` [运行时依赖] - 取得会话工作区根作为查询作用域，缺失即拒绝查询而不回退
  - 证据: `package.json:36 peerDep + src/index.ts:13 type import；src/index.ts:46 inject 'workingDirectory'、src/index.ts:184 ctx.workingDirectory.ensure`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
