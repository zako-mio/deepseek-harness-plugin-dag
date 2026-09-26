#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RC8 DAG 数据层更新：新增/删除节点、更新重点节点、新增/删除边、更新组、seam、版本标注"""
import json, os, sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
sys.stdout.reconfigure(encoding='utf-8')

BASE = BASE
DAG_PATH = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
SEAMS_PATH = os.path.join(BASE, "01-dag-data", "external-seams.json")

with open(DAG_PATH, encoding="utf-8") as f:
    dag = json.load(f)
with open(SEAMS_PATH, encoding="utf-8") as f:
    seams_data = json.load(f)

nodes = dag["nodes"]
edges = dag["edges"]
groups = dag["groups"]
node_ids = {n["id"] for n in nodes}
edge_set = {(e["from"], e["to"]) for e in edges}

# ============ 1. 新增 9 节点 ============
NEW_NODES = [
{
 "id":"dsh-client-ui-brand-official","name":"@deepseek-ai/dsh-client-ui-brand-official",
 "group":"G29","group_name":"UI底座","path":"packages/client/ui-brand-official","source_layer":"L2",
 "implementation":"纯浏览器UI插件(node半apply为空占位)。浏览器半 src/client/index.ts:14 apply 在 DSH_CLIENT_BUILD_PROFILE==='official' 时调用 ctx.slots.inject 将官方品牌注入三个brand slot(sidebar.brand.mark/name、conversation.hero.brand.mark)，每slot register一个React组件；Brand.tsx:12 OfficialBrandMark 用 ui-primitives 的 FishLogo 渲染鲸鱼标志，OfficialBrandName 渲染名称字标。装配于 cordis.patch.yml:213-214(E3)。",
 "provides":["ctx.slots 品牌slot填充(sidebar.brand.mark/name、conversation.hero.brand.mark)","官方鱼标志FishLogo与名称字标BrandWordmark的React呈现","仅official构建profile生效的brand占位"],
 "why":{"text":"将官方DeepSeek品牌视觉从通用sidebar/conversation slot中解耦为独立插件，按official构建profile选择性注入，使非官方部署可替换品牌而不改UI框架代码。","history":"RC8 新增"}
},
{
 "id":"dsh-client-ui-reference","name":"@deepseek-ai/dsh-client-ui-reference",
 "group":"G27","group_name":"会话交互UI","path":"packages/client/ui-reference","source_layer":"L2",
 "implementation":"纯浏览器UI插件。浏览器半 src/client/index.ts:30 注册本地化字典并构造 InputTriggerSource：trigger='@'，candidates 并行调用 ctx.remote.fileReferences.list 与 ctx.remote.sessionReferenceResolver.candidates 合并文件与会话候选，onPick 按kind返回file/session插入内容。文件候选经 file-reference/grammar 的 formatFileMention 格式化@mention；最终 ctx.effect 调用 inputTriggers.registerSource 注册统一@源。装配于 cordis.patch.yml:254-255(E3)。",
 "provides":["ctx.inputTriggers 统一@菜单源(同时含@file与@session候选)","文件/会话mention格式化(引用file-reference/grammar)","本地化字典(zh/en)"],
 "why":{"text":"将Web端@file与@session引用统一为单一输入触发源，合并原分散的引用逻辑，保证文件与会话候选顺序确定、标签统一。","history":"RC8 新增"}
},
{
 "id":"dsh-client-ui-renderer","name":"@deepseek-ai/dsh-client-ui-renderer",
 "group":"G29","group_name":"UI底座","path":"packages/client/ui-renderer","source_layer":"L2",
 "implementation":"纯浏览器插件(immediately=true)。浏览器半 src/client/index.ts:78 调用 ctx.slots.install(createSlotRenderer()) 安装slot渲染器，并通过 ctx.reflect.provide('uiRenderer') 提供 mount 服务：挂载应用根并返回卸载disposer。app.tsx:22 buildRenderApp 构建整棵应用树：SessionDocumentTitle 经 bindSnapshotSelector 订阅会话标题，主布局为 ctx.slots.renderSlot('root',{})；mountApp 通过 hydrateRoot 保留框架无关的启动DOM(data-dsh-boot)。装配于 cordis.patch.yml:191-192(E3)。",
 "provides":["ctx.uiRenderer.mount(container) 应用挂载服务","slot渲染器(createSlotRenderer)安装","应用根root slot渲染+DocumentTitle","启动DOM hydration"],
 "why":{"text":"统一承载浏览器React渲染骨架(原web-react的React glue)并新增应用根装配与uiRenderer挂载面，成为无框架boot kernel与React UI之间的唯一装配入口。","history":"RC8 新增(取代 dsh-client-web-react)"}
},
{
 "id":"dsh-code-runtime-python","name":"@deepseek-ai/dsh-code-runtime-python",
 "group":"G39","group_name":"代码执行运行时","path":"packages/code-runtime/code-runtime-python","source_layer":"L3",
 "implementation":"CPython子进程代码执行运行时，实现 code-execution seam 的Python后端。src/index.ts:11-19 再导出 fd-3 线上协议；protocol.ts:18 PROTOCOL_FD=3 定义子进程专用控制通道fd，stdout/stderr留给程序自身输出。协议含 boot(资源限制RLIMIT_CPU/RLIMIT_AS)、run、boot-ack、call(桥接工具调用)、log(流式日志含truncated)、done 帧，host将每帧视为敌意并validateChildFrame。py/protocol.py 为Python端镜像。为库/后端包，未装配进bundle，经dsh-tools的Code Mode间接生效。",
 "provides":["code-execution seam的CPython子进程实现","fd-3版本无关JSON-lines线上协议codec与敌意帧校验","跨语言协议镜像(TS↔Python)"],
 "why":{"text":"为代码执行seam提供资源受限、精确无损JSON的CPython子进程后端，与现有worker-thread后端互为可选实现，满足需要真实Python解释器环境的场景。","history":"RC8 新增"}
},
{
 "id":"dsh-file-reference","name":"@deepseek-ai/dsh-file-reference",
 "group":"G21","group_name":"上下文治理","path":"packages/context/file-reference","source_layer":"L2",
 "implementation":"文件引用发现seam(抽象基座)，供host侧UI共享。src/index.ts:27 声明 FileReferenceService extends TypertRemoteService，抽象 list 按agent cwd列出确定性候选，remoteExportList 以@Remote('list')装饰器暴露远程face；index.ts:20-24 声明 ctx.fileReferences。grammar.ts:26 activeAtToken 提取光标处@/@\"token，formatFileMention 按空格/引号规则格式化mention。为纯seam包，由具体实现(如file-reference-local)实现。",
 "provides":["ctx.fileReferences 抽象FileReferenceService(可取消list)","@file token语法(activeAtToken/formatFileMention)","FILE_REFERENCE_PROMPT模型指引","FileReferenceCandidate类型"],
 "why":{"text":"将@file引用发现抽象为host能力seam与共享语法，使terminal/web客户端与本地/远程实现共用同一契约，避免各UI重复实现发现逻辑。","history":"RC8 新增"}
},
{
 "id":"dsh-file-reference-local","name":"@deepseek-ai/dsh-file-reference-local",
 "group":"G21","group_name":"上下文治理","path":"packages/context/file-reference-local","source_layer":"L2",
 "implementation":"ctx.fileReferences 的本地文件系统实现。src/index.ts:45 LocalFileReferenceService extends FileReferenceService(seam)，list 按agent懒建 WorkspaceFileSearch(以agent cwd为root)；构造函数为每个agent安装FILE_REFERENCE_PROMPT的systemPrompt section(仅在read工具存在时)，并监听agent/created、tool/result事件维护搜索缓存与失效。search.ts:49 WorkspaceFileSearch 提供可取消可复用的有界模糊索引(默认maxEntries=10000)。装配于 cordis.patch.yml:85-86(E3)。",
 "provides":["ctx.fileReferences 本地实现(LocalFileReferenceService)","有界可取消WorkspaceFileSearch模糊索引","按agent的@file系统提示注入"],
 "why":{"text":"为@file引用seam提供本地文件系统实现，以有界索引保证性能与可取消性，同时按agent注入引用指引，使Web端@菜单能实时补全工作区路径。","history":"RC8 新增"}
},
{
 "id":"dsh-experimental-agent-team","name":"@deepseek-ai/dsh-experimental-agent-team",
 "group":"G38","group_name":"多智能体协作","path":"packages/experimental/agent-team","source_layer":"L3",
 "implementation":"隐式root多智能体协作服务(私有包,opt-in)。src/index.ts:56 TeamService extends Service(agentTeams)，inject=['agents','sessions','sessionPersistence','subagents']。组合Roster(花名册/隐式root)、Mailbox(持久peer消息箱)、TaskBoard(共享任务DAG)、Journal(Lead会话日志)、Lifecycle与Activity。公开API：membership、spawnTeammate、sendMessage、createTask/getTask/listTasks/updateTask、waitForChange、interrupt。监听session/event、agent/session-start驱动mailbox/recovery。未装配bundle，按需加载。",
 "provides":["ctx.agentTeams TeamService(花名册/持久邮箱/任务DAG/生命周期)","spawnTeammate/sendMessage/waitForChange/interrupt等协作原语","会话恢复与运行时清理"],
 "why":{"text":"为Profile Bundle按需安装的多智能体场景提供隐式root团队花名册、持久peer消息与共享任务DAG，使多个子代理能以协作方式共享同一工作区工作。","history":"RC8 新增"}
},
{
 "id":"dsh-experimental-tool-agent-team","name":"@deepseek-ai/dsh-experimental-tool-agent-team",
 "group":"G38","group_name":"多智能体协作","path":"packages/experimental/tool-agent-team","source_layer":"L3",
 "implementation":"面向模型的Agent Teams工具集(私有包)。src/index.ts:14 inject=['agents','agentTeams','tools','systemPrompt']。install 在每个exact Agent作用域注册：POLICY系统提示section、spawn_teammate(仅Lead可调)、send_message/followup_task(quiet/wakeup两种投递)、list_agents、wait_agent(含no-progress快速路径)、interrupt_agent、team_task_create/list/get/update等。所有工具经 ctx.agentTeams 服务转发，callingAgent 从exec.agent恢复调用者身份。Config含freshProvider/forkProvider指定teammate子代理提供者。",
 "provides":["模型面向工具: spawn_teammate/send_message/followup_task/list_agents/wait_agent/interrupt_agent/team_task_*","Team协作POLICY系统提示注入","Agent-scoped工具注册"],
 "why":{"text":"把agent-team的底层服务封装成模型可直接调用的协作工具，屏蔽服务细节，使Lead与teammate通过工具协议协作并遵守写作用域纪律。","history":"RC8 新增"}
},
{
 "id":"dsh-tool-pwsh-persistent","name":"@deepseek-ai/dsh-tool-pwsh-persistent",
 "group":"G14","group_name":"Shell工具","path":"packages/shell/tool-pwsh-persistent","source_layer":"L2",
 "implementation":"面向模型的owner-scoped持久PowerShell工具，基于Harness PTY服务(与tool-bash-persistent镜像)。src/index.ts:425 registerPersistentPwsh 注册 name='pwsh' 工具，execute 按owner串行执行；persistentShells 维护 owner→TerminalSessionId 注册表，get 懒spawn PTY并注入PWSH_PROMPT_SETUP 设置OSC状态提示；executeCommand 用deadline限制超时，wrapCommand 将命令包进单行带START/END nonce的PowerShell包装精确捕获退出码，retainedScrollback 分页重组回滚缓冲。inject=['tools','terminals']。未装配进bundle(Windows按需)。",
 "provides":["模型面向持久'pwsh'工具(跨调用保留cwd/env)","owner-scoped PTY会话注册表(懒spawn/重置/清理)","命令nonce包装精确捕获退出码+滚动缓冲重组"],
 "why":{"text":"为Windows提供持久PTY PowerShell会话工具(镜像bash-persistent)，使模型跨调用保持PowerShell状态，解决一次性pwsh无法保留工作目录/环境变量的问题。","history":"RC8 新增"}
},
]

