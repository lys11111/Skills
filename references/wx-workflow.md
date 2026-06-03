# wx-cli workflow — fetch and folder layout

Condensed from [baoyu-wechat-summary](C:\Users\86199\.agents\skills\baoyu-wechat-summary\SKILL.md). Use **full sandbox disable** on first `wx` call (reads `~/.wx-cli` and WeChat data dirs).

---

## 1. Prerequisites (stop at first failure)

1. `wx --version` — user installs manually if missing (`npm install -g @jackwener/wx-cli` or [releases](https://github.com/jackwener/wx-cli/releases)). **Do not** auto-install via piped scripts.
2. `%USERPROFILE%\.wx-cli` owned by current user (not Administrator/root). Repair ACL + remove stale `daemon.pid` / `daemon.sock`, then `wx daemon start`.
3. `wx sessions --json --limit 5` returns data; else user runs `wx init` with WeChat 4.x logged in.
4. WeChat client running.

Windows: prefer `cmd /c "command1 & command2"` — avoid PowerShell `&&` on older shells.

---

## 2. Resolve chat

### Group

```bash
wx contacts --query "<name>" --json
```

Pick `username` ending in `@chatroom`. Disambiguate with `AskUserQuestion` if multiple.

Folder: `{data_root}/{group_id}-{sanitized_group_name}/`

Sanitize: replace `/ \ : * ? " < > |` and control chars with `_`; trim trailing dots.

**Rename**: if folder `{group_id}-*` exists with different suffix, rename to match new group title.

### Private

```bash
wx sessions --json --limit 200
```

Match `chat_type: private` or `username` (e.g. `filehelper` for 文件传输助手).

Folder: `{data_root}/private/{wxid}-{sanitized_nickname}/`

If only nickname known: `wx contacts --query "<nick>" --json` and prefer private `chat_type`.

---

## 3. Fetch messages

```bash
wx history "<username_or_id>" --since YYYY-MM-DD --until YYYY-MM-DD -n 10000 --json > "%TEMP%\wx-msgs.json"
```

- Default cap `10000`; raise for very long threads.
- Filter by `timestamp` locally after load.
- Ranges > 7 days or > 500 messages: consider splitting per 3-day batches then meta-summary.

**Incremental**: read `{folder}/history.json` → `last_digest.last_message_time`; drop messages `<=` anchor. If zero remain, report and skip.

**Parse fields**: `local_id`, `sender` / `from_nickname`, `from_wxid`, `content`, `timestamp`, `type`.

Skip: `[系统]`, `revokemsg`, bare `[图片]` unless user asked to list media inventory.

---

## 4. Self attribution

From EXTEND: replace messages from `self_wxid` with `self_display` in stats and quotes.

Resolve ambiguous nicks (≤2 chars, `test`, etc.) via `wx contacts --query`.

---

## 5. Output paths (per folder)

| Artifact | Group | Private |
|----------|-------|---------|
| Digest | `YYYY-MM-DD.md` or `YYYY-MM-DD_YYYY-MM-DD.md` | same |
| Profiles | `profiles/{wxid}-{nick}.md` | N/A (use memory + digest) |
| Memory | `memory/{wxid}.yaml` | `memory.md` |
| Playbook | `playbook-{wxid}.md` | `playbook.md` |
| History | `history.json` + optional `history-digests.jsonl` | `history.json` |

---

## 6. Large JSON handling

Do not load entire `%TEMP%\wx-msgs.json` into context at once if > 200 messages.

Use Python/jq slices, or `Read` with offset/limit on a pre-split file.

Example skeleton pass (Python one-liner in shell):

```python
import json; d=json.load(open(r"%TEMP%\wx-msgs.json",encoding="utf-8"))
msgs=d["messages"] if isinstance(d,dict) else d
print(len(msgs), msgs[0]["time"], msgs[-1]["time"])
```
