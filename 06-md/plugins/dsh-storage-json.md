# dsh-storage-json

- 包名: `@deepseek-ai/dsh-storage-json`
- 分组: G25 宿主服务
- 拓扑层: Layer 1
- 来源层: L2 web-app
- 源码路径: `packages/storage/storage-json`

## 为什么需要它（设计初衷）
存储中心 JSON 后端：每个单元一个可读 `<unit>.json` 文件、整文件原子替换发布，可读性是存在理由，扩展交给 SQLite 后端。

来源：
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/storage/storage-json
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/storage

## 实现逻辑
JSON 文件后端：每 unit 一个 <root>/<unit>.json，原子整文件重写（atomic.ts），只提供 kv facet；apply 在 storage 中枢 ctx.storage.backend.register('json') 注册后端，并 ctx.provide(storageBackendServiceKey('json')) 供 domain 层注入等待激活；root 无默认值。

## Provides
- storage.backend.json 后端（kv facet）
- storage.backend.json 服务键

## Depends On (上游依赖)
- `dsh-storage` [编译依赖] - 注册到 hub 后端注册表并取 storageBackendServiceKey
  - 证据: `packages/storage/storage-json/package.json:36; src/index.ts:12-13`

## Dependents (下游被依赖)
- `dsh-storage-domain` - config backend: json → 经 hub 解析 'json' 后端（E2 解析）
- `dsh-storage-sqlite` - 后端注册模式参照：与 json 后端并列的 kv facet 后端实现
