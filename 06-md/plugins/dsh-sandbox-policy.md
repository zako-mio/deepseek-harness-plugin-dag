# dsh-sandbox-policy

- 包名: `@deepseek-ai/dsh-sandbox-policy`
- 分组: G15 沙箱执行
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/sandbox/sandbox-policy`

## 实现逻辑
沙箱策略中枢(SandboxPolicyService extends Service,注册 ctx.sandboxPolicy):部署默认模式(read-only fail-safe)+ per-session 解析——resolve({session}) 合并 approved override > 会话 sandbox/mode 事件折叠 > 部署默认;会话级 mode 切换以 setSandboxMode 写 sandbox/mode 日志事件;另经 ctx.inject(['systemPrompt']) 提供 sandbox:policy 动态上下文段落。

## Provides
- ctx.sandboxPolicy 服务
- sandbox/mode 会话事件 + setSandboxMode/effectiveSandboxMode
- ctx.systemPrompt context: sandbox:policy

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 类型依赖
  - 证据: `packages/sandbox/sandbox-policy/src/index.ts:24`
- `dsh-session` [运行时依赖] - 会话事件日志作模式折叠存储
  - 证据: `packages/sandbox/sandbox-policy/src/index.ts:26,139-150; session-mode.ts:70`
- `dsh-system-prompt` [运行时依赖] - 策略投影进运行时上下文
  - 证据: `packages/sandbox/sandbox-policy/src/index.ts:112-123`

## Dependents (下游被依赖)
- `dsh-bash-sandbox` - 默认模式事实
- `dsh-fs-sandbox` - static inject sandboxPolicy;默认模式取自 defaultMode
- `dsh-permission-presets` - sandbox 旋钮写穿
- `dsh-pwsh-sandbox` - 默认模式事实
- `dsh-terminal-bash` - 沙箱模式决策与默认模式
- `dsh-tool-bash` - standing policy 解析
- `dsh-tool-fs` - per-call 策略解析
- `dsh-tool-pwsh` - standing policy
- `dsh-tool-str-replace-editor` - MutationPolicy per-call 模式
