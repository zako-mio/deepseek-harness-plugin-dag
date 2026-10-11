# dsh-settings

- 包名: `@deepseek-ai/dsh-settings`
- 分组: G33 设置
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/settings/settings`

## 实现逻辑
提供 ctx.settings（SettingsForms 服务），把已激活插件条目的 schemastery Config 投影为可编辑表单并按 namespace 读写 profile patch (src/index.ts:222-429)。describe() 计算 value/base/user 三层、维护 revision 并在变化时 emit settings/document-updated，update/replace/mutate 以 JSON 净化 + 分层合并写回，revision 不符抛 SettingsConflictError (src/index.ts:302-423)。redact.ts 按 schema 的 role('secret') 结构式剥离敏感字段并记录已设置槽位，schema.ts 负责 plainConfig/projectForm/volatileForm 投影 (src/redact.ts:106-116, src/schema.ts:10-79)。启动时另把遗留 settings.yaml 一次性导入当前 profile (src/index.ts:241-258)。

## Provides
- ctx.settings (SettingsForms：插件 Config schema → 可编辑表单投影与 profile patch 写回，含 secret 脱敏与 revision 冲突检测)

## Depends On (上游依赖)
- `dsh-config-editor` [E1+E2] - 通过配置编辑器枚举 profile 条目并对其原始文档执行 edit/写回
  - 证据: `src/index.ts:9 import type {}; src/index.ts:224 static inject ['configEditor']; src/index.ts:292 ctx.configEditor.documentPath`

## Dependents (下游被依赖)
- `dsh-agent-default-model` - 关闭 settings 自动模式并使默认模型从 settings 读取
- `dsh-agent-preset-registry` - 把 preset 定义排除在自动设置持久化之外
- `dsh-api-remotes` - 导出设置命名空间视图词汇
- `dsh-api-session-controller` - 读取模型目录相关设置声明
- `dsh-api-settings-controller` - 设置 seam：describe/update/replace/mutate/prepareDocument
- `dsh-client-locale` - 声明 locale 命名空间的 settings 配置面（auto:false）
- `dsh-client-product-analytics` - 关闭该服务的自动设置文档
- `dsh-client-ui-chat` - 关闭该服务的自动设置文档
- `dsh-client-ui-conversation` - 关闭该服务的自动设置文档
- `dsh-client-ui-settings` - 设置命名空间与 wire 类型
- `dsh-client-ui-settings-account` - 把本插件的 Config 以 auto:false 显式登记进 settings 服务，交由浏览器半经配置表单读取
- `dsh-client-ui-settings-general` - Host 半把欢迎提示版本这一偏好登记进 settings 服务，供浏览器半经配置表单读取
- `dsh-client-ui-theme` - Host 侧把主题偏好登记为不可自动生成设置的字段
- `dsh-experimental-client-ui-cot-translation` - 翻译偏好是设置文档的一部分，并声明部署值为权威
- `dsh-llm-pi-ai` - 把 provider profile 暴露为 llm-pi-ai 设置段供界面编辑
- `dsh-permission-presets` - 把 defaultPreset 作为用户设置项写入 settings 命名空间
