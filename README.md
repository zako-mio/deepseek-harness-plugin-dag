# DeepSeek Harness 插件级 DAG 依赖链分析

> **版本**：`v0.2.1-alpha.2`（基于官方源码 dsh-v0.2.1-alpha.2，2026-10-09 发布，commit `d7432673`）
> **留档位置**：本库于 2026-10-11 由 `Mission-file/2026-09/0927-dsh-plugin-dag-017rc2` 整仓迁移至 `Mission-file/2026-10/1011-dsh-plugin-dag-021alpha2`（Git 仓与远端不变；历史差异报告中的旧目录名为迁移前名称）。
> **升级记录**：RC5 → RC7（08-19）→ RC8（08-20）→ RC2（08-21）→ 0.1.7-rc.2（09-27 全量重建）→ **0.2.1-alpha.2（10-11 增量级联）**。本次跨度 **21403 commits**，包树（按 id）321 → **340**（+21 / −2）。与前一轮不同，本轮 **319 个共同包中仅 180 个源码变化**（122 个仅版本号变化），故走**增量级联**：248 节点中 **93 个复用旧版分析、155 个重做**（复用率 37.5%）。详见 `017rc2-021alpha2-DIFF-REPORT.md`。

## 简介

以 **cordis 插件为最小分析单元**，回答三个问题：
1. **该插件以什么逻辑实现了什么功能**（实现逻辑 + provides）
2. **该插件依赖哪些插件的哪些功能**（depends_on 上游）
3. **该插件的哪些功能被谁依赖**（dependents 下游）

依赖判定**三硬依据 + 源码行引用**，逐条可溯源：
- **E1 编译依赖**：package.json peerDependencies / import 语句
- **E2 运行时依赖**：ctx 服务注入 / ctx.get / 事件订阅
- **E3 组合依赖**：cordis.patch.yml 装配位置

## 核心数据（v0.2.1-alpha.2）

| 指标 | 数值 |
|---|---|
| 插件节点 | **248**（L1 核心 91 + L2 web-app 84 + L3 其余 73） |
| 节点间依赖边 | **1167**（另 **584** 条指向 seam 的边，经 `external-seams.referred_by` 表达） |
| 外部 seam 基座 | **83**（抽象基座 / 工具库 / 测试支撑） |
| 拓扑层 | **17**（最长路径分层：被依赖方先于依赖方） |
| 分组 | **48**（按 `packages/<域>` 划分，客户端 UI 独立成组） |
| HTML 插件页 | **331**（248 插件 + 83 seam）+ 48 组页 + 8 特殊模块页（共 388 文件） |
| 装配行 disabled 标注 | **18** 行（映射到 **16** 个唯一节点） |

> 判据统计口径：`edges` 仅含**节点间**边（schema 约定，避免页面生成器 KeyError）；指向纯 seam 的边不重复计入 `edges`，改由 `external-seams.json` 的 `referred_by` 表达。
> 拓扑只由**运行时边**决定（排除 type-only 类型导入边 324 条 + 1 条 soft 反馈边）；TS 类型层 import 环合法，门控仅作 WARN 上报。

## 范围分层（装配来源）

| 层 | 范围 | 插件数 |
|----|------|-------|
| **L1 核心集** | `bundle/base/cordis.patch.yml`（94 条 insert 行） | 91 核心 |
| **L2 web-app** | `bundle/web-app/cordis.patch.yml`（87 条 insert 行，含全部客户端 UI 包） | 84 |
| **L3 其余** | 各 bundle 之外的可挂载插件：web 搜索变体、SSH、Browser-Use、Computer-Use、实验特性、会话格式、deliverables、hooks 等 | 73 |
| **特殊模块** | base/headless/web-app/sdk-app/sdk-minimal/acp-app（bundle）+ app-boot/cmdline（boot 胶水） | 8（独立成页，不进 DAG） |

## 快速开始

| 想做什么 | 去哪 |
|---------|------|
| **主页仪表盘**（核心统计条 + 主入口三卡 + 分区总览） | `index.html` |
| **交互 DAG 总览**（组级视图 + 点击下钻 + `?drill=Gxx` 深链） | `04-interactive/index.html` |
| 分组目录（区 → 簇卡片 + seam 分区默认折叠） | `03-groups/index.html` |
| 每插件一页（含**模块内部结构动态 DAG**） | `02-plugin-pages/`（331 页） |
| 特殊模块结构（base/web-app/sdk/boot…） | `08-special-modules/`（8 页） |
| 任务报告 | `report.html`（人类版） / `report.md`（AI 镜像） |
| AI 检索 MD 镜像 | `06-md/00-index.md`（248 插件 + 83 seam 全量） |
| 差异报告（AI 镜像，4 份） | `017rc2-021alpha2-DIFF-REPORT.md` / `RC2-0.1.7-DIFF-REPORT.md` / `RC7-RC8-DIFF-REPORT.md` / `RC8-RC2-DIFF-REPORT.md` |
| DAG 数据（JSON） | `01-dag-data/webapp-dag.json`（248 节点 + 1167 边 + 584 seam_edges） |
| 模块级 import 数据 | `07-checkpoint/plugin-internal-all.json` |

