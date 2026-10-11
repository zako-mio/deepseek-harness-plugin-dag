# dsh-experimental-claude-code-mods

- 包名: `@deepseek-ai/dsh-experimental-claude-code-mods`
- 分组: G13 实验特性
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/experimental/claude-code-mods`

## 实现逻辑
以 TypertRemoteService 实现 ctx.claudeCodeMods 桥接服务：用 ModsEngine 加载以 defineMod 包装的 Claude Code mod（register(on, options)），并维护 mod 注册表、工具名别名表与表面（band）表 (src/index.ts:201-285, src/define-mod.ts:45-64)。桥把 harness 扩展点翻译成 mod 事件：agent/created→session.start、agent/pre-step→prompt.submit 与 turn.start（可改写提示文本或丢弃提示）、tools/execute→tool.call（可 deny 或替换结果，并拒绝改路由/改参数）、turn/end→turn.complete、agent/disposed→session.end (src/index.ts:304-482)。$ 宿主操作面把 mods API 映射到 harness 服务：fs、subprocess、storageDomain、sessionProjections、commands、tools、userQuestions 等，缺失服务按名报错 (src/host-ops.ts:1-9, src/host-ops.ts:174-501)。

## Provides
- ctx.claudeCodeMods (Claude Code mod 加载、事件桥接、工具/命令注册、Remote band 服务)
- defineMod / ModPlugin 插件包装与 MODS_API_VERSION、DEFAULT_TOOL_ALIASES、KNOWN_EVENTS 等 mod API 面
- Remote: watchBand / pressBand (会话提示框上方 band 的流与按键)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - mod 事件以 Agent 生命周期与 pre-step 为触发点，绑定对象是 Agent
  - 证据: `src/index.ts:16 import type { Agent, PreStepDecision } + src/index.ts:232 ctx.get('agents')?.get(SessionId(sessionId)) + src/index.ts:304 ctx.on('agent/created') + src/index.ts:340 ctx.on('agent/pre-step') + package.json:59 peerDep`
- `dsh-commands` [E1+E2] - mod 注册的斜杠命令与 command.run 事件由 commands seam 提供
  - 证据: `src/host-ops.ts:17 import type { CommandDefinition } from '@deepseek-ai/dsh-commands' + src/host-ops.ts:307 ctx.get('commands') + package.json:60 peerDep`
- `dsh-llm` [编译依赖] - $.session 的消息构造与 callId 品牌类型来自 llm 包
  - 证据: `src/host-ops.ts:19-20 import { createUserMessage, ToolCallId } + import type { ContentBlock, Message } from '@deepseek-ai/dsh-llm' + package.json:62 peerDep`
- `dsh-session` [E1+E2] - turn.complete 由会话事件折叠得到，mod 状态按会话 id 归属
  - 证据: `src/index.ts:19 import { SessionId } from '@deepseek-ai/dsh-session' + src/index.ts:449 ctx.on('session/event', ...) + src/index.ts:321 ctx.on('agent/disposed') 中的 session 记账 + package.json:64 peerDep`
- `dsh-session-projection` [E1+E2] - $.session 的用量等派生事实读取会话投影状态
  - 证据: `src/host-ops.ts:15-16 import type {} + import type { SessionProjectionStateMap } + src/host-ops.ts:230 ctx.get('sessionProjections')?.stateOf(session, key) + package.json:65 peerDep`
- `dsh-storage-domain` [E1+E2] - $.store 的 per-plugin JSON 存储落在一个 storage domain 上
  - 证据: `src/host-ops.ts:26-27 import { defineDomain, domainTable } + src/host-ops.ts:174 ctx.get('storageDomain') + package.json:66 peerDep`
- `dsh-token-meter` [编译依赖] - 类型面需要 token-meter 的投影状态声明以读取会话用量
  - 证据: `src/host-ops.ts:25 import type {} from '@deepseek-ai/dsh-token-meter' + package.json:67 peerDep`
- `dsh-tools` [E1+E2] - mod 的工具注册与 tool.call 拦截都通过 tools seam
  - 证据: `src/index.ts:22-23 import { validateJsonSchemaValue, type PostToolDecision, ... } from '@deepseek-ai/dsh-tools' + src/host-ops.ts:359 ctx.get('tools') + src/index.ts:382 ctx.on('tools/execute') + src/index.ts:436 ctx.on('tools/post-execute') + package.json:69 peerDep`
- `dsh-user-questions` [E1+E2] - $.ui.ask 与 session.start 的 isInteractive 判定依赖用户提问服务
  - 证据: `src/host-ops.ts:30 import type { AskUserQuestionOption } from '@deepseek-ai/dsh-user-questions' + src/host-ops.ts:256 ctx.get('userQuestions') + src/index.ts:313 ctx.get('userQuestions') !== undefined + package.json:71 peerDep`
- `dsh-working-directory` [E1+E2] - session.start 需要先确定会话工作目录
  - 证据: `src/host-ops.ts:23 import type { WorkingDirectoryService } + src/index.ts:212 static inject = ['workingDirectory'] + src/index.ts:311 ctx.workingDirectory.ensure(agent, abandon) + package.json:72 peerDep`

## Dependents (下游被依赖)
- `dsh-experimental-client-ui-claude-code-mods` - band 数据与按键回传都来自桥接服务的 Remote 命名空间
