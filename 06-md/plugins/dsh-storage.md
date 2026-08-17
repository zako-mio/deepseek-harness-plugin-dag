# dsh-storage

- 包名: `@deepseek-ai/dsh-storage`
- 分组: G25 宿主服务
- 拓扑层: Layer 0
- 来源层: L2 web-app
- 源码路径: `packages/storage/storage`

## 为什么需要它（设计初衷）
解决非会话数据（设置/工作区/领域 KV）的统一持久化枢纽问题：ctx.storage 作为后端注册表 + 数据形态(data-form)挂载点，自身不做 IO，后端各自拥有媒介（json/sqlite），数据形态拥有语义（如 domain 领域层），使持久化后端可插拔且可并存。

发展史：定位为存储枢纽（storage hub）。设计依据见 2026-07-24 的 domain-KV-storage-and-workspace Agent Note。当前仅支持 kv 数据形态，forms 惰性解析。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/storage/storage/README.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-storage

## 实现逻辑
存储中枢 ctx.storage：Storage 服务 = 命名后端注册表 BackendRegistry + 可挂载数据形式（StorageForms 接口声明合并扩展）。本身不做 IO；storageBackendServiceKey(name) 生成后端生命周期服务键；domain getter 读取挂载的 domain 形式。default export 服务类（非函数插件）。

## Provides
- ctx.storage（Storage：backend 注册表 + mount/form 数据形式）
- storageBackendServiceKey(name) 服务键生成器

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-storage-domain` - storageBackendServiceKey 与 StorageForms 声明合并
- `dsh-storage-json` - 注册到 hub 后端注册表并取 storageBackendServiceKey
- `dsh-storage-sqlite` - 存储中枢：后端注册表 + 服务键提供
