# dsh-acp-demo

- 包名: `@deepseek-ai/dsh-acp-demo`
- 分组: G37 示例与框架
- 拓扑层: Layer 8
- 来源层: L3 其余
- 源码路径: `packages/examples/acp-demo`

## 实现逻辑
ACP 自动化服务器示例应用：apply(ctx, config) 在一个复合 effect('acp-demo.composition') 中按顺序 ctx.plugin 装配 agent-spine-demo(spine, 不预创建 agent) → JsonlSessionPersistence(JSONL 持久化) → sessionCheckpointPolicy(flush 屏障) → SqliteSessionQueryEngine(查询索引) → dsh-acp 传输桥(每 session/new 用 provider/model 创建 agent)；卸载按逆序保证 ACP 会话 quiesce 先于持久化 detach。bin.ts 经 dsh-app-boot 的 boot/loadEnv/resolveConfigPath 启动 stdio JSON-RPC ACP 服务，stdout 保持纯净(仅 stderr 诊断)。Config schema 由 schemastery 定义并转发各子插件配置。

## Provides
- acp-demo 组合插件(apply)
- dsh-acp-demo bin(stdio ACP JSON-RPC 服务)
- 完整可读 Config schema(provider/model/toolOrder/workspaceContext/skills/goals 等)

## Depends On (上游依赖)
- `dsh-agent-spine-demo` [运行时依赖] - ctx.plugin(agentCore) 装配默认 spine 作为 ACP 会话后端
  - 证据: `packages/examples/acp-demo/src/index.ts:117`
- `dsh-session-checkpoint-policy` [运行时依赖] - ctx.plugin(sessionCheckpointPolicy) 强制 flush 屏障
  - 证据: `packages/examples/acp-demo/src/index.ts:131-133`
- `dsh-session-persistence-jsonl` [运行时依赖] - ctx.plugin(JsonlSessionPersistence) 挂载 JSONL 会话持久化
  - 证据: `packages/examples/acp-demo/src/index.ts:123-129`
- `dsh-session-query-sqlite` [运行时依赖] - ctx.plugin(SqliteSessionQueryEngine) 挂载 SQLite 会话查询索引
  - 证据: `packages/examples/acp-demo/src/index.ts:134-136`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
