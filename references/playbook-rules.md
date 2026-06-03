# Playbook rules — 关系攻略生成

Load during **Round P** or `playbook` / `consult` modes. Output must match the subject's **communication_style** and evidence in memory/profiles.

See also [social-scenarios.md](social-scenarios.md) and [privacy.md](privacy.md).

---

## 1. Inputs

Read in order:

1. `memory/{wxid}.yaml` or private `memory.md`
2. `profiles/{wxid}-*.md` (group) if exists
3. Latest digest excerpts for this chat (if any)
4. User's goal this run: `invite` | `gift` | `open_line` | `repair` | `deepen` | `general`

---

## 2. Output file shape

`playbook-{wxid}-{nickname}.md` (group) or `playbook.md` (private)

```markdown
# 关系攻略 · {display_name}

> 关系：{relationship_to_self} · 基于 {date_range} 聊天记录  
> 证据强度：{strong|mixed|weak} · 生成 {YYYY-MM-DD}

## 一句话读懂 TA

{1-2 句，只写有证据的性格/节奏}

## 沟通要点

| 维度 | 建议 |
|------|------|
| 语气 | … |
| 最佳时机 | …（仅当聊天中有作息线索） |
| 避免 | taboos |
| 有效钩子 | likes / hobbies |

## 分场景话术（示例原句风格）

### 稳妥
- …

### 中等
- …

### 冒险
- …

## 送礼 / 邀约（如适用）

- …

## 证据摘录

- [date] 「quote」→ 支撑 …

## 免责声明

本攻略由 AI 根据本地聊天记录生成，推断处已标注；请尊重对方边界，勿用于操纵或骚扰。
```

---

## 3. Generation rules

1. **Evidence first** — every tactic ties to a quote or memory field; no generic pickup lines.
2. **Match voice** — if they use short `@` bursts, suggest short `@` bursts; if they use dry humor, don't suggest formal essays.
3. **Three tiers** — 稳妥 = low risk; 中等 = needs rapport; 冒险 = only if chat already playful.
4. **Group vs private** — group playbooks include `@` timing and public-face concerns; private playbooks avoid exposing group-only jokes.
5. **No roast by default** — supportive/neutral tone unless user asked for 毒舌 and `allow_roast: true`.
6. **Weak evidence** — output shorter playbook + explicit "先确认喜好" steps instead of inventing hobbies.

---

## 4. Group digest embedded section

When `include_playbook_in_digest: true`, add **关系攻略建议** after 群友画像:

Per active user (3+ msgs) OR only users user named:

```markdown
### {昵称}

- **语气**：…
- **钩子**：…
- **避免**：…
- **可直接发送**（稳妥）：「…」
```

Keep 3-5 lines per person in digest; full detail goes to `playbook-*.md` if user requested.

---

## 5. consult mode

Answer in chat with bullets; cite file paths. Do not rewrite memory unless user asked. Max ~400 words unless user wants depth.
