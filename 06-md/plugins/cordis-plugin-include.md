# cordis-plugin-include

- 包名: `@deepseek-ai/cordis-plugin-include`
- 分组: G45 框架 vendor
- 拓扑层: Layer 1
- 来源层: L3 其余
- 源码路径: `vendor/include`

## 实现逻辑
文件支持的 Loader 子树：Include 继承 EntryTree（src/index.ts:159），从 ctx.baseUrl 解析 YAML/JSON 入口清单，应用 patch（src/index.ts:57-127），并支持写回与热重载（src/index.ts:279-287, 289-334）。entryListSchema 承载 !!js 表达式的 YAML 方言，供配置工具与挂载共用（src/index.ts:9-23）。

## Provides
- Include 插件（文件支持的 Loader 子树 EntryTree，src/index.ts:159）
- entryListSchema（支持 !!js 表达式的 YAML 方言，src/index.ts:23）

## Depends On (上游依赖)
- `cordis-plugin-loader` [E1+E2] - 继承 EntryTree/EntryGroup 并注入 loader 写入挂载结果
  - 证据: `package.json:33 peerDep + src/index.ts:1 import EntryGroup/EntryTree + src/index.ts:160 static inject=['loader']`

## Dependents (下游被依赖)
- `dsh-agent-preset-registry` - 以 Loader 自身的 entry-list YAML 方言导出声明，使 !!js 条件按声明原样呈现
- `dsh-config-editor` - 解析 profile 补丁条目表并识别 include 归属
- `dsh-hmr` - 对 include 树做局部刷新而非整体重启
- `dsh-plugin-manager` - 读写 profile 补丁的条目与插入语义
