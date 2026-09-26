# DeepSeek Harness 插件级 DAG 依赖链分析

> **版本**：`v0.1.7-rc.2`（基于官方源码 dsh-v0.1.7-rc.2，2026-09-24 发布，commit `477b4f42`）
> **留档位置**：本库于 2026-09-27 由 `Mission-file/2026-08/0822-plugin-dag-v0.1.1-rc2` 整仓迁移至 `Mission-file/2026-09/0927-dsh-plugin-dag-017rc2`（Git 仓与远端不变；历史差异报告中的旧目录名为迁移前名称）。
> **升级记录**：RC5 → RC7（08-19）→ RC8（08-20）→ RC2（08-21）→ **0.1.7-rc.2（09-27 全量重建）**。本次跨度 **6875 commits / 6 个 minor**，包树 227 → **312**（+102 / −17），**210/210 共有包源码全部变化**（0 个「仅版本号变化包」），故放弃增量级联、改走**全量重推导**。详见 `RC2-0.1.7-DIFF-REPORT.md`。

## 简介

以 **cordis 插件为最小分析单元**，回答三个问题：
1. **该插件以什么逻辑实现了什么功能**（实现逻辑 + provides）
2. **该插件依赖哪些插件的哪些功能**（depends_on 上游）
3. **该插件的哪些功能被谁依赖**（dependents 下游）

依赖判定**三硬依据 + 源码行引用**，逐条可溯源：
- **E1 编译依赖**：package.json peerDependencies / import 语句
- **E2 运行时依赖**：ctx 服务注入 / ctx.get / 事件订阅
- **E3 组合依赖**：cordis.patch.yml 装配位置

## 核心数据（v0.1.7-rc.2）

| 指标 | 数值 |
|---|---|
| 插件节点 | **239**（L1 核心 90 + L2 web-app 82 + L3 其余 67） |
| 节点间依赖边 | **1077**（另 **536** 条指向 seam 的边，经 `external-seams.referred_by` 表达） |
| 外部 seam 基座 | **73**（抽象基座 / 工具库 / 测试支撑） |
| 拓扑层 | **19**（最长路径分层：被依赖方先于依赖方） |
| 分组 | **50**（按 `packages/<域>` 划分，客户端 UI 独立成组） |
| HTML 插件页 | **312**（239 插件 + 73 seam）+ 50 组页 + 8 特殊模块页 |
| 装配行 disabled 标注 | **19** |

> 判据统计口径：`edges` 仅含**节点间**边（schema 约定，避免页面生成器 KeyError）；指向纯 seam 的边不重复计入 `edges`，改由 `external-seams.json` 的 `referred_by` 表达。
> 拓扑只由**运行时边**决定（排除 type-only 类型导入边 281 条 + 1 条 soft 反馈边）；TS 类型层 import 环合法，门控仅作 WARN 上报。

## 范围分层（装配来源）

| 层 | 范围 | 插件数 |
|----|------|-------|
| **L1 核心集** | `bundle/base/cordis.patch.yml`（93 条 insert 行） | 90 核心 |
| **L2 web-app** | `bundle/web-app/cordis.patch.yml`（85 条 insert 行，含全部客户端 UI 包） | 82 |
| **L3 其余** | SDK/ACP bundle 之外的可挂载插件：hooks、web 搜索变体、SSH、Browser-Use、Computer-Use、实验特性、会话格式、deliverables、webhook 等 | 67 |
| **特殊模块** | base/headless/web-app/sdk-app/sdk-minimal/acp-app（bundle）+ app-boot/cmdline（boot 胶水） | 8（独立成页，不进 DAG） |

## 快速开始

| 想做什么 | 去哪 |
|---------|------|
| **交互 DAG 总览**（组级视图 + 点击下钻 + `?drill=Gxx` 深链） | `04-interactive/index.html` |
| 分组目录 | `03-groups/index.html` |
| 每插件一页（含**模块内部结构动态 DAG**） | `02-plugin-pages/`（312 页） |
| 特殊模块结构（base/web-app/sdk/boot…） | `08-special-modules/`（8 页） |
| AI 检索 MD 镜像 | `06-md/00-index.md`（239 插件 + 73 seam 全量） |
| DAG 数据（JSON） | `01-dag-data/webapp-dag.json`（239 节点 + 1077 边 + 536 seam_edges） |
| 模块级 import 数据 | `07-checkpoint/plugin-internal-all.json` |

## 目录结构

```
0927-dsh-plugin-dag-017rc2/
├── 01-dag-data/          # webapp-dag.json（239节点/1077边/19层/50组/536 seam_edges）/ core-dag.json（L1 90节点）/ external-seams.json（73 seam）
├── 02-plugin-pages/      # 每插件一页 HTML（239 插件 + 73 seam = 312 页）
├── 03-groups/            # 50 组索引页 + 组目录
├── 04-interactive/       # cytoscape 交互总览（组级 + 下钻 + URL 深链）+ vendor/
├── 05-source/            # 官方源码：dsh-rc8 / dsh-v0.1.1-rc.2 / dsh-v0.1.7-rc.2（tarball+SHA256；解压树 gitignore）
├── 06-md/                # AI 友好 MD 镜像
├── 07-checkpoint/        # 生成管线（含 v017/ 本轮全量重建中间产物）
├── 08-special-modules/   # 特殊模块 8 页
└── index.html            # 根入口
```

## 生成管线（07-checkpoint，可重放）

