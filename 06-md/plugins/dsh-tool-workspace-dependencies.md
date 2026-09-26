# dsh-tool-workspace-dependencies

- 包名: `@deepseek-ai/dsh-tool-workspace-dependencies`
- 分组: G37 技能
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/skill/tool-workspace-dependencies`

## 实现逻辑
注册只读工具 load_workspace_dependencies：校验 payload 的 runtime.json（parsePrimaryRuntime 把 legacy components 格式归一化为顶层版本与发行版映射）并返回捆绑 Python/Node/pnpm 的绝对路径与 Python 发行版版本 (src/index.ts:82-156)。配置 root 时经 installPrimaryRuntime 以 staging 复制 + previous 目录回滚实现原子安装，未配置时原地校验使用 (src/index.ts:204-233, src/index.ts:267-274)。

## Provides
- load_workspace_dependencies 工具 (返回捆绑 Python/Node/pnpm 绝对路径与捆绑发行版版本)

## Depends On (上游依赖)
- `dsh-tools` [E1+E2] - 向工具注册表注册其读路径查询工具
  - 证据: `package.json:29 peerDep + src/index.ts:7 import + src/index.ts:12 inject['tools'] + src/index.ts:249 ctx.tools.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
