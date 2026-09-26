# cordis-plugin-loader

- 包名: `@deepseek-ai/cordis-plugin-loader`
- 分组: G46 框架 vendor
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `vendor/loader`

## 实现逻辑
cordis 插件加载器：Loader 继承 EntryTree（src/index.ts:77），持有 entry 树与模块导入器，负责导入配置插件、解析 inject、处理自卸载与热更新写回（src/index.ts:129-166）。它注册 loader 服务并声明 exit 与 loader/* 事件（src/index.ts:23-55, 102）。

## Provides
- ctx.loader（插件加载器：entry 树、插件导入与热更新，src/index.ts:77/102）
- 事件 loader/config-update、loader/entry-init、loader/partial-dispose、loader/volatile-update、loader/patch-context、exit（src/index.ts:23-42）

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `cordis-plugin-group` - 复用 Loader 的 Group 实现
- `cordis-plugin-include` - 继承 EntryTree/EntryGroup 并注入 loader 写入挂载结果
- `dsh-agent-preset` - 借用 EntryGroup 语义保留声明式子插件表达式
- `dsh-agent-preset-registry` - 挂载、审计并定位预设的 Loader entry 树
- `dsh-client-modules` - 以 Loader 行为输入扫描 dsh.client 声明并解析包真实位置
- `dsh-client-web` - 在浏览器端挂载 Loader 并逐行激活客户端插件
- `dsh-config-editor` - 读取 loader.entries() 定位可编辑行，并在写盘后走正常 Loader 重载路径
- `dsh-cordis-client-runner` - 把求值后的动态包注册为 loader entry 并管理其生命周期
- `dsh-hmr` - 经 loader.internal 访问 Node ModuleLoader(loadCache)并重建插件 fiber
- `dsh-plugin-manager` - 读取活动 Loader 行以判定可寻址性与 bundle 贡献是否在用
- `dsh-tool-cordis` - Config provider 遍历 Loader entry 树并解析条目
- `dsh-typert-loader` - 观察 Loader entry 生命周期并定位包
