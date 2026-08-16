# PLAN · 第三层：其余插件（39 插件节点 + 13 seam + 4 特殊模块）

> 本文件为**落盘接力文件**：第二层 web-app bundle（0816-plugin-dag）已完成，L3 范围与决策已核验。新窗口打开本文件即可续跑第三层。
> 生成日期：2026-08-17 ｜ 范围核验：2026-08-17（PACKAGE-MAP 219 包 vs 已分析 169 包）

## 任务背景

deepseek-harness 基于 cordis 插件机制 + 单向依赖 DAG 拼接。用户要以**官方基础插件为最小分析单元**，理解插件如何一步一步拼接成完整 harness。分三层执行，每层一个上下文窗口：
- L1 核心集（base bundle）✅ 已完成
- L2 web-app bundle ✅ 已完成 → 本任务目录 `0816-plugin-dag/`
- **L3 其余插件（本计划）**

## L3 范围（已精确核验 = 56 未覆盖包）

**比对方法**：`PACKAGE-MAP.json` 219 包 - 已分析 169 包（134 节点 + 36 seam，有 1 个 name 重复） = **56 未覆盖包**。
执行脚本：`07-checkpoint/list-l3-uncovered.py`（已落盘）。

### 56 包三分法（决策已确认）

| 类别 | 数量 | 处理 | 决策来源 |
|------|-----|------|---------|
| **特殊独立模块** | 4 | 单独一节分析，**不进主 DAG 插件节点** | 用户：bundle 自身+boot 层有相对独立性 |
| **归入 seam** | 13 | 追加到 `external-seams.json` | 用户：test-support 归 seam + L3 抽象基座并 seam |
| **L3 插件节点** | 39 | 进主 DAG（G30-G37 新组） | 默认 |

### 特殊独立模块（4）
```
@deepseek-ai/dsh-base        @ packages/bundle/base      (2 ts)  base bundle 自身
@deepseek-ai/dsh-headless    @ packages/bundle/headless  (3 ts)  独立 bundle，有 cordis.patch.yml
@deepseek-ai/dsh-app-boot    @ packages/boot/app-boot    (3 ts)  启动框架
@deepseek-ai/dsh-cmdline     @ packages/boot/cmdline     (2 ts)  命令行解析
```
> 分析方式：单独一节（README 或独立章节），描述装配结构，不建 DAG 节点（避免 E3 元信息边）。

### 归入 seam（13）
```
抽象基座 7: dsh-acp / dsh-e2b / dsh-hook-protocol / dsh-lsp / dsh-mcp-client / dsh-sdk-protocol / dsh-terminal
test-support 6: dsh-acp-snapshot / dsh-agent-loop-testkit / dsh-client-test-runtime / dsh-llm-mock-server / dsh-llm-replay / dsh-loader-smoke
```
> 追加到 `01-dag-data/external-seams.json`（schema 同 36 个已有 seam：id/name/path/description/referred_by/mechanisms/ref_count）。L3 采集时若 L3 插件依赖它们，referred_by 填 L3 插件 id。

### L3 插件节点（39，分 8 组）

| 组 | 名称 | 插件 |
|----|------|------|
| G30 | 外部执行后端 (6) | dsh-fs-e2b, dsh-subprocess-e2b, dsh-terminal-bash, dsh-tool-terminal, dsh-tool-bash-persistent, dsh-schedule |
| G31 | 协议与SDK (2) | dsh-sdk-client, dsh-sdk-jsonrpc-server |
| G32 | LSP集成 (2) | dsh-lsp-stdio, dsh-tool-lsp |
| G33 | 子代理外部后端 (4) | dsh-subagent-acp, dsh-subagent-claude-code, dsh-subagent-codex, dsh-subagent-dsh-sdk |
| G34 | Web上下文扩展 (6) | dsh-web-fetch-http, dsh-web-search-exa, dsh-web-search-perplexity, dsh-session-reference, dsh-time-context, dsh-tmux-context |
| G35 | 会话存储变体 (4) | dsh-session-persistence-sqlite, dsh-storage-sqlite, dsh-session-title-all-prompts-llm, dsh-tool-session-query |
| G36 | Hooks工具扩展 (6) | dsh-hooks-claude-code, dsh-hooks-codex, dsh-tool-cordis, dsh-tool-ask-user, dsh-persona, dsh-agent-tool-presentation |
| G37 | 示例与框架 (9) | dsh-acp-demo, dsh-agent-spine-demo, dsh-sdk-jsonrpc-demo, dsh-typert-generator, dsh-native-command, dsh-host-frontend-static, dsh-host-directory-picker, dsh-host-directory-picker-browse, dsh-host-directory-picker-native |

> ⚠️ **注意 host-directory-picker 三件套**：L2 已分析 client 前端（ui-directory-picker-browse/native），L3 补 **host 后端**（directory-picker 抽象 + browse/native 实现）——这是 L2 采集时发现的方向补齐。

## 三硬依据要点（L3 特殊性）

- **E3 几乎无**：56 包几乎都不在任何 bundle 装配中（仅 dsh-headless 在 headless patch 装配，dsh-base 是 base 自身）。E3 只用于 dsh-headless 装配行（若有）。
- **以 E1/E2 为主**：E1（package.json peerDeps + import）、E2（ctx 服务注入/事件订阅/协议实现）。
- **seam 方向**：抽象基座（lsp/mcp/e2b/terminal/hook-protocol/sdk-protocol/acp）被实现包依赖 → **实现包依赖抽象包**（如 dsh-subprocess-e2b → dsh-e2b, dsh-lsp-stdio → dsh-lsp）。

