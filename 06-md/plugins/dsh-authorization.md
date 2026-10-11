# dsh-authorization

- 包名: `@deepseek-ai/dsh-authorization`
- 分组: G10 凭据与授权
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/credentials/authorization`

## 实现逻辑
以 Cordis Service 形式实现 `ctx.authorization` 授权 seam：维护 CredentialKey 到 AuthorizationFlow 的注册表与 CredentialKey 到在飞尝试的表，registerFlow() 用 ctx.effect 保证卸载时注销并取消在飞尝试 (src/index.ts:209-225)。begin() 先做 key/方法/并发校验，再运行 flow，并强制「本次尝试内必须真的提交过凭据记录」的契约——未观察到提交或记录被删除都抛 NOT_COMMITTED (src/index.ts:283-323, src/index.ts:435-446)。提交经 ctx.credentials.modifyRecord 完成，并通过监听 credentials/record-updated 确认提交发生在本尝试之内 (src/index.ts:386-400)。结束后以 contained-dispatch 方式扇出 authorization/settled 事件，监听器异常只记日志、不改变调用方结果 (src/index.ts:337-351)。

## Provides
- ctx.authorization (凭据获取流的注册、单次授权尝试编排与取消的 seam)
- authorization/settled 事件 (emit 模式，报告每次尝试终态，含 failed)
- AuthorizationError / AuthorizationDeclinedError 错误分类

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 授权错误继承 HarnessError，复用统一的错误分类与展示
  - 证据: `src/index.ts:31 import { HarnessError } from '@deepseek-ai/dsh-llm' + package.json:36 peerDep`

## Dependents (下游被依赖)
- `dsh-deepseek-account-platform` - 登录流程以 authorization flow 形式注册，取消与单飞语义由该 seam 保证
- `dsh-llm-pi-ai` - 为 pi-ai 提供方注册交互式登录流程
