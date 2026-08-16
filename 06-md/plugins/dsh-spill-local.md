# dsh-spill-local

- 包名: `@deepseek-ai/dsh-spill-local`
- 分组: G21 上下文治理
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/spill/spill-local`

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
