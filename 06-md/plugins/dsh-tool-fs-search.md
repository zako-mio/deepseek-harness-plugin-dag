# dsh-tool-fs-search

- 包名: `@deepseek-ai/dsh-tool-fs-search`
- 分组: G16 文件系统
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/fs/tool-fs-search`

## 实现逻辑
以 npm 包内置的 ripgrep 二进制注册模型面 glob/grep 工具：两者均经 ctx.subprocess.spawn() 以固定 argv 模板运行 rg，工具层负责 schema、参数校验、argv 构造、结果解析、保留与格式化结果 spill (src/index.ts:1-27, 128-159)；不注入 fs 也不经 shell，ctx.spillStore 用 ctx.get() 机会式读取 (src/index.ts:17-19, 69-70)。glob/grep 在 tools/post-execute 上做格式化结果落盘 (src/glob.ts:355, src/grep.ts:342)。

## Provides
- 工具 glob / grep

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 搜索结果以 LLM 可消费的内容部件返回
  - 证据: `src/search-core.ts:25 import`
- `dsh-system-prompt` [运行时依赖] - 向系统提示注入搜索工具使用指引
  - 证据: `src/index.ts:70 inject 'systemPrompt' + src/glob.ts:297 ctx.systemPrompt`
- `dsh-tools` [E1+E2] - 通过工具注册表发布 glob/grep 工具
  - 证据: `src/index.ts:70 inject ['tools','systemPrompt','subprocess'] + src/search-core.ts:30 import`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