## 目录结构

```
1011-dsh-plugin-dag-021alpha2/
├── 01-dag-data/          # webapp-dag.json（248节点/1167边/17层/48组/584 seam_edges）/ core-dag.json（L1 91节点/270边）/ external-seams.json（83 seam）
├── 02-plugin-pages/      # 每插件一页 HTML（248 插件 + 83 seam = 331 页）
├── 03-groups/            # 48 组索引页 + 组目录
├── 04-interactive/       # cytoscape 交互总览（组级 + 下钻 + URL 深链）+ vendor/
├── 05-source/            # 官方源码：dsh-rc8 / dsh-v0.1.1-rc.2 / dsh-v0.1.7-rc.2 / dsh-v0.2.1-alpha.2（tarball+SHA256；解压树 gitignore）
├── 06-md/                # AI 友好 MD 镜像
├── 07-checkpoint/        # 生成管线（含 v017/ 与 v021/ 两轮中间产物、prototype/ 评审原型生成器）
├── 08-special-modules/   # 特殊模块 8 页
├── 09-prototype/         # 评审原型（只读 demo，**非生产入口**；生成器见 07-checkpoint/prototype/）
└── index.html            # 根入口
```

> ⚠️ `09-prototype/` 与 `07-checkpoint/prototype/` 原为带 `_` 前缀的 demo 目录。因 **GitHub Pages 的 Jekyll 会忽略 `_` 前缀目录**，其内容上线即不可见，故统一去前缀改名为上述目录。**目录名不含 `_` 前缀**是 Pages 可见的硬前提，后续勿再改回。

## 增量级联管线（07-checkpoint/v021-*，可重放）

本轮在既有 v017 全量管线上**新增增量层**，只对变化/新增包重做源码分析：

| 脚本 | 作用 |
|------|------|
| `v021-inventory.py` | 解析 6 个 bundle `cordis.patch.yml` + 枚举 `packages/*/*` 与 `vendor/*` → `v021/inventory.json` |
| `v021-facts.py` | 逐包扫 `src/**/*.ts` 提取 E1 import（含 file:line）/ E2 inject·ctx·事件 / 插件导出特征 → `v021/facts.json` |
| `v021-classify.py` | 分类 nodes / seams / special / uncovered + 分组 → `v021/classification.json`（248 节点 / 83 seam / 48 组） |
| **`v021-delta.py`** | **以包 id 为键**（非目录路径）对比两版源码树 → `v021/delta-017-021.json`。关键：本轮有 10 处「同 id 换目录」搬迁，按路径比对会误判为「删除+新增」 |
| **`v021-merge-reuse.py`** | **增量核心**：对每个新节点判定「复用 / 重做」→ `v021/reuse-map.json` + `v021/stage-01-shard-00-reuse.json`（93 条复用 entry）。附**证据存活性自检**（解析复用 entry 的 file:line，共 874 条） |
| `v021-make-shards.py` | **仅对 redo 集合**分片（155 插件 → 13 分片），复用节点不进分片 |
| （委派）13 个子 Agent | 逐插件实读源码 → `v021/stage-01-shard-*.json`（含 implementation / provides / depends_on / evidence） |
| `v021-validate.py` | 回盘复验：13 分片 + 1 复用片 ∪ == 节点全集；条目数 / ids / 证据格式 |
| `v021-build-dag.py` | 合并全部 stage-01 → DAG（最长路径分层 + 反馈边 soft + type-only 标注）→ `01-dag-data/*.json` |
| `v021-prep-inputs.py` | 生成 `special-modules.json`（8 模块）/ `disabled-rows.json`（18 行） |
| `v021-clean-pages.py` | 删除不在新节点集内的陈旧页面（本轮移除 6 个） |

生成器与门控（v017 时代建立，本轮仅参数化到 `v021/`）：

