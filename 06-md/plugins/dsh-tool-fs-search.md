# dsh-tool-fs-search

- 包名: `@deepseek-ai/dsh-tool-fs-search`
- 分组: G16 文件系统
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/fs/tool-fs-search`

## 实现逻辑
以 ctx.subprocess.spawn 执行 npm 内置的 @vscode/ripgrep 二进制（纯 argv 向量、无 shell 层），实现模型面向的 glob 与 grep 两个发现工具 (src/index.ts:129-160, src/search-core.ts:222-287)。apply 校验条数/字节/毫秒各项上限（graceMs 不得超 MAX_TIMER_DELAY_MS）后注册两个工具 (src/index.ts:129-160)；runRipgrep 统一前置 --no-config 阻断宿主 ripgrep 配置注入，按 exit 0/1 区分有结果与零命中，其余退出码归入 SEARCH_* 错误词表，stdout 超限报 SEARCH_RAW_OUTPUT_OVERFLOW (src/search-core.ts:239-286)。两个工具各自订阅 tools/post-execute，超过内联上限时把完整结果经 ctx.spillStore.saveText 落盘并在正文报告保存位置 (src/glob.ts:355-367, src/grep.ts:342-362)。

## Provides
- ctx.tools 的 glob 工具（按路径模式发现文件，含隐藏与忽略文件）
- ctx.tools 的 grep 工具（ripgrep 正则搜索文件内容，按文件分组返回匹配行）
- tool:glob / tool:grep 两条 systemPrompt 片段
- glob/grep 结果的 search 卡片 presentationMeta（可回放的结构化搜索结果）

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - SearchError 以 HarnessError 为基类，携带稳定 code 供重试/权限/UI 层分流
  - 证据: `src/search-core.ts:25 import HarnessError`
- `dsh-session` [编译依赖] - peer 声明，用于搜索结果元数据与会话日志持久化的对齐
  - 证据: `package.json:36 peerDependencies @deepseek-ai/dsh-session`
- `dsh-system-prompt` [运行时依赖] - 注册「用 glob/grep 工具而非 shell find/grep」的指引片段
  - 证据: `src/glob.ts:297-303 ctx.systemPrompt.section + package.json:39 peerDependencies`
- `dsh-tools` [E1+E2] - 注册两个工具定义并取得工具执行上下文与结果呈现钩子
  - 证据: `src/glob.ts:14-15 import defineTool / ToolResult + src/index.ts:71 static inject ['tools','systemPrompt','subprocess','workingDirectory'] + src/glob.ts:353 ctx.tools.register`
- `dsh-working-directory` [E1+E2] - 解析搜索命令的工作目录，并作为返回路径的相对化基准
  - 证据: `src/index.ts:29 import type {} from '@deepseek-ai/dsh-working-directory' + src/search-core.ts:236 ctx.workingDirectory.ensure`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
