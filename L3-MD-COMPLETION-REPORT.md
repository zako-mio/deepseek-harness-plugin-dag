# L3 补全执行报告 · MD 镜像全量 + 缺口核查（2026-08-17）

> 追加：disabled 节点点击修复（2026-08-17）见文末 §6。

## 1. 当时情况

L3 主任务完成后，用户指出"有部分插件的分析没有做"，点名 dsh-skill-filesystem / dsh-tool-skill 在主 DAG 上有节点但"没有对应 html"，且交互图出现红框。经核查，这暴露了 L3 交付的一个真实缺口：**06-md/ AI 检索镜像只覆盖 L1**（112 个 = 76 插件 + 36 seam），L2 的 58 插件与 L3 的 39 插件 + 13 新增 seam 全部没有 MD 镜像。

## 2. 制定计划

1. **全量核查**：写 audit 脚本对比 PACKAGE-MAP 219 包 vs DAG 节点 / seam / 特殊模块 / HTML / drawio / MD，定位所有真实缺口
2. **区分三类"缺失"**：
   - 真实缺口（MD 镜像）→ 补
   - 设计行为（disabled 红框）→ 确认 + 文档说明
   - 命名体系差异（0814 目录）→ 确认非缺失
3. **补 MD**：改造 gen-md.py 数据源 → webapp-dag.json（L1+L2+L3 合并）+ external-seams.json（49 seam）
4. **门控强化**：quality-gate-l3.py 新增 MD 镜像覆盖校验

## 3. 执行情况

**核查阶段**（audit-all-gaps.py）：
- PACKAGE-MAP 219 包中 dsh-\* 未覆盖数 = **0**（主 DAG 无缺口）
- HTML 插件页 221 页全覆盖（**0 缺**）
- drawio 174 张全覆盖（含 L3 39 张）
- **MD 镜像缺口确认**：96 插件（L2 57 + L3 39）+ 13 seam = 109 个缺失
- 根因：gen-md.py 数据源硬编码 core-dag.json（L1 专用），从未切换到 webapp-dag.json

**红框核查**：
- dsh-skill-filesystem / dsh-tool-skill 的 HTML 页面**均存在**（02-plugin-pages/ 221 页全覆盖）
- 红框 = **disabled 设计样式**：两插件在 `stage-00-l2-inventory.json` 的 `disabled_base_rows`（web 变体禁用 base 插件，22 个），交互图 `node[kind="disabled"]` → 灰色红边 `#c0504d`
- 0814 目录（L1 9 层架构分析）命名体系不同（L3-M04-tools 等），skill 相关已覆盖，非缺失

**补全执行**：
- 新建 `gen-md-l3.py`（数据源 webapp-dag.json + external-seams.json，插件 MD 含来源层标注，索引更新 173/49/17/37）
- 重跑：06-md/plugins/ 从 112 → **221 个**（173 插件 + 49 seam 全量）
- 00-index.md 统计更新为"173（76+58+39）/ 49 seam / 545 边 / 17 层 / 37 组"
- quality-gate-l3.py 新增第 8 项 MD 覆盖校验（173/173 + 49/49）
- README 增加红框说明

## 4. 完成情况

| 交付物 | 数量 | 状态 |
|--------|------|------|
| 06-md/plugins/ | 221 个 MD（173 插件 + 49 seam） | ✅ 全量 |
| 00-index.md | 173（76+58+39）/ 49 / 545 / 17 / 37 | ✅ 更新 |
| 01-groups.md / 02-layers.md | 37 组 / 17 层重建 | ✅ |
| quality-gate-l3.py | 8 项全 PASS（新增 MD 覆盖） | ✅ ALL PASS |
| README.md | 红框说明 + MD 全量标注 | ✅ |
| dsh-skill-filesystem / dsh-tool-skill | HTML 存在 + MD 补全 + 红框确认设计 | ✅ |

**改动文件**：
- 新增：`07-checkpoint/gen-md-l3.py`
- 修改：`06-md/plugins/*.md`（+109 个）、`06-md/00-index.md`、`01-groups.md`、`02-layers.md`、`07-checkpoint/quality-gate-l3.py`、`README.md`

## 5. 反思/分析/建议

**过程反思**：
1. **"看起来缺失"≠"真的缺失"**：用户看到红框以为缺页面，实际是 disabled 设计标注；审计脚本逐项核实后才区分三类（真缺 / 设计 / 命名差异），避免误补
2. **MD 镜像断档的根本原因**：gen-md.py 绑定 L1 数据源（core-dag.json），L2/L3 的 PLAN 未把 MD 生成纳入管线（只列了 gen-html/inject/quality-gate）——跨窗口任务必须逐项核对交付物清单的**每个产物**是否在后续窗口继续生成
3. **门控要覆盖所有交付物**：quality-gate 原 7 项不含 MD，导致 109 个缺失静默存在；现在第 8 项 MD 覆盖校验可防回归

**经验教训**：
- 多窗口接力任务：每个窗口开始前先跑一遍"交付物覆盖率审计"，避免新窗口只补主产物漏掉辅助产物
- disabled 视觉标注（红框）需要在 README/图例中显式说明，否则用户误判为缺失

**未来建议**：
- 若后续还有新层，直接把"MD 镜像覆盖"作为每个窗口的必做项（gen-md-l3.py 已支持增量）
- 0614/0816 两套产物（架构分析 vs 插件 DAG）建议在总 README 中加交叉索引，避免命名体系差异造成困惑

## 6. 追加：disabled 节点点击修复（2026-08-17）

### 6.1 问题
用户反馈交互图中**标红框的 disabled 节点点不进去**，但其专属页面（02-plugin-pages/{id}.html）实际存在。

### 6.2 根因
`04-interactive/index.html` 的点击处理 `cy.on('tap', 'node', ...)` 只识别 `kind === 'plugin' | 'seam' | 'stub'`。而 inject-data-l3.py 在 DATA 注入时，将 22 个 web 禁用插件（disabled_base_rows）的 kind 设为 **"disabled"**，导致点击这些节点时没有任何分支命中 → 跳转失败。

### 6.3 修复
第 218 行 tap 处理器加入 `'disabled'` 分支：
```js
} else if (k === 'plugin' || k === 'disabled' || k === 'seam' || k === 'stub'){
  const url = n.data('url');
  if (url) window.location.href = url;
}
```

### 6.4 验证
| 检查项 | 结果 |
|--------|------|
| tap 处理器含 disabled | ✅ |
| 22 个 disabled 节点 url 完整（0 缺） | ✅ |
| url 目标文件全部存在（含 dsh-skill-filesystem / dsh-tool-skill） | ✅ |
| 无 pointer-events 拦截 | ✅ |
| 真实页面 headless 渲染（zcount=38 / 下钻 23 / 36） | ✅ |
| quality-gate-l3.py 8 项 | ✅ ALL PASS |
| 编码（UTF-8 无 BOM + CRLF） | ✅ |

### 6.5 经验
- **kind 枚举不匹配 bug**：DATA 注入的 kind 集合与 tap 处理器分支集合必须保持同步；新增 kind（disabled）时若只改注入不改消费方，就会出现"节点存在但点不动"的静默缺陷
- 此类问题门控难覆盖（需浏览器事件级验证），建议在 inject 脚本与消费方之间约定 kind 白名单常量
