# dsh-api-account-controller

- 包名: `@deepseek-ai/dsh-api-account-controller`
- 分组: G02 API 网关与控制器
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/api/account-controller`

## 实现逻辑
AccountController 继承 TypertRemoteService，构造时以 namespace 'account' 注册并静态注入 deepseekAccount/agents (src/index.ts:10-13)。它把账号 seam 的读写几乎原样暴露为 @Remote 方法：getState/getProfile/getBalance/getUnnotifiedBonuses/ackBonusNotified/startSignIn/cancelSignIn/signOut (src/index.ts:18-90)，并有 hasRunningAccountTasks 经 ctx.agents.list() 过滤正在运行的账号任务 (src/index.ts:80-83)。两个 @Remote({mode:'stream'}) 方法提供重连安全状态流：watch 直通 deepseekAccount.watch，watchExpiry 订阅 deepseek-account/session-expired 事件并用 pending 计数去重产出 (src/index.ts:96-119)。

## Provides
- ctx.remote.account（account 命名空间 Remote：账号状态/资料/余额/奖励读取与确认、浏览器登录启停、登出、运行任务探测、状态与凭证过期流）

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - 枚举运行中的 Agent 以判断账号任务
  - 证据: `src/index.ts:5 import type {} + src/index.ts:82 ctx.agents.list()`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配 account 命名空间