# ============ 2. 新增边（真实新增依赖）============
# 新增 9 包的 depends_on 边
NEW_EDGES = [
# ui-brand-official
("dsh-client-ui-brand-official","dsh-client-runtime","E2","src/client/index.ts:14 apply(ctx); peerDependencies","注入品牌slot所需slots注册表"),
("dsh-client-ui-brand-official","dsh-client-ui-sidebar","E1","src/client/index.ts:19 注册sidebar.brand.* slot","填充侧边栏品牌slot contract"),
("dsh-client-ui-brand-official","dsh-client-ui-conversation","E1","src/client/index.ts:21 注册conversation.hero.brand.mark","填充会话Hero品牌slot contract"),
("dsh-client-ui-brand-official","dsh-client-ui-primitives","E2","Brand.tsx:1 import BrandWordmark, FishLogo","复用官方品牌图形组件"),
# ui-reference
("dsh-client-ui-reference","dsh-client-ui-input-trigger","E2","src/client/index.ts:88-89 inputTriggers.registerSource","注册@触发源所需服务"),
("dsh-client-ui-reference","dsh-client-runtime","E2","src/client/index.ts:12 ClientContext","提供ctx根上下文"),
("dsh-client-ui-reference","dsh-api-remotes","E2","src/client/index.ts:23 inject remote; :38-44 ctx.remote.fileReferences","远程文件/会话引用发现namespace"),
("dsh-client-ui-reference","dsh-client-locale","E2","src/client/index.ts:31 ctx.locale.register","本地化字典服务"),
("dsh-client-ui-reference","dsh-file-reference","E1","src/client/index.ts:16-17 import formatFileMention","复用@file语法与候选类型"),
("dsh-client-ui-reference","dsh-session-reference","E1","src/client/index.ts:18 SessionReferenceMentionCandidate","会话引用候选类型contract"),
# ui-renderer
("dsh-client-ui-renderer","dsh-client-runtime","E2","src/client/index.ts:41 inject ['slots','sessions']","依赖slots注册表与sessions服务装配应用"),
("dsh-client-ui-renderer","dsh-client-ui-slots","E2","scoped-slots.tsx:11 import SlotRenderer","声明式slot渲染与快照选择器基座"),
# code-runtime-python
("dsh-code-runtime-python","dsh-code-runtime","E1","package.json位于code-runtime/下, CPython实现","作为code-execution seam的具体后端"),
("dsh-code-runtime-python","dsh-tools","E2","README.zh.md:20 经dsh-tools Code Mode间接生效","通过Code Mode暴露执行能力"),
# file-reference
("dsh-file-reference","dsh-typert-protocol","E1","src/index.ts:9 import Remote, TypertRemoteService","远程服务与Remote装饰器基座"),
("dsh-file-reference","dsh-agent","E1","src/index.ts:8 Agent类型; list以agent cwd为界","以agent会话cwd限定发现范围"),
# file-reference-local
("dsh-file-reference-local","dsh-file-reference","E1","src/index.ts:10-13 extends FileReferenceService","实现seam抽象list契约"),
("dsh-file-reference-local","dsh-agent","E2","src/index.ts:46 static inject=['agents']","枚举agent并安装提示"),
("dsh-file-reference-local","dsh-system-prompt","E2","src/index.ts:69-74 scope.systemPrompt.section","注入@file模型指引"),
("dsh-file-reference-local","dsh-tools","E2","src/index.ts:73 agent.ctx.tools.get('read')","检测read工具决定是否注入提示"),
# agent-team
("dsh-experimental-agent-team","dsh-subagent","E2","src/index.ts:57 static inject ['subagents']","teammate的continuable子代理提供者"),
("dsh-experimental-agent-team","dsh-session","E2","src/index.ts:57 inject ['sessions']","以Lead会话为journal基底"),
("dsh-experimental-agent-team","dsh-session-persistence","E2","src/index.ts:57 inject ['sessionPersistence']","持久化Team消息/任务"),
("dsh-experimental-agent-team","dsh-llm","E2","peerDependencies @deepseek-ai/dsh-llm","teammate模型推理"),
("dsh-experimental-agent-team","dsh-agent","E2","src/index.ts:57 inject ['agents']","枚举live agent并判membership"),
# tool-agent-team
("dsh-experimental-tool-agent-team","dsh-experimental-agent-team","E2","src/index.ts:14 inject ['agentTeams']","转发所有Team协作操作"),
("dsh-experimental-tool-agent-team","dsh-tools","E2","src/index.ts:8 defineTool","工具定义与注册"),
("dsh-experimental-tool-agent-team","dsh-system-prompt","E2","src/index.ts:164 scoped.systemPrompt.section","注入Team协作策略提示"),
("dsh-experimental-tool-agent-team","dsh-agent","E2","src/index.ts:152-156 callingAgent","恢复exact调用者agent身份"),
# tool-pwsh-persistent
("dsh-tool-pwsh-persistent","dsh-terminal","E2","src/index.ts:469 inject ['terminals']","PTY会话服务"),
("dsh-tool-pwsh-persistent","dsh-tools","E2","src/index.ts:441 ctx.tools.register","工具注册"),
("dsh-tool-pwsh-persistent","dsh-timeout","E2","src/index.ts:13 deadline/timeoutOf","命令超时控制"),
("dsh-tool-pwsh-persistent","dsh-agent","E2","src/index.ts:457 exec.agent作为owner","owner作用域隔离shell会话"),
# 既有包新增边
("dsh-api-remotes","dsh-file-reference","E1","client/index.ts:6-11 新增fileReferencesRemote","@菜单引用文件远程namespace"),
("dsh-api-remotes","dsh-session-reference","E1","client/index.ts:93-96 新增sessionReferencesRemote","@菜单引用会话远程namespace"),
("dsh-llm-deepseek","dsh-attachment","E1","package.json:35,48 新增attachment依赖","原生多模态图片请求"),
("dsh-commands","dsh-attachment","E1","peerDependencies 新增attachment","/goal /plan 图文输入"),
("dsh-commands","dsh-llm","E1","peerDependencies 新增llm","命令图文输入模型处理"),
("dsh-session-persistence-sqlite","dsh-llm","E1","package.json:37 新增llm依赖","打包StreamChunk类型"),
("dsh-session-reference","dsh-typert-protocol","E1","peerDependencies 新增typert-protocol","会话引用远程契约"),
# web-app 装配新增（E3）
("dsh-web-app","dsh-client-ui-attachment","E3","cordis.patch.yml:212-218 ui-attachment装配","web-app装配附件UI"),
("dsh-web-app","dsh-client-ui-brand-official","E3","cordis.patch.yml:213-214 装配","web-app装配官方品牌"),
("dsh-web-app","dsh-client-ui-reference","E3","cordis.patch.yml:253-255 装配","web-app装配@引用UI"),
("dsh-web-app","dsh-client-ui-renderer","E3","cordis.patch.yml:191-192 装配","web-app装配渲染器"),
("dsh-web-app","dsh-file-reference","E3","cordis.patch.yml:84-86 装配","web-app装配文件引用seam"),
("dsh-web-app","dsh-file-reference-local","E3","cordis.patch.yml:85-86 装配","web-app装配文件引用本地实现"),
("dsh-web-app","dsh-session-reference","E3","cordis.patch.yml:82-83 装配","web-app装配会话引用"),
("dsh-web-app","dsh-launch-environment","E3","cordis.patch.yml webStartup/openBrowser","web-app装配启动环境"),
("dsh-web-app","dsh-subprocess","E3","cordis.patch.yml 装配","web-app装配子进程"),
]

