# DSH Harness Config — dsh 接入外部 provider/API 的配置与硬约束

> 本文档为 **dsh-harness-config** skill 的**阅读版**（供人类浏览，无 frontmatter）。
> 可安装版见同目录 `SKILL.md`（含 `name`/`description` frontmatter，复制到 `~/.config/opencode/skills/dsh-harness-config/` 即被 opencode 识别）。
> **定位**：**dsh 插件 DAG 知识库的伴生 skill**（`archive/Mission-file/2026-09/0927-dsh-plugin-dag-017rc2/`），⛔ **不挂 live**（dsh ≠ opencode：配置格式 / 运行目录 / 生命周期均不同）。
> **来源**：2026-09-27 Command Code 免费模型 → dsh + opencode 双 harness 接入（`cycle_20260927_cmdcode_free_dual_harness`）。

---

## 一、边界（dsh ≠ opencode）

| 项 | dsh | opencode |
|---|---|---|
| 配置格式 | `cordis.patch.yml` | `opencode.jsonc` |
| 运行目录 | `~/.dsh/`（`$DSH_HOME`） | `~/.config/opencode/` |
| 生命周期 | systemd | 交互进程 |

`opencode-config` skill 自述范围明确限于 `~/.config/opencode/` ⇒ 承载 dsh 属越界，故独立成本 skill。

## 二、provider 落点

- 落点：`~/.dsh/profiles/{web,headless}/cordis.patch.yml` 的 `llm-pi-ai.config.providers`。
- 两个 profile **各自挂载、互不继承** ⇒ headless 若要同款须在其 `cordis.patch.yml` **另行挂载**（当前该文件整体为**注释停用态**）。

## 三、凭据 seam 优先级

- 优先级：**launch env → `~/.dsh/.credentials.yaml` → 项目 `.env` → `$DSH_HOME/.env`**。provider 侧以 `apiKeyEnv` **引用变量名** ⇒ key 值可单点更换。
- **一 key 一变量名 / 一账户一 provider**：⛔ 不同账户的凭据共用一个变量名会让「装载新 key」静默改变既有 provider 的账户归属（细则见 `opencode-config/ops/scenarios.md` 场景 5 ⑧⑨）。

## 四、代理机制（含旧认知修正）

- 代理变量（`http_proxy`/`https_proxy`/`no_proxy`）**只能**放 `$DSH_HOME/.env`（`~/.dsh/.env`）；放进**项目** `.env` 会被 launcher 判定为「仓库决定流量走向」而**拒绝启动**。
- 本版本 launcher 启动时 `installProxyFromEnvironment()` 经 undici `setGlobalDispatcher` 装**全局 dispatcher**（源码 `packages/util/http-proxy/src/install.ts`；`scripts/verify-no-bare-dispatcher.ts` 明示 Node fetch 经 undici 全局 dispatcher）⇒ **pi-ai 请求链与 `globalThis.fetch` 均受代理管辖**。
- ⇒ 旧陈述「Node fetch 不读代理 env、境外 API 必须直连」**在本版本已不准确**。该过时文本现仍写在 `~/.dsh/profiles/web/cordis.patch.yml` 的 persona 中，**待修订**（否则后续会话可能照旧文本误撤代理配置）。

## 五、模型参数语义

- `reasoningEfforts`：**未声明某档 = 该模型不支持该档**；请求未声明的档位报 `UNSUPPORTED_REASONING_EFFORT`。
- **可用档位集合的权威源 = 服务端对非法值的枚举错误**（实测 `Invalid option: expected one of "low"|"medium"|"high"|"xhigh"|"max"`），比文档权威；`minimal` 不被 Command Code 支持 ⇒ 不声明。档位**映射表须写全**。
- 同一纪律见 `opencode-config/troubleshooting/index.md` §参数/能力枚举的权威源。

## 六、验证三档

1. `dsh --profile <p> --dump-config` 退出码（配置级）；
2. in-harness 真跑（产出级）；
3. `env -u` 环境隔离（剥离继承变量）。

> 同级纪律见 `opencode-config`，本 skill 不重复展开。

## 七、坑与事实

- `~/.dsh/profiles/web/cordis.patch.yml` 的 persona 文本含**过时代理陈述**（见 §四），建议修订。
- headless profile **尚未挂载 Command Code**（行动项，本轮未擅改）。
- 路径：源码树 `~/dsh`，运行目录 `~/.dsh/`；provider 落盘原文与内嵌注释见该公司原任务的 `report.md` §3/§5。