## 复用上一轮资产（关键！）

### 数据接口
- `01-dag-data/webapp-dag.json`：134 节点 / 434 边 / 17 拓扑层 / 29 组。schema：`nodes[{id,name,group,group_name,layer,implementation,provides,path,source_layer}]` + `edges[{from,to,mechanism,evidence,purpose,source_layer}]` + `groups` + `layers`。**L3 更新此文件**（→ ~173 节点 / 37 组）
- `01-dag-data/external-seams.json`：36 个外部 seam。**L3 追加 13 个**（→ 49 个）
- L3 插件若引用 L1/L2 已分析插件，直接链接 `../02-plugin-pages/{id}.html`，**不要重复采集**

### 生成管线（L2 版本直接改数据源）
- `07-checkpoint/gen-l3-inventory.py`：**L3 清单已生成**（stage-00-l3-inventory.json，39 插件 + 13 seam + 4 特殊模块）
- `07-checkpoint/build-dag-l2.py` → build-dag-l3.py：建模（读 webapp-dag.json + L3 采集 → 合并扩展）
- `07-checkpoint/gen-html-l2.py` → gen-html-l3.py：插件页 + 组页
- `07-checkpoint/inject-data-l2.py` → inject-data-l3.py：交互图 DATA
- `07-checkpoint/quality-gate-l2.py` → quality-gate-l3.py：门控
- `07-checkpoint/headless-verify-l2.py` → headless-verify-l3.py：headless + VLM

## 执行步骤

### S0 清单（已 95% 完成）
- [x] `list-l3-uncovered.py` 比对 56 包
- [x] `gen-l3-inventory.py` 生成 stage-00-l3-inventory.json（39 插件 8 组 + 13 seam + 4 特殊）
- [ ] 追加 13 seam 到 external-seams.json（schema 参照现有 36 个）

### S1 采集（5 路并行 explore）
| 路 | 范围 | 插件数 |
|----|------|-------|
| r1 | G30 外部执行后端 + G37 部分（e2b/terminal/schedule/directory-picker/frontend-static） | ~11 |
| r2 | G31 协议SDK + G32 LSP + G33 子代理后端 | ~8 |
| r3 | G34 Web上下文扩展 + G35 会话存储变体 | ~10 |
| r4 | G36 Hooks工具扩展 + 特殊模块（base/headless/app-boot/cmdline 结构分析） | ~10 |
| r5 | G37 示例框架（examples/typert-generator/native-command） | ~5 |

每路输出 stage-01-l3-r{N}.json（schema 同 L2：id/name/implementation/provides/depends_on[{plugin_id,mechanism,evidence,purpose}]/dependents）。
seam 路（r2 的抽象基座）额外输出 referred_by 供 external-seams.json 追加。

### S2 建模
- 复用 build-dag-l2.py 改造：读 webapp-dag.json + L3 采集 → 合并（~173 节点 / 37 组）→ 层次遍历重算拓扑层
- **L2 环修复方法论（必用）**：
  1. E3 装配元信息过滤（is_assembly_meta）
  2. slot/协议注册方向修正（实现依赖抽象）
  3. dependents 不反推边（删 7c 逻辑）
  4. 双向耦合合并节点（若真存在）
- 无环校验 + 组合引用拆分

### S3 交互图
- 复用 inject-data-l2.py：读 L3 扩展 DAG + external-seams.json（49 seam）→ 注入 DATA
- 组级视图：37 组（29 + 8）+ EXT；disabled 标注保留（22 个）
- ⚠️ 图例静态文字（29 组/134 插件 → 37 组/~173 插件）

### S4 插件页
- 复用 gen-html-l2.py：39 L3 页 + 更新总览 + L1/L2 页重生成（含 L3 下游）
- 特殊模块单独生成 `08-special-modules/` 页（base/headless/boot）

### S5 drawio
- 委派 drawio-worker 2-3 批，drawio-reference 强制加载
- 输出目录：`05-drawio/l3-{G30..G37}/` 或并入现有域目录
- 新增 seam 也补 drawio 参考页（可选）

### S6 门控
- quality-gate-l3.py 数据源切 L3 扩展 DAG，必须 ALL PASS
- headless + VLM 验证组级/下钻

### S7 接力
- 更新 README（L3 完成状态、~173 节点 / 37 组 / 49 seam / 特殊模块节）
- 生成 PLAN-layer4.md（若还有第四层；否则收尾总结）

## 坑与经验（L1+L2 实证，L3 必读）

1. **交互图 DATA 注入**：index.html 第 60 行是单行 `const DATA = {...};`，无 `__DATA__` 占位符；按行整体替换，保持 CRLF + UTF-8 无 BOM
2. **cytoscape 数据属性选择器**：必须 `node[kind="plugin"]` / `node[kind="disabled"]`（类选择器需 classes 字段，缺失全不命中）
3. **headless 验证**：`--dump-dom` 看 zmode/zcount，`--screenshot` + VLM 看 canvas；截图字节变化判断视图切换
4. **python -c 禁用**、**bash heredoc 禁用**：脚本独立 .py；subprocess 捕获 Chrome DOM 用 bytes + utf-8 decode（GBK 报错）
5. **大采集输出截断**：>15 插件/路会触发 task 输出截断，拆更小批或要求子Agent 分文件落盘
6. **drawio 导出 scale=2**（避免视口上限截断）；MCP 挂起用同源 exportDiagram() 直调
7. **L2 环修复方法论**：E3 过滤 + slot 方向 + dependents 不反推 + 双向合并，L3 复用为破环标准流程
