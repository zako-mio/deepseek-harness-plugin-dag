# dsh-client-ui-reference

- 包名: `@deepseek-ai/dsh-client-ui-reference`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-reference`

## 实现逻辑
注册一个 '@' 输入触发源：候选阶段先确保目标 Session 已 retain 且历史 open，再并行发起 fileReferences.list 与 sessionReferenceResolver.candidates（src/client/index.ts:60-76），失败通道降级为空集；随后分别映射文件候选（含目录 drill 语义与父目录描述，index.ts:212-242）与会话候选（区分子会话/普通会话并附工作区与相对时间，index.ts:244-260）。onPick 把候选 value 反解为 file/session：文件返回可插入引用文本，目录在 drill 动作下保留继续下钻（index.ts:96-135）；openReference 则经 sidebarRight.openResource 打开文件地址（index.ts:143-151）。最后经 inputTriggers.registerSource 挂载（index.ts:158）。

## Provides
- ctx.inputTriggers 的 '@' 参考源（@文件 / @会话统一候选、分组、相对时间与工作区标签）
- 目录下钻的面包屑 header 与 drill 继续语义
- 参考插入/剪贴板序列化 codec 与文件引用在右侧栏打开（openReference）

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 文件与会话候选的 Remote 查询
  - 证据: `src/client/index.ts:17 import type + src/client/index.ts:71 ctx.remote.fileReferences.list`
- `dsh-api-session-controller` [E1+E2] - retain 会话并用 using() 挂参考候选数据源
  - 证据: `src/client/index.ts:11 import type { ISessions } + src/client/index.ts:53 ctx.get('sessions')`
- `dsh-client-locale` [运行时依赖] - 注册 reference 文案
  - 证据: `src/client/index.ts:19 import type + src/client/index.ts:51 ctx.locale.register(NS)`
- `dsh-client-ui-input-trigger` [E1+E2] - 注册 '@' 触发源并消费其 Source/Crumb 契约
  - 证据: `src/client/index.ts:26 import type + src/client/index.ts:158 inputTriggers.registerSource`
- `dsh-client-ui-primitives` [编译依赖] - 会话候选相对时间展示
  - 证据: `src/client/index.ts:23 import { relativeTime }`
- `dsh-client-ui-sidebar-right` [E1+E2] - 在右侧栏打开被引用的文件
  - 证据: `src/client/index.ts:20 import type + src/client/index.ts:149 ctx.sidebarRight.openResource`
- `dsh-session-reference` [编译依赖] - 会话引用候选类型
  - 证据: `src/client/index.ts:29 import type`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
