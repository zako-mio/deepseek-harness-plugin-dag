# dsh-credentials-local

- 包名: `@deepseek-ai/dsh-credentials-local`
- 分组: G11 凭据设置
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/credentials/credentials-local`

## 为什么需要它（设计初衷）
凭证引用缝的本地提供者：配置只携带引用而非密钥，消费者在操作边界解析。四层单一优先级（进程环境 > $DSH_HOME/.credentials.yaml > 项目 .env > 用户 .env），环境层启动快照冻结、可写存储经原子写+0600/0700 权限+热重载。既支持『非侵入式读取』（进入 launch env 快照）又满足运行期覆盖意图。

发展史：credentials 能力族缝（reference seam）+ env-over-.env 文件提供者；随 core spine 起步。明确把『模型可见路径』与『OS-keychain 隔离存储』标为后续工作——文件权限是谨慎性而非安全边界。

来源：
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/credentials/credentials-local
- https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/credentials.md

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
