# DeepSeek Harness 插件级 DAG 依赖链分析

> **版本**：`v0.1.0-rc.8`（基于官方源码 dsh-v0.1.0-rc.8，2026-08-19 发布）
> **升级记录**：RC5 → RC7（2026-08-19）→ **RC8（2026-08-20）**。本次 RC8 升级新增 9 插件、删除 2 插件（web-react 改名并入 ui-renderer、schema-form 并入 ui-settings），源码实质变化 61 包。详见 `RC7-RC8-DIFF-REPORT.md`。

## 简介

以 **cordis 插件为最小分析单元**，回答三个问题：
1. **该插件以什么逻辑实现了什么功能**（实现逻辑 + provides）
2. **该插件依赖哪些插件的哪些功能**（depends_on 上游）
3. **该插件的哪些功能被谁依赖**（dependents 下游）

依赖判定**三硬依据 + 源码行引用**，逐条可溯源：
- **E1 编译依赖**：package.json peerDependencies / import 语句
- **E2 运行时依赖**：ctx 服务注入 / ctx.get / 事件订阅
- **E3 组合依赖**：cordis.patch.yml 装配位置

## 范围分层（三个上下文窗口）

| 层 | 范围 | 插件数 | 状态 |
|----|------|-------|------|
| **L1 核心集** | `bundle/base/cordis.patch.yml` 装配的全部插件 | 76 核心 + 36 外部 seam | ✅ **完成** |
| **L2 web-app bundle** | base 之上 web-app 装配的宿主层 + 前端 runtime + 30+ ui-* 包 | 58（含 6 import 底座） | ✅ **完成** |
| **L3 其余** | examples/demo、hooks、web 搜索变体、e2b、lsp、sdk、子代理外部后端等 | 46 插件 + 13 seam + 4 特殊模块 | ✅ **本轮完成** |

## 快速开始

| 想做什么 | 去哪 |
|---------|------|
| **交互 DAG 总览**（组级视图 + 点击下钻） | `04-interactive/index.html` |
| 分组目录 | `03-groups/index.html` |
| 每插件一页（含**模块内部结构动态 DAG**） | `02-plugin-pages/`（229 页：180 插件 + 49 seam - 1 双身份） |
| 特殊模块结构（base/headless/boot） | `08-special-modules/` |
| AI 检索 MD 镜像 | `06-md/00-index.md`（180 插件 + 49 seam 全量） |
| DAG 数据（JSON） | `01-dag-data/webapp-dag.json`（L1+L2+L3 合并） |
| 模块级 import 数据 | `07-checkpoint/plugin-internal-all.json`（215 插件 1130 模块） |

## 目录结构

```
0816-plugin-dag/
├── 01-dag-data/          # DAG 数据: webapp-dag.json(180节点+578边+17层+39组) / core-dag.json(L1) / external-seams.json(49 seam)
├── 02-plugin-pages/      # 每插件一页 HTML（180 核心/Web/L3 + 49 外部 seam = 229 页，1 双身份共享）
├── 03-groups/            # 39 组索引页 + 组目录
├── 04-interactive/       # cytoscape 交互总览 (index.html, 组级+下钻) + vendor/(cytoscape+dagre)
├── 06-md/                # AI 友好 MD 镜像
├── 07-checkpoint/        # 中间产物: stage-00/01 采集 / build-dag-l3.py / gen-html-l3.py / inject-data-l3.py / quality-gate-l3.py
├── 08-special-modules/   # 特殊模块 4 页 (dsh-base/headless/app-boot/cmdline)
└── index.html            # 根入口
```

## 核心数据（L1+L2+L3 合并 webapp-dag.json）

- **180 节点**：76 L1 核心 + 58 L2 web-app + 46 L3 其余插件
- **49 外部 seam 基座**（dsh-invariants/dsh-scope/dsh-timeout 等抽象包 + L3 追加 13：7 抽象基座 + 6 test-support）
- **578 依赖边**（含 22 个 web 变体 disabled 标注）
- **17 拓扑层**（层次遍历：被依赖方先于依赖方）
- **39 分组**（L1 24 组 + L2 5 组 + L3 8 组 + 新增 G38 多智能体协作 / G39 代码执行运行时：G30 外部执行后端 / G31 协议与SDK / G32 LSP集成 / G33 子代理外部后端 / G34 Web上下文扩展 / G35 会话存储变体 / G36 Hooks工具扩展 / G37 示例与框架）

## 交互图（组级 + 点击下钻）

- **组级视图**：40 节点（39 组 + EXT），每组不同配色，点击组节点下钻组内插件 DAG
- **下钻视图**：组内插件 + 跨组 stub 灰显节点（可跳转），插件按组配色
- **disabled 标注**：22 个 web 变体禁用插件以灰色红边样式呈现（`node[kind="disabled"]` 数据属性选择器）
- hash 路由 `#G03` / query `?drill=G03` / 面包屑返回

