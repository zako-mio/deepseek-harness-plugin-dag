# dsh-agent-tool-presentation

- 包名: `@deepseek-ai/dsh-agent-tool-presentation`
- 分组: G36 Hooks工具扩展
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/core/agent-tool-presentation`

## 为什么需要它（设计初衷）
解决「工具注册表无法下沉进 preset」的矛盾：工具的消费者（agent-loop 调度器、apiproxy 的 presenter、各工具插件）全在宿主平面，preset 唯一能拥有的只是这份注册表的呈现方式。该插件作为 agent preset 中一行声明，指定模型看到的工具是 native（全 schema）、code（仅 run_code + 生成 TypeScript SDK）还是 both，使 Code Mode 会话可与 native 会话同进程并存。code 模式同时决定可调用面：注册表把模型直呼其他工具名解析为 UNKNOWN_TOOL，保证通告面与可调用面一致。

发展史：位于 packages/core/agent-tool-presentation，agent 平面呈现选择器，0.1.0-rc.6（2026-08-13）由 @deepseek-ai 发布，2026-08-12 首版 0.0.1-rc.3。强调 mode 必填、每个 agent 只声明一次，第二次声明会被拒绝而非合并。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/core/agent-tool-presentation/README.zh.md
- https://registry.npmjs.org/@deepseek-ai/dsh-agent-tool-presentation

## 实现逻辑
Agent 平面工具呈现选择器：agent preset 携带的一行，声明模型看到的工具形态。name='tool-presentation', inject=['tools']（src/index.ts:28-35）。config.mode 必填（native|code|both, :46-52）：native 立即 ctx.tools.presentAs('native')（:63-64）；code/both 经 ctx.inject(['codeRuntime']) 等待宿主平面 codeRuntime 服务后 presentAs(mode)（:69-71）——未组装运行时的部署会令该行停在 pending，dsh-agent-presets 指名此 id 拒绝挂载。注册表本身留在宿主平面，preset 只能拥有呈现声明。

## Provides
- ctx.tools.presentAs() 呈现声明（native/code/both，per-scope）
- code 模式 codeRuntime 等待挂载语义（pending→audit 拒绝）
- tool-presentation-invariant 伴随插件

## Depends On (上游依赖)
- `dsh-code-runtime-worker-thread` [运行时依赖] - code 模式所需的宿主平面 TypeScript 运行时
  - 证据: `packages/core/agent-tool-presentation/src/index.ts:69 (ctx.inject(['codeRuntime'], ...))`
- `dsh-tools` [编译依赖] - 呈现模式类型
  - 证据: `packages/core/agent-tool-presentation/src/index.ts:23 (ToolPresentationMode 类型); package.json:39 (peerDep)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
