# 把本地文件同步到飞书 · 新手指南

> 适合第一次用的同学。按顺序做，10 分钟内能跑通。
> 适用：Windows（PowerShell）和 macOS（终端）。

---

## 1. 这个工具能干什么

你本地改好了一份文件（比如 `.md`、`.xlsx`、`.docx`、`.pdf`），飞书云盘里已经有一份同名的旧文件。这个工具会把新文件**作为新版本**传上去：

- 飞书链接**不变**，之前发出去的链接仍然能打开最新内容；
- 分享权限、协作者都**不变**；
- 飞书「历史记录」里多一个版本，随时能回退。

效果和你在飞书网页上点「…」→「上传新版本」完全一样，只是不用开浏览器、可以一次传多份。

**不能做的：**

| 情况 | 怎么办 |
|---|---|
| 飞书上还没有这个文件 | 先在飞书网页里手动上传一次，拿到链接，以后用本工具更新 |
| 目标是在线文档或在线表格（链接里是 `/docx/`、`/sheets/`、`/wiki/`） | 本工具不支持，只支持链接里是 `/file/` 的云盘文件 |
| 文件超过 20 MB | 暂不支持，用网页上传 |

---

## 2. 第一次使用：准备三件事（只做一次）

### 2.1 电脑上有 Python 3

打开终端（Windows 按 `Win` 键搜「PowerShell」；Mac 打开「终端」），输入：

```powershell
python --version      # Windows
python3 --version     # Mac
```

