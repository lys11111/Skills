# Memory schema — per-chat memory files

Memory is **scoped to one chat folder** (one group or one private thread). Do not auto-merge the same `wxid` across different folders unless the user explicitly asks.

Load this file during **Round M** and when running `memory_only` mode.

---

## 1. Group chat — `memory/{wxid}.yaml`

Path: `{data_root}/{group_id}-{group_name}/memory/{wxid}-{nickname}.yaml`

Filename: sanitize like profiles (`/ \ : * ? " < > |` → `_`, cap 200 chars). Stable key is `wxid`.

### 1.1 Required top-level fields

```yaml
wxid: wxid_xxxxxxxx
display_name: 当前昵称
relationship_to_self: friend   # friend | crush | partner | colleague | family | unknown
updated_at: "2026-06-01"
memory:
  birthday: null              # "MM-DD" only unless user explicitly stored full date in chat
  likes: []
  dislikes: []
  gift_ideas: []
  taboos: []
  hobbies: []
  communication_style: null   # one short sentence
  notes: []                   # free-form bullets, each short
evidence:
  - date: "2026-02-06"
    quote: "原句 verbatim"
    field: hobbies            # which memory field this supports
    confidence: high          # high | low — low = inference
```

### 1.2 Field rules

| Field | Rules |
|-------|--------|
| `birthday` | Prefer `MM-DD`. Full `YYYY-MM-DD` only if the person said it in chat. |
| `likes` / `dislikes` / `hobbies` | Merge dedupe by meaning. Cap display lists at ~12 items; keep full history in `evidence`. |
| `gift_ideas` | Suggestions grounded in likes/hobbies; tag inferred ideas with `confidence: low` in evidence. |
| `taboos` | Things that annoy them or topics to avoid (from chat, not stereotype). |
| `communication_style` | Refine when a new pattern is clear; do not rewrite every run. |
| `notes` | Append-only short bullets (e.g. "深夜更活跃"). |

### 1.3 Update procedure

1. Read existing file if present.
2. From this batch, extract new memory candidates with dated quotes.
3. **Merge** list fields; **refine** `communication_style` only when warranted.
4. Append to `evidence` — never delete evidence rows.
5. On conflict (old `likes` vs new signal), keep both in evidence; update list to reflect latest understanding and add a `notes` bullet if needed.
6. Set `updated_at` to digest end date.
7. Run `python scripts/validate-memory.py <path>` when available.

---

## 2. Private chat — `memory.md`

Path: `{data_root}/private/{wxid}-{nickname}/memory.md`

Same semantic fields as §1, wrapped in YAML frontmatter + optional markdown body for human notes:

```markdown
---
wxid: wxid_xxxxxxxx
display_name: 小红
relationship_to_self: crush
updated_at: "2026-06-01"
memory:
  birthday: "03-15"
  likes: ["猫", "独立游戏"]
  ...
evidence:
  - date: "2026-05-20"
    quote: "..."
    field: likes
    confidence: high
---

## 人工备注

（用户或 agent 手写的补充，不参与自动覆盖）
```

Private `memory.md` is the **single counterpart** for that thread (no `memory/` subfolder per wxid).

---

## 3. Confidence and inference

- **high**: direct statement by the person (`我喜欢…`, `别送花`, `我生日是…`).
- **low**: inferred from behavior, third-party mention, or weak signals.

Store low-confidence items in `memory` only when useful for playbooks; always attach `confidence: low` in `evidence`.

---

## 4. Link to profiles

Group `profiles/{wxid}-*.md` holds behavioral portrait (tags, quotes, events).

`memory/{wxid}.yaml` holds **actionable personal facts** for social/playbook use.

In digest **群友画像**, add one line: `记忆点见 memory/{wxid}.yaml` when memory was updated this run.
