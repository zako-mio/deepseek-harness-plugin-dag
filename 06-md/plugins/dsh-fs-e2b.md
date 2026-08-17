# dsh-fs-e2b

- 包名: `@deepseek-ai/dsh-fs-e2b`
- 分组: G30 外部执行后端
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/e2b/fs-e2b`

## 为什么需要它（设计初衷）
E2B 云沙箱的 ctx.fs provider 实现：让文件工具观察与 E2B 支撑的 Bash 进程同一执行世界（远端 cwd + SDK handle），支持远端身份/元数据、UTF-8 流读、有界原始字节读、原子变更（staging 目录 + 同文件系统原子 rename）。解决'无头 Agent 如何操作远端沙箱文件系统'的问题，使文件工具整体随 provider 切换迁移到远端。

发展史：dsh 的 fs provider 可替换接缝的远端实现，POC 性质（依赖 E2B 默认 Linux 镜像的 realpath/base64/atomic rename），明确不做 Host 工作区同步。与 fs-local 并列验证 seam 一处切换全线迁移的架构主张。版本 0.1.0-rc.5。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/e2b/fs-e2b/README.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/e2b/fs-e2b/package.json

## 实现逻辑
E2BFileSystem extends FileSystem seam (src/index.ts:171), static inject ['e2b'] (:172) pulls ctx.e2b sandbox; 所有 fs 操作(resolve/read/write/edit/list/stat) 经 sandbox.files/sandbox.commands 执行，canonicalPath 用 realpath+base64 传输 (:443-454)，写入走 staging 目录+原子 rename/guarded ln 发布 (:510-579)，per-targetKey 锁 (:431-441)，版本用 entry 事实 sha256 (:122-133)，含 CRLF/二进制检测。

## Provides
- ctx.fs (FileSystem seam 的 E2B 远程后端，E2BFileSystem extends FileSystem)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
