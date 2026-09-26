# dsh-settings

- 包名: `@deepseek-ai/dsh-settings`
- 分组: G35 设置
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
- `dsh-agent-preset-registry` - 关闭 settings 自动持久化以自管 selectedDefault
- `dsh-api-remotes` - 设置事件类型声明
- `dsh-api-session-controller` - 设置域参与模型/凭证表面
- `dsh-api-settings-controller` - 设置 seam：describe/update/replace/mutate/prepareDocument
- `dsh-client-locale` - 声明 locale 命名空间的 settings 配置面（auto:false）
- `dsh-client-ui-chat` - 宿主侧投影 Chat 偏好为设置表单字段
- `dsh-client-ui-conversation` - 宿主侧投影 busyEnter 为设置字段
- `dsh-client-ui-settings` - 设置命名空间与 wire 类型
- `dsh-client-ui-settings-account` - Host 侧设置命名空间类型/接口
- `dsh-client-ui-settings-general` - Host 侧把欢迎版本配置挂到 settings 服务
- `dsh-client-ui-theme` - Host 侧设置作用域配置（关闭自动保存）
- `dsh-llm-pi-ai` - 激活 settings 服务声明，使插件可按设置命名空间配置 provider 路由
- `dsh-permission-presets` - 为 defaultPreset 提供用户设置默认值
