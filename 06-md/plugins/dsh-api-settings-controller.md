# dsh-api-settings-controller

- 包名: `@deepseek-ai/dsh-api-settings-controller`
- 分组: G02 API 网关与控制器
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/api/settings-controller`

## 实现逻辑
SettingsController 继承 TypertRemoteService，以 namespace 'settings' 注册，并在构造时把 CredentialsController 作为子插件挂载，两个命名空间即使缺少 provider 也保持注册以便返回可操作的缺失诊断 (src/index.ts:85-89)。describe 以 redactSecrets 读取全部命名空间并逐字段投影成线视图 (src/index.ts:48-60, 97-105)；update/replace/mutate 统一走 write()，串行调用 settings seam 的合并/替换/路径操作，并把 SETTINGS_CONFLICT 分类为 settings/conflict、其余 refusal 归为 settings/rejected (src/index.ts:187-213, 249-268)。openSettingsDocument 先 prepareDocument 再交原生文本编辑器，并把取消映射为 gateway/cancelled (src/index.ts:166-185)。CredentialsController 另以 namespace 'credentials' 暴露批量 describe/set/unset，且任何读路径都不返回密钥值 (src/credentials.ts:67-118)。

## Provides
- ctx.remote.settings（settings 命名空间：describe/update/replace/mutate/openSettingsDocument，读路径强制 redactSecrets）
- ctx.remote.credentials（credentials 命名空间：describe/set/unset，密钥单向写入不回读）

## Depends On (上游依赖)
- `dsh-settings` [运行时依赖] - 设置 seam：describe/update/replace/mutate/prepareDocument
  - 证据: `src/index.ts:14 import type + src/index.ts:217 ctx.get('settings')`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配 settings/credentials 命名空间
