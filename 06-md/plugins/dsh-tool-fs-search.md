# dsh-tool-fs-search

- 包名: `@deepseek-ai/dsh-tool-fs-search`
- 分组: G13 文件系统
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/fs/tool-fs-search`

## 为什么需要它（设计初衷）
面向模型的文件发现工具 glob/grep，由打包 ripgrep 二进制支持（经 ctx.subprocess），不依赖宿主 rg 安装。

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/fs/tool-fs-search/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/fs

## 实现逻辑
模型面向的 glob/grep 发现工具套件,基于 @vscode/ripgrep:apply() 注册两工具,执行经 ctx.subprocess.spawn() 以固定 argv 模板直接运行,无 shell 层;runRipgrep 完成 stdout 预算/退出码分类,超限结果经 ctx.get('spillStore') 尽力保存并附 recovery 提示;tools/post-execute 监听在 top-level 直接调用时替换投影以携带 spill 引用。

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
