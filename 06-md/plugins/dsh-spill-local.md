# dsh-spill-local

- 包名: `@deepseek-ai/dsh-spill-local`
- 分组: G21 上下文治理
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/spill/spill-local`

## 为什么需要它（设计初衷）
工具输出溢出存储的本地文件系统实现（ctx.spillStore）：把超大工具输出持久化到会话私有文件，inline 结果替换为有界预览+检索定位符（read/grep 该路径）。用随机十六进制前缀防 symlink 投毒、独占 owner-only 写入、0700 私有临时根，解决超大输出撑爆模型上下文与多用户本地的安全问题。

发展史：2026-07-08 tool-output spill files 决策划定存储/保留/工具自有输出处理的边界；与保留策略（dsh-output-retention head/tail 截断）协作。后端无会话生命周期删除，留待外部清理。

来源：
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/spill/spill-local
- https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/notes/implemented/architecture/2026-07-08-tool-output-spill-files.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/spill.md

## 实现逻辑
以 LocalSpillStore 类(extends SpillStore)默认导出，static Config 仅 root(缺省 OS temp 下 mkdtemp 私有 0700)。saveText 将完整文本写入 <root>/session-<sha256前12>/<随机hex>-<sanitizedName>，open('wx',0600) 独占写入防符号链接投毒，返回 SpillLocator。

## Provides
- ctx.spillStore 服务
- session-scoped 私有文件存储
- traversal-safe 命名

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-spill-policy` - ctx.get('spillStore') 存溢出
