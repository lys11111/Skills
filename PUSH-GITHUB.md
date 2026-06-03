# 推送到 GitHub（一次性）

本地仓库已初始化并完成首次提交，目录：`用于share的skills/`。

## 1. 登录 GitHub CLI

在终端执行（会打开浏览器）：

```powershell
gh auth login
```

选择：GitHub.com → HTTPS → Login with a web browser。

## 2. 创建仓库并推送

```powershell
cd "d:\桌面\skills相关\用于share的skills"

gh repo create shiki-wechat-summary-plus --public `
  --description "Cursor Agent Skill: WeChat digest, profiles, memory and playbooks via local wx-cli" `
  --source=. --remote=origin --push
```

若仓库名已被占用，改用：

```powershell
gh repo create 你的用户名/shiki-wechat-summary-plus --public --source=. --remote=origin --push
```

## 3. 更新 README 里的链接

推送成功后，把 [README.md](README.md) 中的 `REPLACE_OWNER` 换成你的 GitHub 用户名，再：

```powershell
git add README.md
git commit -m "docs: fix raw download links"
git push
```

单文件 Raw 链将为：

```text
https://raw.githubusercontent.com/<你的用户名>/shiki-wechat-summary-plus/main/shiki-wechat-summary-plus.md
```

## 不用 gh 时（手动）

1. 在 GitHub 网页新建空仓库 `shiki-wechat-summary-plus`（不要勾选 README）。
2. 执行：

```powershell
cd "d:\桌面\skills相关\用于share的skills"
git remote add origin https://github.com/<你的用户名>/shiki-wechat-summary-plus.git
git push -u origin main
```

## 仓库内容说明

| 路径 | 说明 |
|------|------|
| `SKILL.md` + `references/` + `scripts/` | 完整 Skill，克隆到 `.cursor/skills/shiki-wechat-summary-plus/` |
| `shiki-wechat-summary-plus.md` | 单文件版，社区 Raw 链分享用 |
| `shiki-wechat-summary-plus.zip` | 与线上一致的 zip 备份 |
| `.gitignore` | 排除 `wechat/`、`.shiki-skills/` |
