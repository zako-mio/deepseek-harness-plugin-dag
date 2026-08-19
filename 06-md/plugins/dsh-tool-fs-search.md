# dsh-tool-fs-search

- 包名: `@deepseek-ai/dsh-tool-fs-search`
- 分组: G13 文件系统
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/fs/tool-fs-search`

## 为什么需要它（设计初衷）
面向模型的文件发现工具 glob/grep，由打包 ripgrep 二进制支持（经 ctx.subprocess），不依赖宿主 rg 安装。

发展史：RC8 SDK rg/glob搜索工具链(单文件运行时侧车支持)

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/fs/tool-fs-search/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/fs

## 实现逻辑
search-core.ts:162-166 rg二进制解析新增 pkg 单文件运行时支持: 若'pkg' in process 且存在 process.execPath+'-rg' sidecar 则用侧车二进制，否则回退 @vscode/ripgrep 平台包。修复 pkg 打包下原生rg无法spawn问题。

## Provides
- ctx.tools 注册 glob、grep
- tools/post-execute 监听(spill 投影)
- ctx.systemPrompt section: tool:glob/grep
- SEARCH_* 错误词汇

## Depends On (上游依赖)
- `dsh-session` [运行时依赖] - 会话 cwd 作 rg workdir
  - 证据: `packages/fs/tool-fs-search/src/search-core.ts:223,377`
- `dsh-tools` [运行时依赖] - 工具注册与 post-execute 瀑布
  - 证据: `packages/fs/tool-fs-search/src/index.ts:70; glob.ts:359,361`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
