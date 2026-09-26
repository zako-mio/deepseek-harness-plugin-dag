# dsh-invariants

- 包名: `@deepseek-ai/dsh-invariants`
- 分组: G29 运行时诊断
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/runtime-diagnostics/invariants`

## 实现逻辑
以 InvariantRegistry（Service）实现包级运行时不变式注册表，注册为 ctx.invariants（src/index.ts:94-118）；register(packageName, installer) 校验包名合法性与唯一性，并在子 fiber（ctx.effect + ctx.plugin）中运行每个包自带的检查安装器，违规时抛出带包名的 InvariantError（src/index.ts:136-197）。Config 提供全局开关与 package_allowlist/package_blocklist 正则过滤（src/index.ts:95-99,121-126）。该包无本仓内部依赖。

## Provides
- ctx.invariants (包级运行时不变式注册表，供各包 ./invariant 伴侣注册检查)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-agent` - 作为 invariant companion 注册 agent 生命周期不变量
- `dsh-agent-loop` - 注册 loop 请求可重建性不变量
- `dsh-agent-preset-registry` - 注册预设隔离与 Agent 绑定不变式
- `dsh-authorization` - 注册 single-flight 释放不变式，检测 settled 后 key 残留 in-flight
- `dsh-client-hmr` - 注册包级不变量，检查 bundle 监视器不被泄漏
- `dsh-client-modules` - 注册包级不变量，校验模块注册表随 fiber 释放而清理
- `dsh-client-ui-renderer` - 注册渲染器拥有的运行时不变式检查
- `dsh-commands` - 注册命令生命周期配对不变量
- `dsh-goal` - 注册目标流不变量校验伴随件
- `dsh-goal-round-driver` - 注册续轮提示词不变量伴随件
- `dsh-hook-protocol` - 注册 hook 事件配对不变量伴随件
- `dsh-llm` - 注册 llm 包拥有的流协议与注册表不变量 companion
- `dsh-llm-retry` - 注册包拥有的重试持久事件不变量 companion
- `dsh-permission-presets` - 注册 preset 事件可解析性不变量
- `dsh-plan-mode` - 注册 plan/mode 载荷校验不变式
- `dsh-sandbox-policy` - 注册本包事件字段的运行时不变式检查
- `dsh-schedule` - 注册 schedule/change 事件流的运行时不变式
- `dsh-scope` - 注册作用域派发关系的运行时不变量
- `dsh-session` - 注册会话日志关系不变量
- `dsh-session-log-deepseek` - 注册水位字段的运行时不变式
- `dsh-session-title` - 注册 session/title 事件来源与 messageSeqs 关系的运行时不变式
- `dsh-storage-domain` - 注册 domain/changed 与内存状态一致性不变量
- `dsh-subagent` - 注册 provider 注册表与 start/end 配对不变量
- `dsh-system-prompt` - 注册提示装配结果合法性不变量
- `dsh-time-context` - 注册包级不变量，校验时间读数格式、位置与时间戳在加载与派发时可重放一致
- `dsh-tool-subagent` - 注册可选路由定义完整性不变量
- `dsh-tool-todo` - 注册 todo 快照不变量校验
- `dsh-tool-workflow` - 注册 tool-workflow 记录的伴生不变量校验器
- `dsh-tools` - 注册会话内工具调用关系不变量
- `dsh-user-approval` - 注册审批审计流不变量
- `dsh-workspace` - ./invariant 伴生插件需向 runtime 不变量服务注册『实体缓存 ↔ 持久表』一致性断言
