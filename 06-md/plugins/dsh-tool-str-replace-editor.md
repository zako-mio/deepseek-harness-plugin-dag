# dsh-tool-str-replace-editor

- 包名: `@deepseek-ai/dsh-tool-str-replace-editor`
- 分组: G16 文件系统
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/fs/tool-str-replace-editor`

## 实现逻辑
注册模型面 str_replace_editor 工具，支持 view/create/str_replace/insert 四类命令 (src/index.ts:429-430, 20-32)。每次读取或变更后 emit fs/observed 供观察策略记录 presence/absence (src/index.ts:110, 237, 272, 326)；变更前用 ctx.get('sandboxPolicy') 解析每调用策略并把 FS_SANDBOX_DENIED 映射为拒绝标记，构造期在 ctx.fs 受限但缺 sandboxPolicy 时报错 (src/index.ts:71-73, 249-270, 287-324, 364-366)。工具描述与输出经 maybeTruncate 按字符上限截断 (src/index.ts:34-38)。

## Provides
- 工具 str_replace_editor (view / create / str_replace / insert)

## Depends On (上游依赖)
- `dsh-sandbox-policy` [E1+E2] - 解析每调用沙箱策略并映射拒绝错误
  - 证据: `src/index.ts:71 ctx.get('sandboxPolicy') + src/index.ts:14 import`
- `dsh-tools` [E1+E2] - 通过工具注册表发布 str_replace_editor
  - 证据: `src/index.ts:503 inject ['tools','fs'] + src/index.ts:15 defineTool import`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
