# dsh-spill-policy

- 包名: `@deepseek-ai/dsh-spill-policy`
- 分组: G21 上下文治理
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/spill/spill-policy`

## 为什么需要它（设计初衷）
工具结果 spill 策略：tools/post-execute 转换器，超过 maxInlineBytes 的纯文本结果保存到 spillStore 并替换为有界首尾预览+取回指引。

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/spill/spill-policy/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/notes/implemented/architecture/2026-07-08-tool-output-spill-files.md

## 实现逻辑
纯 apply(ctx, config) 函数插件，inject=['tools']，Config 仅 maxInlineBytes(省略则 no-op)。注册 tools/post-execute prepend 监听：对 accept 且纯文本且超限的顶层结果，spillReplacement 经 ctx.get('spillStore').saveText 存全量文本，用 TextRetainer 做 head/tail 预算内预览 + spillNotice 定位行；第二臂 tools/code-dispatch-log prepend 对 tool/code-dispatch 子调用做相同 cap。

## Provides
- tools/post-execute prepend 结果溢出转存
- tools/code-dispatch-log prepend 日志溢出转存

## Depends On (上游依赖)
- `dsh-session` [组合依赖] - SessionId 类型
  - 证据: `packages/spill/spill-policy/src/index.ts:52`
- `dsh-spill-local` [编译依赖] - ctx.get('spillStore') 存溢出
  - 证据: `packages/spill/spill-policy/src/index.ts:142-155`
- `dsh-tools` [运行时依赖] - 订阅 tools/post-execute waterfall
  - 证据: `packages/spill/spill-policy/src/index.ts:190,217`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
