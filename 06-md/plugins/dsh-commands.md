# dsh-commands

- 包名: `@deepseek-ai/dsh-commands`
- 分组: G21 交互命令
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/interaction/commands`

## 实现逻辑
实现 ctx.commands 人类命令注册表：全局与 agent 作用域分层（NamedEntries/ScopedLayers），register() 校验并冻结定义（src/index.ts:94-111、179-292）。execute() 解析斜杠命令行，先写 command/run 再执行处理函数并写 command/done，附件准入与取消也在此强制（src/index.ts:360-431）。list/execute 以 TypertRemote 暴露给 UI（src/index.ts:314、360），invariant.ts 校验生命周期事件按 commandId 成对（src/invariant.ts:20-67）。

## Provides
- ctx.commands (命令注册与执行服务 + Remote list/execute；命令生命周期事件配对不变量，src/index.ts:263-490)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 命令以 agent 及其 session 为作用域与日志目标
  - 证据: `package.json:56 peerDep + src/index.ts:8 type import Agent`
- `dsh-invariants` [E1+E2] - 注册命令生命周期配对不变量
  - 证据: `package.json:59 peerDep + src/invariant.ts:9 import; src/invariant.ts:67 ctx.invariants.register`
- `dsh-llm` [编译依赖] - 附件以 LLM 块类型参与模型可见输入
  - 证据: `package.json:60 peerDep + src/index.ts:11 import FileBlock/ImageBlock`
- `dsh-scope` [E1+E2] - 全局与 agent 作用域的命令分层
  - 证据: `package.json:61 peerDep + src/index.ts:12-13 import NamedEntries/ScopedLayers; src/index.ts:264 ScopedLayers`
- `dsh-session` [E1+E2] - 把命令运行生命周期写入会话日志
  - 证据: `package.json:62 peerDep + src/index.ts:14-15、src/invariant.ts:8 import; src/index.ts:373 session.append`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配 commands 命名空间与事件签名
- `dsh-api-session-controller` - 命令注册表会话侧表面
- `dsh-client-file-upload` - 让命令 prompt 能解析上传 receipt 为文件引用
- `dsh-client-ui-chat` - 命令节点数据
- `dsh-client-ui-commands` - 命令目录与结果类型
- `dsh-client-ui-conversation` - 命令记录节点类型
- `dsh-client-ui-goal` - goal 命令输入节点类型
- `dsh-command-compact` - 承载 `/compact` 命令的注册面与命令调用/结果类型，命令必须注册进 commands 注册表才能被人类命令适配器看见
- `dsh-command-feedback` - 注册 /feedback 命令定义并与命令适配器对接
- `dsh-command-goal` - 把 /goal 命令注册进命令注册表并复用其调用/结果类型
- `dsh-compaction-basic` - 手动命令发起的压缩需把发起命令身份写进压缩生命周期事件用于呈现关联
- `dsh-permission-presets` - 以 /permission 命令暴露唯一写路径
- `dsh-plan-mode` - 注册 /plan 命令并关联命令生命周期事件
- `dsh-session-log-export` - 注册 Web /export 命令作为导出入口
