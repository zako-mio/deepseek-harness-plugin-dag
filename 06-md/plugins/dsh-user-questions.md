# dsh-user-questions

- 包名: `@deepseek-ai/dsh-user-questions`
- 分组: G21 交互命令
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/interaction/user-questions`

## 实现逻辑
实现 ctx.userQuestions 能力 seam 的服务定义：ask() 校验信号、非空问题与意图一致性，并确认传入 agent 是注册表的确切存活实例且为 runtime root（src/index.ts:86-151）。随后经作用域 waterfall user-questions/request 交给 UI 答案者，无答案者时 fail-closed（src/index.ts:130-150）。

## Provides
- ctx.userQuestions (人类问答服务 + user-questions/request 作用域 waterfall，src/index.ts:65-152)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 限定只有运行时根的存活 agent 可发起人类交互
  - 证据: `package.json:35 peerDep + src/index.ts:11、src/types.ts:4 type import Agent; src/index.ts:95 ctx.get('agents') 校验存活 root`
- `dsh-llm` [编译依赖] - 错误基类与工具调用 id 类型
  - 证据: `package.json:36 peerDep + src/index.ts:12 import HarnessError、src/types.ts:5 ToolCallId`
- `dsh-scope` [E1+E2] - 按 agent 作用域分派问答请求
  - 证据: `package.json:37 peerDep + src/index.ts:13、src/types.ts:3 import scopeTarget/Scoped; src/index.ts:138 作用域 waterfall`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 用户提问 waterfall 事件签名
- `dsh-client-ui-user-questions` - 复用 Host 侧问题结构与答案类型
- `dsh-plan-mode` - 呈现计划评审问答通道
- `dsh-tool-ask-user` - 调用人类问答能力 seam
