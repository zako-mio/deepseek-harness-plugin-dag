# dsh-client-product-analytics

- 包名: `@deepseek-ai/dsh-client-product-analytics`
- 分组: G05 客户端运行时
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/client/product-analytics`

## 实现逻辑
Host 半 ProductAnalytics（TypertRemoteService）只负责已认证的事件接收：按 config.enabled 判断是否采集，把事件补上设备/用户/版本属性后交给 ctx.productTelemetry.emit（src/index.ts:28-100），并用 @Remote 暴露 enabled/report 与 watchPolicy 流（src/index.ts:50-74）。浏览器半 DesktopAnalytics 只在桌面环境（globalThis.dshDesktop）订阅策略流并转发 track 事件，缺失或断连的 Remote 不打断交互（src/client/index.ts:14-53）。

## Provides
- ctx.productAnalytics (Host 事件采集策略与上报入口；浏览器端 track/enabled 发送面)

## Depends On (上游依赖)
- `cordis-plugin-loader` [E1+E2] - 配置热更新时通知策略订阅者
  - 证据: `src/index.ts:8 import type + src/index.ts:37 ctx.on('loader/volatile-update')`
- `dsh-api-gateway` [编译依赖] - 浏览器端 Remote 调用与流承载
  - 证据: `src/client/index.ts:3 import type`
- `dsh-host-product-telemetry-otel` [E1+E2] - 把产品事件交给 OTel 遥测出口
  - 证据: `src/index.ts:5 import type + src/index.ts:29 static inject ['productTelemetry'] + src/index.ts:87 ctx.productTelemetry.emit`
- `dsh-llm` [编译依赖] - 事件属性中的模型标识类型
  - 证据: `src/events.ts:3 import`
- `dsh-session` [E1+E2] - 订阅 compaction/start 上报上下文压缩事件
  - 证据: `src/index.ts:9 import type + src/index.ts:39 ctx.on('session/event')`
- `dsh-settings` [E1+E2] - 关闭该服务的自动设置文档
  - 证据: `src/index.ts:7 import type + src/index.ts:38 ctx.inject(['settings'])`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 把该业务包的 /remote 命名空间装配进 Client
- `dsh-client-ui-chat` - 分支会话等交互埋点
- `dsh-client-ui-conversation` - 提交行为埋点
- `dsh-client-ui-model-selection` - 模型切换埋点
- `dsh-client-ui-plugin-manager` - 插件管理操作埋点
- `dsh-client-ui-settings-account` - 引导各步与配额通知上报产品分析事件（可选服务用 ctx.get 读取）
- `dsh-client-ui-settings-models` - 引导对话框上报产品分析事件（可选服务经 ctx.get 读取）
- `dsh-client-ui-sidebar` - 面板切换时上报产品分析事件（可选服务用 ctx.get 读取，不写进 inject）
- `dsh-client-ui-workspace` - 拉入产品分析客户端的 Context 合并以记录会话动作
