# dsh-api-terminal-controller

- 包名: `@deepseek-ai/dsh-api-terminal-controller`
- 分组: G02 API 网关与控制器
- 拓扑层: Layer 4
- 来源层: L2 web-app
- 源码路径: `packages/api/terminal-controller`

## 实现逻辑
实现 Session 拥有的交互式终端：TerminalController 继承 TypertRemoteService 并以 namespace 'terminal' 注册 ctx.terminalController(src/index.ts:76-103)，按 Session 维护终端/待分配/清理映射并在销毁时聚合清理(src/index.ts:61-73,104-109,287-314)。Remote 方法 environment/shells/list/create/follow/write/resize/rename/close/retain 提供分配、附着、输入、尺寸、重命名与关闭(src/index.ts:118-285)，底层用 subprocess.spawnTerminal 起 PTY(src/index.ts:342-378)。终端自身用 @xterm/headless 做屏幕恢复、TerminalRetention 做窗口持有与空闲回收(src/terminal.ts:1-15, src/retention.ts:1-14)。

## Provides
- ctx.terminalController(Session 拥有的交互式终端与 ctx.remote.terminal 命名空间所有者，src/index.ts:19-24,76-103)
- ctx.remote.terminal 远程方法集 environment/shells/list/create/follow/write/resize/rename/close/retain(src/index.ts:118-285)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 以 Agent 作为 Session 所有者参数与执行环境选择器
  - 证据: `package.json:71 devDependencies + src/index.ts:4 import type { Agent }(仅类型)`
- `dsh-api-gateway` [E1+E2] - Client 面经 Gateway 的 ctx.remote 暴露终端命名空间
  - 证据: `package.json:43,46 dsh.client.inject/external + src/client/index.ts:5 import '@deepseek-ai/dsh-api-gateway/client' + src/client/index.ts:235 inject ['remote','remote.terminal']`
- `dsh-sandbox-policy` [E1+E2] - 按 Session 沙箱策略选择执行提供者
  - 证据: `src/index.ts:6 import type {} + src/index.ts:77 inject 'sandboxPolicy' + src/index.ts:335 agent.ctx.get('sandboxPolicy')`
- `dsh-session` [编译依赖] - 以 SessionId 作为终端所有者键
  - 证据: `package.json:79 devDependencies + src/index.ts:5 import type { SessionId } + src/client/bindings.ts:2 import`
- `dsh-working-directory` [E1+E2] - 解析终端进程的当前目录
  - 证据: `package.json:84 devDependencies + src/index.ts:7 import type {} + src/index.ts:77 inject 'workingDirectory' + src/index.ts:344 workingDirectory.ensure`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 把该业务包的 /remote 命名空间装配进 Client
- `dsh-client-ui-sidebar-terminal` - 终端视图、启动 shell、关闭与保留窗口全部经 webTerminals 服务
