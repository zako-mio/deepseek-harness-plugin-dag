# dsh-client-ui-reference

- 包名: `@deepseek-ai/dsh-client-ui-reference`
- 分组: G27 会话交互UI
- 拓扑层: Layer 13
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-reference`

## 为什么需要它（设计初衷）
将Web端@file与@session引用统一为单一输入触发源，合并原分散的引用逻辑，保证文件与会话候选顺序确定、标签统一。

发展史：RC8 新增

## 实现逻辑
纯浏览器UI插件。浏览器半 src/client/index.ts:30 注册本地化字典并构造 InputTriggerSource：trigger='@'，candidates 并行调用 ctx.remote.fileReferences.list 与 ctx.remote.sessionReferenceResolver.candidates 合并文件与会话候选，onPick 按kind返回file/session插入内容。文件候选经 file-reference/grammar 的 formatFileMention 格式化@mention；最终 ctx.effect 调用 inputTriggers.registerSource 注册统一@源。装配于 cordis.patch.yml:254-255(E3)。

## Provides
- ctx.inputTriggers 统一@菜单源(同时含@file与@session候选)
- 文件/会话mention格式化(引用file-reference/grammar)
- 本地化字典(zh/en)

## Depends On (上游依赖)
- `dsh-api-remotes` [运行时依赖] - 远程文件/会话引用发现namespace
  - 证据: `src/client/index.ts:23 inject remote; :38-44 ctx.remote.fileReferences`
- `dsh-client-locale` [运行时依赖] - 本地化字典服务
  - 证据: `src/client/index.ts:31 ctx.locale.register`
- `dsh-client-runtime` [运行时依赖] - 提供ctx根上下文
  - 证据: `src/client/index.ts:12 ClientContext`
- `dsh-client-ui-input-trigger` [运行时依赖] - 注册@触发源所需服务
  - 证据: `src/client/index.ts:88-89 inputTriggers.registerSource`
- `dsh-file-reference` [编译依赖] - 复用@file语法与候选类型
  - 证据: `src/client/index.ts:16-17 import formatFileMention`
- `dsh-session-reference` [编译依赖] - 会话引用候选类型contract
  - 证据: `src/client/index.ts:18 SessionReferenceMentionCandidate`

## Dependents (下游被依赖)
- `dsh-web-app` - web-app装配@引用UI
