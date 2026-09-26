# DeepSeek Harness 插件级 DAG 依赖链分析 (MD 镜像)

## 统计
- 插件节点: 239（L1 核心集 90 + L2 web-app 82 + L3 其余 67）
- 外部 seam 基座: 73
- 依赖边: 1077
- 拓扑层: 19
- 分组: 50

## 阅读导航
- [分组清单](01-groups.md)
- [拓扑分层](02-layers.md)
- [交互总览 HTML](../04-interactive/index.html)
- [每插件 HTML](../02-plugin-pages/index.html)

## 拓扑分层速览
- **Layer 0** (29): cordis-plugin-loader, cordis-plugin-logger-console, cordis-plugin-timer, dsh-attachment-local, dsh-bash-local, dsh-client-resources, dsh-client-ui-primitives, dsh-credentials-local, dsh-deepseek-llm-api-extensions, dsh-experimental-api-speech-to-text, dsh-experimental-ptc-runtime-python, dsh-experimental-speech-to-text-sensevoice, dsh-fs-local, dsh-fs-observation-policy, dsh-host-directory-picker-browse, dsh-host-directory-picker-native, dsh-host-webserver, dsh-invariants, dsh-lsp-stdio, dsh-pwsh-local, dsh-sandbox-local, dsh-sandbox-ssh, dsh-shell-env, dsh-spill-local, dsh-storage, dsh-subprocess-local, dsh-typert-registry, dsh-workspace-changes, schemastery
- **Layer 1** (13): cordis-plugin-group, cordis-plugin-include, dsh-client-modules, dsh-client-ui-dockkit, dsh-client-ui-renderer, dsh-experimental-inspector, dsh-llm, dsh-scope, dsh-storage-domain, dsh-storage-json, dsh-storage-sqlite, dsh-subprocess-ssh, dsh-typert-loader
- **Layer 2** (11): dsh-authorization, dsh-client-connection, dsh-client-hmr, dsh-client-web, dsh-hmr, dsh-llm-deepseek-account, dsh-llm-deepseek-api-key, dsh-session, dsh-skill, dsh-system-prompt, dsh-web
- **Layer 3** (24): dsh-api-gateway, dsh-commands, dsh-config-editor, dsh-deepseek-account-platform, dsh-experimental-webworker-runtime, dsh-hook-protocol, dsh-host-frontend-static, dsh-host-open-in-app, dsh-llm-pi-ai, dsh-persona, dsh-session-log-deepseek, dsh-session-persistence-jsonl, dsh-session-projection, dsh-session-query-sqlite, dsh-session-telemetry-otel, dsh-skill-badge, dsh-skill-filesystem, dsh-skill-office, dsh-user-approval, dsh-web-fetch-http, dsh-web-search-exa, dsh-web-search-perplexity, dsh-webhook-github, dsh-workspace
- **Layer 4** (13): dsh-agent, dsh-api-job-controller, dsh-api-workspace-controller, dsh-command-compact, dsh-command-feedback, dsh-sandbox-policy, dsh-session-projection-cache, dsh-session-stats, dsh-session-title, dsh-session-turn-outline, dsh-settings, dsh-token-meter, dsh-tools
- **Layer 5** (55): dsh-agent-default-model, dsh-agent-instructions, dsh-agent-loop, dsh-agent-preset-registry, dsh-agent-tool-presentation, dsh-api-account-controller, dsh-api-settings-controller, dsh-api-terminal-controller, dsh-api-workspace-files, dsh-bash-sandbox, dsh-client-file-upload, dsh-compaction-image-offload, dsh-compaction-tool-result-pruner, dsh-cordis-host-runner, dsh-experimental-browser-use-chrome-devtools-mcp, dsh-experimental-browser-use-playwright-mcp, dsh-experimental-tool-agent-team, dsh-file-reference-local, dsh-fs-sandbox, dsh-fs-ssh, dsh-goal, dsh-hooks-codex, dsh-jobs-local, dsh-llm-retry, dsh-mcp-resources, dsh-message-feedback, dsh-permission-presets, dsh-ptc-runtime-node, dsh-pwsh-sandbox, dsh-repeat-tool-reminder, dsh-sdk-jsonrpc-server, dsh-session-checkpoint-policy, dsh-session-reference, dsh-session-title-all-prompts-llm, dsh-session-title-first-prompt-llm, dsh-spill-policy, dsh-terminal, dsh-time-context, dsh-tmux-context, dsh-tool-bash, dsh-tool-call-timeout-policy, dsh-tool-fs, dsh-tool-fs-search, dsh-tool-jobs, dsh-tool-lsp, dsh-tool-present, dsh-tool-pwsh, dsh-tool-session-query, dsh-tool-skill, dsh-tool-str-replace-editor, dsh-tool-todo, dsh-tool-web, dsh-tool-workspace-dependencies, dsh-user-questions, dsh-web-search-deepseek
- **Layer 6** (18): dsh-agent-preset, dsh-command-goal, dsh-compaction-basic, dsh-experimental-auto-review, dsh-goal-round-driver, dsh-host-plugin-inventory, dsh-mcp-client, dsh-office-to-pdf, dsh-plan-mode, dsh-plugin-package-inventory-deepseek, dsh-subagent, dsh-terminal-bash, dsh-tool-ask-user, dsh-tool-bash-persistent, dsh-tool-cordis, dsh-tool-goal, dsh-tool-pwsh-persistent, dsh-tool-terminal
- **Layer 7** (16): dsh-acp, dsh-api-session-controller, dsh-experimental-browser-use-stagehand-native, dsh-experimental-computer-use-cua-driver-mcp, dsh-experimental-computer-use-cua-driver-native, dsh-hooks-claude-code, dsh-plugin-manager, dsh-subagent-acp, dsh-subagent-claude-code, dsh-subagent-codex, dsh-subagent-dsh-sdk, dsh-subagent-fork-in-process, dsh-subagent-spawn-in-process, dsh-tool-subagent, dsh-tool-subagent-control, dsh-workflow-ptc
- **Layer 8** (4): dsh-client-ui-session, dsh-schedule, dsh-tool-ralph, dsh-tool-workflow
- **Layer 9** (1): dsh-api-remotes
- **Layer 10** (3): dsh-client-ui-settings, dsh-client-ui-tool, dsh-cordis-client-runner
- **Layer 11** (1): dsh-client-locale
- **Layer 12** (6): dsh-client-shortcuts, dsh-client-ui-cordis, dsh-client-ui-settings-models, dsh-client-ui-settings-plugins, dsh-client-ui-theme, dsh-client-ui-user-questions
- **Layer 13** (4): dsh-client-ui-conversation, dsh-client-ui-layout, dsh-client-ui-settings-general, dsh-client-ui-shortcuts
- **Layer 14** (7): dsh-client-ui-approval, dsh-client-ui-input-trigger, dsh-client-ui-jobs, dsh-client-ui-sidebar, dsh-client-ui-sidebar-right, dsh-client-ui-trajectory, dsh-client-ui-workspace
- **Layer 15** (16): dsh-client-ui-agent-preset, dsh-client-ui-brand-official, dsh-client-ui-commands, dsh-client-ui-directory-picker-browse, dsh-client-ui-directory-picker-native, dsh-client-ui-plugin-manager, dsh-client-ui-reference, dsh-client-ui-schedule, dsh-client-ui-sidebar-browser, dsh-client-ui-sidebar-documentpreview, dsh-client-ui-sidebar-files, dsh-client-ui-sidebar-terminal, dsh-client-ui-skill, dsh-client-ui-subagent, dsh-client-ui-workflow-run, dsh-experimental-client-ui-agent-team
- **Layer 16** (11): dsh-client-ui-chat, dsh-client-ui-message-feedback, dsh-client-ui-model-selection, dsh-client-ui-permission-presets, dsh-client-ui-settings-agent-loop, dsh-client-ui-settings-plugin-inventory, dsh-client-ui-settings-shell, dsh-client-ui-settings-subagent, dsh-client-ui-settings-web-search, dsh-experimental-client-ui-voice-input, dsh-host-directory-picker-auto
- **Layer 17** (6): dsh-client-ui-attachment, dsh-client-ui-deliverables, dsh-client-ui-goal, dsh-client-ui-plan, dsh-client-ui-settings-account, dsh-session-log-export
- **Layer 18** (1): dsh-client-ui-open-in-app
