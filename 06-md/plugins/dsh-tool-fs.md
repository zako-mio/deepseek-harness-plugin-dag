# dsh-tool-fs

- 包名: `@deepseek-ai/dsh-tool-fs`
- 分组: G16 文件系统
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/fs/tool-fs`

## 实现逻辑
注册模型面 read/read_image/write/edit 工具套件：apply() 校验四个读取上限后挂载 read 工具，并用 ctx.inject(['attachments']) 条件注册 read_image（无附件存储时不注册）(src/index.ts:54-72)；写与 edit 共用一个 FsSandboxController 处理升级广告、每调用策略解析与拒绝标记映射 (src/index.ts:76-78)。工具层只声明 schema、校验、读取窗口与格式化，把实际读写交给 ctx.fs (src/index.ts:1-5)。

## Provides
- 工具 read / read_image / write / edit

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 图像以 LLM 可消费的内容部件返回
  - 证据: `src/read-image.ts:18 import`
- `dsh-sandbox-policy` [编译依赖] - 解析每调用沙箱策略并映射拒绝错误
  - 证据: `src/sandbox.ts:17 import`
- `dsh-system-prompt` [运行时依赖] - 向系统提示注入工具使用指引
  - 证据: `src/index.ts:22 inject 'systemPrompt' + src/edit.ts:76 ctx.systemPrompt`
- `dsh-tools` [E1+E2] - 通过工具注册表发布文件系统工具
  - 证据: `src/index.ts:22 inject ['tools','fs','systemPrompt'] + src/read.ts:8 import`
- `dsh-user-approval` [编译依赖] - 沙箱升级等敏感操作走用户审批
  - 证据: `src/index.ts:10 import`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
