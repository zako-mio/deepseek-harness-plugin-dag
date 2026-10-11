# dsh-client-ui-primitives

- 包名: `@deepseek-ai/dsh-client-ui-primitives`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/client/ui-primitives`

## 实现逻辑
零 cordis 的纯 React 原子库：以 src/index.ts 为唯一桶导出，集中暴露按钮/菜单/弹窗/Toast/JsonTree/终端与 diff/search/web 块、图标集与 markdown 渲染器等展示原语 (src/index.ts:5-118)。路径标签用 pathPartsOf 拆出目录与文件名，并以 ResizeObserver 判定溢出后做左侧裁剪淡出 (src/PathLabel.tsx:4-29)。代码高亮把扩展名→语法的选择表交给 util-code-language 统一持有，再用 useSyncExternalStore 跟随语法懒加载 (src/code-highlighting.ts:10-22)。设置表单以 SettingsFormModel 暂存用户输入，只在保存时做一次带 revision 围栏的原子写入，并以「用户层是否存在」而非值比较判定 overridden (src/settings-form/form-model.ts:16-56)。

## Provides

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-client-locale` - Language 行复用共享 UI 原语
- `dsh-client-shortcuts` - 复用基础控件渲染键位与菜单
- `dsh-client-ui-agent-preset` - 复用基础控件渲染名册行
- `dsh-client-ui-approval` - 审批面板复用基础组件
- `dsh-client-ui-attachment` - 附件卡片与图片画廊的基础组件
- `dsh-client-ui-brand-official` - 品牌标志与品牌名的呈现组件
- `dsh-client-ui-chat` - 复用基础控件与 markdown 渲染
- `dsh-client-ui-commands` - 复用弹出层与列表基础控件
- `dsh-client-ui-conversation` - 复用基础控件与图标
- `dsh-client-ui-cordis` - 复用客户端基础 UI 原语渲染准备中卡片
- `dsh-client-ui-deliverables` - 复用基础控件渲染文件行
- `dsh-client-ui-dockkit` - 复用菜单、图标与工具提示等基础控件
- `dsh-client-ui-goal` - 复用基础控件渲染命令输入
- `dsh-client-ui-input-trigger` - 候选菜单列表基础组件
- `dsh-client-ui-message-feedback` - 复用 ui-primitives 的 Toast/Button 等控件
- `dsh-client-ui-model-selection` - 复用图标与基础控件
- `dsh-client-ui-open-in-app` - 失败提示控件
- `dsh-client-ui-permission-presets` - 复用基础控件渲染选择器
- `dsh-client-ui-plan` - 复用 markdown 纯文本提取与基础控件
- `dsh-client-ui-plugin-manager` - 复用提示与图标控件
- `dsh-client-ui-reference` - 会话候选相对时间展示
- `dsh-client-ui-schedule` - 任务卡片、目录反馈与锚定弹层复用共享原子控件
- `dsh-client-ui-settings-account` - 登录/登出/充值等对话框与账户区复用共享原子控件与图标
- `dsh-client-ui-settings-agent-loop` - 设置页复用共享的 SettingsForm 与数值字段控件
- `dsh-client-ui-settings-general` - 设置面板复用连接指示器、模态层工具与关闭顶层弹窗的原语
- `dsh-client-ui-settings-models` - 模型页与其编辑器复用共享原子控件与模态
- `dsh-client-ui-settings-plugin-inventory` - 清单表复用共享的菜单、状态点与标签控件
- `dsh-client-ui-settings-session-log` - 设置行与提示复用共享的开关与 Toast 原语
- `dsh-client-ui-settings-shell` - 设置页复用共享表单与字段控件，字典类型也取自其 labels 契约
- `dsh-client-ui-settings-subagent` - 设置页与字段复用共享表单控件及其暂存模型类型
- `dsh-client-ui-settings-web-search` - 设置页复用共享表单、密钥字段与字典标签契约
- `dsh-client-ui-shortcuts` - 参考面板、录制编辑器与快捷键键位显示复用共享原语
- `dsh-client-ui-sidebar-browser` - guide 入口图标与工具条控件复用共享原语
- `dsh-client-ui-sidebar-documentpreview` - 加载指示、缩放控件等复用共享原语
- `dsh-client-ui-sidebar-files` - 标题图标与控件复用共享原语
- `dsh-client-ui-sidebar-right` - 面板控件与图标复用共享原语
- `dsh-client-ui-sidebar-terminal` - guide 入口图标与终端控件复用共享原语
- `dsh-client-ui-skill` - 候选排序复用共享的按名排序实现
- `dsh-client-ui-subagent` - 血统行图标与提示控件复用共享原语
- `dsh-client-ui-theme` - 设置行控件复用共享原语
- `dsh-client-ui-tool` - 卡片、标签与图标复用共享原语
- `dsh-client-ui-trajectory` - 表格、时间轴与工具条控件复用共享原语
- `dsh-client-ui-workspace` - 行、菜单与按钮复用共享原语
- `dsh-client-web` - 种子静态模块表内联 UI 原语库
- `dsh-experimental-client-ui-claude-code-mods` - 客户端基元组件的声明依赖，保证组合中存在同一份实现
- `dsh-experimental-client-ui-cot-translation` - 译文按钮与表单控件使用客户端基元组件
- `dsh-experimental-client-ui-voice-input` - 麦克风按钮、波形与卡片使用客户端基元组件
- `dsh-experimental-inspector` - 检查器面板的按钮与提示使用客户端基元组件
- `dsh-experimental-session-inspector` - 表格与筛选器使用客户端基元组件
- `dsh-session-log-export` - 复用 Button/Menu/Modal 等基础组件渲染菜单与下载弹窗