| 脚本 | 作用 |
|------|------|
| `gen-html-l3.py` | HTML 全量生成器（`--only {all,plugin-pages,groups-pages,groups-index,special}` 分阶段；**默认 dry-run，须显式 `--write` 才落盘**） |
| `gen-plugin-dyn.py` | 插件页「动态 DAG」**事后注入器**（跑完 `gen-html-l3.py --only plugin-pages --write` 后必须补跑） |
| `gen-overview.py` | `04-interactive/index.html` 的**唯一权威生成器**（组级 `layout:'preset'` + 下钻数据，坐标 Python 侧算定，渲染零随机） |
| `inject-data-l3.py` | `04-interactive/index.html` 的**幂等 DATA 同步器**（内容一致时不改动字节） |
| `gen-root-index.py` | 根 `index.html` 主页**唯一生成器**（统计数字全部从 DAG/seam 数据派生；确定性，重复运行 byte-identical） |
| `prototype/gen-{grid,groups,home}-demo.py` | `09-prototype/` **评审原型** 3 页生成器（只读产出，**非生产入口**） |
| `gen-md-l3.py` | `06-md/` AI 检索镜像生成器 |
| `quality-gate-l3.py` | 结构/数据一致性门控（8 项） |
| `quality-gate-readable.py` | 可读性/骨架不变量门控（A–F 六项 + `--selftest` 负向自检） |
| `headless-verify-l3.py` | chromium headless DOM 断言（**非空断言**：下钻视图 ≠ 组级视图）+ 截图 |

> ⚠️ **管线配对顺序（事故机制，务必遵守）**：`gen-html-l3.py` 生成的插件页**不含**「动态 DAG」区块，
> 该区块由 `gen-plugin-dyn.py` **事后注入**。因此执行 `gen-html-l3.py --only plugin-pages --write`
> （或 `--only all --write`）之后，**必须补跑** `python3 07-checkpoint/gen-plugin-dyn.py`，
> 否则 248 个插件页会丢失动态 DAG（每页约 −3982 字符）。
> 2026-09-27 的误跑事故正是如此（当时 `--help` 被静默忽略 → 全量执行），靠 `git checkout` 回滚。
> 现已加「默认 dry-run + 显式 `--write`」保护，并由可读性门控判据 **D**（`id="dyn-dag"` 覆盖数 == `len(nodes)`）作事故防线。

> ⚠️ **分类学表有三份副本，改动须同步**：区/簇/组映射（`F1..F9` + EXT、`L1/L2/L3`）同时存在于
> `gen-html-l3.py`（`GROUP_CLUSTERS`）、`gen-overview.py`（`CLUSTERS`）、`gen-root-index.py`（`CLUSTERS` + `REGION` + `REGION_GROUPS_EXPECTED`）。
> 三者均对「展开是否恰好覆盖全部组」做硬断言；改分组必须三处同改，否则生成器直接 `SystemExit`。
> 本轮已将三处全部改为**数据派生**（不再写死 50 / 264 / 19 等旧版统计量）。

## 关键发现（v0.2.1-alpha.2）

- **增量级联首次可行**：上轮 0.1.1→0.1.7 是 210/210 共同包源码全变（被迫全量重建）；本轮 319 个共同包中仅 **180 个源码变化**，122 个仅版本号变化，故 93 个节点可直接复用旧分析。强验证信号：新增的 151 条节点间边**100% 来自重做节点**，复用节点零新增边。
- **域重组**：`hooks` / `webhook` / `runtime-diagnostics` 三个域消失，其包整体迁入 `experimental/`（10 处搬迁）；新增 `telemetry` 域。
- **破坏性变更落地**：`runtime-diagnostics/invariants`（`dsh-invariants`）随「移除运行时 invariant 插件及各包 `./invariant` 导出」被真删；`subagent-in-process-driver` 随「统一子代理执行与完成通知」被删。
- **新能力成节点**：`working_directory` 工具（2 包）、`tool-schedule`、`otel` 遥测、`client/product-analytics`、CoT 机器翻译（3 包）、Git Worktrees（2 包）、Claude Code Mods（2 包）、session-inspector。
- **节点重分类**：`dsh-scope`（`core/scope`）与 `dsh-hook-protocol` 从 DAG 节点**降级为 seam**（不再具备插件导出特征），故节点集是 +12 / −3 而非简单相加。
- **客户端层仍是变更重心**：`client` 域 45 包源码变化，占全部 180 个变化包的 **25%**。
- **类型导入占比上升**：1167 条节点间边中 **324 条为纯类型边**（27.8%，上轮 26%）——已显式标注，不参与分层。

## 质量门控

本库有两道相互独立、可机检的门控：

### 1. `07-checkpoint/quality-gate-l3.py` —— 结构 / 数据一致性

