# Privacy and ethics — shiki-wechat-summary-plus

Applies to digests, profiles, memory files, and playbooks. Stricter than group-only summaries when handling **private chats** or **romantic/social** advice.

---

## 1. Inherited from baoyu (always forbidden)

Do not persist in profiles, memory, or playbooks:

- Real-world full names inferred outside what the person used in chat
- Phone, email, ID numbers, home/work addresses, exact birth year unless they stated it
- Health, medical, or psychological labels (even if self-disclosed — do not bake into permanent memory)
- Private romantic/family details not openly discussed by that person in **this** chat
- Embarrassing **private** failures (job rejection mentioned once, etc.)
- Sleep/timezone surveillance from message timestamps

---

## 2. Private chat extras

- Do not infer cheating, stalking narratives, or "they read you at 3am so they care."
- Do not store or repeat content from **revoked** messages as facts.
- Treat filehelper / self-notes as **user's own data** — still warn before exporting paths with API keys or passwords; redact obvious secrets in digests unless user asked for full dump.

---

## 3. Playbook and social advice

**Allowed**

- Tone-matched openers, activity invites, gift ideas grounded in stated likes
- "Avoid X topic" when evidenced in chat
- Light humor matching group norms

**Forbidden**

- PUA, manipulation, guilt-tripping, love-bombing scripts
- Deception (fake emergencies, impersonation)
- Pressure for dates, sex, or money
- Appearance/body shaming; identity-based attacks
- Instructions to violate someone's stated boundaries

**Required disclaimers in playbooks**

- Label inferred points: `（基于聊天记录推断）`
- Offer 2–3 tiers: 稳妥 / 中等 / 冒险 — user picks
- Note when evidence is thin: `证据不足，建议先闲聊确认喜好`

---

## 4. Roast / 毒舌

- Default **off** (`allow_roast: false` in EXTEND.md).
- Never generate roast for `relationship_to_self: crush | partner` private threads.
- Roast the take, not the person (same as baoyu).

---

## 5. Storage and sharing

- `data_root` contains chat excerpts — do not commit to public repos without user consent.
- Playbooks are for the user's personal use; not for sharing with the subject without their consent.
