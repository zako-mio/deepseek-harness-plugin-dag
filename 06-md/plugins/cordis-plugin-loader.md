# cordis-plugin-loader

- 包名: `@deepseek-ai/cordis-plugin-loader`
- 分组: G45 框架 vendor
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `vendor/loader`

## 实现逻辑
Loader extends EntryTree 以 'loader' 名注册 ctx.loader，持有 entry 树（Entry/EntryGroup）、隔离 realm 与模块加载器，负责按配置导入插件并管理其 fiber 生命周期 (src/index.ts:77-102, src/config/tree.ts:7-20, src/config/entry.ts:43-59)。构造时挂三个全局钩子：internal/config 上对非树载体 entry 的配置做 !!js 表达式插值，internal/update 上把运行时配置 simplify 后回写配置树，internal/plugin 上依据 entry 归属与 fiber 状态判定自卸载并置 disabled (src/index.ts:104-127, src/index.ts:129-166, src/config/utils.ts:5-22)。配置变更的等价判定走 equalExceptVolatile，只把 schema 声明的 volatile 字段视为相等，不执行表达式或校验器 (src/config/diff.ts:43-45)。internal.ts 按 loader 自身拥有的 module-job API 形状（v1/v2）分类 Node 内部 ESM loader，供 HMR 使用 (src/internal.ts:131-143)。

## Provides
- ctx.loader (插件加载器服务：entry 树与分组、隔离 realm、配置插值与持久化回写、fiber 生命周期与自卸载判定)
- Entry / EntryGroup / Realm / EntryTree 等可复用加载器 API (src/index.ts:10-21 再导出)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `cordis-plugin-group` - 复用 Loader 的 Group 实现
- `cordis-plugin-include` - 继承 EntryTree/EntryGroup 并注入 loader 写入挂载结果
- `dsh-agent-preset` - 借用 EntryGroup 语义保留声明式子插件表达式
- `dsh-agent-preset-registry` - 复用 Loader 的入口树与入口类型来装配并审计 preset 子树
- `dsh-client-modules` - 读取 Loader 条目并接管其 internal 模块系统
- `dsh-client-product-analytics` - 配置热更新时通知策略订阅者
- `dsh-client-web` - 在浏览器端挂载 Loader 并逐行激活客户端插件
- `dsh-config-editor` - 枚举并校验可编辑的 Loader 条目
- `dsh-cordis-client-runner` - 复用 Loader 机制为动态包创建/移除条目，从而获得 inject 门控、fiber 效应清理与状态投影
- `dsh-hmr` - 读取模块加载缓存、重新 import 并重注册插件条目
- `dsh-host-directory-picker-auto` - 把选中的交互以真实 Loader 条目挂载，使客户端界面按普通配置行被发现
- `dsh-llm-deepseek-api-key` - 读取 loader 注入的 fiber 条目 id 作为 settings 命名空间
- `dsh-llm-pi-ai` - 配置热更新事件由 loader 发出，据此重建路由与目录
- `dsh-plugin-manager` - 枚举 Loader 条目以决定哪些插件行可写
- `dsh-plugin-package-inventory-deepseek` - 活跃插件包身份只能从 loader 条目树与 fiber 状态取得
- `dsh-tool-cordis` - 以 Loader 条目类型遍历运行中的插件树，投影每个条目的 Config 状态
- `dsh-typert-loader` - 观察 Loader entry 生命周期并定位包
