---
name: shiki-wechat-summary-plus
description: >-
  WeChat group and private chat intelligence via local wx-cli: structured digests,
  per-chat user profiles, memory points (birthday, likes, gifts, taboos, hobbies),
  and relationship playbooks for friends, dating, and social scenarios. Use when
  the user asks for shiki-wechat-summary, 微信总结+, 群聊精华, 私聊分析, 用户画像,
  记忆点, 生日, 喜好, 礼物, 恋爱, 交友, 攻略, 怎么聊, 开场白, filehelper, or
  consult-style advice from chat history. NOT for roast-only group digest (baoyu-wechat-summary),
  JSON topic/knowledge nodes (wechat-chat-insight), or QQ/direct non-WeChat sources.
version: 0.1.0
metadata:
  requires:
    anyBins:
      - wx
---

# shiki-wechat-summary+

微信群 / 私聊 **精华 + 画像 + 记忆点 + 关系攻略**。底层 [wx-cli](https://github.com/jackwener/wx-cli)（`wx` 命令）。数据按**会话分目录**存放，默认不跨群/私聊自动合并同一人。

> **Sandbox**: 从第一次 `wx` 起需完整文件系统权限（`~/.wx-cli`、微信数据目录）。Windows 命令用 `cmd /c`，见 [references/wx-workflow.md](references/wx-workflow.md)。

> **分工**: 只要群精华无毒舌无攻略 → `baoyu-wechat-summary`；topics.json / knowledge.json → `wechat-chat-insight`；记忆/恋爱/私聊攻略 → **本 skill**。

## When to use which mode

| Mode | User intent | Main outputs |
|------|-------------|--------------|
| `group_digest` | 总结 XX 群、群聊精华+攻略 | `{group_folder}/YYYY-MM-DD.md`, `profiles/`, `memory/` |
| `private_digest` | 总结和小红私聊、文件传输助手 | `private/{wxid}-{name}/*.md`, `memory.md` |
| `memory_only` | 记住 TA 喜欢猫、更新记忆点 | `memory/*.yaml` or `memory.md` |
| `playbook` | 怎么聊 TA、送礼、拉群话术 | `playbook-*.md` or `playbook.md` |
| `consult` | 根据已有画像给建议（可不再拉 wx） | 对话回复 ± `consult-*.md` |

Default mode when ambiguous: `group_digest` if name looks like a group; `private_digest` if「私聊」「某人」或 `filehelper`.

## Preferences (EXTEND.md)

Search order (first wins):

1. `.shiki-skills/shiki-wechat-summary-plus/EXTEND.md` (project root)
2. `%USERPROFILE%\.shiki-skills\shiki-wechat-summary-plus\EXTEND.md`

| Key | Required | Default |
|-----|----------|---------|
| `self_wxid` | yes | — |
| `self_display` | yes | — |
| `data_root` | no | `{project_root}/wechat` |
| `default_time_range` | no | `7d` |
| `default_relationship` | no | `friend` |
| `include_playbook_in_digest` | no | `true` |
| `allow_roast` | no | `false` |

Template: [EXTEND.md.example](EXTEND.md.example).

**First-time setup (BLOCKING)** if no EXTEND.md: discover via `wx whoami --json` or `wx sessions --json`; batch AskUser for `self_wxid`, `self_display`, `data_root`; write EXTEND to project `.shiki-skills/...` unless user picks home.

## Workflow overview

```text
Parse request → Pick mode → wx prerequisites → Resolve folder → Fetch history
→ Round 1 skeleton → Round 2 write → Round 3 audit
→ Round M memory → Round P playbook (if applicable) → history.json
```

Detailed wx steps: [references/wx-workflow.md](references/wx-workflow.md).

### Step 1 — Parse request

Extract: chat name/id, time range (same rules as baoyu: 今天/7d/日期区间/从上次), mode override, target person for playbook, `relationship_to_self` if user stated (暧昧→crush, 同事→colleague).

### Step 2 — Resolve folder

- **Group**: `{data_root}/{group_id}-{sanitized_name}/`
- **Private**: `{data_root}/private/{wxid}-{sanitized_name}/`

Create folder if missing. See wx-workflow for rename rules.

### Step 3 — Fetch messages

```bash
wx history "<id>" --since YYYY-MM-DD --until YYYY-MM-DD -n 10000 --json > "%TEMP%\wx-msgs.json"
```

Incremental: `{folder}/history.json` → skip messages before `last_message_time`.

Message handling: same as baoyu (skip revoke/system; `[链接]` title is content). Large pulls: process via temp file, not full inline dump.

### Step 4 — Round 1: skeleton

Internal only:

- Topic list with anchors (`local_id`), participants, one-line summary
- **Memory candidates** per person (or counterpart in private): field → quote → confidence
- Speaker stats for group

Flag image-dependent topics; optional `{folder}/imgs/{id}.txt` descriptions if present.

### Step 5 — Round 2: write

Load [references/output-formats.md](references/output-formats.md).

- **group_digest**: sections 一–八 per format doc; load prior `profiles/` in Step 3.7
- **private_digest**: private template; update `memory.md`
- **memory_only**: skip digest body
- **playbook**: use [references/playbook-rules.md](references/playbook-rules.md) + [references/social-scenarios.md](references/social-scenarios.md)

Load profiles: [references/profiles.md](references/profiles.md) Step 3.7.

### Step 6 — Round 3: audit

Skeleton vs output; quotes verbatim; privacy [references/privacy.md](references/privacy.md).

### Step 7 — Round M: memory

Write/update per [references/memory-schema.md](references/memory-schema.md).

Run validator when available:

```bash
python .cursor/skills/shiki-wechat-summary-plus/scripts/validate-memory.py "<path-to-yaml>"
```

### Step 8 — Round P: playbook

If `group_digest` + `include_playbook_in_digest`: embed 关系攻略 section.

If `playbook` mode or user asked full攻略: write standalone `playbook-*.md`.

### Step 9 — Profiles update

After digest, for users 3+ messages in batch, update `profiles/` per [references/profiles.md](references/profiles.md). Skip `profiles-roast/` unless `allow_roast` and user requested毒舌.

### Step 10 — history.json

Update `last_digest` metadata (file name, date_range, message_count, last_message_time).

## User input tools

1. Prefer `AskUserQuestion` for disambiguation (group pick, relationship type, time range).
2. Fallback: numbered plain-text options.

## Backfill

User says `回溯画像` / `初始化记忆` / `backfill`:

- **Profiles**: same as baoyu Step 9 — read past digests in folder, merge into `profiles/`
- **Memory**: scan past digests + optional re-fetch; merge into `memory/` with evidence; do not delete evidence rows

Cross-folder merge only when user explicitly names a person and asks to combine.

## Security

- `wx init` has account risk — user runs manually; disclose on first setup.
- Do not commit `data_root` to public repos.
- Redact obvious secrets (API keys, passwords) in digests unless user requested full archive.

## Reference index

| File | Purpose |
|------|---------|
| [wx-workflow.md](references/wx-workflow.md) | wx-cli, paths, Windows |
| [output-formats.md](references/output-formats.md) | Digest templates |
| [profiles.md](references/profiles.md) | Group portraits |
| [memory-schema.md](references/memory-schema.md) | memory YAML / md |
| [playbook-rules.md](references/playbook-rules.md) | 攻略 structure |
| [social-scenarios.md](references/social-scenarios.md) | 恋爱/群聊/送礼分支 |
| [privacy.md](references/privacy.md) | Ethics guardrails |

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `wx` not found | User installs wx-cli; `cmd /c` on Windows |
| Empty history | WeChat running; `wx init`; widen date range |
| Only recent messages | wx-cli DB window; note limit in digest header |
| PowerShell `&&` fails | Use `cmd /c "a & b"` |