**ALL PASS**（当前实测：ERRORS 0 / WARNINGS 1）：
1. JSON 合法（**64 个文件**，含 v021 全部中间产物）
2. DAG 无环（运行时边 842 条 → 248/248 可达）+ layers 全覆盖 + **分层方向一致性**（每条运行时边 level[from] > level[to]）
3. HTML：UTF-8 无替换字符 / div 开闭平衡 / 内链断链 **0**（390 页）
4. vendor 完整（cytoscape + dagre）
5. 插件页覆盖 **248/248 + 83/83 + 特殊 8/8**；`seam_edges` ↔ `referred_by` 一致性
6. 交互图 DATA：plugins=248 / seams=83 / groups=48 + disabled 样式选择器存在
7. MD 镜像覆盖 248/248 + 83/83
8. （唯一 WARN）含 type-only 边时存在 **62 节点**类型层环 —— TS 合法，仅上报

### 2. `07-checkpoint/quality-gate-readable.py` —— 可读性 / 骨架不变量

**ALL PASS**（A–F 全 OK；阈值全部由「逐页统计 / 数据源长度」推导，非拍脑袋）：
- **A 页面区块骨架**：DAG 插件页 248/248 命中「插件信息 / ① 实现逻辑 / ② 注册/提供（provides）/ ③ 依赖（depends_on·上游前驱）/ ④ 被依赖（dependents·下游消费者）」五段；seam 页 83/83 命中「基座 seam 说明 / 被依赖（下游）/ 依赖机制分布」三段
- **B `.md` 链接自标注 + HTML 人类入口**：站内 6 条 `.md` 链接的链接文本均含 `MD`/`Markdown`/`AI`；且 `index.html` 链接 `report.html` 且该文件存在（人类入口一律 HTML，`.md` 仅作 AI/机器镜像且必须自标注形态）
- **C `index.html` 统计一致性**：统计块 6 项数字与数据源实测一致（248/83/1167/48/331）
- **D 动态 DAG 注入覆盖**：含 `id="dyn-dag"` 的插件页数 == `len(nodes)` == 248（**事故防线**）
- **E 主图不变量**：`grp-` 节点 49 == 48 组 + EXT；组级为确定性 `layout:'preset'`（节点含 position、无 dagre 组级布局）；差异化高亮三色语义（上游橙 `#e8933b` / 下游绿 `#2fb98a` / 自身蓝 `#4f8cff`）
- **F 分组索引不变量**：`03-groups/index.html` 的 `Gxx` 链接去重 48、`../02-plugin-pages/*.html` 链接去重 83、区锚点 `L1/L2/L3` 各 1、簇锚点 `F1..F9` 各 1

> `quality-gate-readable.py --selftest` 为内置**负向自检**：对每个判据在临时副本上定点破坏
> （删区块 / 换无标注链接文本 / 删 `id="dyn-dag"` / 删 grp- 节点 / 改区锚点），断言对应判据
> **确实 FAIL**（证明判据非恒真），真实产物零改动。本轮实测 7 项负例全部如期 FAIL。

`headless-verify-l3.py`：组级视图 `zmode=组级 / zcount=49`；hover `G06` 的**排他三分类**（橙 only 21 / 绿 only 3 / 双向 3 / dim 21）与从 `DATA.groupEdges` **独立复算的结果逐项一致**；下钻 `G06` → `zmode=G06 · 客户端 UI 包 / zcount=79`（**断言下钻视图 ≠ 组级视图，防假绿**）；49 组下钻几何全部 0 相交 / 标签内嵌 / 无出界 / `zoom>=0.9`；0 个 JS 报错；3 张截图产出。

> 浏览器路径为**自动探测**：优先 playwright 自带 chrome-for-testing，回退系统/snap chromium。
> 本机 snap chromium 因缺 `cap_dac_override` 在容器内无法启动，故必须支持回退。

## 已知保留项

- 页面中 `0.1.0-rc.8` / `0.1.1-rc.2` / `0.1.7-rc.2` 等为各包**历史版本演进记录**，按设计保留。
- `type_only` 边在交互图中与运行时边同色显示（未做虚线区分），下游消费者可按 `edges[].type_only` 字段自行过滤。
- `05-source/dsh-v0.2.1-alpha.2/` 的**解压树不入库**（165MB），仅 tarball + SHA256 入库；解压命令见该目录说明。
- `02-plugin-pages/*.html` 与 `03-groups/G*.html` 内嵌的 **48 组 treenav 未改**（仍为平铺 chip，未做层级折叠）。
- `03-groups/index.html` 为**区 / 簇卡片目录**，seam 分区以 `<details>` **默认折叠**。
- `07-checkpoint/v017/` 保留为**上一轮（0.1.7-rc.2）的中间产物**，是本轮复用分析的来源，**勿删**。
