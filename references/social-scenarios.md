# Social scenarios — scenario branches

Use with [playbook-rules.md](playbook-rules.md). Pick the branch that matches user intent and `relationship_to_self`.

---

## 1. 群聊拉人 / 维系（friend, colleague）

**Signals**: low message count but high value; responds to `@`; specific game/topic hooks.

**Playbook focus**

- Fixed time + concrete activity (`22:30 4人雀魂差1`)
- Named role (`你来当牌理顾问`)
- Callback to group memes (裤衩子、大坝焚决) when evidenced

**Avoid**: long rules posts; generic「在吗」

---

## 2. 暧昧 / 追求（crush）

**Signals**: private thread; mixed initiative; personal sharing; no explicit boundary statements.

**Playbook focus**

- Steady low-pressure presence; shared interest threads
- Questions over declarations early
- Gift: small, stated-interest-aligned; note 证据不足时只建议「问清楚」

**Avoid**: love confessions as first move when chat is cold; jealousy framing; reading delays as tests

**Privacy**: no storing crush's data for「监视」reminders

---

## 3. 稳定关系（partner）

**Signals**: routine check-ins; logistics; inside jokes.

**Playbook focus**

- Maintenance: remember dates in memory (MM-DD); practical support
- Repair: acknowledge specific incident from chat, not generic apology template

---

## 4. 送礼 / 节日

**Inputs**: `likes`, `hobbies`, `gift_ideas`, `taboos`, past gifts mentioned.

**Output**

| 档位 | 说明 |
|------|------|
| 稳妥 | 低价格、明确喜好、易拒绝无压力 |
| 中等 | 需要一定了解 |
| 冒险 | 高个性化；标注需确认 |

Include 「若不确定，先问」 option always.

---

## 5. 冷场 / 已读不回

**Do**

- One light ping with new information (link, meme, shared plan)
- Change channel (「改天线下说」) if chat showed fatigue

**Don't**

- Double-text guilt;「你怎么不理我」; passive-aggressive memes

---

## 6. 道歉 / 修复（friend, partner, colleague）

- Reference **specific** friction from messages
- Short accountability + concrete next step
- No public group apology unless the harm was public

---

## 7. 文件传输助手 / 自备忘（private filehelper）

Treat as **self archive**, not a relationship.

- `private_digest`: thematic index (学业/求职/工具/提示词) + 高重要性原句
- `memory.md`: user's own preferences and recurring projects
- No flirt/playbook unless user explicitly frames another person

---

## 8. 咨询场景映射

| User says | Mode | Scenario |
|-----------|------|----------|
| 怎么约 TA 打游戏 | playbook | 群聊拉人 |
| 情人节送什么 | playbook | 送礼 |
| 好久没聊了 | playbook | 冷场 |
| 总结一下和小红的聊天 | private_digest | crush/partner |
| 记住她喜欢猫 | memory_only | any |
