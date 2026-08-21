# RC8 → RC2 差异分析报告

> DeepSeek Harness 插件级 DAG 知识库升级差异分析
> 分析日期：2026-08-21 ｜ 知识库：`0822-plugin-dag-v0.1.1-rc2`
> 基线：RC8（commit `141eb6f`，tag `dsh-v0.1.0-rc.8`，2026-08-19）→ 目标：RC2（commit `b150a551`，tag `dsh-v0.1.1-rc.2`，2026-08-21）
> 方法论：`version-upgrade-cascade`（三层差异分析 + 全量重生成 + 三重验证）

---

## 一、升级范围

| 维度 | RC8 | RC2 | 变化 |
|------|-----|-----|------|
| GitHub 对比 | 141eb6f → b150a551 | — | **207 commits**（2026-08-19 ~ 08-21） |
| packages 目录 | 226 包 | 227 包 | **新增 1 包、删除 0 包**（净 +1） |
| 版本号 | 0.1.0-rc.8 | 0.1.1-rc.2 | 全部包批量升级（minor 0→1） |
| 源码实质变化 | — | — | **43 包**（src/ 变更） |
| 仅 tests 变化 | — | — | **6 包** |
| 仅版本号变化 | — | — | **177 包** |
| DAG 节点 | 180 | **180** | 无新增/删除（RC2 新增包为 seam，不进入 DAG 节点集） |
| DAG 依赖边 | 578 | **578** | 无变化 |
| 分组 | 39 | **39** | 无变化 |
| 拓扑层 | 17 | **17** | 无变化 |
| 外部 seam | 49 | **50** | +1 `dsh-authorization` |

---

## 二、新增 1 包

### 新增包（seam）

| # | DAG 节点 | 包名 | 组 | 功能 |
|---|---------|------|----|------|
| 1 | `dsh-authorization`（seam） | @deepseek-ai/dsh-authorization | 外部基座 seam | Authorization seam（`ctx.authorization`）：插件拥有的、通过与人类对话获取凭据的流程注册与生命周期服务 |

新增包位于 `packages/credentials/authorization`，对外提供 `AuthorizationService`（`ctx.authorization.registerFlow`）与 `authorization/settled` 事件；自身依赖 `dsh-credentials`、`dsh-invariants`、`dsh-llm`、`cordis`。

---

## 三、官方 RC2 Release Notes 与源码映射

RC2 是 0.1.0-rc.8 之后的小版本迭代，核心主题是**凭据获取流程 seam 化**与**LLM 适配器工程化拆分**：

| Release Note 要点 | 涉及源码包 | 变更要点 |
|-------------------|-----------|---------|
| 新增 `ctx.authorization` seam，统一 OAuth/登录/授权对话流程 | `credentials/authorization`（新增） | 提供 `registerFlow`/`settled` 事件；把“需要人机对话才能拿到的凭据”抽象为可插拔 flow |
| Pi-AI 适配器接入 authorization flow | `llm/llm-pi-ai` | 新增 `@deepseek-ai/dsh-authorization` E1 依赖；`login.ts` 实现授权对话 |
| DeepSeek 适配器工程化：原子写、品牌、home 路径独立成库 | `llm/llm-deepseek` | 新增 `@deepseek-ai/dsh-atomic-write`、`@deepseek-ai/dsh-brand`、`@deepseek-ai/dsh-home-paths` E1 依赖 |
| 大量 UI/核心/适配器内部修复与测试增强 | `api/gateway`、`api/remotes`、`attachment/*`、`client/*`、`credentials/*`、`core/agent`、`extensions/*`、`host/apiproxy`、`jobs/*`、`session/*`、`subagent/*`、`web/*` 等 43 包 | 源码内部逻辑调整，未改变 DAG 拓扑 |

---

## 四、43 个源码实质变化包清单

按 domain 归类（完整记录见 `07-checkpoint/src-diff-rc8-rc2.json`）：

| domain | 变化包数 | 包 |
|--------|---------|----|
| api | 2 | gateway, remotes |
| attachment | 2 | attachment, attachment-local |
| client | 8 | connection, modules, runtime, ui-conversation, ui-primitives, ui-settings-models, ui-settings-plugins, ui-subagent, ui-theme, ui-user-questions, ui-workspace, web |
| credentials | 2 | credentials, credentials-local |
| core | 1 | agent |
| experimental | 2 | agent-team, tool-agent-team |
| extensions | 2 | cordis-client-runner, cordis-host-runner |
| fs | 1 | tool-fs |
| host | 1 | apiproxy |
| jobs | 2 | jobs, jobs-local |
| llm | 2 | llm-deepseek, llm-pi-ai |
| mcp | 1 | mcp-client |
| session | 2 | session-persistence, session-telemetry-otel |
| subagent | 5 | subagent, subagent-codex, subagent-claude-code, tool-subagent-control, tool-subagent-report |
| web | 3 | tool-web, web-search-deepseek, web-search-exa, web-search-perplexity |
| bundle/examples/interaction/test-support | 6（tests only） | bundle/web-app, examples/acp-demo, examples/agent-spine-demo, interaction/commands, mcp/mcp-client, test-support/client-runtime |

