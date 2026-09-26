# dsh-spill-policy

- 包名: `@deepseek-ai/dsh-spill-policy`
- 分组: G38 溢出存储
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/spill/spill-policy`

## 实现逻辑
为工具结果与 PTC dispatch 日志挂载 token 预算保留策略：命中 tools/post-execute 与 tools/ptc-dispatch-log 时，若内容估算 token 超过 maxInlineTokens，则把完整文本（含图像附件可读路径）经 ctx.spillStore.saveText 落盘，再用 retainContent 保留头尾并按预算裁剪，末尾追加带 locator 与检索提示的省略通知 (src/index.ts:91-155, src/retention.ts:48-104, src/notice.ts:21-24)。图像定价缺失或保存失败时捕获异常并保持原始内联内容不改 (src/index.ts:56-75, src/index.ts:127-130)。

## Provides

## Depends On (上游依赖)
- `dsh-llm` [E1+E2] - 按当前模型路由估算图像 token 定价，并构造 PTC 图像结果的 additionalContexts 用户消息 (src/index.ts:144)
  - 证据: `package.json:35 peerDep + src/index.ts:10-11 import + src/index.ts:65 ctx.get('llm').imageRequestPricing`
- `dsh-session` [编译依赖] - 溢出归属 session id 的类型来源 (src/types.ts:16-25)
  - 证据: `package.json:37 peerDep + src/types.ts:13 import type`
- `dsh-token-meter` [编译依赖] - 用 estimateContent 估算文本/内容 token 以决定溢出并计算头尾保留预算
  - 证据: `package.json:43 peerDep + src/index.ts:12 import`
- `dsh-tools` [E1+E2] - 挂载工具结果后处理与 PTC dispatch 日志的 token 保留策略
  - 证据: `package.json:39 peerDep + src/index.ts:14 import type + src/index.ts:33 inject['tools'] + src/index.ts:133,152 events`

## Dependents (下游被依赖)
- `dsh-client-ui-tool` - 渲染输出溢出/截断提示 notice
