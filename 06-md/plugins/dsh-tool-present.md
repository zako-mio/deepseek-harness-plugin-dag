# dsh-tool-present

- 包名: `@deepseek-ai/dsh-tool-present`
- 分组: G11 交付物
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/deliverables/tool-present`

## 实现逻辑
函数插件在 agent scope 注册模型可见工具 `present`，让模型把已存在的文件声明为最终交付物（src/index.ts:38-99）。`execute` 先校验存在 open turn（经 sessionProjections 的 `turnBoundary`）、文件数 1..maxFiles，再用 `ctx.fs.lstat/resolve/stat` 确认每个路径都是常规文件，否则报错（src/index.ts:76-97）。成功结果经 `tools/result` 监听器把 `deliverables/presented` 事件追加进 Session，文件内容仍留在源路径不被复制（src/index.ts:100-108、src/types.ts:12-16）。

## Provides
- 工具 present (声明已存在文件为最终交付物)
- Session 事件 deliverables/presented

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 取得调用 Agent 及其 Session
  - 证据: `src/index.ts:6 import type {} from '@deepseek-ai/dsh-agent' + src/index.ts:77 exec.agent`
- `dsh-llm` [编译依赖] - 事件 payload 使用品牌化 ToolCallId
  - 证据: `src/types.ts:2 import ToolCallId from '@deepseek-ai/dsh-llm/brand'`
- `dsh-session` [编译依赖] - 把交付声明持久化为 Session 事件
  - 证据: `src/index.ts:8 import type { Session } + src/index.ts:105 session.append`
- `dsh-session-projection` [E1+E2] - 读取当前 open turn 与 turn 号
  - 证据: `src/index.ts:7 import type {} from '@deepseek-ai/dsh-session-projection' + src/index.ts:26 inject + src/index.ts:78 stateOf(..., 'turnBoundary')`
- `dsh-tools` [E1+E2] - 注册工具并订阅 tools/result
  - 证据: `src/index.ts:5 import defineTool + src/index.ts:26 inject ['tools','fs','sessionProjections'] + src/index.ts:38 ctx.tools.register`

## Dependents (下游被依赖)
- `dsh-client-ui-deliverables` - present 工具结果数据