其中与 DAG 节点/边强相关、已更新 `external-seams.json` 的关键包：

| 包 | DAG 节点 | 变更类型 | 关键变更 |
|----|---------|---------|---------|
| credentials/authorization | dsh-authorization（seam） | 新增 seam | `ctx.authorization` 授权对话抽象 |
| llm/llm-pi-ai | dsh-llm-pi-ai | 新依赖 | +`dsh-authorization` E1 |
| llm/llm-deepseek | dsh-llm-deepseek | 新依赖 | +`dsh-atomic-write` / `dsh-brand` / `dsh-home-paths` E1 |

---

## 五、依赖关系变化（E1 编译依赖）

### 新增 seam 依赖（通过 `external-seams.json` 表达）

| seam | 新增 referred_by | 说明 |
|------|-----------------|------|
| `dsh-authorization` | `dsh-llm-pi-ai` | Pi-AI 适配器通过 authorization flow 获取凭据 |
| `dsh-atomic-write` | `dsh-llm-deepseek` | DeepSeek 适配器文件写入工具拆出 |
| `dsh-brand` | `dsh-llm-deepseek` | DeepSeek 适配器品牌/标识工具拆出 |
| `dsh-home-paths` | `dsh-llm-deepseek` | DeepSeek 适配器 home 路径解析拆出 |

### E3 组合依赖（装配文件）

- `packages/bundle/base/cordis.patch.yml`：**字节级一致**
- `packages/bundle/headless/cordis.patch.yml`：**字节级一致**
- `packages/bundle/web-app/cordis.patch.yml`：**字节级一致**
- `packages/subagent/subagent-claude-code/cordis.patch.yml`：**字节级一致**
- `packages/subagent/subagent-codex/cordis.patch.yml`：**字节级一致**

> 结论：RC2 装配位置零变化，新增 `dsh-authorization` 尚未进入 base/web-app/headless 装配。

---

## 六、知识库更新明细

### 数据层
- `webapp-dag.json`：180 节点 / 578 边 / 39 组 / 17 层，保持不变
- `external-seams.json`：49 → 50 seams；`dsh-authorization` 新增；`dsh-atomic-write` / `dsh-brand` / `dsh-home-paths` 的 `referred_by` 增加 `dsh-llm-deepseek`
- 版本标注：README / index / report 中「当前版本」`v0.1.0-rc.8` → `v0.1.1-rc.2`；各插件 `why.history` 中的 `0.1.0-rc.8` 作为历史版本记录保留

### 页面层（全量重生成）
- `02-plugin-pages/`：230 页（180 插件 + 50 seam，1 双身份共享）
- `03-groups/`：39 组页 + 索引
- `04-interactive/index.html`：DATA 更新（180 插件 + 50 seam + 829 边 + 40 组级节点），图例改为动态统计
- `06-md/`：180 插件 + 50 seam MD 镜像
- `08-special-modules/`：4 页保留

### 生成脚本调整
- `07-checkpoint/gen-overview.py`：图例文本从硬编码 `173/49/38` 改为基于 `core-dag.json` + `external-seams.json` 的动态统计
- `07-checkpoint/headless-verify-l3.py`：Chrome 路径改为 `/snap/bin/chromium`（本机 WSL2 可用）

---

## 七、验证结果

- **静态门控**：`quality-gate-l3.py` ALL PASS（7 项：JSON/DAG无环 180/180/HTML断链 0/vendor/插件页覆盖/DATA 校验/MD 覆盖，0 错误 0 警告）
- **headless DOM**（`/snap/bin/chromium --headless=new`）：
  - 组级视图：`zmode=组级`，`zcount=40`（39 组 + EXT），无 JS 错误
  - 截图：组级 / G30 下钻 / G37 下钻均成功生成且大于 10KB
- **源码三依据重验**：RC2 官方源码 `05-source/dsh-v0.1.1-rc.2/`；E1 依赖变化经 `07-checkpoint/deps-diff-rc8-rc2.py` 逐包核对
- **纯官方源码**：RC2 tarball 下载自 `https://github.com/deepseek-ai/deepseek-harness/archive/refs/tags/dsh-v0.1.1-rc.2.tar.gz`，SHA256 `142e2f67db41425e8a96a265f77d94997d6e222c9817075b9f34dfc9653bbf75`，无魔改

---

## 八、已知保留项

- 交互图 `04-interactive/index.html` 仍无 URL drill 路由（`?drill=` 参数未解析，仅点击下钻可用）——RC7 遗留，非本次引入
- 页面中 `0.0.1-rc.1` / `0.0.1-rc.3` / `0.1.0-rc.6` / `0.1.0-rc.8` 为各包**历史版本演进记录**，按设计保留
- `vendor/` 目录（@deepseek-ai/cordis 等）不在 packages/ 树内，后者为 seam（path 为空）
