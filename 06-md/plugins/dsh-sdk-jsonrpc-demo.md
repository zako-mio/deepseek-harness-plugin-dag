# dsh-sdk-jsonrpc-demo

- 包名: `@deepseek-ai/dsh-sdk-jsonrpc-demo`
- 分组: G37 示例与框架
- 拓扑层: Layer 7
- 来源层: L3 其余
- 源码路径: `packages/examples/jsonrpc-demo`

## 为什么需要它（设计初衷）
示例 bin（dsh-jsonrpc-agent），引导外部 Cordis 配置启动 stdio JSON-RPC SDK 运行时，演示进程外 SDK 集成方式。

来源：
- https://registry.npmjs.org/@deepseek-ai/dsh-sdk-jsonrpc-demo
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/examples/jsonrpc-demo/README.zh.md

## 实现逻辑
Bin-only 示例应用包：不导出组合插件(index.ts 仅 export {})。runJsonrpcAgent(bareModuleBaseUrl?) 共享进程生命周期：installFailLoud+loadEnv 后按 DSH_CORDIS_CONFIG 环境变量/argv 解析外部 cordis.yml 路径(不存在则报 usage 退出)，经 dsh-app-boot 的 boot() 启动外部配置，并安装 stdin 'end'/SIGTERM/SIGINT 处理器统一 dispose 退出。bin.ts 是通用 dsh-jsonrpc-agent bin(外部配置自带插件包)；packaged-bin.ts 传 import.meta.url 作 bareModuleBaseUrl(闭包运行时装包内解析裸插件)。外部配置决定是否装载 dsh-sdk-jsonrpc-server 服务插件。

## Provides
- dsh-jsonrpc-agent bin(通用 JSON-RPC agent)
- packaged-bin 闭包运行时入口
- runner.ts 共享进程生命周期

## Depends On (上游依赖)
- `dsh-sdk-jsonrpc-server` [编译依赖] - doc 契约：外部配置决定是否装载 dsh-sdk-jsonrpc-server 服务插件(运行时经 cordis.yml 装载)
  - 证据: `packages/examples/jsonrpc-demo/src/index.ts:5`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
