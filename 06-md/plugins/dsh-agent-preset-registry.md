# dsh-agent-preset-registry

- 包名: `@deepseek-ai/dsh-agent-preset-registry`
- 分组: G27 Agent 预设
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/preset/agent-preset-registry`

## 实现逻辑
AgentPresetRegistry 为 TypertRemoteService，构造时注册 agentPreset 投影并监听 session/event 转发 agent-preset/selected（src/index.ts:63-71、src/session.ts:35-44）。register() 立即激活定义，activate() 在独立 scope 内用 mountPreset 挂载 Loader 子树，失败则记录 broken 并 dispose scope（src/index.ts:80-118、src/mount.ts:258-272）。mount()/bind() 以 bindScopeParent 把 Agent scope 绑到保留的 standing revision，用引用计数 collect 回收，composeFrom 让子 Agent 继承父的精确版次（src/index.ts:208-284）。auditRows 与 leakedServices 审计行可用性与根域服务泄漏（src/mount.ts:86-212）；invariant.ts 在 internal/service 与 system-prompt/assemble 复核隔离与绑定（src/invariant.ts:33-59）。

## Provides
- ctx.agentPresets (Agent 预设注册表：激活/绑定/选择与 composition 读取，src/index.ts:51-365)
- sessionProjections `agentPreset` 投影（会话实际运行的预设定，src/index.ts:66、src/session.ts:35-44）
- Remote 方法 list/read/select（客户端花名册读取与选择，src/index.ts:170-206、:318-334）

## Depends On (上游依赖)
- `cordis-plugin-include` [编译依赖] - 以 Loader dialect 序列化预设声明的 entry 列表供查看
  - 证据: `src/index.ts:6 import entryListSchema`
- `cordis-plugin-loader` [E1+E2] - 挂载、审计并定位预设的 Loader entry 树
  - 证据: `src/index.ts:52 inject 'loader' + src/composition-inventory.ts:3 EntryTree/isJsExpr + src/mount.ts:3 EntryTree + src/index.ts:137 this.owner.loader.await()`
- `dsh-agent` [编译依赖] - 绑定并读取活动 Agent 的预设版次
  - 证据: `src/index.ts:8 type import Agent + src/index.ts:325 agent.ctx、src/index.ts:326 agent.session`
- `dsh-invariants` [E1+E2] - 注册预设隔离与 Agent 绑定不变式
  - 证据: `src/invariant.ts:7 type InvariantInstaller + src/invariant.ts:68 ctx.invariants.register`
- `dsh-scope` [编译依赖] - 建立 Agent scope 与 preset standing scope 的父子绑定关系
  - 证据: `src/index.ts:5 bindScopeParent/createScope/scopeOf + src/mount.ts:6 scopeOf/scopeParentOf`
- `dsh-session` [编译依赖] - 把预设选择写入会话日志
  - 证据: `src/types.ts:2 type SessionId + src/index.ts:326 agent.session.append('agent-preset/selected')`
- `dsh-session-projection` [E1+E2] - 注册 agentPreset 投影并读取 turnBoundary 判定空会话
  - 证据: `src/index.ts:66 ctx.sessionProjections.register + src/session.ts:17 type ProjectionDefinition + src/index.ts:321 stateOf`
- `dsh-settings` [运行时依赖] - 关闭 settings 自动持久化以自管 selectedDefault
  - 证据: `src/index.ts:10 type import + src/index.ts:67 ctx.inject(['settings'], ...) settings.configure({ auto: false })`
- `dsh-system-prompt` [E1+E2] - 在模型组装水线校验 Agent 已加入某预设
  - 证据: `src/invariant.ts:10 type import + src/invariant.ts:48 ctx.on('system-prompt/assemble')`
- `dsh-tools` [E1+E2] - 预设重绑后通知工具目录变更
  - 证据: `src/index.ts:11 type import + src/index.ts:308 this.owner.emit('tools/change')`

## Dependents (下游被依赖)
- `dsh-agent-preset` - 把本行声明的预设定义提交给注册表激活
- `dsh-api-remotes` - 装配 agent preset registry 命名空间
- `dsh-api-session-controller` - 解析并挂载 Agent 预设
- `dsh-client-ui-agent-preset` - 消费 preset 组合类型与 display 文案
- `dsh-client-ui-settings-plugin-inventory` - 复用共享的预设显示名折叠逻辑
- `dsh-host-plugin-inventory` - 读取 agent preset 组合清单并投影其行
- `dsh-plugin-package-inventory-deepseek` - 查询 agent 的 standing preset 挂载树以纳入预设内活跃插件包
- `dsh-subagent` - 让子代理加入父的 preset 组合
