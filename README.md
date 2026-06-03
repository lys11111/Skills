# shiki-wechat-summary-plus

[![Cursor Agent Skills](https://img.shields.io/badge/Cursor-Agent%20Skills-blue)](https://cursor.com/docs/context/skills)
[![wx-cli](https://img.shields.io/badge/wx--cli-required-green)](https://github.com/jackwener/wx-cli)

微信群 / 私聊：**精华摘要 · 用户画像 · 记忆点 · 关系攻略**（恋爱、交友、拉群等）。依赖本机 [wx-cli](https://github.com/jackwener/wx-cli) 读取微信记录，**数据不出本机**。

## 快速链接

| 用途 | 文件 |
|------|------|
| **单文件版**（下载后任意目录 `@` 即可） | [shiki-wechat-summary-plus.md](shiki-wechat-summary-plus.md) |
| **完整 Skill**（推荐安装到 Cursor） | 本仓库根目录 `SKILL.md` + `references/` + `scripts/` |
| **ZIP 打包** | [Releases](https://github.com/lys11111/Skills/releases) 或仓库内 `shiki-wechat-summary-plus.zip` |

单文件 Raw 直链：

```text
https://raw.githubusercontent.com/lys11111/Skills/main/shiki-wechat-summary-plus.md
```

本 Skill 位于仓库 [lys11111/Skills](https://github.com/lys11111/Skills)。

## 安装（3 步）

### 1. 克隆到 Cursor Skills 目录

任选一种：

| 方式 | 命令 / 路径 |
|------|-------------|
| **项目内**（可进 git） | `git clone <本仓库> <项目>/.cursor/skills/shiki-wechat-summary-plus` |
| **个人全局** | `git clone <本仓库> %USERPROFILE%\.cursor\skills\shiki-wechat-summary-plus` |

或下载 [shiki-wechat-summary-plus.zip](shiki-wechat-summary-plus.zip) 解压到上述路径。

### 2. 安装并初始化 wx-cli

```powershell
npm install -g @jackwener/wx-cli
wx init
wx daemon start
wx sessions --json --limit 5
```

微信 4.x 需已登录。风险说明见 [wx-cli README](https://github.com/jackwener/wx-cli)。

### 3. 配置 EXTEND.md

复制 [EXTEND.md.example](EXTEND.md.example) 为：

- `<项目根>/.shiki-skills/shiki-wechat-summary-plus/EXTEND.md`，或
- `%USERPROFILE%\.shiki-skills\shiki-wechat-summary-plus\EXTEND.md`

必改 `self_wxid`、`self_display`；可选 `data_root`（报告输出目录）。

## 怎么用

**完整 Skill**（克隆安装后）：在 Cursor 里说：

```text
用 shiki 总结 XX 群最近 7 天，带攻略
```

**单文件版**：把 [shiki-wechat-summary-plus.md](shiki-wechat-summary-plus.md) 放进任意项目后：

```text
@shiki-wechat-summary-plus.md 用 shiki+ 总结「群名」最近 7 天，更新记忆和攻略
```

## 输出目录（`data_root`，默认 `./wechat`）

```text
wechat/
├── {群id}-{群名}/
│   ├── YYYY-MM-DD.md
│   ├── profiles/
│   ├── memory/
│   └── playbook-*.md
└── private/{wxid}-{昵称}/
```


## 可选：校验记忆 YAML

```bash
python scripts/validate-memory.py path/to/memory.yaml
```

## 许可与免责

仅供个人学习；遵守微信用户协议与 wx-cli 说明；社交建议需人工判断，禁止骚扰或 PUA。
