# dsh-tool-present

- 包名: `@deepseek-ai/dsh-tool-present`
- 分组: G11 交付物
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/deliverables/tool-present`

## 实现逻辑
函数式插件，向 tools 注册模型工具 present：逐个校验路径非空、存在且为普通文件后返回交付清单 (src/index.ts:34-99)。execute 要求调用方有 Agent Session 与打开的 turn（读 sessionProjections.stateOf(..., 'turnBoundary')），相对路径经 ctx.workingDirectory.ensure 解析，文件判定用 ctx.fs.lstat/resolve/stat 并把结果规范化为进程路径 (src/index.ts:77-97)。成功结果在 tools/result 事件里由插件 append deliverables/presented 会话事件，使「声明了哪些交付物」进入会话日志，而文件内容仍留在原路径 (src/index.ts:100-108, src/types.ts:12-16)。

## Provides
- present 工具 (声明最终交付文件，产出 deliverables/presented 会话事件)
- SessionEventMap 扩展: deliverables/presented

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 工具执行信封的 agent 载体类型来自 agent 包
  - 证据: `src/index.ts:7 import type {} from '@deepseek-ai/dsh-agent' + src/index.ts:78 exec.agent === undefined 检查 + package.json:39 peerDep`
- `dsh-llm` [编译依赖] - 会话事件里的 callId 使用 llm 的 branded ToolCallId 类型
  - 证据: `src/types.ts:2 import type { ToolCallId } from '@deepseek-ai/dsh-llm/brand' + package.json:41 peerDep`
- `dsh-session` [E1+E2] - 把交付声明写入会话日志，并扩展 SessionEventMap
  - 证据: `src/index.ts:9 import type { Session } from '@deepseek-ai/dsh-session' + src/index.ts:105 session.append('deliverables/presented', {...}) + src/types.ts:12 declare module '@deepseek-ai/dsh-session/types' + package.json:42 peerDep`
- `dsh-session-projection` [E1+E2] - 读取 turnBoundary 投影以确认存在打开的 turn 并取得 turn 号
  - 证据: `src/index.ts:8 import type {} from '@deepseek-ai/dsh-session-projection' + src/index.ts:79 ctx.sessionProjections.stateOf(exec.agent.session, 'turnBoundary') + package.json:43 peerDep`
- `dsh-tools` [E1+E2] - 工具注册、执行信封与 tools/result 扩展点都由 tools seam 提供
  - 证据: `src/index.ts:6 import { defineTool, type ToolExecution } + src/index.ts:27 export const inject = ['tools', 'fs', 'sessionProjections', 'workingDirectory'] + src/index.ts:39 ctx.tools.register + src/index.ts:100 ctx.on('tools/result') + package.json:44 peerDep`
- `dsh-working-directory` [E1+E2] - 把相对交付路径解析到会话工作目录
  - 证据: `src/index.ts:2 import type {} from '@deepseek-ai/dsh-working-directory' + src/index.ts:82 ctx.workingDirectory.ensure(exec.agent, exec.signal) + package.json:45 peerDep`

## Dependents (下游被依赖)
- `dsh-client-ui-deliverables` - present 工具结果类型
