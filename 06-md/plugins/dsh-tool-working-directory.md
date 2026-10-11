# dsh-tool-working-directory

- 包名: `@deepseek-ai/dsh-tool-working-directory`
- 分组: G31 会话核心
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/session/tool-working-directory`

## 实现逻辑
把工作目录读写注册成模型工具：apply 通过 ctx.tools.register(defineTool({...})) 定义 working_directory，参数只有可选 cd，输出为 { cwd } 并渲染为文本 (src/index.ts:19-41)。execute 要求 exec.agent 存在，cd 缺省时调 ctx.workingDirectory.ensure(agent, signal) 读取（目录消失时会恢复），提供时调 set 切换，二者都把 exec.signal 透传以支持取消 (src/index.ts:34-40)。插件声明 inject ['tools','workingDirectory']，只在两个服务都可用时激活 (src/index.ts:13)。

## Provides
- tools 注册项 working_directory (读取或切换当前会话工作目录的模型工具)

## Depends On (上游依赖)
- `dsh-tools` [E1+E2] - 把工具定义注册进工具注册表
  - 证据: `package.json:31 peerDep + src/index.ts:7 import defineTool；src/index.ts:20 ctx.tools.register`
- `dsh-working-directory` [E1+E2+E3] - 读写会话有效工作目录并在缺失时恢复
  - 证据: `package.json:32 peerDep + src/index.ts:8 import type {}；src/index.ts:13 inject 'workingDirectory'、src/index.ts:37-38 ctx.workingDirectory.ensure/set；packages/bundle/base/cordis.patch.yml:161-165 装配顺序`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
