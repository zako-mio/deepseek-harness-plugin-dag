# dsh-code-runtime-python

- 包名: `@deepseek-ai/dsh-code-runtime-python`
- 分组: G39 代码执行运行时
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/code-runtime/code-runtime-python`

## 为什么需要它（设计初衷）
为代码执行seam提供资源受限、精确无损JSON的CPython子进程后端，与现有worker-thread后端互为可选实现，满足需要真实Python解释器环境的场景。

发展史：RC8 新增

## 实现逻辑
CPython子进程代码执行运行时，实现 code-execution seam 的Python后端。src/index.ts:11-19 再导出 fd-3 线上协议；protocol.ts:18 PROTOCOL_FD=3 定义子进程专用控制通道fd，stdout/stderr留给程序自身输出。协议含 boot(资源限制RLIMIT_CPU/RLIMIT_AS)、run、boot-ack、call(桥接工具调用)、log(流式日志含truncated)、done 帧，host将每帧视为敌意并validateChildFrame。py/protocol.py 为Python端镜像。为库/后端包，未装配进bundle，经dsh-tools的Code Mode间接生效。

## Provides
- code-execution seam的CPython子进程实现
- fd-3版本无关JSON-lines线上协议codec与敌意帧校验
- 跨语言协议镜像(TS↔Python)

## Depends On (上游依赖)
- `dsh-tools` [运行时依赖] - 通过Code Mode暴露执行能力
  - 证据: `README.zh.md:20 经dsh-tools Code Mode间接生效`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
