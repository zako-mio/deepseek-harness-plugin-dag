# dsh-api-terminal-controller

- 包名: `@deepseek-ai/dsh-api-terminal-controller`
- 分组: G02 API 网关与控制器
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/api/terminal-controller`

## 实现逻辑
TerminalController 继承 TypertRemoteService，以 namespace 'terminal' 注册并注入 subprocess/sandboxPolicy/typert，构造时登记进程清理 effect (src/index.ts:75-109)。它按 Session 身份维护 OwnedSession（terminals/pending/allocations），create 幂等地经 subprocess.spawnTerminal 分配用户 shell 并用 BrowserTerminal 包装 (src/index.ts:157-188, 339-375)。BrowserTerminal 用 headless xterm + SerializeAddon 维护有界屏幕，follow 先送 snapshot 再推有序 output/state，write/resize 由唯一 controller attachment 校验后串行执行 (src/terminal.ts:77-130, 167-180)。其余 @Remote 方法提供 environment/shells/list/retain/rename/close，并施加尺寸、输入字节、终端数量等配置上限 (src/index.ts:117-284)。

## Provides
- ctx.remote.terminal（terminal 命名空间：environment/shells/list/create/retain/follow/write/resize/rename/close，Session 级用户终端）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - Remote 方法以 Agent 作为 Session 所有者参数
  - 证据: `src/index.ts:4 import type Agent`
- `dsh-api-gateway` [编译依赖] - 客户端 Remote 载体
  - 证据: `src/client/index.ts:5 import + src/client/model.ts:5 import`
- `dsh-sandbox-policy` [运行时依赖] - 取工作目录与沙箱工作区根
  - 证据: `src/index.ts:6 import type {} + src/index.ts:335 agent.ctx.get('sandboxPolicy')`
- `dsh-session` [编译依赖] - 会话身份类型
  - 证据: `src/index.ts:5 import type SessionId + src/client/bindings.ts:2 import`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配 terminal 命名空间
- `dsh-client-ui-sidebar-terminal` - 通过 ctx.webTerminals 服务管理 Web 终端视图、shell 启动与关闭
