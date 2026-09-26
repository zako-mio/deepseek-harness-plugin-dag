# dsh-cordis-host-runner

- 包名: `@deepseek-ai/dsh-cordis-host-runner`
- 分组: G14 宿主扩展
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/extensions/cordis-host-runner`

## 实现逻辑
DynamicCordisRunnerService（继承 TypertRemoteService）实现进程级动态插件注册表与宿主半生命周期：持有不可变包定义、每插件单一活动运行、经人工审批后激活客户端半，并支持 Host/Client 双向调用 (src/index.ts:129-149)。宿主半代码在 node:vm 沙箱中求值，沙箱仅暴露 tagged console、harness.defineTool/registerTool 与 Node API 陷阱（重定向到 ctx.fs/ctx.web/ctx.bash/cordis 定时器）(src/sandbox.ts:101-117)；CordisInspectRegistryService 则提供只读 Inspect provider 注册表与跨页查询路由 (src/inspect-registry.ts:45-69, 37-42)。运行期发出 cordis/request-run、cordis/dynamic-package、cordis/dynamic-retract、cordis/inspect-query(-resolved) 等事件 (src/index.ts:296-1021, src/inspect-registry.ts:153-189)。

## Provides
- ctx.dynamicCordisRunner (宿主动态插件注册表、宿主半沙箱生命周期与 Host/Client 调用表)
- ctx.cordisInspect (宿主 Inspect provider 注册表与跨页查询路由)
- 事件 cordis/request-run、cordis/request-run-resolved、cordis/dynamic-package、cordis/dynamic-retract、cordis/inspect-query、cordis/inspect-query-resolved

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - Inspect 查询与运行请求以 Agent 为其作用域主体
  - 证据: `src/index.ts:10 import + src/inspect-registry.ts:5 import`
- `dsh-llm` [编译依赖] - 运行结果以用户消息源写入会话
  - 证据: `src/index.ts:11 createUserMessage + src/guard.ts:21 import`
- `dsh-scope` [编译依赖] - 校验动态包作用域与守卫条件
  - 证据: `src/guard.ts:18 import`
- `dsh-session` [编译依赖] - 运行与库存行以 SessionId 关联会话
  - 证据: `src/registry.ts:7 import + src/types.ts:7 import`
- `dsh-tools` [E1+E2] - 动态包经 harness 注册的工具须落入 tools 注册表
  - 证据: `src/index.ts:130 static inject ['tools'] + src/guard.ts:19 import`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配动态包运行器命名空间
- `dsh-tool-cordis` - 消费宿主 Inspect 注册表以注册 provider 与执行查询
