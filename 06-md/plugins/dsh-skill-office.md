# dsh-skill-office

- 包名: `@deepseek-ai/dsh-skill-office`
- 分组: G37 技能
- 拓扑层: Layer 3
- 来源层: L3 其余
- 源码路径: `packages/skill/skill-office`

## 实现逻辑
内置 Office 技能提供者：从打包 assets 目录为 office-docx/office-pptx/office-xlsx 三个技能解析 frontmatter 描述生成候选（bundled 来源、统一 BUNDLED_SKILL_RANK），get 返回 SKILL.md 正文并追加 LibreOffice Kit 运行时说明 (src/index.ts:37-96)。officeRuntime 校验 node 与 kit cli.js 均为绝对可执行文件，或按显式 cli:false 关闭 KIT (src/index.ts:47-62)。

## Provides
- office-docx/office-pptx/office-xlsx 技能 (bundled 提供者：文档编写工作流与 LibreOffice Kit 资源指引)

## Depends On (上游依赖)
- `dsh-skill` [E1+E2] - 向技能注册表注册 office bundled provider，并复用其 BUNDLED_SKILL_RANK 与 SkillCandidate/SkillProvider 契约
  - 证据: `package.json:30 peerDep + src/index.ts:10 import + src/index.ts:35 inject['skills'] + src/index.ts:96 ctx.skills.registerProvider`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
