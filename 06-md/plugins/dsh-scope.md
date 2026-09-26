# dsh-scope

- 包名: `@deepseek-ai/dsh-scope`
- 分组: G09 核心运行时
- 拓扑层: Layer 1
- 来源层: L3 其余
- 源码路径: `packages/core/scope`

## 实现逻辑
提供作用域上下文原语：`createScope` 用 `ctx.plugin()` 铸造带 `kScope` 标记的子上下文并给出 exact/shared 两种拆卸边界 (src/index.ts:137-147)；`bindScopeParent`/`scopeParentOf`/`scopeChainOf` 维护 key 的父子链并做环检测 (src/index.ts:54-102)；`scopeTarget` 构造保留基础 filter、按 key 及其祖先准入监听的作用域载体 (src/index.ts:170-185)。store.ts 提供 `NamedEntries`/`AnonymousEntries` 插入有序存储与 `ScopedLayers` 全局/精确作用域层聚合，经 `ctx.effect()` 绑定注册所有权与可见性 (src/store.ts:30-266)。invariant.ts 注册作用域派发不变量，要求 scope-filtered 事件必须携带匹配的 scope carrier (src/invariant.ts:16-32)。

## Provides
- createScope/bindScopeParent/scopeParentOf/scopeChainOf/scopeOf (作用域铸造与父子链)
- scopeTarget/isScopeCarrier/carrierKeyOf (作用域路由载体)
- NamedEntries/AnonymousEntries/ScopedLayers/ScopeLayer (作用域感知注册表存储)
- ScopeKey/Scope/Scoped/ScopeParentBinding 类型

## Depends On (上游依赖)
- `dsh-invariants` [E1+E2] - 注册作用域派发关系的运行时不变量
  - 证据: `package.json:35 peerDep + src/invariant.ts:4 import + src/invariant.ts:13 inject(['invariants']) + src/invariant.ts:41 register`

## Dependents (下游被依赖)
- `dsh-agent` - 用 scopeTarget/Scoped 构建 agent 作用域载体
- `dsh-agent-loop` - 为每个 agent 铸造作用域上下文
- `dsh-agent-preset-registry` - 建立 Agent scope 与 preset standing scope 的父子绑定关系
- `dsh-api-remotes` - 从 waterfall 的 this 提取 carrier Agent 作用域
- `dsh-api-session-controller` - 作用域工具
- `dsh-client-connection` - 构造 OperatorPeer 的作用域语义
- `dsh-client-file-upload` - 用 scopeOf 校验操作发生在目标 Agent 自身作用域内
- `dsh-commands` - 全局与 agent 作用域的命令分层
- `dsh-cordis-host-runner` - 校验动态包作用域与守卫条件
- `dsh-goal` - goal/changed 事件按 agent 作用域分发的类型约束
- `dsh-jobs-local` - 用 scope 分层存放控制器与订阅，使每 owner 的读与通知相对化
- `dsh-mcp-client` - 按注册作用域隔离 serverName 与 Agent 级命名空间复用
- `dsh-mcp-resources` - 按 Agent 作用域分层保存与合并资源 provider
- `dsh-sdk-jsonrpc-server` - 使用作用域能力装配 SDK 运行时
- `dsh-session` - 为会话构造作用域路由载体并读取上下文作用域
- `dsh-skill` - 复用 ScopedLayers/NamedEntries/scopeOf/scopeChainOf 实现按 agent scope 分层的注册表与缓存键 (src/index.ts:362-371)
- `dsh-subagent` - 按委派父级做作用域过滤的事件派发
- `dsh-system-prompt` - 以作用域层存储并合并各作用域的提示贡献
- `dsh-tool-subagent` - 识别 preset 组合作用域
- `dsh-tools` - 以作用域层存储工具注册与呈现模式
- `dsh-user-approval` - 按 agent 过滤审批请求分派
- `dsh-user-questions` - 按 agent 作用域分派问答请求
