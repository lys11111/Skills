---
name: shiki-wechat-summary-plus
description: >-
  读本机微信聊天记录（wx-cli），输出群/私聊精华、用户画像、记忆点（生日喜好礼物）、
  关系攻略（交友恋爱拉群）。触发词：微信总结+、群聊精华、私聊分析、用户画像、记忆点、
  恋爱、交友、攻略、filehelper。需安装 wx 命令。单文件 skill，无需 references 目录。
version: 0.1.0
requires: wx
---

# shiki-wechat-summary+（单文件版）

> **给接收方**：把本文件放进你的项目（任意目录），对话里 `@shiki-wechat-summary-plus.md` 或说「按 shiki-wechat-summary-plus 执行」。Agent 应**完整阅读并遵守**下文，无需其他附件。

## 前置（缺一则先指导用户完成）

1. 安装 [wx-cli](https://github.com/jackwener/wx-cli)：`npm install -g @jackwener/wx-cli`
2. 微信 4.x 已登录 → `wx init` → `wx daemon start` → `wx sessions --json --limit 5` 有数据
3. 在项目根或用户目录创建配置（二选一，先找到先用）：
   - `.shiki-skills/shiki-wechat-summary-plus/EXTEND.md`
   - `%USERPROFILE%\.shiki-skills\shiki-wechat-summary-plus\EXTEND.md`

```yaml
self_wxid: wxid_你的id
self_display: 你的昵称
data_root: ./wechat          # 报告输出根目录
default_time_range: 7d
include_playbook_in_digest: true
allow_roast: false
```

Windows 跑 wx 用 `cmd /c "wx history ..."`，大 JSON 写到 `%TEMP%`，不要一次性塞进对话。

---

## 模式选择

| 模式 | 用户怎么说 | 产出 |
|------|------------|------|
| group_digest | 总结 XX 群、带攻略 | `{data_root}/{群id}-{群名}/YYYY-MM-DD.md` + profiles + memory |
| private_digest | 总结私聊、文件传输助手 | `{data_root}/private/{wxid}-{名}/` + memory.md |
| memory_only | 记住 TA 喜欢… | 只更新 memory 文件 |
| playbook | 怎么聊 TA、送礼、拉群 | playbook-*.md |
| consult | 根据已有画像给建议 | 对话回答，可读已有 md/yaml |

---

## wx 拉取

**群**：`wx contacts --query "群名" --json` → `@chatroom`；文件夹 `{data_root}/{group_id}-{群名}/`

**私聊**：`wx sessions --json` → `chat_type: private`；文件夹 `{data_root}/private/{wxid}-{昵称}/`

**历史**：

```bash
wx history "<id或名>" --since YYYY-MM-DD --until YYYY-MM-DD -n 10000 --json > %TEMP%\wx-msgs.json
```

增量：读 `{folder}/history.json` 的 `last_message_time`，跳过更早消息。

跳过：`[系统]`、撤回、纯 `[图片]`（除非用户要媒体清单）。`self_wxid` 的消息显示为 `self_display`。

---

## 分析四轮 + 记忆 + 攻略

1. **Round 1 骨架**：话题列表（local_id 锚点）、发言统计、**记忆候选**（字段+原句+置信度）
2. **Round 2 成文**：按下方模板写 digest
3. **Round 3 审计**：骨架是否都写入、原句是否 verbatim
4. **Round M 记忆**：写入 memory（见下 Schema）
5. **Round P 攻略**：按画像写话术（稳妥/中等/冒险三档）

---

## 群聊 digest 结构

```markdown
# {群名} 群聊精华+
> 区间 · 消息数 · 生成日期

## 一、30 秒读懂（表：气质/结构/时间锚）
## 二、发言排行
## 三、话题时间线
## 四、主题深读（每主题 blockquote 原句）
## 五、群友画像卡（3+ 条/人：标签、风格、代表原句）
## 五-b、记忆点更新（本次有改动的 wxid）
## 六、关系攻略建议（语气/钩子/避免/可发示例句）
## 七、梗词典（可选）
## 八、附录（profiles/ memory/ 路径）
```

---

## 私聊 digest 结构

关系概览 → 高频话题 → 记忆点表 → 待跟进 → 近期攻略 3 条 → 关键原句。同步更新同目录 `memory.md`。

**文件传输助手**：按主题归档（学业/求职/工具/提示词），不做恋爱攻略。

---

## 记忆 Schema

**群**：`{folder}/memory/{wxid}-{昵称}.yaml`

**私聊**：`{folder}/memory.md`

```yaml
wxid: wxid_xxx
display_name: 昵称
relationship_to_self: friend   # friend|crush|partner|colleague|family|unknown
updated_at: "YYYY-MM-DD"
memory:
  birthday: null               # 仅 MM-DD，除非对话里给了完整日期
  likes: []
  dislikes: []
  gift_ideas: []
  taboos: []
  hobbies: []
  communication_style: null
  notes: []
evidence:
  - date: "YYYY-MM-DD"
    quote: "原句 verbatim"
    field: likes
    confidence: high           # high|low
```

更新：合并列表字段；evidence **只增不删**；推断标 `confidence: low`。

**群画像** `{folder}/profiles/{wxid}-{昵称}.md`：角色标签、关注领域、发言风格、互动模式、**记忆点摘要**、经典金句（追加）、标志性事件（追加）。每人本批 3+ 条消息才更新 profile。

---

## 攻略规则（Round P）

- 每条建议必须有聊天记录证据；无证据则写「证据不足，先确认」
- 三档：**稳妥 / 中等 / 冒险**
- 匹配对方语气（短句党就短句，梗群就 callback 群梗）
- **禁止**：PUA、骚扰、appearance 羞辱、逼 CS/约会/金钱
- 文末免责声明：AI 推断，尊重边界

群攻略 embedded 示例结构：

```markdown
### {昵称}
- 语气：…
- 钩子：…
- 避免：…
- 稳妥示例：「…」
```

---

## 隐私（必守）

不写进 memory/攻略：电话身份证住址、心理健康标签、未在**本会话**公开的隐私、用时间戳监视对方。

私聊禁止出轨/心理揣测。不把其他会话秘密写进群 profile。

`data_root` 勿提交公开 git。

---

## history.json（群/私聊文件夹内）

```json
{
  "last_digest": {
    "file": "2026-06-01.md",
    "date_range": "2026-02-06 ~ 2026-06-01",
    "message_count": 4371,
    "last_message_time": "06-01 01:57"
  }
}
```

每次 digest 后覆盖更新。

---

## 与 baoyu / wechat-chat-insight

- 只要群精华、不要记忆攻略 → baoyu-wechat-summary
- 要 topics.json / knowledge.json → wechat-chat-insight
- **本文件**：记忆点 + 恋爱交友 + 私聊 + 群攻略

---

## 接收方一句话用法

```
@shiki-wechat-summary-plus.md 用 shiki+ 总结「群名」最近 7 天，更新记忆和攻略
```

首次使用若缺 EXTEND.md，Agent 应先 AskUser 填写 `self_wxid` 与 `self_display` 再拉 wx。