# ============ 3. 删除边（真正不再引用）============
DEL_EDGES = [
("dsh-client-web","dsh-client-web-react","web-react节点删除"),
("dsh-client-web-react","dsh-client-locale","web-react节点删除"),
("dsh-client-web-react","dsh-client-runtime","web-react节点删除"),
("dsh-client-web-react","dsh-client-ui-slots","web-react节点删除"),
("dsh-client-ui-directory-picker-browse","dsh-client-ui-slots","rc8声明移除且不再import"),
("dsh-client-ui-directory-picker-native","dsh-client-ui-slots","rc8声明移除且不再import"),
("dsh-cordis-client-runner","dsh-client-ui-slots","rc8声明移除且不再import"),
]

# ============ 4. 重点节点 implementation 更新 ============
UPDATES = {
"dsh-session-persistence-sqlite": {
 "implementation":"物理存储重构为 schema-17: schema.ts:13 SCHEMA_VERSION 15→17; schema.sql:25-26 events.data/source_event_seqs 由 TEXT 改为 ANY(支持BLOB)。codec.ts:44 新增 packChunkRuns 将连续assistant/chunk增量(<1MiB、≤1024条)打包进单行; compression.ts:9,31 用 node:zlib zstd 压缩>4KiB载荷。store.ts:192-193 appendBatch 按打包记录插入，显著降低行数/存储体积。index.ts:41-42 新增 busyTimeoutMs 配置; schema.ts:265 validateSchemaForMutation 每次变更校验表结构。⚠️ 因表 data 列类型与 packed 行变化，与 rc7 数据库不兼容，需重建。",
 "note":"RC8 SQLite 数据结构不兼容(SCHEMA 15→17)，存储格式变更需重建数据库"
},
"dsh-llm-deepseek":{
 "implementation":"新增原生多模态图片请求: index.ts:95 模型可声明 inputModalities(['image'])，:107 新增 maxRequestImageBytes 配置(默认20MiB); index.ts:276-281 通过 ctx.get('attachments') 解析attachment服务。serialize.ts:99-157 新增 imagePart/contentParts/userContent，将durable图片附件读为 data:base64 的 image_url part(仅限user角色)。adapter.ts:235-252 请求含图时校验模型模态并解析attachments; serialize.ts:185+ 推理CoT 改为每个带reasoning的turn均回传 reasoning_content。新增依赖 dsh-attachment。",
 "note":"RC8 新增原生多模态图片请求(DeepSeek适配器可配置)"
},
"dsh-llm":{
 "implementation":"content.ts:92+ 新增 offloadRequestImages: 按base64长度收集请求内全部图片(含tool-result嵌套)，超 maxRequestImageBytes 时按流序替换最旧图片为 OFFLOADED_IMAGE_TEXT 占位，解决图片累计载荷过高致请求失败。assembler.ts:159-177 新增 interruptedBlocks(): 流被取消时保留已流出的text/reasoning前缀，供agent-loop落地中断回复。",
 "note":"RC8 修复图片累计载荷过高 + 取消流式后回复前缀保留"
},
"dsh-llm-pi-ai":{
 "implementation":"config.ts:45-55 新增 DEFAULT_MAX_REQUEST_IMAGE_BYTES(20MiB); context.ts:151-175 toPiContext 增加 maxRequestImageBytes 参数并调用 offloadRequestImages 脱载最旧图片。catalog.ts:221-352 + config.ts:217-253 大幅扩展 OpenAI 兼容网关 compat 面(chat-template/qwen-chat-template thinking格式、maxTokensField、cacheControlFormat、supportsReasoningEffort、requiresReasoningContentOnAssistantMessages等)，修复自定义网关请求格式差异与推理回传缺失。stream.ts:43-45 将413/请求体超限判定为 INVALID_REQUEST。",
 "note":"RC8 修复图片载荷过高 + 自定义OpenAI兼容网关请求格式/推理回传"
},
"dsh-api-remotes":{
 "implementation":"client/index.ts:6-11,93-96 新增 fileReferencesRemote 与 sessionReferencesRemote 两个远程命名空间(依赖 dsh-file-reference/remote 与 dsh-session-reference/remote)，并导出 FileReferenceCandidate/SessionReferenceMentionCandidate 类型，为 @ 菜单引用文件与会话提供 RPC 面。",
 "note":"RC8 @菜单支持引用文件和会话(新增远程namespace)"
},
"dsh-attachment":{
 "implementation":"新增 admission.ts:36-41 admitEncodedImages: 统一各 RPC 端点的 base64 图片上传准入(校验规范base64，再委托 saveImages 做批量数量/聚合字节/媒体类型校验)，index.ts:15 导出。替换 host/apiproxy 原有内联 decodeBase64 逻辑。支持被 web/llm 端图片上传复用。",
 "note":"RC8 新增图片上传统一准入(admitEncodedImages)"
},
"dsh-attachment-local":{
 "implementation":"image.ts:47-54 新增 DecodedImageLimits(maxPixels + maxDimension 独立边长限制); :57-69 detectImage 在原有解码像素上限外新增每边维度上限，超限抛 IMAGE_DIMENSION_TOO_LARGE，拦截超大尺寸图片。",
 "note":"RC8 拦截超大尺寸图片(维度上限)"
},
"dsh-subagent-claude-code":{
 "implementation":"index.ts:37,40 由固定'claude-code' provider改为可配置 providerName(默认claude-code，支持多命名实例); index.ts:46-52 + run.ts:42-55 新增 permissionMode 配置(dontAsk默认/acceptEdits/auto/plan/bypassPermissions)固定非交互权限。cordis.patch.yml 将provider注册为可选 Profile Bundle(dsh.bundle.patch)，支持按需安装; process.ts:20 移除Windows batch shim改用共享subprocess管理。",
 "note":"RC8 Claude Code子代理Profile Bundle按需安装 + 非交互权限模式"
},
"dsh-subagent-codex":{
 "implementation":"index.ts:37,44 改为 providerName 可配置(多命名实例); run.ts:37-127 新增 CodexPermissionMode(never默认/approve-for-me/dangerously-bypass-approvals-and-sandbox)，wire.ts:24-33 THREAD_PERMISSION_PARAMS 映射到thread/start审批策略，实现非交互权限模式。run.ts:40-45 用 createRequire 解析 @openai/codex bin 生成包内wrapper(CODEX_PACKAGE_BIN)，argv固定为[node, wrapper, app-server, --stdio]，不依赖PATH的codex命令，支持Profile Bundle按需安装。cordis.patch.yml可选注册; @openai/codex 由devDeps移入deps。",
 "note":"RC8 Codex Profile Bundle按需安装 + 非交互权限模式 + 多命名实例"
},
"dsh-subagent":{
 "implementation":"index.ts:312-327 新增 drainContinuableChildren(parent, childIds): 释放指定父会话的常驻continuable直接子代理(验证父身份)。run-settlement.ts:21-28 新增 failureDetail 渲染provider自述诊断; types.ts:236-242 SubagentResult 新增 diagnostic 字段(限制4096字节)。",
 "note":"RC8 子代理reportDelivery及时反馈并唤醒父任务 + 失败诊断回传"
},
"dsh-tool-subagent-report":{
 "implementation":"index.ts:29-37 reportDelivery 取值由 'quiet'/'wakeup' 改为 'quiet'/'next-step'(默认next-step): 'next-step' 在最近步骤边界唤醒父代理并注入上下文，比旧wakeup更及时地让父任务在步骤边界继续。",
 "note":"RC8 reportDelivery 语义变更 wakeup→next-step(更及时唤醒父任务)"
},
"dsh-tool-web":{
 "implementation":"search.ts:22-29 新增 WEB_SEARCH_MAX_QUERIES=4 与 WebSearchArgs.queries 数组; parseSearchArgs 校验queries非空/上限/去重。:220-296 新增 runSearchQueries: 多query用 Promise.allSettled 并发执行(ctx.web.search)，任一失败abort兄弟查询并等全部settle后抛首个错误; mergeSearchResults round-robin去重合并并封顶maxResults。",
 "note":"RC8 web_search 支持并发查询(最多4个)"
},
"dsh-core-agent-loop":{
 "implementation":"agent.ts:345-370 流式生成改为 try/catch: signal中止时若 assembler.interruptedBlocks() 有内容，则追加一条 assistant/message(interrupted:true, sourceEventSeqs关联已落chunk)，将取消前已展示的回复前缀持久化进会话，使后续提问与分叉会话能继承该前缀。",
 "note":"RC8 取消流式生成后回复前缀带入后续提问/分叉"
},
"dsh-host-apiproxy":{
 "implementation":"api-proxy.ts:135-137 图片上传改用 attachment 包新 admitEncodedImages(ctx.attachments) 统一准入(替换原内联decodeBase64); :2853 host信息新增 home: homedir()，供前端以~缩写HOME目录。",
 "note":"RC8 HOME目录~缩写 + 图片上传统一准入"
},
"dsh-tool-fs-search":{
 "implementation":"search-core.ts:162-166 rg二进制解析新增 pkg 单文件运行时支持: 若'pkg' in process 且存在 process.execPath+'-rg' sidecar 则用侧车二进制，否则回退 @vscode/ripgrep 平台包。修复 pkg 打包下原生rg无法spawn问题。",
 "note":"RC8 SDK rg/glob搜索工具链(单文件运行时侧车支持)"
},
"dsh-session-persistence":{
 "implementation":"coordinator.ts:1173-1174 fork种子事件不再 structuredClone，改为直接复用session持有的稳定深冻结快照，消除大历史分叉时整份克隆开销(配合sqlite packed行提升分叉性能)。",
 "note":"RC8 大历史会话分叉性能优化(复用冻结快照)"
},
}

