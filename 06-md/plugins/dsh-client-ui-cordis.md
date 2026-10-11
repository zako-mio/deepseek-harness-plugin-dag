# dsh-client-ui-cordis

- 包名: `@deepseek-ai/dsh-client-ui-cordis`
- 分组: G14 宿主扩展
- 拓扑层: Layer 12
- 来源层: L2 web-app
- 源码路径: `packages/extensions/ui-cordis`

## 实现逻辑
以「客户端 UI 面 + 远程端口」实现：Host 半边是空 apply，仅让该包出现在 host cordis.yml/Loader 中，浏览器半边经 package.json 的 dsh.client 声明发布 (src/index.ts:8-9)。客户端 apply 注册中英文字典，构造 CordisDynamicPort（stop/remove/inventory 经 ctx.remote.dynamicCordisRunner 调 Host），再用 createCordisInventory 维护帧级定义清单，并订阅 remote 的 cordis/dynamic-package、cordis/dynamic-retract、cordis/request-run、cordis/request-run-resolved 与 connection/reset 以重读或复位 (src/client/index.ts:42-84, src/client/index.ts:45-62)。随后向 ctx.slots 注入 sidebar.footer.action 的 cordis-panel 面板，以及 tool.call.toolview 的 cordis_define/cordis_run/cordis_stop/cordis_undefine 四种卡片，把批准/运行/停止/移除动作接到 ctx.dynamicCordisRunner 与端口 (src/client/index.ts:86-147)。

## Provides
- ctx.slots (注册 sidebar.footer.action 的 cordis-panel 面板，以及 tool.call.toolview 下 cordis_define/cordis_run/cordis_stop/cordis_undefine 四个键控卡片)
- ctx.locale (注册 ui-cordis 命名空间的中英文字典)

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 经 Remote 组装体调用 Host 侧 stop/remove/inventory，并订阅转发过来的 cordis/* 事件
  - 证据: `src/client/CordisPanel.tsx:13 import .../client + src/client/events.ts:4 type import + src/client/index.ts:47/53/58 ctx.remote.dynamicCordisRunner`
- `dsh-client-locale` [E1+E2] - 注册 ui-cordis 命名空间的中英文字典，供面板与卡片取文案
  - 证据: `src/client/index.ts:6 type import + src/client/index.ts:43 ctx.locale.register`
- `dsh-client-ui-primitives` [编译依赖] - 复用客户端基础 UI 原语渲染准备中卡片
  - 证据: `src/client/CordisPreparingRow.tsx:3 import + package.json:57 devDep`
- `dsh-client-ui-renderer` [编译依赖] - 声明渲染面类型，保证本包插件的客户端渲染接缝类型完整
  - 证据: `src/client/index.ts:9 type import + package.json:59 devDep`
- `dsh-client-ui-session` [编译依赖] - 声明会话 UI 面类型，使卡片能落在会话视图上下文
  - 证据: `src/client/index.ts:10 type import + package.json:60 devDep`
- `dsh-client-ui-sidebar` [编译依赖] - 把 Cordis 面板挂到侧边栏底部动作位
  - 证据: `src/client/CordisPanel.tsx:11 import .../client + src/client/index.ts:7 type import + src/client/index.ts:86 注册 sidebar.footer.action`
- `dsh-client-ui-tool` [编译依赖] - 复用工具卡片行组件契约与 toolview 注入协议，渲染 cordis_* 工具调用
  - 证据: `src/client/CordisDefineRow.tsx:8 import .../client + src/client/CordisRunRow.tsx:8 + src/client/index.ts:5 type import`
- `dsh-cordis-client-runner` [E1+E2] - 读取浏览器侧动态包的加载状态与活动运行，并把面板上的批准/运行/停止动作委托给运行面
  - 证据: `src/client/CordisPanel.tsx:12 import .../client + src/client/status.ts:3 import DynamicCordisLivePackage + src/client/index.ts:37-39 inject 'dynamicCordisRunner' + src/client/index.ts:66 ctx.dynamicCordisRunner`
- `dsh-session` [编译依赖] - 为卡片注入函数提供 SessionId 类型，按会话维度保存运行卡片状态
  - 证据: `src/client/index.ts:4 import SessionId + package.json:56 devDep`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
