# dsh-commands

- 包名: `@deepseek-ai/dsh-commands`
- 分组: G20 交互命令
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/interaction/commands`

## 实现逻辑
以 ScopedLayers + NamedEntries 实现插件自有的人类命令注册表：全局注册与按 Agent 作用域影子覆盖，register() 返回精确的 effect 释放器，定义在写入前被校验并规范化为不可变描述符 + 处理器 (src/index.ts:263-292, src/index.ts:179-225, src/index.ts:470-472)。execute() 解析斜杠命令行，先追加 command/run、再跑处理器、最后追加 command/done，形成按 commandId 配对的可回放生命周期 (src/index.ts:360-431, src/index.ts:457-467)。附件准入在处理器之前完成：图片经 admitEncodedImages 入库、文件凭据经 receipt resolver 解析并按提交顺序还原为 LLM 内容块 (src/index.ts:389-420, src/index.ts:493-531)。注册表变更通过非否决的 commands/change 事件广播，监听器异常被逐个隔离 (src/index.ts:475-489)。

## Provides
- ctx.commands (CommandRuntime：命令注册/列举/查找/执行与作用域影子)
- Session 事件 command/run 与 command/done（配对 commandId 的可回放生命周期）
- Cordis 事件 commands/change（注册表变更广播，非否决）
- 解析入口 parseCommand 与命令身份 brand（CommandDefinitionId / CommandId）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - Agent 既是命令作用域键也是命令的接收者
  - 证据: `src/index.ts:8 import type { Agent } + package.json:51 peerDep`
- `dsh-llm` [编译依赖] - 准入后的附件以 LLM 内容块类型交给命令处理器
  - 证据: `src/index.ts:11 import type { FileBlock, ImageBlock } + package.json:54 peerDep`
- `dsh-session` [编译依赖] - 命令生命周期事件必须写入会话日志
  - 证据: `src/index.ts:14-15 import { SessionSeq } + src/index.ts:466 session.append`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 把该业务包的 /remote 命名空间装配进 Client
- `dsh-api-session-controller` - 复用命令目录词汇与 Client 契约
- `dsh-client-file-upload` - 让命令提交解析 staged 文件 receipt
- `dsh-client-ui-chat` - 命令节点类型
- `dsh-client-ui-commands` - 命令描述与执行结果类型
- `dsh-client-ui-conversation` - 命令记录类型
- `dsh-client-ui-goal` - 命令输入事件类型
- `dsh-command-compact` - 承载 `/compact` 命令的注册面与命令调用/结果类型，命令必须注册进 commands 注册表才能被人类命令适配器看见
- `dsh-command-feedback` - 注册 /feedback 命令定义并与命令适配器对接
- `dsh-command-goal` - 把 /goal 命令注册进命令注册表并复用其调用/结果类型
- `dsh-compaction-basic` - 手动命令发起的压缩需把发起命令身份写进压缩生命周期事件用于呈现关联
- `dsh-experimental-claude-code-mods` - mod 注册的斜杠命令与 command.run 事件由 commands seam 提供
- `dsh-permission-presets` - 注册 /permission 命令，作为 Web 客户端使用的唯一写入入口
- `dsh-plan-mode` - 注册 /plan 斜杠命令；命令子插件仅在命令注册表被组合时激活
- `dsh-session-log-export` - 注册 Web /export 命令作为导出入口