## 拓扑分层速览（L1+L2+L3 合并）

- **Layer 0**（19）：cordis-plugin-timer, dsh-llm, dsh-storage, dsh-host-webserver, dsh-fs-e2b, dsh-host-directory-picker, dsh-native-command, dsh-subprocess-e2b, dsh-typert-generator...
- **Layer 4**（15，含 L3）：dsh-session-title-all-prompts-llm, dsh-terminal-bash, dsh-web-search-exa, dsh-web-search-perplexity...
- **Layer 5**（26，L3 最多层）：dsh-agent-tool-presentation, dsh-hooks-codex, dsh-schedule, dsh-tool-ask-user, dsh-tool-bash-persistent, dsh-tool-lsp, dsh-tool-session-query, dsh-tool-terminal...
- **Layer 6**（19）：dsh-hooks-claude-code, dsh-sdk-jsonrpc-server, dsh-subagent-acp, dsh-subagent-claude-code, dsh-subagent-codex, dsh-subagent-dsh-sdk, dsh-tool-cordis...
- **Layer 8**（3，最末）：dsh-acp-demo

## L2 关键发现

- **Web 传输链**：dsh-host-webserver（node:http 宿主）→ dsh-client-modules（bundle 扫描/__DSH_BOOT__）→ dsh-client-connection（/api + WebSocket downlink）→ dsh-client-runtime（SlotRegistry+SessionRuntime）→ 各 UI 包
- **UI 包依赖方向**：UI 依赖 host 的服务与事件契约（import + ctx 远程调用），slot 注册是协商网络而非严格 DAG（conversation 声明 11 个 slot，子 UI 包注册进槽位）
- **base 覆盖**：dsh-host-apiproxy 覆盖 base 行 api-gateway（web 变体网关）；22 个 base 插件在 web 下 disabled（模型侧工具移到 agent presets）

## L3 关键发现

- **抽象基座 seam 聚合**：7 个 L3 抽象基座（lsp/sdk-protocol/e2b/terminal/hook-protocol/acp/mcp-client）被实现包依赖，形成"实现包 → 抽象包"方向（如 dsh-lsp-stdio → dsh-lsp）
- **子代理后端 4 变体**：acp/claude-code/codex/dsh-sdk 均以 `inject['subagents']` 依赖宿主 dsh-subagent；subagent-acp 走外部 @agentclientprotocol/sdk 而非 dsh-acp seam
- **Web 搜索变体**：exa/perplexity 是 dsh-web-search-deepseek（L1）的 seam 注册变体，以 E1 依赖 dsh-web seam
- **特殊模块独立**：dsh-base/dsh-headless（bundle）+ dsh-app-boot/dsh-cmdline（boot 胶水）不进主 DAG，单独 08-special-modules/ 分析
- **原生命令库**：dsh-native-command 是纯库（非插件），供 directory-picker-native 与 apiproxy 复用

## 模块内部结构（源码 DAG）动态图

每个插件专属页面（`02-plugin-pages/{id}.html`）内置**模块级内部结构动态 DAG**（cytoscape 渲染）：
- **节点** = 插件 `src/` 下各文件（模块），共解析 215 插件 + 1130 模块
- **边** = 文件间 `import` / `export from` 依赖关系（共 1073 条）
- **染色**：蓝=入口/核心（index 或被高频引用）、深蓝=普通模块、灰=叶子
- **排版**：LR 横排（节点多时自动横排防狭长）+ 布局后 fit 适配容器 + 窗口 resize 自动重排
- **交互**：可拖拽/缩放/点击节点（点击显示完整模块路径）
- **数据源**：`07-checkpoint/plugin-internal-all.json`（由源码 `src/*.ts` 解析生成）
- **框架插件**（cordis-plugin-hmr/timer）：无源码包，显示占位说明

生成脚本：`07-checkpoint/parse-all-internal.py`（解析）+ `apply-all-internal.py`（插入页面）。

## 质量门控

`07-checkpoint/quality-gate-l3.py` 全部通过：JSON 合法 / DAG 无环（180/180）/ HTML 断链 0 / vendor 完整 / 插件页覆盖 180+49+4 特殊模块 / 交互图 DATA 校验（180 插件 + 49 seam + 39 组）/**MD 镜像覆盖 180+49**。
headless + VLM 验证：组级视图 40 节点、L3 组下钻正常（G30 下钻 23 节点 / G37 下钻 36 节点）、中文渲染完整、模块 DAG 染色/排版正确。

> ℹ️ **关于"红框"插件**：交互图中灰色红边的节点（22 个，如 dsh-skill-filesystem / dsh-tool-skill）是 **web 变体禁用 base 插件**的刻意标注（`node[kind="disabled"]` 样式），并非缺页面——它们的 HTML 页面与 MD 镜像均存在，点击可正常跳转。
