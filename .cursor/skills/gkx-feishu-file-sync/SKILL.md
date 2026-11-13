---
name: gkx-feishu-file-sync
description: 飞书文件与在线文档的本地往返。覆盖上传云空间文件（链接不变）；或把在线文档（/docx/、指向 docx 的 /wiki/）拉到本地，用 Cursor 改文字后再写回，只改动过的段落。不开浏览器，只用 Python 标准库。Use when the user says 同步到飞书、推到飞书文件、上传新版本、用 Cursor 改飞书文档、拉下飞书文章来改, or gives a feishu.cn/file or /docx or /wiki link.
---

# gkx-feishu-file-sync · 本地文件 → 飞书云空间文件（保留链接）

> 团队成员（新手）看 [USAGE.md](./USAGE.md)：从零配置到上传、报错对照。

## 做什么

对飞书云空间里已经存在的普通文件（链接形如 `https://xxx.feishu.cn/file/<file_token>`）上传一份新版本。链接、file_token、分享权限都不变，飞书历史记录里会多一个版本。

用的是飞书官方接口 `POST /open-apis/drive/v1/files/upload_all`，请求里多传 `file_token` 就是原地覆盖，和官方 `lark-cli drive +upload --file-token` 的语义相同。

不适用：
- 在线表格（`/sheets/`）。往表格里写数据用 `gkx-feishu-case-sync`。在线文档用下面的 `feishu_edit.py`。
- 大于 20 MB 的文件（要走分片接口，脚本暂不支持）。
- 第一次新建上传。先在飞书网页里把文件传上去一次，拿到链接，以后都用本 skill 更新。

## 用 Cursor 改线上文章

脚本 `scripts/feishu_edit.py`。支持云空间文件（`/file/`）和在线文档（`/docx/`，以及指向 docx 的 `/wiki/`）。

```powershell
# 1. 拉到本地（同时生成 同名.feishu.json 快照，不要删、不要提交）
python .cursor/skills/gkx-feishu-file-sync/scripts/feishu_edit.py pull "<飞书链接>" --out "本地.md"
# 2. 在 Cursor 里改本地.md
# 3. 先看将要改哪些段，再写回
python .cursor/skills/gkx-feishu-file-sync/scripts/feishu_edit.py push "本地.md"
python .cursor/skills/gkx-feishu-file-sync/scripts/feishu_edit.py push "本地.md" --apply
```

在线文档拉下来是带标记的文本，每段前面一行 `<!-- b:<block_id> <类型> -->`。只改标记下面的文字。

- 写回只更新文字变了的段落，其它段落和格式不动。
- 不支持新增段落、删除段落、改标题级别、改表格单元格。标记标了 `readonly` 的段（含 @人、公式）会跳过。
- 一段里原来有多种行内样式（加粗、链接混排）时，改完后整段沿用第一段样式。
- pull 之后如果线上又被别人改过同一段，push 会停下来，要求重新 pull。
- 云空间文件走整份覆盖，和 `push_file.py` 相同，但会先核对线上内容是否还是 pull 时的那份。

2026-11-13 实测：在线文档拉取和「无改动」判断已用真实文档跑通（300 段）。写回按官方 `PATCH .../blocks/{id}` 的 `update_text_elements` 实现，第一次对某篇文档 `--apply` 前先看试跑输出。应用需要能读、改该文档：把「GKX周报和WBS」加成可编辑；若报缺 `docx:document` 权限，在开发者后台开通并发布版本。

## 一次性准备（每个文件只做一次）

统一用自建应用「GKX周报和WBS」，App ID `cli_aa7b0396a878dcf7`（2026-11-13 已验证可覆盖上传）。注意：部分机器 `.env` 里的 `FEISHU_APP_ID` 是另一个应用 `cli_aa698af4efb9dc09`，它没开云空间权限，会报 `99991672`。

1. **应用权限**（已开通，新换应用时才需要）：开发者后台给应用开通 `drive:file:upload`（或 `drive:file`、`drive:drive` 任选一个），然后**创建版本并发布**。只开通、不发布，权限不会生效。
2. **文件协作者**（每个文件做一次）：在飞书里打开目标文件，「…」→「文档权限」或「添加文档应用」→ 搜「GKX周报和WBS」→ 权限选**可编辑**。
3. **凭证**：专用变量 `FEISHU_DRIVE_APP_ID` / `FEISHU_DRIVE_APP_SECRET`，写在编排仓 `.env`（已被 git 忽略，模板见 `.env.example`）或环境变量里。原有的 `FEISHU_APP_ID` / `FEISHU_APP_SECRET` 留给多维表格、日报等其他同步，不要改。App Secret 向应用管理员要，不进 git、不贴群聊。

```
# 编排仓 .env
FEISHU_DRIVE_APP_ID=cli_aa7b0396a878dcf7
FEISHU_DRIVE_APP_SECRET=<向管理员要>
```

脚本取凭证的顺序：先环境变量、后 `.env`；每处按 `FEISHU_DRIVE_APP_*` → `LARK_APP_*` → `FEISHU_APP_*`，取第一组 ID 和 SECRET 都有值的。

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
