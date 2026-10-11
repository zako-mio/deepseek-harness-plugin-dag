# dsh-cordis-host-runner

- 包名: `@deepseek-ai/dsh-cordis-host-runner`
- 分组: G14 宿主扩展
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/extensions/cordis-host-runner`

## 实现逻辑
以「动态包注册表 + Host 半沙箱生命周期」实现：DynamicCordisRunnerService（TypertRemoteService，inject ['tools']）用 DynamicCordisRegistry 保存不可变 package 定义、owner session 与待决审批 (src/index.ts:141-162, src/registry.ts:141-275)。define 校验 name/purpose 与至少一个代码半边并做 define 期语法预检；runHostHalf/getClientCode/resolveRequestRun/settleUserRun 等 @Remote 方法驱动 Host/Client 两半激活，需用户批准的 Client 半经 ctx.emit('cordis/request-run') 广播，Host 半启动时 emit 'cordis/dynamic-package'、撤回时 emit 'cordis/dynamic-retract' (src/index.ts:169-178, src/index.ts:295-318, src/index.ts:342-392, src/index.ts:876-881)。Host 代码在 node:vm 沙箱中求值（tagged console、harness 注册助手、编码原语，以及 fs/web/bash/timer 的重定向陷阱），经 guardedPlugin 包成子 fiber 启动，启动失败即 dispose (src/sandbox.ts:101-117, src/sandbox.ts:226-236, src/lifecycle.ts:22-45)；CordisInspectRegistryService 提供 ctx.cordisInspect 与跨页查询路由 (src/inspect-registry.ts:47-120)。

## Provides
- ctx.dynamicCordisRunner (Host 侧动态 Cordis 包服务：不可变 package 注册表、Plugin 生命周期、审批与 Host/Client 调用路由)
- ctx.cordisInspect (Host 侧 Inspect Provider 注册表、Client manifest 镜像与跨页只读查询路由)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 以发起 Agent 的 Session 作为插件归属与权限边界，并向运行失败上报目标 Agent
  - 证据: `package.json:53 peerDep + src/index.ts:10 import Agent + src/inspect-registry.ts:5`
- `dsh-api-gateway` [编译依赖] - 声明 Gateway 接缝类型，使无存活 Client 时 Inspect 查询能快速失败而非等待超时
  - 证据: `package.json:65 devDep + src/inspect-registry.ts:6 type import（声明 Gateway 的 Client 能力，供跨页查询失败快速返回）`
- `dsh-llm` [编译依赖] - 构造带 cordis-host-runner 来源标记的用户消息向模型汇报运行结果，并校验动态工具的渲染内容块
  - 证据: `package.json:55 peerDep + src/index.ts:11 import createUserMessage + src/guard.ts:21 import ContentBlock`
- `dsh-session` [编译依赖] - 以 SessionId 标识插件归属会话，贯穿注册表、库存行与待决审批
  - 证据: `package.json:57 peerDep + src/types.ts:7 import SessionId + src/registry.ts:7`
- `dsh-tools` [E1+E2] - 把沙箱返回的工具定义规范化后注册进真实 Tool 注册表，并在 Inspect 侧校验 JSON Schema 与按 Agent 读取工具 schema
  - 证据: `package.json:58 peerDep + src/guard.ts:19-20 import defineTool/assertSupportedJsonSchema + src/inspect-registry.ts:8-9 + src/index.ts:142 static inject = ['tools']`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 把该业务包的 /remote 命名空间装配进 Client
- `dsh-tool-cordis` - 向 Host Inspect 注册表登记四个 Provider，并让工具侧通过 ctx.cordisInspect 列出与执行只读查询
