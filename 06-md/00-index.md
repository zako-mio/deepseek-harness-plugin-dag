# DeepSeek Harness 插件级 DAG 依赖链分析 (MD 镜像)

## 统计
- 插件节点: 248（L1 核心集 91 + L2 web-app 84 + L3 其余 73）
- 外部 seam 基座: 83
- 依赖边: 1167
- 拓扑层: 17
- 分组: 48

## 阅读导航
- [分组清单](01-groups.md)
- [拓扑分层](02-layers.md)
- [交互总览 HTML](../04-interactive/index.html)
- [每插件 HTML](../02-plugin-pages/index.html)

## 拓扑分层速览
- **Layer 0** (30): cordis-plugin-loader, cordis-plugin-logger-console, cordis-plugin-timer, dsh-attachment-local, dsh-bash-local, dsh-client-resources, dsh-client-ui-primitives, dsh-client-ui-renderer, dsh-credentials-local, dsh-deepseek-llm-api-extensions, dsh-experimental-api-speech-to-text, dsh-experimental-speech-to-text-sensevoice, dsh-fs-local, dsh-fs-observation-policy, dsh-host-directory-picker-browse, dsh-host-directory-picker-native, dsh-host-webserver, dsh-llm, dsh-lsp-stdio, dsh-otel, dsh-pwsh-local, dsh-sandbox-ssh, dsh-shell-env, dsh-skill, dsh-spill-local, dsh-storage, dsh-subprocess-local, dsh-system-prompt, dsh-typert-registry, schemastery
- **Layer 1** (21): cordis-plugin-group, cordis-plugin-include, dsh-authorization, dsh-client-connection, dsh-client-modules, dsh-client-ui-dockkit, dsh-host-product-telemetry-otel, dsh-llm-deepseek-account, dsh-llm-deepseek-api-key, dsh-persona, dsh-sandbox-local, dsh-session, dsh-skill-badge, dsh-skill-filesystem, dsh-skill-office, dsh-storage-domain, dsh-storage-json, dsh-storage-sqlite, dsh-subprocess-ssh, dsh-typert-loader, dsh-web
- **Layer 2** (18): dsh-api-gateway, dsh-client-hmr, dsh-client-web, dsh-commands, dsh-deepseek-account-platform, dsh-hmr, dsh-host-frontend-static, dsh-host-open-in-app, dsh-session-log-deepseek, dsh-session-persistence-jsonl, dsh-session-projection, dsh-session-query-sqlite, dsh-user-approval, dsh-web-fetch-http, dsh-web-search-exa, dsh-web-search-perplexity, dsh-webhook-github, dsh-workspace
- **Layer 3** (13): dsh-agent, dsh-api-job-controller, dsh-api-workspace-controller, dsh-command-compact, dsh-command-feedback, dsh-config-editor, dsh-experimental-webworker-runtime, dsh-sandbox-policy, dsh-session-projection-cache, dsh-session-stats, dsh-session-turn-outline, dsh-token-meter, dsh-working-directory
- **Layer 4** (24): dsh-api-account-controller, dsh-api-terminal-controller, dsh-api-workspace-files, dsh-bash-sandbox, dsh-client-file-upload, dsh-compaction-image-offload, dsh-compaction-tool-result-pruner, dsh-experimental-ptc-runtime-python, dsh-fs-sandbox, dsh-fs-ssh, dsh-goal, dsh-jobs-local, dsh-llm-retry, dsh-message-feedback, dsh-ptc-runtime-node, dsh-pwsh-sandbox, dsh-session-reference, dsh-settings, dsh-terminal, dsh-time-context, dsh-tmux-context, dsh-tools, dsh-user-questions, dsh-web-search-deepseek
- **Layer 5** (47): dsh-agent-default-model, dsh-agent-instructions, dsh-agent-loop, dsh-agent-preset-registry, dsh-agent-tool-presentation, dsh-api-settings-controller, dsh-client-product-analytics, dsh-command-goal, dsh-compaction-basic, dsh-cordis-host-runner, dsh-experimental-browser-use-chrome-devtools-mcp, dsh-experimental-browser-use-playwright-mcp, dsh-experimental-claude-code-mods, dsh-experimental-tool-agent-team, dsh-experimental-tool-worktree, dsh-file-reference-local, dsh-goal-round-driver, dsh-hooks-codex, dsh-llm-pi-ai, dsh-mcp-resources, dsh-office-to-pdf, dsh-permission-presets, dsh-plan-mode, dsh-repeat-tool-reminder, dsh-session-checkpoint-policy, dsh-session-telemetry-otel, dsh-spill-policy, dsh-subagent, dsh-terminal-bash, dsh-tool-ask-user, dsh-tool-call-timeout-policy, dsh-tool-fs, dsh-tool-fs-search, dsh-tool-goal, dsh-tool-jobs, dsh-tool-lsp, dsh-tool-present, dsh-tool-session-query, dsh-tool-skill, dsh-tool-str-replace-editor, dsh-tool-terminal, dsh-tool-todo, dsh-tool-web, dsh-tool-workflow, dsh-tool-working-directory, dsh-tool-workspace-dependencies, dsh-workspace-changes
- **Layer 6** (20): dsh-agent-preset, dsh-experimental-auto-review, dsh-hooks-claude-code, dsh-host-plugin-inventory, dsh-mcp-client, dsh-plugin-package-inventory-deepseek, dsh-sdk-jsonrpc-server, dsh-session-title, dsh-subagent-acp, dsh-subagent-dsh-sdk, dsh-subagent-fork-in-process, dsh-subagent-spawn-in-process, dsh-tool-bash, dsh-tool-bash-persistent, dsh-tool-cordis, dsh-tool-pwsh, dsh-tool-pwsh-persistent, dsh-tool-subagent, dsh-tool-subagent-control, dsh-workflow-ptc
- **Layer 7** (11): dsh-acp, dsh-api-session-controller, dsh-experimental-browser-use-stagehand-native, dsh-experimental-computer-use-cua-driver-mcp, dsh-experimental-computer-use-cua-driver-native, dsh-plugin-manager, dsh-session-title-all-prompts-llm, dsh-session-title-first-prompt-llm, dsh-subagent-claude-code, dsh-subagent-codex, dsh-tool-ralph
- **Layer 8** (2): dsh-client-ui-session, dsh-schedule
- **Layer 9** (2): dsh-api-remotes, dsh-tool-schedule
- **Layer 10** (2): dsh-client-ui-settings, dsh-cordis-client-runner
- **Layer 11** (1): dsh-client-locale
- **Layer 12** (10): dsh-client-shortcuts, dsh-client-ui-cordis, dsh-client-ui-jobs, dsh-client-ui-settings-models, dsh-client-ui-settings-plugin-inventory, dsh-client-ui-settings-plugins, dsh-client-ui-settings-session-log, dsh-client-ui-theme, dsh-client-ui-tool, dsh-experimental-client-ui-claude-code-mods
- **Layer 13** (6): dsh-client-ui-conversation, dsh-client-ui-layout, dsh-client-ui-settings-account, dsh-client-ui-settings-general, dsh-client-ui-shortcuts, dsh-experimental-inspector
- **Layer 14** (11): dsh-client-ui-approval, dsh-client-ui-commands, dsh-client-ui-goal, dsh-client-ui-input-trigger, dsh-client-ui-open-in-app, dsh-client-ui-plugin-manager, dsh-client-ui-sidebar, dsh-client-ui-sidebar-right, dsh-client-ui-trajectory, dsh-client-ui-user-questions, dsh-client-ui-workspace
- **Layer 15** (26): dsh-client-ui-agent-preset, dsh-client-ui-brand-official, dsh-client-ui-chat, dsh-client-ui-deliverables, dsh-client-ui-directory-picker-browse, dsh-client-ui-directory-picker-native, dsh-client-ui-message-feedback, dsh-client-ui-model-selection, dsh-client-ui-permission-presets, dsh-client-ui-reference, dsh-client-ui-schedule, dsh-client-ui-settings-agent-loop, dsh-client-ui-settings-shell, dsh-client-ui-settings-subagent, dsh-client-ui-settings-web-search, dsh-client-ui-sidebar-browser, dsh-client-ui-sidebar-documentpreview, dsh-client-ui-sidebar-files, dsh-client-ui-sidebar-terminal, dsh-client-ui-skill, dsh-client-ui-subagent, dsh-client-ui-workflow-run, dsh-experimental-client-ui-agent-team, dsh-experimental-client-ui-cot-translation, dsh-experimental-client-ui-voice-input, dsh-experimental-session-inspector
- **Layer 16** (4): dsh-client-ui-attachment, dsh-client-ui-plan, dsh-host-directory-picker-auto, dsh-session-log-export