看到 `Python 3.8` 或更高就行。没有的话装一个 [Python 3](https://www.python.org/downloads/)，安装时勾选「Add Python to PATH」。**不需要 pip 装任何包。**

### 2.2 填好凭证

1. 找淮政玮要「GKX周报和WBS」应用的 **App Secret**（一串 32 位字母数字）。
   ⚠️ 这是密码，不要发群、不要写进任何会提交到 git 的文件。
2. 打开编排仓根目录下的 `.env` 文件（`gkx-orchestration/.env`）。没有这个文件就把 `.env.example` 复制一份改名为 `.env`。
3. 找到或加上这两行，把 Secret 填进去：

   ```
   FEISHU_DRIVE_APP_ID=cli_aa7b0396a878dcf7
   FEISHU_DRIVE_APP_SECRET=这里填你拿到的Secret
   ```

4. 保存。`.env` 已被 git 忽略，不会被提交。

> 不要改 `.env` 里原有的 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`，那是别的同步工具在用。

### 2.3 让应用能改你的飞书文件

每个要同步的飞书文件，都要把应用加成协作者，**每个文件只加一次**：

1. 在飞书里打开那个文件；
2. 点右上角「…」→「文档权限」（或「更多」→「添加文档应用」）；
3. 搜索 **GKX周报和WBS**，添加，权限选 **可编辑**。

---

## 3. 日常使用

### 方式一：让 Cursor 里的 agent 帮你做（推荐）

在 Cursor 对话里直接说，例如：

> 把 `agent-delivery/xxx/方案-v0.2.md` 同步到飞书 https://zhipu-ai.feishu.cn/file/XXXXXXXX

agent 会先试跑核对，再正式上传，最后告诉你新版本号。

### 方式二：自己敲命令

**第 1 步：拿到飞书链接。** 在飞书里打开文件，复制浏览器地址栏，形如：

```
https://zhipu-ai.feishu.cn/file/CjMRbUFaWo3XHhxM2jJciLaZnEe
```

**第 2 步：进入编排仓根目录。**

```powershell
cd E:\zhipu\gkx-lumen\gkx-orchestration        # Windows，换成你自己的路径
```

```bash
cd ~/gkx-lumen/gkx-orchestration               # Mac，换成你自己的路径
```

**第 3 步：试跑（不会改飞书，只检查）。**

Windows：

```powershell
python .cursor/skills/gkx-feishu-file-sync/scripts/push_file.py `
  --pair "本地文件路径" "飞书链接"
```

Mac：

```bash
python3 .cursor/skills/gkx-feishu-file-sync/scripts/push_file.py \
  --pair "本地文件路径" "飞书链接"
```

看到下面这样就说明凭证、文件、链接都没问题：

```
[dry-run] 本地文件路径 (17000 B) -> https://feishu.cn/file/CjMR...
[i] 令牌已取到、文件已核对；加 --apply 正式覆盖
```

**第 4 步：正式上传。** 同样的命令末尾加 `--apply`：

```powershell
python .cursor/skills/gkx-feishu-file-sync/scripts/push_file.py `
  --pair "本地文件路径" "飞书链接" --apply
```

成功会显示：

```
[ok] 文件名 -> file_token=CjMR... version=7707...
```

**第 5 步：去飞书确认。** 刷新文件页面，点「…」→「历史记录」，最上面一条是「刚刚」就对了。

### 一次传多份

每份文件写一个 `--pair`：

```powershell
python .cursor/skills/gkx-feishu-file-sync/scripts/push_file.py `
  --pair "docs/规范.md"   "https://zhipu-ai.feishu.cn/file/AAAA" `
  --pair "docs/模板.xlsx" "https://zhipu-ai.feishu.cn/file/BBBB" --apply
```

### 小提示

- 路径里有中文、空格或括号时，**整段用英文双引号包起来**。
- Windows 命令换行用反引号 `` ` ``，Mac 用反斜杠 `\`。不想换行就写成一整行。
- 飞书上的文件名会变成本地文件名。两边名字一样就没影响；要改飞书显示名时，用目标名作本地文件名再覆盖，或调改名接口。
- 文件在 git 仓里的，建议先提交推送，再同步飞书，这样飞书上的每个版本在仓里都能找到。
- **链接**：上传前检查正文里没有 `./`、`../` 这类相对链接；飞书上要点得开，一律写成 `https://zhipu-ai.feishu.cn/...` 或公网 URL（无权限除外）。

---

## 4. 出错了怎么办

把报错里的 `code=` 后面的数字对一下：

| 报错里看到 | 意思 | 怎么解决 |
|---|---|---|
| `缺少凭证` | `.env` 里没填或填错了变量名 | 按 2.2 检查两行是否都在、Secret 是否填了 |
| `code=99991663` | App ID 或 Secret 不对 | 重新向淮政玮确认 Secret，注意别多复制空格 |
| `code=99991672` | 用的应用没有云盘权限 | 多半是 `.env` 里没配 `FEISHU_DRIVE_*`，脚本退回用了旧应用；按 2.2 配好 |
| `code=1061004` | 应用不是这个文件的协作者，或只能阅读 | 按 2.3 把应用加为**可编辑** |
| `code=1061002` | 链接不对或文件已被删 | 重新从飞书地址栏复制链接 |
| `不是云空间文件（/file/）链接` | 用的是 push_file.py，目标却是在线文档 | 在线文档改用第 6 节的 feishu_edit.py；在线表格不支持 |
| `本地文件不存在` | 路径写错 | 检查路径；含中文空格的路径要加双引号；路径是相对编排仓根目录的 |
| `大小 ... 必须在 1B–20MB 之间` | 文件为空或太大 | 超过 20 MB 用网页上传 |
| `Permission denied`（生成 Excel 时） | 文件正被 WPS / Excel 打开 | 关掉文件再重试 |
| `python 不是内部或外部命令` | 没装 Python 或没加 PATH | 按 2.1 安装；Mac 用 `python3` |

自检工具是否完好（不联网）：

```powershell
python .cursor/skills/gkx-feishu-file-sync/scripts/push_file.py --self-check
python .cursor/skills/gkx-feishu-file-sync/scripts/feishu_edit.py --self-check
```

两条都输出 `self-check ok` 即正常。

---

## 5. 一页速查

```
一次性：装 Python 3 → .env 填 FEISHU_DRIVE_APP_ID / FEISHU_DRIVE_APP_SECRET → 每个飞书文件加「GKX周报和WBS」为可编辑
每次：  cd 编排仓 → push_file.py --pair "本地" "飞书链接"（试跑）→ 加 --apply（上传）→ 飞书历史记录确认
```

有问题找淮政玮。

---

## 6. 用 Cursor 改飞书上的文章

适用：链接里是 `/docx/` 的在线文档，或指向文档的 `/wiki/` 链接。云空间文件（`/file/`）也能用这套命令，效果是整份覆盖。

**第 1 步：拉下来。**

```powershell
python .cursor/skills/gkx-feishu-file-sync/scripts/feishu_edit.py pull "https://zhipu-ai.feishu.cn/docx/XXXX" --out "文章.md"
```

会得到两个文件：`文章.md`（正文）和 `文章.md.feishu.json`（对照用的快照）。快照不要删、不要改、不要提交到 git。

**第 2 步：在 Cursor 里改 `文章.md`。**

正文被分成一段一段，每段上面有一行标记：

```
<!-- b:doxcnXXXX text -->
这里是这一段的文字，改这里。
```

- 只改标记下面的文字。
- 不要删、不要改 `<!-- b:... -->` 那一行，也不要自己加新的标记。想新增一段或删掉一段，到飞书网页上做。
- 标记末尾写着 `readonly` 的段先别动，写回时会自动跳过。

**第 3 步：先看改了什么，再写回。**

```powershell
python .cursor/skills/gkx-feishu-file-sync/scripts/feishu_edit.py push "文章.md"
```

输出里每一段都有删掉的旧文字和加上的新文字。确认无误后：

```powershell
python .cursor/skills/gkx-feishu-file-sync/scripts/feishu_edit.py push "文章.md" --apply
```

到飞书里刷新，只有改过的段落会变，其它段落和格式保持原样。

**常见提示：**

| 看到 | 意思 |
|---|---|
| `[i] 本地没有改动` | 文字和拉下来时一样，不用写回 |
| `[!] ... 线上在你 pull 之后被改过` | 别人也改了这段。重新 pull，把你的修改合进去再推 |
| `[x] 本地缺少 N 个段落标记` | 标记被删了。从飞书历史或重新 pull 恢复标记 |
| `code=99991672` 且提到 `docx` | 应用还没开文档权限。找淮政玮在开发者后台开通 `docx:document` 并发布 |
