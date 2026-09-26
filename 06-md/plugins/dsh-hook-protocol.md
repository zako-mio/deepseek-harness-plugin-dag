# dsh-hook-protocol

- 包名: `@deepseek-ai/dsh-hook-protocol`
- 分组: G19 Hooks 扩展
- 拓扑层: Layer 3
- 来源层: L3 其余
- 源码路径: `packages/hooks/hook-protocol`

## 实现逻辑
不注册插件的共享协议库：导出方言中立的 matcher 匹配（Claude 字面/正则双模、Codex 全正则）、codec 对退出码与 stdout 的解码、merge 的「最严格优先」结果折叠、runner 经 shell 执行 hook，以及 events/detached 工具（src/index.ts:9-25）。runner.ts 用注入的 shell 执行器运行命令，并把基础设施异常降级为无退出码的非阻断结果（src/runner.ts:67-105）。events.ts 追加成对的 hook/invoked、hook/result 持久事件（src/events.ts:75-103），invariant.ts 校验其配对与 open-turn 边界（src/invariant.ts:31-113）。

## Provides
- hook 协议库 (匹配/解码/合并/执行/持久事件/脱离运行静默) 供各方言桥复用
- hook-protocol-invariant 不变量伴随件 (hook invoked/result 配对与轮次边界校验)

## Depends On (上游依赖)
- `dsh-invariants` [E1+E2] - 注册 hook 事件配对不变量伴随件
  - 证据: `src/invariant.ts:5 import InvariantInstaller + src/invariant.ts:13 inject ['invariants'] + src/invariant.ts:122 ctx.invariants.register`
- `dsh-session` [E1+E2] - 追加 hook/invoked、hook/result 持久会话事件
  - 证据: `src/events.ts:9 import Session + src/events.ts:76 session.append('hook/invoked', ...)`

## Dependents (下游被依赖)
- `dsh-hooks-claude-code` - 复用共享的 hook 执行/解析/合并/持久事件与 matcher 校验
- `dsh-hooks-codex` - 复用共享的 hook 执行/解析/合并/持久事件与 matcher 校验
