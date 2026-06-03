# Profiles — group member portraits

Based on [baoyu-wechat-summary profiles](C:\Users\86199\.agents\skills\baoyu-wechat-summary\references\profiles.md). **Normal profiles only** — shiki+ defaults to no `profiles-roast/` unless `allow_roast: true` and user requests毒舌.

Path: `{data_root}/{group_id}-{group_name}/profiles/{wxid}-{nickname}.md`

Memory facts live separately in `memory/{wxid}.yaml` — see [memory-schema.md](memory-schema.md).

---

## 1. Frontmatter

```yaml
---
name: "当前昵称"
wxid: "wxid_xxx"
aliases: []
first_seen: "YYYY-MM-DD"
last_seen: "YYYY-MM-DD"
total_messages: N
digest_appearances: N
avg_messages_per_digest: N.N
relationship_to_self: friend
---
```

`relationship_to_self`: set on first memory/playbook run; user can override via AskQuestion.

---

## 2. Body sections (fixed order)

```
角色标签

• 4-6 短语

关注领域

• …

发言风格

1-3 句

互动模式

• 与某某 …

记忆点摘要

• 指向 memory/{wxid}.yaml 的关键字段（生日 MM-DD、likes、taboos 各最多 1 行）
• 无 memory 文件时写「暂无结构化记忆」

经典金句

• [YYYY-MM-DD] 「verbatim」

标志性事件

• [YYYY-MM-DD] 事件
```

### Update rules (same as baoyu)

| Section | Mode |
|---------|------|
| 角色标签, 关注领域, 互动模式 | Merge, cap tags |
| 发言风格 | Refine only on clear new pattern |
| 记忆点摘要 | Rewrite from latest `memory/*.yaml` each run that updates memory |
| 经典金句, 标志性事件 | Append-only |

Threshold: update profile when user has **3+ messages** in batch (same as baoyu).

---

## 3. Step 3.7 — load for digest

For each active user in batch, read `profiles/{wxid}-*.md` and `memory/{wxid}.yaml` if present.

Condensed working block:

```
== {name} ==
标签: … | 记忆: 喜欢X，忌Y | 近期金句: …
```

Use for contrast/continuity in 群友画像; do not dump full files into digest.

---

## 4. Privacy

Follow [privacy.md](privacy.md). Profiles hold **public-to-group** behavior; do not move private 1:1 secrets from other folders into group profiles.