本轮为 v0.1.7-rc.2 建立了**自包含、确定性、可复现**的管线（不依赖跨任务 PACKAGE-MAP，不依赖 Windows 路径）：

| 脚本 | 作用 |
|------|------|
| `v017-inventory.py` | 解析 6 个 bundle `cordis.patch.yml` + 枚举 `packages/*/*` 与 `vendor/*` → `v017/inventory.json` |
| `v017-facts.py` | 逐包扫 `src/**/*.ts` 提取 E1 import（含 file:line）/ E2 inject·ctx·事件 / 插件导出特征 → `v017/facts.json` |
| `v017-classify.py` | 分类 nodes / seams / special / uncovered + 分组 → `v017/classification.json` |
| `v017-make-shards.py` | 按组打包为 21 个委派分片 → `v017/shards/*.json` |
| （委派）21 个 general 子 Agent | 逐插件实读源码 → `v017/stage-01-shard-*.json`（含 implementation / provides / depends_on / evidence） |
| `v017-validate.py` | 分片回盘复验（条目数 / ids / 证据格式） |
| `v017-build-dag.py` | 合并 → DAG（最长路径分层 + 反馈边 soft + type-only 标注）→ `01-dag-data/*.json` |
| `v017-prep-inputs.py` | 生成 `special-modules.json`（8 模块）/ `disabled-rows.json`（19 行） |
| `v017-clean-pages.py` | 删除不在新节点集内的陈旧页面 |
| `gen-html-l3.py` / `gen-md-l3.py` / `gen-plugin-dyn.py` / `gen-overview.py` / `inject-data-l3.py` | 全量页面重生成（复用既有生成器） |
| `quality-gate-l3.py` | 8 项门控（已强化：纳入 v017 全部 JSON / 8 特殊模块全集 / seam_edges↔referred_by 一致性 / 分层方向一致性） |
| `headless-verify-l3.py` | chromium headless DOM 断言（**非空断言**：下钻视图 ≠ 组级视图）+ 截图 |

## 关键发现（v0.1.7-rc.2）

- **装配分层重构**：新增 3 个 bundle（`acp-app` / `sdk-app` / `sdk-minimal`），base 装配 93 行、web-app 85 行、sdk-minimal 32 行；`dsh-sdk-minimal` 不叠 base、自身即完整 Cordis 树。
- **客户端层大扩张**：client 域 61 包（含 41 个 `ui-*`），web-app 单 bundle 装配 85 行；客户端 UI 与 `dsh-api-remotes` 存在 1 处运行时注册回环（已标 soft）。
- **抽象基座 seam 化**：`dsh-fs` / `dsh-sandbox` / `dsh-spill` / `dsh-jobs` / `dsh-shell` / `dsh-subprocess` / `dsh-attachment` / `dsh-compaction` / `dsh-credentials` / `dsh-session-persistence` / `dsh-session-query` / `dsh-lsp` / `dsh-workflow` 等为**非装配的抽象基座**，由 `*-local` / `*-jsonl` 等实现包注入；形成「实现包 → 抽象包」方向。
- **新域**：`browser-use`（5 包）/ `computer-use`（5 包）/ `ssh`（4 包，替代已删除的 e2b 三件套）/ `ptc-runtime`（3 包）/ `webhook`（2 包）/ `document` / `deliverables` / `util`（17 包）。
- **已删除**：`code-runtime/*`（4 包）、`e2b/*`（3 包）、`host/apiproxy`、`session/session-persistence-sqlite`、`settings/settings-file`、`workflow/workflow-worker-thread` 等 17 包。
- **类型导入占比高**：cordis 插件普遍使用 `import type {} from '@deepseek-ai/dsh-x'` 做 Context 声明合并，故 1077 条节点间边中 **281 条为纯类型边**（26%）——已显式标注，不参与分层。

## 质量门控

`07-checkpoint/quality-gate-l3.py` **ALL PASS**（0 error / 1 warning）：
1. JSON 合法（**84 个文件**，含 v017 全部中间产物）
2. DAG 无环（运行时边 795 条 → 239/239 可达）+ layers 全覆盖 + **分层方向一致性**（每条运行时边 level[from] > level[to]）
3. HTML：UTF-8 无替换字符 / div 开闭平衡 / 内链断链 **0**（373 页）
4. vendor 完整（cytoscape + dagre）
5. 插件页覆盖 **239/239 + 73/73 + 特殊 8/8**；`seam_edges` ↔ `referred_by` 一致性
6. 交互图 DATA：plugins=239 / seams=73 / groups=50 + disabled 样式选择器存在
7. MD 镜像覆盖 239/239 + 73/73
8. （唯一 WARN）含 type-only 边时存在 57 节点类型层环 —— TS 合法，仅上报

`headless-verify-l3.py`（`/snap/bin/chromium --headless=new`）：组级视图 `zmode=组级 / zcount=51`；下钻 `G01` → `zmode=G01 · ACP 协议 / zcount=10`（**断言下钻视图 ≠ 组级视图，防假绿**）；三张截图字节数各异，目视确认中文完整、图例 239/73/50、面包屑与 seam 虚线边正常。

## 已知保留项

- 页面中 `0.1.0-rc.8` / `0.1.1-rc.2` 等为各包**历史版本演进记录**，按设计保留。
- `type_only` 边在交互图中与运行时边同色显示（未做虚线区分），下游消费者可按 `edges[].type_only` 字段自行过滤。
- `05-source/dsh-v0.1.7-rc.2/` 的**解压树不入库**（155MB），仅 tarball + SHA256 入库；解压命令见该目录说明。
