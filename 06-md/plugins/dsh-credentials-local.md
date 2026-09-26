# dsh-credentials-local

- 包名: `@deepseek-ai/dsh-credentials-local`
- 分组: G10 凭据与授权
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/credentials/credentials-local`

## 实现逻辑
实现文件型 `CredentialProvider`（`LocalCredentialProvider`，src/index.ts:513）：以 `$DSH_HOME/.credentials.yaml` 为可写的托管层，按可信度分层解析 ref（继承环境 > 托管文件 > 项目 .env > 用户 .env，src/index.ts:609-631、553-567）。文档解析严格拒绝未知版本/顶层键/记录字段而非跳过（src/index.ts:188-227、328-358），写入在跨进程文件锁下 read-modify-write、保留注释并以 0600 原子写（src/index.ts:666-699）；同时校验文件不得 group/other 可读（src/index.ts:127-146）。chokidar 监听外部编辑并在 `ready` 时补一次对账热发布（src/index.ts:569-607、869-891）。

## Provides
- CredentialProvider 实现 (文件型 refs/records 凭据存储，供 ctx.credentials seam 消费)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
