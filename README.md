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
| **主页仪表盘**（核心统计条 + 主入口三卡 + 分区总览） | `index.html` |
| **交互 DAG 总览**（组级视图 + 点击下钻 + `?drill=Gxx` 深链） | `04-interactive/index.html` |
| 分组目录（区 → 簇卡片 + seam 分区默认折叠） | `03-groups/index.html` |
| 每插件一页（含**模块内部结构动态 DAG**） | `02-plugin-pages/`（312 页） |
| 特殊模块结构（base/web-app/sdk/boot…） | `08-special-modules/`（8 页） |
| 任务报告 | `report.html`（人类版） / `report.md`（AI 镜像） |
| AI 检索 MD 镜像 | `06-md/00-index.md`（239 插件 + 73 seam 全量） |
| 差异报告（AI 镜像，3 份） | `RC2-0.1.7-DIFF-REPORT.md` / `RC7-RC8-DIFF-REPORT.md` / `RC8-RC2-DIFF-REPORT.md` |
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
├── 07-checkpoint/        # 生成管线（含 v017/ 本轮全量重建中间产物、prototype/ 评审原型生成器）
├── 08-special-modules/   # 特殊模块 8 页
├── 09-prototype/         # 评审原型（只读 demo，**非生产入口**；生成器见 07-checkpoint/prototype/）
└── index.html            # 根入口
```

> ⚠️ `09-prototype/` 与 `07-checkpoint/prototype/` 原为带 `_` 前缀的 demo 目录。因 **GitHub Pages 的 Jekyll 会忽略 `_` 前缀目录**，其内容上线即不可见，故本次统一去前缀改名为上述目录。**目录名不含 `_` 前缀**是 Pages 可见的硬前提，后续勿再改回。

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
| `gen-html-l3.py` | HTML 全量生成器（`--only {all,plugin-pages,groups-pages,groups-index,special}` 分阶段；**默认 dry-run，须显式 `--write` 才落盘** —— 2026-09-27 误跑事故的根因修复，见下） |
| `gen-plugin-dyn.py` | 插件页「动态 DAG」**事后注入器**（跑完 `gen-html-l3.py --only plugin-pages --write` 后必须补跑，否则插件页丢区块） |
| `gen-overview.py` | `04-interactive/index.html` 的**唯一权威生成器**（组级 `layout:'preset'` + 下钻数据，坐标 Python 侧算定，渲染零随机） |
| `inject-data-l3.py` | `04-interactive/index.html` 的**幂等 DATA 同步器**（复用 `gen-overview.build_payload()` 同一 payload 原地替换 `const DATA = ...;`；内容一致时不改动字节） |
| `gen-root-index.py` | 根 `index.html` 主页**唯一生成器**（统计数字全部从 `webapp-dag.json` / `external-seams.json` 派生；确定性，重复运行 byte-identical） |
| `prototype/gen-{grid,groups,home}-demo.py` | `09-prototype/` **评审原型** 3 页生成器（只读产出，**非生产入口**；页面顶部带「本页为评审原型」醒目标注） |
| `gen-md-l3.py` | `06-md/` AI 检索镜像生成器 |
| `quality-gate-l3.py` | 结构/数据一致性门控（8 项，已强化：纳入 v017 全部 JSON / 8 特殊模块全集 / seam_edges↔referred_by 一致性 / 分层方向一致性） |
| `quality-gate-readable.py` | 可读性/骨架不变量门控（A–F 六项 + `--selftest` 负向自检，见「质量门控」） |
| `headless-verify-l3.py` | chromium headless DOM 断言（**非空断言**：下钻视图 ≠ 组级视图）+ 截图 |

> ⚠️ **管线配对顺序（事故机制，务必遵守）**：`gen-html-l3.py` 生成的插件页**不含**「动态 DAG」区块，
> 该区块由 `gen-plugin-dyn.py` **事后注入**。因此执行 `gen-html-l3.py --only plugin-pages --write`
> （或 `--only all --write`）之后，**必须补跑** `python3 07-checkpoint/gen-plugin-dyn.py`，
> 否则 239 个插件页会丢失动态 DAG（每页约 −3982 字符）。
> 2026-09-27 02:43 的误跑事故正是：一次 `python3 gen-html-l3.py --help`（当时该脚本无 argparse，
> `--help` 被静默忽略 → 全量执行）重写了 `02-plugin-pages`(239) + `03-groups`(51) + `08-special-modules`(8)，
> 冲掉 `gen-plugin-dyn.py` 注入层，靠 `git checkout` 回滚。现已加「默认 dry-run + 显式 `--write`」保护，
> 并由可读性门控判据 **D**（`id="dyn-dag"` 覆盖数 == `len(nodes)`）作事故防线：下次误跑即刻报警。

## 关键发现（v0.1.7-rc.2）

- **装配分层重构**：新增 3 个 bundle（`acp-app` / `sdk-app` / `sdk-minimal`），base 装配 93 行、web-app 85 行、sdk-minimal 32 行；`dsh-sdk-minimal` 不叠 base、自身即完整 Cordis 树。
- **客户端层大扩张**：client 域 61 包（含 41 个 `ui-*`），web-app 单 bundle 装配 85 行；客户端 UI 与 `dsh-api-remotes` 存在 1 处运行时注册回环（已标 soft）。
- **抽象基座 seam 化**：`dsh-fs` / `dsh-sandbox` / `dsh-spill` / `dsh-jobs` / `dsh-shell` / `dsh-subprocess` / `dsh-attachment` / `dsh-compaction` / `dsh-credentials` / `dsh-session-persistence` / `dsh-session-query` / `dsh-lsp` / `dsh-workflow` 等为**非装配的抽象基座**，由 `*-local` / `*-jsonl` 等实现包注入；形成「实现包 → 抽象包」方向。
- **新域**：`browser-use`（5 包）/ `computer-use`（5 包）/ `ssh`（4 包，替代已删除的 e2b 三件套）/ `ptc-runtime`（3 包）/ `webhook`（2 包）/ `document` / `deliverables` / `util`（17 包）。
- **已删除**：`code-runtime/*`（4 包）、`e2b/*`（3 包）、`host/apiproxy`、`session/session-persistence-sqlite`、`settings/settings-file`、`workflow/workflow-worker-thread` 等 17 包。
- **类型导入占比高**：cordis 插件普遍使用 `import type {} from '@deepseek-ai/dsh-x'` 做 Context 声明合并，故 1077 条节点间边中 **281 条为纯类型边**（26%）——已显式标注，不参与分层。

## 质量门控

本库有两道相互独立、可机检的门控：

### 1. `07-checkpoint/quality-gate-l3.py` —— 结构 / 数据一致性

**ALL PASS**（当前实测：ERRORS 0 / WARNINGS 1）：
1. JSON 合法（**85 个文件**，含 v017 全部中间产物）
2. DAG 无环（运行时边 795 条 → 239/239 可达）+ layers 全覆盖 + **分层方向一致性**（每条运行时边 level[from] > level[to]）
3. HTML：UTF-8 无替换字符 / div 开闭平衡 / 内链断链 **0**（373 页）
4. vendor 完整（cytoscape + dagre）
5. 插件页覆盖 **239/239 + 73/73 + 特殊 8/8**；`seam_edges` ↔ `referred_by` 一致性
6. 交互图 DATA：plugins=239 / seams=73 / groups=50 + disabled 样式选择器存在
7. MD 镜像覆盖 239/239 + 73/73
8. （唯一 WARN）含 type-only 边时存在 57 节点类型层环 —— TS 合法，仅上报

### 2. `07-checkpoint/quality-gate-readable.py` —— 可读性 / 骨架不变量

**ALL PASS**（A–F 全 OK；阈值全部由「逐页统计 / 数据源长度」推导，非拍脑袋）：
- **A 页面区块骨架**：DAG 插件页 239/239 命中「插件信息 / ① 实现逻辑 / ② 注册/提供（provides）/ ③ 依赖（depends_on·上游前驱）/ ④ 被依赖（dependents·下游消费者）」五段；seam 页 73/73 命中「基座 seam 说明 / 被依赖（下游）/ 依赖机制分布」三段
- **B `.md` 链接自标注 + HTML 人类入口**：站内 5 条 `.md` 链接的链接文本均含 `MD`/`Markdown`/`AI`；且 `index.html` 链接 `report.html` 且该文件存在（人类入口一律 HTML，`.md` 仅作 AI/机器镜像且必须自标注形态）
- **C `index.html` 统计一致性**：统计块数字与数据源实测一致（239/73/1077/19/50/312）
- **D 动态 DAG 注入覆盖**：含 `id="dyn-dag"` 的插件页数 == `len(nodes)` == 239（**事故防线**）
- **E 主图不变量**：`grp-` 节点 51 == 50 组 + EXT；组级为确定性 `layout:'preset'`（节点含 position、无 dagre 组级布局）；差异化高亮三色语义（上游橙 `#e8933b` / 下游绿 `#2fb98a` / 自身蓝 `#4f8cff`）
- **F 分组索引不变量**：`03-groups/index.html` 的 `Gxx` 链接去重 50、`../02-plugin-pages/*.html` 链接去重 73、区锚点 `L1/L2/L3` 各 1、簇锚点 `F1..F9` 各 1

> `quality-gate-readable.py --selftest` 为内置**负向自检**：对每个判据在临时副本上定点破坏
> （删区块 / 换无标注链接文本 / 删 `id="dyn-dag"` / 删 grp- 节点 / 改区锚点），断言对应判据
> **确实 FAIL**（证明判据非恒真），真实产物零改动。

`headless-verify-l3.py`（`/snap/bin/chromium --headless=new`）：组级视图 `zmode=组级 / zcount=51`；下钻 `G01` → `zmode=G01 · ACP 协议 / zcount=10`（**断言下钻视图 ≠ 组级视图，防假绿**）；三张截图字节数各异，目视确认中文完整、图例 239/73/50、面包屑与 seam 虚线边正常。

## 已知保留项

- 页面中 `0.1.0-rc.8` / `0.1.1-rc.2` 等为各包**历史版本演进记录**，按设计保留。
- `type_only` 边在交互图中与运行时边同色显示（未做虚线区分），下游消费者可按 `edges[].type_only` 字段自行过滤。
- `05-source/dsh-v0.1.7-rc.2/` 的**解压树不入库**（155MB），仅 tarball + SHA256 入库；解压命令见该目录说明。
- `02-plugin-pages/*.html` 与 `03-groups/G*.html` 内嵌的 **50 组 treenav 本轮未改**（仍为平铺 chip，未做层级折叠）。
- `03-groups/index.html` 已改为**区 / 簇卡片目录**，seam 分区以 `<details>` **默认折叠**。
