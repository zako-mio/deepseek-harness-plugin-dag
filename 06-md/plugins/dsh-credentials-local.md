# dsh-credentials-local

- 包名: `@deepseek-ai/dsh-credentials-local`
- 分组: G11 凭据设置
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/credentials/credentials-local`

## 实现逻辑
实现 CredentialProvider 抽象(默认导出)，文件位于 $DSH_HOME/.credentials.yaml。resolve() 按信任层级查值：继承环境(只读,获胜)>managed 文件>项目 .env>用户 .env。写路径经 withFileLock 读-改-写(0600/0700、保留注释)，chokidar 热重载，write() 拒绝 env 遮蔽的 ref，notifyUpdated 发 credentials/updated 事件。

## Provides
- ctx.credentials(LocalCredentialProvider)
- resolve/describe/set/unset
- credentials/updated 事件扇出
- CREDENTIALS_FILENAME/resolveSpec

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
