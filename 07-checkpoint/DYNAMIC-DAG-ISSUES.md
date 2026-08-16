# 0816-plugin-dag 动态 DAG 迭代问题追踪（2026-08-17）

> 本文件记录插件页动态 DAG 功能迭代中发现的问题、根因与修复状态，供后续批量扩展与 GitHub 上传参考。

## 问题清单

### P1. 动态 DAG 内容错误：展示的是插件间依赖而非插件内部结构 ✅ 已修复
- **现象**：用户指出"DAG 不对，我说的是插件内结构啊"——第一版动态 DAG 渲染的是插件的上游/下游插件依赖（插件级），而用户要的是**插件 src 内部模块间的 import 依赖**（模块级）
- **根因**：设计理解偏差。第一版 gen-plugin-dyn.py 用 webapp-dag.json 的 edges（插件间依赖）构图；用户要的是源码解析（src/*.ts 文件的 import 关系）
- **修复**：新写 parse-plugin-internal.py（解析 src import）→ replace-plugin-internal.py（替换为模块级 DAG）
- **遗留**：插件级 DAG 仍保留在 173 页（gen-plugin-dyn.py），试点页被模块级覆盖

### P2. 染色错误：节点全是灰色 ✅ 已修复
- **现象**：用户反馈"没有颜色，是灰色方块"
- **根因**：cytoscape 样式 `'background-color': 'data(cls)'` 期望**颜色值**，但脚本把 `cls` 存成了 **CSS 类名**（dyn-self/dyn-entry 等），cytoscape 无法解析类名 → 渲染默认灰色
- **修复**：cls 字段直接存颜色值（#4f8cff 蓝 / #2f6fd0 深蓝 / #5a6b8c 灰等），选择器改用 `node[kind="..."]`
- **验证**：verify-color.py 确认全部 cls 为 # 开头颜色值；VLM 截图确认彩色

### P3. 排版狭长：DAG 过度竖向堆叠 ✅ 已修复（部分）
- **现象**：用户反馈"各元素分布范围与图片窗口比例不一致，形成过度狭长"
- **量化**：bb-check 显示 dsh-llm 布局 bounding box 234x4044（**17.3:1**），14 模块沿竖向堆成竖线
- **根因**：dagre rankDir 写死 TB（竖向），14 个模块纵向堆叠
- **修复**：
  1. 初始 layout rankDir 改 LR（横向）—— bb 改善到 466x793（1.7:1）
  2. 布局后 `cy.fit()` 缩放适配容器
  3. 容器 height:auto + max-height:900px
- **状态**：**部分修复**——headless 697x418 容器下 1.7:1 仍略竖，真实浏览器（max-width 1200px）会更好；后续可再调 spacingFactor 或节点分组

### P4. 页面脚本累积：replace 脚本多次运行导致 5 个 cytoscape script 叠加 ⚠️ 已规避
- **现象**：`const raw =` 出现 5 次，初始 layout 读到的还是最老层（TB）
- **根因**：replace_and_move 的清理逻辑只删到第一个 `</script>`，多次运行残留旧 script
- **处理**：改为"先 gen-html-l3.py 生成干净页 → 再 replace 一次"的流程，避免累积；replace 脚本加了"无旧区块时直接插入"分支
- **风险**：replace-plugin-internal.py 的"替换旧区块"路径仍不完善，批量扩展时应保持"干净页→插一次"流程

### P5. 双身份节点（dsh-client-connection）页面被 seam 版本覆盖 ✅ 已修复
- **现象**：dsh-client-connection 既是 L2 插件（DAG 节点）又是 seam，gen-html 先写插件页后写 seam 页，seam 页覆盖插件页
- **修复**：gen-html-l3.py seam 段跳过 DAG 节点中已存在的 dual id；插件页补 "⑤ 作为 seam 接口被依赖" 段

### P6. 路径分隔符 bug：Windows 混合分隔符导致 import 解析 0 依赖 ✅ 已修复
- **现象**：parse-plugin-internal.py 解析 dsh-agent 得 0 内部依赖
- **根因**：glob 返回混合 `\` 与 `/` 分隔符路径，resolve_local 生成的统一反斜杠路径与 ts_set 比较不相等
- **修复**：所有路径统一正斜杠比较

## 遗留/待办
- [ ] P3 排版在真实浏览器大容器下最终确认（用户浏览器查看）
- [ ] 试点确认后批量扩展到全部 173 插件（parse-plugin-internal.py 需批量跑）
- [ ] GitHub 上传（已确认 Public，仓库名 deepseek-harness-plugin-dag，待动态化稳定）
- [ ] 染色/排版确认后把替换脚本固化为 gen-plugin-internal-l3.py（正式版）

## 关键技术决策
1. **cls 字段必须存颜色值**（非 CSS 类名）—— cytoscape data 驱动样式
2. **模块级 DAG 数据源** = src/*.ts 文件（节点）+ import/export from 关系（边）
3. **rankDir 由节点数决定**：≥12 用 LR 横排防狭长，<12 用 TB
4. **布局后 cy.fit()** 缩放适配容器，防内容溢出
5. **替换流程**：gen-html 干净页 → 单次 replace，防脚本累积