# ============ 5. seam referred_by 更新 ============
SEAM_UPDATES = {
 "dsh-attachment": {"delta": 2, "add": ["dsh-commands","dsh-llm-deepseek"]},
 "dsh-typert-protocol": {"delta": 2, "add": ["dsh-client-ui-goal","dsh-session-reference"]},
 "dsh-client-connection": {"delta": 1, "add": ["dsh-client-ui-tool","dsh-client-ui-workspace"], "remove": ["dsh-client-ui-user-questions"]},
 "dsh-launch-environment": {"delta": 1, "add": ["dsh-web-app"]},
 "dsh-subprocess": {"delta": 1, "add": ["dsh-web-app"]},
 "dsh-pwsh-local": {"delta": 1, "add": ["dsh-terminal-bash"]},
}

# ============ 应用 ============
def apply():
    # 1. 新增节点
    for nn in NEW_NODES:
        if nn["id"] in node_ids:
            print(f"[SKIP] 节点已存在: {nn['id']}")
            continue
        nodes.append(nn)
        node_ids.add(nn["id"])
    # 2. 删除节点
    for rid in ("dsh-client-web-react","dsh-client-schema-form"):
        if rid in node_ids:
            nodes[:] = [n for n in nodes if n["id"] != rid]
            node_ids.discard(rid)
            print(f"[DEL] 节点: {rid}")
    # 3. 新增边
    for f,t,m,ev,pur in NEW_EDGES:
        if (f,t) in edge_set:
            print(f"[SKIP] 边已存在: {f}->{t}")
            continue
        edges.append({"from":f,"to":t,"mechanism":m,"evidence":ev,"purpose":pur,"source_layer":next((x.get("source_layer","L2") for x in NEW_NODES if x["id"]==f),"L1")})
        edge_set.add((f,t))
    # 4. 删除边
    del_keys = {(f,t) for f,t,_ in DEL_EDGES}
    edges[:] = [e for e in edges if (e["from"],e["to"]) not in del_keys]
    # 5. 更新重点节点
    for n in nodes:
        if n["id"] in UPDATES:
            upd = UPDATES[n["id"]]
            n["implementation"] = upd["implementation"]
            if "note" in upd:
                n.setdefault("why",{})["history"] = upd["note"]
    # 6. 新增组
    existing_gids = {g["id"] for g in groups}
    for gid,gname,plist in [("G38","多智能体协作",["dsh-experimental-agent-team","dsh-experimental-tool-agent-team"]),
                            ("G39","代码执行运行时",["dsh-code-runtime-python"])]:
        if gid not in existing_gids:
            groups.append({"id":gid,"name":gname,"plugins":plist})
            existing_gids.add(gid)
        else:
            g=next(x for x in groups if x["id"]==gid)
            for p in plist:
                if p not in g["plugins"]: g["plugins"].append(p)
    # 7. 从删除的组 plugins 移除已删除节点
    for g in groups:
        g["plugins"] = [p for p in g["plugins"] if p in node_ids]
    # 8. 新组中加入已新增节点（把新增节点加入其组）
    for nn in NEW_NODES:
        gid = nn["group"]
        g = next((x for x in groups if x["id"]==gid), None)
        if g and nn["id"] not in g["plugins"]:
            g["plugins"].append(nn["id"])
    # 更新 meta
    dag["meta"]["plugin_count"] = len(nodes)
    dag["meta"]["edge_count"] = len(edges)
    dag["meta"]["group_count"] = len(groups)
    dag["meta"]["generated_at"] = "2026-08-20"

    # 9. seam 更新
    seam_map = {s["id"]: s for s in seams_data["seams"]}
    for sid, upd in SEAM_UPDATES.items():
        s = seam_map.get(sid)
        if not s: 
            print(f"[WARN] seam 不存在: {sid}")
            continue
        rb = set(s.get("referred_by", []))
        for a in upd.get("add", []): rb.add(a)
        for r in upd.get("remove", []): rb.discard(r)
        s["referred_by"] = sorted(rb)
        s["ref_count"] = len(rb)
    seams_data["count"] = len(seams_data["seams"])

    # 写回
    with open(DAG_PATH,"w",encoding="utf-8") as f:
        json.dump(dag,f,ensure_ascii=False,indent=2)
    with open(SEAMS_PATH,"w",encoding="utf-8") as f:
        json.dump(seams_data,f,ensure_ascii=False,indent=2)
    print(f"\n[OK] 完成: 节点={len(nodes)}, 边={len(edges)}, 组={len(groups)}, seam={len(seams_data['seams'])}")

apply()
