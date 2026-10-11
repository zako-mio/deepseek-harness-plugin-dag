# dsh-system-prompt

- 包名: `@deepseek-ai/dsh-system-prompt`
- 分组: G09 核心运行时
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/core/system-prompt`

## 实现逻辑
以分层注册表实现系统提示组装。SystemPrompt 服务（ctx.systemPrompt）用 ScopedLayers 维护全局与各作用域分层的 sections/contexts/variables/toolProviders 及 runtimeContextSuppressors（src/index.ts:391-422、src/index.ts:435-438）；section()/context()/tools()/variable()/suppressRuntimeContext() 都经 ctx.effect 登记并返回精确 disposer（src/index.ts:474-566）。assemble() 沿作用域链合并（近作用域覆盖全局）、按中央 SECTION_ORDERS 排序、对工具 schema 做 canonical 排序与 toolOrder 校验，再跑 system-prompt/assemble 瀑布，最后把生效的 complete section 收敛为唯一提示段（src/index.ts:610-684）。refreshContext() 只重算被接受的运行时上下文，支持 required 与抑制语义（src/index.ts:578-598）。

## Provides
- ctx.systemPrompt（系统提示组装注册表，src/index.ts:13-16、src/index.ts:425-438）
- system-prompt/assemble 瀑布与 system-prompt/change 通知（src/index.ts:19-38、src/index.ts:437）
- 中央区段/上下文排序表与查询方法：SECTION_ORDERS/CONTEXT_ORDERS、getSectionOrder/getContextOrder（src/index.ts:131-178、src/index.ts:490-501）
- 渲染助手：renderPrompt/renderContextSnapshot/joinContextSections/renderContextSections（src/index.ts:286、src/index.ts:298、src/index.ts:310、src/index.ts:326）
- 部署人设段名常量与 toolOrder 保留标记（PERSONA_PREFIX_SECTION/PERSONA_SUFFIX_SECTION/TOOL_ORDER_REST，src/index.ts:186-198）

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 复用 LLM 的工具 schema 与上下文快照类型，使组装结果可直接作为模型输入
  - 证据: `src/index.ts:11 import type { ContextSnapshotSection, ToolSchema } from '@deepseek-ai/dsh-llm' + src/index.ts:638 result.schemas.map(({ name, description, parameters, deferLoading }): ToolSchema => ...)`

## Dependents (下游被依赖)
- `dsh-agent` - 组装提示时同时带上 agent 与 scope，避免 agent 作用域贡献被静默遗漏
- `dsh-agent-loop` - 组装每步系统提示与运行时上下文快照，并注册 provider/model 提示变量
- `dsh-agent-preset-registry` - 编译期契约对齐：preset 子树装配的提示词插件共用同一 systemPrompt 基线；仅声明式依赖
- `dsh-client-ui-deliverables` - 注册交付文件引用提示段
- `dsh-experimental-browser-use-chrome-devtools-mcp` - 提示词就绪检查依赖 systemPrompt 服务
- `dsh-experimental-browser-use-playwright-mcp` - 提示词就绪检查依赖 systemPrompt 服务
- `dsh-experimental-browser-use-stagehand-native` - 注入 Stagehand 使用与安全 guidance
- `dsh-experimental-computer-use-cua-driver-native` - 注入桌面操作 guidance 段落
- `dsh-experimental-tool-agent-team` - 协作策略以系统提示段形式随工具一起注入该作用域
- `dsh-file-reference-local` - 向 agent 作用域的系统提示注册文件引用说明段，并复用其 FILE_REFERENCE 中央排序位
- `dsh-mcp-client` - 把服务端 attributed instructions 写入系统提示段
- `dsh-mcp-resources` - 发布资源服务器清单提示段
- `dsh-persona` - 注册 persona 段落并抑制运行时上下文
- `dsh-plan-mode` - 注册 plan:policy 提示词节，按状态决定是否输出部署方指引
- `dsh-sandbox-policy` - 注册 sandbox:policy 上下文节，使模型看到当前文件策略
- `dsh-session-reference` - 在系统提示装配完成后捕获 provider/model 变量作为引用字节预算的模型来源
- `dsh-subagent` - 子代理人格/提示段落在创建窗口内 scoped 应用
- `dsh-tool-bash` - 注册工具专属的提示片段
- `dsh-tool-fs` - 注册工具使用指引片段，并按 scope 内工具是否注册决定文本
- `dsh-tool-fs-search` - 注册「用 glob/grep 工具而非 shell find/grep」的指引片段
- `dsh-tool-goal` - 注册目标工具策略段并按序插入系统提示词
- `dsh-tool-jobs` - 注入 tool:jobs 段系统提示，指导模型跟踪/收集后台作业
- `dsh-tool-lsp` - 注册 tool:lsp 指引节，使工具策略进入稳定系统提示词
- `dsh-tool-pwsh` - 注册 pwsh 专属提示片段
- `dsh-tool-ralph` - 注册 ralph 的显式请求使用策略提示章节
- `dsh-tool-session-query` - 注入会话检索工具的使用引导段落
- `dsh-tool-subagent` - 注册并行委派提示片段
- `dsh-tool-terminal` - 向系统提示注册 tool:pty 使用指导章节，约束模型何时使用持久终端
- `dsh-tool-web` - 注册工具使用与外部内容信任指引的 system prompt 章节
- `dsh-tool-workflow` - 把工具用法策略作为独立 prompt 段落注册，随工具存在而生效
- `dsh-tools` - 把可见工具 schema 与 ptc-only/SDK 提示段注册进系统提示组装
- `dsh-user-approval` - 把有效策略作为运行时上下文告知模型
- `dsh-working-directory` - 把当前工作目录注入系统提示上下文
