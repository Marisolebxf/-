---
name: gkx-feishu-file-sync
description: 把本地文件（md、xlsx、docx、pdf 等）覆盖上传到飞书云空间已有文件，效果等同网页「上传新版本」，链接不变。不开浏览器，只用 Python 标准库。Use when the user says 同步到飞书、推到飞书文件、更新飞书上的文件、上传新版本, or gives a https://*.feishu.cn/file/<token> link with a local file.
---

# gkx-feishu-file-sync · 本地文件 → 飞书云空间文件（保留链接）

## 做什么

对飞书云空间里已经存在的普通文件（链接形如 `https://xxx.feishu.cn/file/<file_token>`）上传一份新版本。链接、file_token、分享权限都不变，飞书历史记录里会多一个版本。

用的是飞书官方接口 `POST /open-apis/drive/v1/files/upload_all`，请求里多传 `file_token` 就是原地覆盖，和官方 `lark-cli drive +upload --file-token` 的语义相同。

不适用：
- 在线文档或在线表格（`/docx/`、`/sheets/`、`/wiki/`）。往在线表格里写数据用 `gkx-feishu-case-sync`。
- 大于 20 MB 的文件（要走分片接口，脚本暂不支持）。
- 第一次新建上传。先在飞书网页里把文件传上去一次，拿到链接，以后都用本 skill 更新。

## 一次性准备（每个文件只做一次）

统一用自建应用「GKX周报和WBS」，App ID `cli_aa7b0396a878dcf7`（2026-11-13 已验证可覆盖上传）。注意：部分机器 `.env` 里的 `FEISHU_APP_ID` 是另一个应用 `cli_aa698af4efb9dc09`，它没开云空间权限，会报 `99991672`。

1. **应用权限**（已开通，新换应用时才需要）：开发者后台给应用开通 `drive:file:upload`（或 `drive:file`、`drive:drive` 任选一个），然后**创建版本并发布**。只开通、不发布，权限不会生效。
2. **文件协作者**（每个文件做一次）：在飞书里打开目标文件，「…」→「文档权限」或「添加文档应用」→ 搜「GKX周报和WBS」→ 权限选**可编辑**。
3. **凭证**：设 `LARK_APP_ID` / `LARK_APP_SECRET`（优先），或 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`；都没设时脚本读编排仓 `.env` 里的 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`。App Secret 向应用管理员要，不进 git、不贴群聊。

```powershell
$env:LARK_APP_ID='cli_aa7b0396a878dcf7'; $env:LARK_APP_SECRET='<向管理员要>'
```

## 用法

在编排仓根目录执行。Windows 用 `python`，macOS 用 `python3`。

```powershell
# 试跑：取令牌、核对本地文件，不写飞书
python .cursor/skills/gkx-feishu-file-sync/scripts/push_file.py `
  --pair "agent-delivery/xxx/指标填写规范-v0.1.md" https://zhipu-ai.feishu.cn/file/CjMRbUFaWo3XHhxM2jJciLaZnEe `
  --pair "agent-delivery/xxx/指标清单填写模板-v0.1.xlsx" https://zhipu-ai.feishu.cn/file/IH1abBecqo6e4VxQYmUcQRocn6e

# 正式覆盖：同样的命令加 --apply
python .cursor/skills/gkx-feishu-file-sync/scripts/push_file.py --pair ... --pair ... --apply

# 离线自检（不联网）
python .cursor/skills/gkx-feishu-file-sync/scripts/push_file.py --self-check
```

- `--pair <本地文件> <飞书链接或 file_token>`：可以重复，一次同步多份。
- 成功输出 `[ok] 文件名 -> file_token=... version=...`。到飞书里刷新，「历史记录」里能看到新版本。
- 飞书上的文件名会改成本地文件名。两边文件名保持一致就不会变。

## agent 执行纪律

1. 先跑一次不带 `--apply` 的试跑，确认本地路径和链接一一对应，再加 `--apply`。
2. 本地文件如果在 git 仓里，先提交推送，再同步飞书，保证飞书上的版本在仓里能找到。
3. 要先重新生成 Excel 时，生成前请用户在 WPS 或 Excel 里关掉该文件，否则写不进去。
4. 报错时按下表处理，不要改走浏览器。

## 报错速查

| 报错 | 原因 | 处理 |
|---|---|---|
| `99991672 Access denied ... drive:file:upload` | 应用没开云空间权限，或开了没发布 | 按准备第 1 步开权限并发布版本 |
| `1061004 forbidden` | 应用不是该文件的协作者，或只能阅读 | 按准备第 2 步把应用加为可编辑 |
| `1061002` / not found | file_token 不对，或文件已被删除 | 核对链接 |
| `99991663` | APP_ID / APP_SECRET 不对 | 向管理员核对 |
| 提示缺 `parent_node` | 覆盖已有文件实测不需要；如遇飞书要求带文件夹 token | 加 `--folder-token <文件夹 token>`，取文件夹链接 `/drive/folder/<token>` 的末段 |
| `1061045` | 飞书内部可重试错误 | 脚本已自动重试 3 次；仍失败稍后再跑 |
