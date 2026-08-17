# 模块级动态 DAG + GitHub 上传执行报告（2026-08-17）

## 1. 当时情况

L3 插件 DAG 分析完成后，用户提出两个方向性反馈：
1. **插件内部结构图风格不统一**：静态 drawio 图（浅色三段式）与插件专属页面（深色主题）风格不一致，且未内嵌到页面
2. **要动态化**：插件内部结构图应做成动态 DAG，而非静态图

经 Grill-Me 确认：**173 插件全部动态化 + GitHub Public 上传**。用户随后明确核心诉求是**插件源码内部模块结构**（src/*.ts 文件的 import 关系），而非插件间依赖；并要求 DAG 放在页面上半部分、布局与窗口比例协调、问题持久化本地。

## 2. 制定计划

1. **试点**：先做 4 个核心插件（agent/session/tools/llm）验证染色+排版，用户浏览器确认
2. **批量**：试点通过后解析全部 215 插件+seam 的 src import，批量替换插件页
3. **GitHub**：Public 仓库上传（zako-mio/deepseek-harness-plugin-dag）
4. **持久化**：问题追踪 DYNAMIC-DAG-ISSUES.md + 5 段报告

## 3. 执行情况

**试点阶段**（4 插件）：
- 解析脚本 parse-plugin-internal.py 修复 Windows 路径分隔符 bug（P6：glob 混合 `\`/`/` 致 import 解析 0 依赖 → 统一正斜杠）
- 第一版动态 DAG 错做成插件间依赖（P1），用户纠正后改模块级（src import）
- 染色失败（P2）：cls 存 CSS 类名而非颜色值 → 全灰；改存 # 颜色值 + 选择器用 kind
- 排版狭长（P3）：bb 17.3:1 竖线 → 初始 layout 改 LR + cy.fit() 适配 → 1.7:1
- 脚本累积（P4）：replace 多次运行致 5 个 raw 块 → 改为"干净页→单次插入"
- 双身份修复（P5）：dsh-client-connection 页面被 seam 版本覆盖 → seam 段跳过 dual id + 插件页补⑤段

**批量阶段**：
- parse-all-internal.py：**215 插件+seam 全部解析成功**（0 跳过），1130 模块 + 1073 内部依赖边
- apply-all-internal.py：**171 插件页插入模块级 DAG**（173 节点 - 2 cordis 框架插件）
- cordis-plugin-hmr/timer（框架自带，无源码包）→ 插入占位说明
- 质量门控 ALL PASS（265 页 0 断链 / drawio 174 / MD 173+49）
- 抽查 3 插件：raw 块=1 无累积、染色正确、canvas 渲染正常

**GitHub 阶段**：
- git init → .gitignore（排除 screenshots）→ add 910 文件 → commit
- `gh repo create deepseek-harness-plugin-dag --public --push`
- **成功**：https://github.com/zako-mio/deepseek-harness-plugin-dag（PUBLIC，master 同步）

**持久化**：
- 07-checkpoint/DYNAMIC-DAG-ISSUES.md（P1-P6 问题追踪 + 技术决策）
- 本报告（5 段模板）

## 4. 完成情况

| 交付物 | 状态 |
|--------|------|
| 173 插件页模块级内部结构动态 DAG（cytoscape） | ✅ 171 插件 + 2 框架占位 |
| 215 插件 src import 解析数据（plugin-internal-all.json） | ✅ 1130 模块 / 1073 边 |
| 染色（蓝入口/深蓝模块/灰叶子）+ 排版（LR 横排 + fit） | ✅ |
| 质量门控 quality-gate-l3.py 8 项 | ✅ ALL PASS |
| GitHub Public 仓库 | ✅ https://github.com/zako-mio/deepseek-harness-plugin-dag |
| 问题追踪 DYNAMIC-DAG-ISSUES.md | ✅ P1-P6 记录 |

**改动文件**：
- 新增：`07-checkpoint/plugin-internal-all.json`、`DYNAMIC-DAG-ISSUES.md`、`README.md`（模块内部 DAG 章节）
- 修改：`02-plugin-pages/*.html`（171 页插入模块 DAG + 2 占位）
- 临时脚本（D:\Temp\opencode\）：parse-plugin-internal.py / parse-all-internal.py / apply-all-internal.py / replace-plugin-internal.py 等

## 5. 反思/分析/建议

**过程反思**：
1. **用户"相当不错"前经历了 3 轮迭代**（P1 内容错误 → P2 染色全灰 → P3 排版狭长），每轮都是"数据驱动式验证"（bb 量化 + VLM 截图 + 用户浏览器确认）而非主观判断——这是复杂 UI 迭代的正确节奏
2. **cytoscape data 驱动样式陷阱**：`data(cls)` 期望颜色值而非类名，这类"字段语义错配"是动态图渲染最常见的静默 bug（不报错只显示错）
3. **Windows 路径分隔符**是解析类脚本的高频坑：glob 返回混合分隔符，必须统一正斜杠比较
4. **脚本幂等与累积**：多次运行生成类脚本必须保证"删除旧块"完整，否则残留叠加（raw 块 5 层）

**经验教训**：
- 动态图迭代流程：**解析数据 → 渲染脚本 → 量化验证（bb 比例/染色值）→ VLM 截图 → 用户浏览器确认**，缺一不可
- 框架插件（cordis 自带）与源码插件要区分处理，不能一刀切
- GitHub 上传前用 .gitignore 排除临时/验证产物（screenshots 等）

**未来建议**：
1. 若继续优化：节点可加"模块函数数"标签（0814 stage-02 有 functions 数据），丰富内部结构信息
2. 交互图（04-interactive）可加"下钻到插件内部模块"能力（点插件节点 → 进入模块级 DAG）
3. 插件级 DAG（gen-plugin-dyn.py 生成）仍保留在 173 页中上部，与模块级共存；如需精简可只保留模块级
