# Output formats — digest, private report, playbook

Load during Round 2 (write) and Round 3 (audit). Tone: **informative, actionable** — not roast unless explicitly enabled.

Reference layout: [雀魂群 digest example](d:\桌面\skills相关\wechat\44350643290@chatroom-雀魂&CS（击飞三角裤）\2026-02-06_2026-06-01.md) for rich group structure.

---

## 1. Group digest (`group_digest`)

### 1.1 Title

```markdown
# {群名} 群聊精华+
```

Blockquote meta line:

```markdown
> **区间** YYYY-MM-DD ~ YYYY-MM-DD · **消息** N 条 · **生成** YYYY-MM-DD
```

### 1.2 Sections (recommended order)

| # | Section | Content |
|---|---------|---------|
| 一 | 30 秒读懂 | Table: 群气质、发言结构、时间锚、活跃时段 + 一句话 |
| 二 | 发言排行 | Table: 昵称、条数、占比、角色标签 |
| 三 | 话题时间线 | ASCII or bullet timeline |
| 四 | 主题深读 | 3-6 themes; each with blockquote **原句** |
| 五 | 群友画像卡 | Per user 3+ msgs; optional HTML `profile-card` (avatar left) |
| 五-b | 记忆点更新 | Table: 昵称、本次新增 memory 字段（仅当有更新） |
| 六 | 关系攻略建议 | Per [playbook-rules.md](playbook-rules.md) §4 (if `include_playbook_in_digest`) |
| 七 | 梗词典 | Optional, group-specific |
| 八 | 附录 | profiles/ memory/ history.json 路径 |

### 1.3 Writing rules

- Quotes must be **verbatim** from messages.
- Attribute speakers with nickname (after `self_display` substitution).
- 群友画像: 表格 + 代表原句 + 互动轴（↔ 某人）when clear.
- Do not invent topics not in Round 1 skeleton.

### 1.4 history.json

Same shape as baoyu — update on each `group_digest` normal run.

---

## 2. Private digest (`private_digest`)

Path: `{data_root}/private/{wxid}-{name}/YYYY-MM-DD.md` or range filename.

```markdown
# 私聊摘要 · {对方昵称}

> **区间** … · **消息** N 条 · **关系** {relationship_to_self}

## 关系概览

1-2 段：互动频率、谁主动、整体温度（有证据）

## 高频话题

Bullets with sub-bullets of 原句

## 记忆点（结构化）

| 字段 | 内容 |
|------|------|
| birthday | MM-DD or — |
| likes | … |
| … | … |

（同步写入同目录 memory.md）

## 待跟进 / 未完成事项

From explicit plans in chat

## 近期攻略（3 条）

Actionable, 稳妥档优先

## 关键原句

Blockquotes, chronological or by theme

## 附录

- memory.md
- playbook.md（如有）
```

**filehelper**: use [social-scenarios.md §7](social-scenarios.md) — thematic index instead of relationship tone.

---

## 3. Playbook standalone

See [playbook-rules.md](playbook-rules.md) template.

---

## 4. memory_only output

Short confirmation message + list of fields updated in `memory/{wxid}.yaml` or `memory.md` with new evidence rows. No full digest unless user asked.

---

## 5. consult output

In-chat reply only unless user asked to save — then append to `{folder}/consult-YYYY-MM-DD.md`.

---

## 6. Optional HTML profile cards

When avatars exist under `{folder}/avatars/*.png`:

```html
<div class="profile-card">
<div class="profile-avatar"><img src="avatars/name.png" alt="昵称" /></div>
<div class="profile-body">
… table + 原句 …
</div>
</div>
```

PDF export is out of scope for the skill unless user requests a separate script.

---

## 7. Audit checklist (Round 3)

- Every skeleton topic appears in digest?
- Memory updates have evidence quotes?
- Playbook tiers present and disclaimers included?
- Privacy rules in [privacy.md](privacy.md) satisfied?
