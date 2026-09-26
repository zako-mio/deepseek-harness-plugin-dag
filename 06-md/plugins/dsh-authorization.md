# dsh-authorization

- 包名: `@deepseek-ai/dsh-authorization`
- 分组: G10 凭据与授权
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/credentials/authorization`

## 实现逻辑
定义 `ctx.authorization` 能力 seam：`AuthorizationService` 继承 cordis `Service` 并 `static inject=['credentials']`（src/index.ts:189-198），以 `registerFlow()` 按 `CredentialKey` 注册「凭据获取流程」且一个 key 只允许一个 flow（src/index.ts:209-225）。`begin()` 用 `running` Map 保证同一 key 单飞、校验 method 合法性，并把流程屏蔽在一个中立会话（notify/commit/prompt）后执行（src/index.ts:283-323）。seam 只在流程于本次尝试内确实提交了凭据记录后才报 `authorized`（`observed.committed` + `describeRecord`，src/index.ts:392-453），并以容错扇出广播 `authorization/settled`（src/index.ts:338-358）。`invariant.ts` 独立校验 settled 后 key 不再 in-flight（src/invariant.ts:24-37），`types.ts` 给出不含 cordis/service 依赖的 wire 安全类型（src/types.ts:1-91）。

## Provides
- ctx.authorization (凭据授权 seam：注册/列出/取消/执行凭据获取流程，按 key 单飞)
- 事件 authorization/settled (一次授权尝试终态广播，含 failed)

## Depends On (上游依赖)
- `dsh-invariants` [E1+E2] - 注册 single-flight 释放不变式，检测 settled 后 key 残留 in-flight
  - 证据: `src/invariant.ts:7 import InvariantInstaller + src/invariant.ts:14 inject ['invariants'] + src/invariant.ts:45 register`
- `dsh-llm` [编译依赖] - AuthorizationError 复用 HarnessError 稳定错误分类
  - 证据: `src/index.ts:31 import HarnessError`

## Dependents (下游被依赖)
- `dsh-deepseek-account-platform` - 把浏览器 PKCE 登录注册为授权流程并驱动一次尝试
- `dsh-llm-pi-ai` - 把 pi-ai 的登录会话翻译成 harness 中立的通知/提问流程
