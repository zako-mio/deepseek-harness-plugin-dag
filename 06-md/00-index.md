# DeepSeek Harness 插件级 DAG 依赖链分析 (MD 镜像)

## 统计
- 插件节点: 173（L1 核心集 76 + L2 web-app 58 + L3 其余 39）
- 外部 seam 基座: 49
- 依赖边: 545
- 拓扑层: 17
- 分组: 37

## 阅读导航
- [分组清单](01-groups.md)
- [拓扑分层](02-layers.md)
- [交互总览 HTML](../04-interactive/index.html)
- [每插件 HTML](../02-plugin-pages/index.html)

## 拓扑分层速览
- **Layer 0** (19): cordis-plugin-timer, dsh-attachment-local, dsh-client-schema-form, dsh-client-ui-primitives, dsh-client-ui-slots, dsh-credentials-local, dsh-fs-e2b, dsh-host-directory-picker, dsh-host-plugin-inventory, dsh-host-webserver, dsh-llm, dsh-native-command, dsh-settings-file, dsh-spill-local, dsh-storage, dsh-subprocess-e2b, dsh-subprocess-local, dsh-typert-generator, dsh-typert-registry
- **Layer 1** (16): cordis-plugin-hmr, dsh-api-gateway, dsh-client-ui-attachment, dsh-host-directory-picker-auto, dsh-host-directory-picker-browse, dsh-host-directory-picker-native, dsh-host-frontend-static, dsh-llm-deepseek, dsh-llm-pi-ai, dsh-lsp-stdio, dsh-session, dsh-skill, dsh-storage-json, dsh-system-prompt, dsh-typert-loader, dsh-web
- **Layer 2** (16): dsh-agent, dsh-code-runtime-worker-thread, dsh-fs-observation-policy, dsh-persona, dsh-sandbox-local, dsh-sdk-client, dsh-session-persistence-jsonl, dsh-session-persistence-sqlite, dsh-session-projection, dsh-session-query-sqlite, dsh-session-telemetry-otel, dsh-skill-badge, dsh-skill-filesystem, dsh-storage-domain, dsh-storage-sqlite, dsh-web-fetch-http
- **Layer 3** (19): dsh-agent-default-model, dsh-agent-presets, dsh-commands, dsh-goal, dsh-jobs-local, dsh-llm-retry, dsh-message-feedback, dsh-sandbox-policy, dsh-session-projection-cache, dsh-session-reference, dsh-session-stats, dsh-session-title, dsh-time-context, dsh-tmux-context, dsh-token-meter, dsh-user-approval, dsh-user-questions, dsh-web-search-deepseek, dsh-workspace
- **Layer 4** (15): dsh-bash-sandbox, dsh-command-compact, dsh-command-feedback, dsh-command-goal, dsh-compaction-tool-result-pruner, dsh-fs-sandbox, dsh-goal-round-driver, dsh-permission-presets, dsh-pwsh-sandbox, dsh-session-title-all-prompts-llm, dsh-session-title-first-prompt-llm, dsh-terminal-bash, dsh-tools, dsh-web-search-exa, dsh-web-search-perplexity
- **Layer 5** (26): dsh-agent-instructions, dsh-agent-loop, dsh-agent-tool-presentation, dsh-compaction-basic, dsh-cordis-host-runner, dsh-hooks-codex, dsh-plan-mode, dsh-repeat-tool-reminder, dsh-schedule, dsh-session-checkpoint-policy, dsh-shell-env, dsh-spill-policy, dsh-subagent, dsh-tool-ask-user, dsh-tool-bash-persistent, dsh-tool-call-timeout-policy, dsh-tool-fs, dsh-tool-fs-search, dsh-tool-goal, dsh-tool-jobs, dsh-tool-lsp, dsh-tool-session-query, dsh-tool-skill, dsh-tool-str-replace-editor, dsh-tool-terminal, dsh-tool-todo
- **Layer 6** (19): dsh-api-remotes, dsh-client-modules, dsh-hooks-claude-code, dsh-sdk-jsonrpc-server, dsh-subagent-acp, dsh-subagent-claude-code, dsh-subagent-codex, dsh-subagent-dsh-sdk, dsh-subagent-fork-in-process, dsh-subagent-spawn-in-process, dsh-tool-bash, dsh-tool-cordis, dsh-tool-pwsh, dsh-tool-subagent, dsh-tool-subagent-control, dsh-tool-subagent-report, dsh-tool-web, dsh-web-app, dsh-workflow-worker-thread
- **Layer 7** (6): dsh-agent-spine-demo, dsh-client-hmr, dsh-host-apiproxy, dsh-sdk-jsonrpc-demo, dsh-tool-ralph, dsh-tool-workflow
- **Layer 8** (3): dsh-acp-demo, dsh-client-connection, dsh-session-log-export
- **Layer 9** (1): dsh-client-runtime
- **Layer 10** (1): dsh-client-ui-settings
- **Layer 11** (3): dsh-client-locale, dsh-client-ui-settings-models, dsh-client-ui-settings-plugin-inventory
- **Layer 12** (4): dsh-client-ui-input-trigger, dsh-client-ui-settings-plugins, dsh-client-ui-theme, dsh-client-web-react
- **Layer 13** (2): dsh-client-ui-layout, dsh-cordis-client-runner
- **Layer 14** (3): dsh-client-ui-conversation, dsh-client-ui-sidebar, dsh-client-web
- **Layer 15** (14): dsh-client-ui-agent-preset, dsh-client-ui-commands, dsh-client-ui-deliverables, dsh-client-ui-goal, dsh-client-ui-jobs, dsh-client-ui-message-feedback, dsh-client-ui-plan, dsh-client-ui-settings-general, dsh-client-ui-subagent, dsh-client-ui-tool, dsh-client-ui-trajectory, dsh-client-ui-user-questions, dsh-client-ui-workflow-run, dsh-client-ui-workspace
- **Layer 16** (6): dsh-client-ui-cordis, dsh-client-ui-directory-picker-browse, dsh-client-ui-directory-picker-native, dsh-client-ui-model-selection, dsh-client-ui-permission-presets, dsh-client-ui-skill
