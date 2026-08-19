# dsh-tool-str-replace-editor

- 包名: `@deepseek-ai/dsh-tool-str-replace-editor`
- 分组: G13 文件系统
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/fs/tool-str-replace-editor`

## 为什么需要它（设计初衷）
独立面向模型的 str_replace_editor 工具（view/create/str_replace/insert）over ctx.fs，可配任意 bash 面。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/fs/tool-str-replace-editor/README.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-tool-str-replace-editor

## 实现逻辑
注册单一 str_replace_editor 工具(view/create/str_replace/insert 四命令):view 经 ctx.fs.readText/listDir 输出 cat -n 风格内容;create/str_replace/insert 经 MutationPolicy 解析 sandboxPolicy、ctx.waterfall 取 fs/write-intent|fs/edit-intent 守卫、writeText 带 replaceIfVersion/createIfAbsent 提交,str_replace 要求 old_str 唯一匹配;denial 映射为 [sandbox:] 标记。

## Provides
- ctx.tools 注册 str_replace_editor
- fs/observed 发射、fs/write-intent|fs/edit-intent 触发

## Depends On (上游依赖)
- `dsh-fs-observation-policy` [运行时依赖] - 写/编辑前守卫与观察记录
  - 证据: `packages/fs/tool-str-replace-editor/src/index.ts:252,284,337`
- `dsh-sandbox-policy` [运行时依赖] - MutationPolicy per-call 模式
  - 证据: `packages/fs/tool-str-replace-editor/src/index.ts:69-72,76`
- `dsh-tools` [运行时依赖] - 工具注册管线
  - 证据: `packages/fs/tool-str-replace-editor/src/index.ts:494,422`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
