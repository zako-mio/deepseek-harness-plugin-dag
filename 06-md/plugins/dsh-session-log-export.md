# dsh-session-log-export

- 包名: `@deepseek-ai/dsh-session-log-export`
- 分组: G25 宿主服务
- 拓扑层: Layer 8
- 来源层: L2 web-app
- 源码路径: `packages/session-query/session-log-export`

## 实现逻辑
宿主侧（src/index.ts）在 commands 注册表注册 /export 命令（无路径参数，返回 success 提示）；同包浏览器侧（src/client）provide sessionLogDownload controller，订阅 command/executed 触发下载 /api/session.export，注入 conversation.session.header.utilities slot 挂共享下载对话框，locale 注册。

## Provides
- /export 人类命令（宿主）
- sessionLogDownload controller（浏览器）
- conversation.session.header.utilities slot 条目

## Depends On (上游依赖)
- `dsh-client-ui-slots` [运行时依赖] - inject ['slots','locale']；slots.inject 头部工具槽
  - 证据: `packages/session-query/session-log-export/src/client/index.ts:26,40-49`
- `dsh-commands` [编译依赖] - CommandResult 类型
  - 证据: `packages/session-query/session-log-export/src/index.ts:4`
- `dsh-host-apiproxy` [运行时依赖] - 浏览器下载控制器 fetch /api/session.export，由网关 downloads.sessionLog 端点服务
  - 证据: `packages/session-query/session-log-export/src/client/controller.ts:114; packages/host/apiproxy/src/api-proxy.ts:3639-3644`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
