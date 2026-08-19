# dsh-file-reference

- 包名: `@deepseek-ai/dsh-file-reference`
- 分组: G21 上下文治理
- 拓扑层: Layer 3
- 来源层: L2 web-app
- 源码路径: `packages/context/file-reference`

## 为什么需要它（设计初衷）
将@file引用发现抽象为host能力seam与共享语法，使terminal/web客户端与本地/远程实现共用同一契约，避免各UI重复实现发现逻辑。

发展史：RC8 新增

## 实现逻辑
文件引用发现seam(抽象基座)，供host侧UI共享。src/index.ts:27 声明 FileReferenceService extends TypertRemoteService，抽象 list 按agent cwd列出确定性候选，remoteExportList 以@Remote('list')装饰器暴露远程face；index.ts:20-24 声明 ctx.fileReferences。grammar.ts:26 activeAtToken 提取光标处@/@"token，formatFileMention 按空格/引号规则格式化mention。为纯seam包，由具体实现(如file-reference-local)实现。

## Provides
- ctx.fileReferences 抽象FileReferenceService(可取消list)
- @file token语法(activeAtToken/formatFileMention)
- FILE_REFERENCE_PROMPT模型指引
- FileReferenceCandidate类型

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 以agent会话cwd限定发现范围
  - 证据: `src/index.ts:8 Agent类型; list以agent cwd为界`

## Dependents (下游被依赖)
- `dsh-api-remotes` - @菜单引用文件远程namespace
- `dsh-client-ui-reference` - 复用@file语法与候选类型
- `dsh-file-reference-local` - 实现seam抽象list契约
- `dsh-web-app` - web-app装配文件引用seam
