# dsh-credentials-local

- 包名: `@deepseek-ai/dsh-credentials-local`
- 分组: G10 凭据与授权
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/credentials/credentials-local`

## 实现逻辑
CredentialProvider 的文件型实现：把 $DSH_HOME/.credentials.yaml 作为唯一可写层，与继承进程环境、项目 .env、用户 .env 按信任度分层（继承环境只读且优先，其余为读回退）(src/index.ts:1-35, src/index.ts:620-642)。文档是 version:1 的 refs/records 两段结构，解析遇到未知版本、未知字段、不可寻址的键一律拒绝而非跳过，并保留旧扁平布局的一次性迁移 (src/index.ts:188-227, src/index.ts:242-266)。写入走跨进程文件锁 + 原子写，读-改-写前先 reconcileFromDisk() 合并外部改动，以 0600/0700 落盘并在每次读取时校验属主之外无权限位 (src/index.ts:677-710, src/index.ts:759-778, src/index.ts:127-146)。用 chokidar 监听文档变化热发布，外部编辑经 notifyUpdated/notifyRecordUpdated 广播给 seam，整份快照每次整体替换 (src/index.ts:569-618, src/index.ts:855-894)。

## Provides
- credentials 的文件型提供者 (.credentials.yaml 的 refs/records 读写、热重载、跨进程写锁、分层解析)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
