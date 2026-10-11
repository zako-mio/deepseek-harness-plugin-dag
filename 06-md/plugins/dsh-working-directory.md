# dsh-working-directory

- 包名: `@deepseek-ai/dsh-working-directory`
- 分组: G31 会话核心
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/session/working-directory`

## 实现逻辑
提供 ctx.workingDirectory 作为每个会话有效目录的唯一所有者：注册 workingDirectory 投影（init 取 header.cwd，apply 消费 working-directory/change 事件），把它作为 systemPrompt 上下文 'working-directory:current' 注入，并在 system-prompt/assemble 瀑布里先 ensure 再回填文本 (src/index.ts:82-110)。get 只读投影值，无记录时回落 defaultDirectory；ensure 校验当前目录、缺失时恢复到原始项目目录并提交，set 校验目标为已存在目录后提交 (src/index.ts:122-170, src/index.ts:176-184)。每次提交都追加 working-directory/change 事件并注入一条 source 为 working-directory 的用户消息通知模型，注入失败只告警不回滚已提交状态 (src/index.ts:186-206)。同一会话的操作通过 pending 链串行化，服务销毁时中止生命周期并等待在途操作静默 (src/index.ts:208-222, src/index.ts:111-114)。

## Provides
- ctx.workingDirectory (会话有效工作目录服务：读取、校验/恢复、切换与提交)
- workingDirectory 投影单元、systemPrompt 上下文 'working-directory:current'，以及 source 为 working-directory 的模型可见变更通知

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 对传入的 Agent 及其会话、fiber 生效
  - 证据: `package.json:31 peerDep + src/index.ts:10 import type Agent；src/index.ts:140 agent.ctx.fiber.assertActive`
- `dsh-llm` [编译依赖] - 构造 source 为 working-directory 的模型可见变更通知
  - 证据: `package.json:33 peerDep + src/index.ts:12 import createUserMessage；src/index.ts:23 声明合并 MessageSourceMap`
- `dsh-session` [编译依赖] - 把目录变更作为会话事件写入日志
  - 证据: `package.json:34 peerDep + src/index.ts:13 import type Session；src/index.ts:33 声明合并 SessionEventMap 的 working-directory/change`
- `dsh-session-projection` [E1+E2] - 注册 workingDirectory 投影并读取当前提交值
  - 证据: `package.json:35 peerDep + src/index.ts:14 import type {}；src/index.ts:82 ctx.sessionProjections.register`
- `dsh-system-prompt` [E1+E2] - 把当前工作目录注入系统提示上下文
  - 证据: `package.json:36 peerDep + src/index.ts:15 import type {}；src/index.ts:90 ctx.systemPrompt.context、src/index.ts:97 ctx.on('system-prompt/assemble')`

## Dependents (下游被依赖)
- `dsh-agent-instructions` - 解析每个 agent 的当前工作目录，作为指令发现与相对作用域键的基准
- `dsh-api-session-controller` - 解析会话当前工作目录
- `dsh-api-terminal-controller` - 解析终端进程的当前目录
- `dsh-experimental-auto-review` - 审查快照的 ENVIRONMENT 段需要会话工作目录
- `dsh-experimental-browser-use-chrome-devtools-mcp` - MCP 进程的启动目录由会话工作目录决定
- `dsh-experimental-browser-use-playwright-mcp` - MCP 进程的启动目录由会话工作目录决定
- `dsh-experimental-claude-code-mods` - session.start 需要先确定会话工作目录
- `dsh-file-reference-local` - 取 agent 的工作目录作为索引根，并据此判断缓存是否需要重建
- `dsh-hooks-claude-code` - 解析会话工作目录，作为钩子进程的 cwd 与默认 CLAUDE_PROJECT_DIR
- `dsh-hooks-codex` - 解析会话工作目录作为钩子进程 cwd 与 payload 的 cwd 字段
- `dsh-sdk-jsonrpc-server` - 实现 SDK 的会话工作目录读取与切换方法
- `dsh-subagent` - 解析子代理启动目录
- `dsh-terminal-bash` - 在调用方未显式给 cwd 时解析并确保该 Agent 的工作目录
- `dsh-tool-bash` - 缺省工作目录取自会话工作区，相对 workdir 据此解析
- `dsh-tool-bash-persistent` - 会话初始 cwd 取自 owner 的工作区
- `dsh-tool-fs` - 解析会话当前工作目录作为 fs 调用的 cwd
- `dsh-tool-fs-search` - 解析搜索命令的工作目录，并作为返回路径的相对化基准
- `dsh-tool-lsp` - 取得会话工作区根作为查询作用域，缺失即拒绝查询而不回退
- `dsh-tool-present` - 把相对交付路径解析到会话工作目录
- `dsh-tool-pwsh` - 缺省工作目录与相对 workdir 解析
- `dsh-tool-pwsh-persistent` - 会话初始 cwd 取自 owner 工作区
- `dsh-tool-skill` - 技能查找需要 cwd 以选择项目根
- `dsh-tool-terminal` - 解析会话当前目录，作为终端会话初始 cwd 与相对 cwd 的解析基准
- `dsh-tool-working-directory` - 读写会话有效工作目录并在缺失时恢复
- `dsh-tools` - 为 Agent 所属的 run_code 解析工作目录；缺失时报错而不是静默使用进程目录
- `dsh-workflow-ptc` - 为运行解析父 Agent 的工作目录，作为沙箱进程 cwd 依据
