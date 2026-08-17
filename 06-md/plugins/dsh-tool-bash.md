# dsh-tool-bash

- 包名: `@deepseek-ai/dsh-tool-bash`
- 分组: G14 Shell工具
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/shell/tool-bash`

## 为什么需要它（设计初衷）
模型侧 bash 工具：注册在 ctx.shell 执行器 seam，前台/后台执行、DSH_* 环境注入、可选沙箱升权与审批流。

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/shell/tool-bash/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/shell

## 实现逻辑
模型面向 bash 工具:apply() 注册 bash 工具,execute 先 validateEscalationArgs、解析 standingPolicy,带 sandbox_permissions 则经 ctx.get('approval') 走 approveEscalation,resolveWorkdir(会话 cwd),收集 ctx.shellEnv.collect 的 DSH_* 环境,前台 ctx.shell.run / 后台 ctx.jobs.start;结果含 sandbox 事实。

## Provides
- ctx.tools 注册 bash
- ctx.jobs 后台任务注册(kind: 'bash')
- ctx.systemPrompt section: tool:bash

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - Agent 类型与 job owner
  - 证据: `packages/shell/tool-bash/src/index.ts:17,149`
- `dsh-sandbox-policy` [运行时依赖] - standing policy 解析
  - 证据: `packages/shell/tool-bash/src/index.ts:194,200`
- `dsh-shell-env` [运行时依赖] - 收集 DSH_* 环境
  - 证据: `packages/shell/tool-bash/src/index.ts:31,341`
- `dsh-tools` [运行时依赖] - 工具注册管线
  - 证据: `packages/shell/tool-bash/src/index.ts:31,242`
- `dsh-user-approval` [运行时依赖] - 升级批准通道
  - 证据: `packages/shell/tool-bash/src/index.ts:226`

## Dependents (下游被依赖)
- `dsh-agent-spine-demo` - 可选 ctx.plugin(toolBash) 模型面 bash 工具
