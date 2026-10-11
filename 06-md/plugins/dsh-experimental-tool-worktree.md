# dsh-experimental-tool-worktree

- 包名: `@deepseek-ai/dsh-experimental-tool-worktree`
- 分组: G13 实验特性
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/experimental/tool-worktree`

## 实现逻辑
函数式插件，注册模型工具 create_worktree：从本地 commit/branch/tag（默认 HEAD）创建新分支与 git worktree，并把当前会话的工作目录切到新 checkout，未提交文件留在原 checkout (src/index.ts:16-43)。工具输出声明 path/branch/baseCommit/repositoryRoot 四个必填字段，并给出 generic 卡片的展示声明；执行体只做调用方检查后把工作交给 ctx.worktrees.create(agent, args, signal) (src/index.ts:24-41)。

## Provides
- create_worktree 工具 (经 ctx.worktrees 创建 git worktree 并切换会话工作目录)

## Depends On (上游依赖)
- `dsh-tools` [E1+E2] - 工具定义与注册由 tools seam 提供
  - 证据: `src/index.ts:5 import { defineTool } from '@deepseek-ai/dsh-tools' + src/index.ts:17 ctx.tools.register(defineTool({...})) + package.json:36 peerDep`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
