# gkx-feishu-case-sync 使用手册

> 把「合规演示用例」的【输入与条件】同步到飞书在线表格的新增列（**只加列，绝不改动原有列与内容**）。
> 适用平台：Windows 10/11（PowerShell）与 macOS / Linux（bash/zsh）。手册面向**首次在新机器上从零跑通**的场景。

---

## 0. 这条链路怎么工作（30 秒理解）

```
本地 Markdown 用例文件（*-合规演示用例.md）
        │  python sync_cases_to_sheet.py
        ▼
飞书开放平台 API（tenant_access_token 鉴权）
        │  读表格层级（A–F 列）做标题匹配
        ▼
飞书在线表格（ Sheets）指定两列写入：
  L 列 = 合规用例·输入与条件
  M 列 = 用例来源文件
```

关键安全机制：

- **clean 模式**（默认）：写入前强制校验目标列全空，非空直接中止——保证绝不覆盖人工内容
- **merge 模式**（`--merge`）：列已有内容时的增量刷新，只重写本次命中的行，其他行零触碰
- 匹配不上 / 有歧义的用例**一律不写**，只进报告等人工核对

---

## 1. 准备飞书应用（管理员或应用创建人操作，每台机器只需一次配置）

> **❓ 常见疑问：需要安装飞书官方 MCP（`lark-mcp`）吗？——不需要。**
> 本 skill 的同步脚本是独立 Python 程序，直接调飞书开放平台 REST API（`tenant_access_token` 鉴权），只用 Python 标准库。MCP 仅在早期链路验证时用过，以及 wiki 链接换 token 时**可选**使用（见 §3.1）；不装 MCP 不影响本手册全流程，机器上也不需要 Node.js。

### 1.1 拿到 APP_ID / APP_SECRET

1. 打开 [飞书开放平台](https://open.feishu.cn/) → 开发者后台
2. 找到自建应用 **`GKX周报WBS`**（APP_ID 形如 `cli_xxxx`）；没有权限就找应用管理员要这两个值
3. 记下 **APP_ID** 和 **APP_SECRET**（Secret 只在创建时完整显示，丢失需重置）

> ⚠️ 这两个值是凭据，**不要提交进 git、不要写进仓库文件**。团队已有值请向管理员索取。

### 1.2 开通权限并发布版本（⚠️ 新电脑报错的头号原因）

脚本用到的 API 与所需权限：

| 脚本行为 | API | 需要的权限 scope |
|---|---|---|
| 获取访问令牌 | `/auth/v3/tenant_access_token/internal` | 无需单独 scope |
| 读表格元信息 / 单元格 | `sheets/v2`、`sheets/v3` | `sheets:spreadsheet:readonly`（建议直接开 `sheets:spreadsheet` 读写） |
| 写单元格 | `sheets/v2/values` PUT | `sheets:spreadsheet`（读写） |

操作步骤：

1. 开发者后台 → 你的应用 → **权限管理**
2. 开通：`sheets:spreadsheet`（读写，一劳永逸；最低要求 `sheets:spreadsheet:readonly` + 写场景会报权限错）
   - 可选加 `drive:drive`（后续贴图二期会用）
3. **创建版本并发布**：**权限管理页右侧「版本管理与发布」→ 创建版本 → 申请发布**，等管理员审批通过
   - ⚠️ **只开通权限不发布 = 权限不生效**。另一台电脑遇到的「明明开了权限还失败」基本都卡在这步

### 1.3 把应用机器人加为表格协作者（可编辑）

应用权限是「应用能干什么」，**协作者身份是「能碰到哪个文档」**，两者缺一不可：

1. 打开目标飞书表格（浏览器即可）
2. 右上角 **「...」→ 更多 → 添加文档应用**（或「文档应用」入口）
3. 搜索并添加应用 **`GKX周报WBS`**，权限选 **「可编辑」**
   - 「可阅读」只能读，写入时报 `9499 Forbidden / 403`

> 需要用到哪些表格，就给哪些表格加。新建了表格页签不用重加，协作者按文档生效。

---

## 2. 机器配置（Windows / macOS）

### 2.1 前置软件

| 软件 | 检查命令 | 版本要求 |
|---|---|---|
| Python 3 | `python --version`（mac 上可能是 `python3 --version`） | ≥ 3.8，**无需任何第三方包**（只用标准库） |
| git（可选，提交报告用） | `git --version` | 任意近期版本 |

脚本**只用 Python 标准库**（urllib/json/glob 等），不需要 pip install 任何东西。

### 2.2 设置环境变量

#### Windows（PowerShell，当前会话有效）

```powershell
$env:LARK_APP_ID = 'cli_xxxxxxxx'
$env:LARK_APP_SECRET = '你的Secret'
```

如果机器上已有 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`（其他工具在用），**无需再映射**——脚本已兼容两组名字（v1.1 起）：

```powershell
# 这两行可以跳过，脚本会自动回落到 FEISHU_* 变量
$env:LARK_APP_ID = $env:FEISHU_APP_ID
$env:LARK_APP_SECRET = $env:FEISHU_APP_SECRET
```

#### macOS / Linux（bash/zsh，当前会话有效）

```bash
export LARK_APP_ID='cli_xxxxxxxx'
export LARK_APP_SECRET='你的Secret'
```

同理，已有 `FEISHU_APP_ID` / `FEISHU_APP_SECRET` 的机器可直接用，不用映射。

#### 想持久化（可选，免得每次开终端都设）

- **Windows**：系统设置 →「编辑账户的环境变量」→ 新建用户变量 `LARK_APP_ID` / `LARK_APP_SECRET`；或 PowerShell 永久写注册表：
  ```powershell
  [Environment]::SetEnvironmentVariable('LARK_APP_ID', 'cli_xxxxxxxx', 'User')
  [Environment]::SetEnvironmentVariable('LARK_APP_SECRET', '你的Secret', 'User')
  ```
  设完**重开终端**才生效。
- **macOS/Linux**：写进 `~/.zshrc` 或 `~/.bashrc`：
  ```bash
  echo "export LARK_APP_ID='cli_xxxxxxxx'" >> ~/.zshrc
  echo "export LARK_APP_SECRET='你的Secret'" >> ~/.zshrc
  source ~/.zshrc
  ```

> ⚠️ 凭据持久化到个人机器环境变量是可接受的；**禁止**写进任何 git 仓库文件。

### 2.3 快速自检（30 秒确认配置通了）

```powershell
# Windows
python -c "import os; print('APP_ID set:', bool(os.environ.get('LARK_APP_ID') or os.environ.get('FEISHU_APP_ID')))"
```

```bash
# macOS
python3 -c "import os; print('APP_ID set:', bool(os.environ.get('LARK_APP_ID') or os.environ.get('FEISHU_APP_ID')))"
```

输出 `APP_ID set: True` 即环境变量就绪。

---

## 3. 跑一次完整同步（从试跑到写入）

### 3.1 拿目标表格参数

从表格 URL 里提取：

```
https://zhipu-ai.feishu.cn/sheets/CWMZsII5Ph9e2Ztm3NlcemfBnGf?sheet=d7d70e
                              └── spreadsheet_token ──┘   └ sheet_id ┘
```

- `spreadsheet_token` = `CWMZsII5Ph9e2Ztm3NlcemfBnGf`
- `sheet_id`（页签 id）= `d7d70e`

> 若 URL 是 `/wiki/<token>` 开头：先用 MCP `wiki_v2_space_getNode`（需已配好的飞书 MCP）把 wiki token 换成真实 obj_token 再用；没有 MCP 时也可在飞书网页端打开该 wiki 节点，从地址栏 `/sheets/<obj_token>?sheet=` 直接取。

### 3.2 第一步：试跑（dry-run，不写任何单元格）

进入编排仓根目录后执行。

**Windows（PowerShell）：**

```powershell
cd E:\zhipu\gkx-lumen\gkx-orchestration
python ".cursor\skills\gkx-feishu-case-sync\scripts\sync_cases_to_sheet.py" `
  --md-dir "agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例" `
  --spreadsheet CWMZsII5Ph9e2Ztm3NlcemfBnGf `
  --sheet-id d7d70e `
  --report "$env:TEMP\case-sync-dryrun.md"
```

**macOS / Linux（bash/zsh）：**

```bash
cd /path/to/gkx-lumen/gkx-orchestration
python3 ".cursor/skills/gkx-feishu-case-sync/scripts/sync_cases_to_sheet.py" \
  --md-dir "agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例" \
  --spreadsheet CWMZsII5Ph9e2Ztm3NlcemfBnGf \
  --sheet-id d7d70e \
  --report /tmp/case-sync-dryrun.md
```

看输出关键行：

```
[i] sheet=d7d70e rows=607
[i] files=46 seqs=372 cases=... bad_lines=0
[i] matched_rows=... unmatched_seqs=... ambiguous=... collisions=...
[i] report -> ...
```

打开报告文件核对：**匹配写入行、未匹配清单、歧义、冲突**。有任何未匹配/歧义都先看报告再决定是否写入。

### 3.3 第二步：正式写入

试跑确认无误后，加 `--apply`：

```powershell
# Windows：同样的命令 + --apply
python ".cursor\skills\gkx-feishu-case-sync\scripts\sync_cases_to_sheet.py" `
  --md-dir "agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例" `
  --spreadsheet CWMZsII5Ph9e2Ztm3NlcemfBnGf `
  --sheet-id d7d70e --apply
```

macOS/Linux 同理（`python3` + 反斜杠换行改 `\`）。

写入成功输出：`[i] written rows=N, revisions=[...]`。到飞书表格里刷新即可看到 L/M 两列新内容，原有列零改动。

### 3.4 常用变体

```powershell
# 只同步一部分用例（按文件名过滤，如只同步政策 POL-*）
... --filter "POL-*" --merge --apply

# 列已被写过、想增量刷新（只重写本次命中的行）
... --merge --apply

# 换目标列（默认 L,M；必须选一对空列）
... --cols N,O --apply
```

| 参数 | 说明 |
|---|---|
| `--md-dir`（必填） | 用例 markdown 目录 |
| `--spreadsheet`（必填） | 表格 token（URL 里 `/sheets/` 后那段） |
| `--sheet-id`（必填） | 页签 id（URL 里 `?sheet=` 后那段） |
| `--cols` | 目标两列，默认 `L,M`（输入与条件, 来源）；**必须为空列**（clean 模式） |
| `--filter` | 只取文件名匹配 glob 的用例，如 `POL-*`；默认 `*` 全部 |
| `--merge` | 增量刷新：只重写本次命中的行，其他行不动；表头只在缺失时补 |
| `--apply` | 真正写入；不加则只出报告 |
| `--report` | 报告输出路径（默认落在用例目录，按日期命名） |

---

## 4. 报错速查表（按报错信息对号入座）

| 报错 | 原因 | 解决 |
|---|---|---|
| `[x] 请设置 LARK_APP_ID / LARK_APP_SECRET` | 环境变量没设或当前终端没生效 | 按 §2.2 设置；持久化设置后要**重开终端**；mac 注意用 `python3` |
| `99991663 / 99991661 app_token 无效`（取 token 失败） | APP_ID / APP_SECRET 错误 | 核对两个值；Secret 丢失去开放平台重置 |
| `9499 Forbidden` / `403`（写入时） | 机器人只有可阅读权限，或不是协作者 | §1.3 重新加协作者并给**可编辑** |
| `91403 Forbidden`（读也失败） | 应用没被加为文档协作者 | §1.3 添加文档应用 |
| `permission deny`（token 都拿不到 / API 全挂） | 权限开了但**版本没发布** | §1.2 创建版本并发布，等审批通过 |
| `90215 not found sheetId` | range 分隔符写错（内部已用 `!`，若手改脚本注意） | 页签与范围之间必须是 `!` 不是 `.` |
| `9499 Missing required parameter: ValueRange` | 写接口 body 没包 `valueRange`（内部已处理） | 若手改脚本，body 必须是 `{"valueRange": {...}}` |
| `[x] 目标列 L:M 已有内容... 中止` | clean 模式防覆盖保护触发 | 这**不是故障**。确认可以刷新→加 `--merge`；要写别的列→`--cols`；都不确定→先出 dry-run 报告人工看 |
| `cannot access local variable ...` / `SyntaxError` | 脚本被手改坏 | `git checkout -- .cursor/skills/gkx-feishu-case-sync/scripts/sync_cases_to_sheet.py` 还原 |

> 关于 `feishu-project-native` 的 MCP 授权（`mcp_auth`）：那只影响「飞书项目」相关 MCP 工具，**与本 skill 的表格同步无关**，不做也能跑通本手册全流程。本 skill 本身不需要任何飞书 MCP。

---

## 5. 新机器从零跑通清单（Checklist）

- [ ] Python 3 ≥ 3.8 可用（`python --version` / `python3 --version`）
- [ ] 拿到 `GKX周报WBS` 的 APP_ID / APP_SECRET（§1.1）
- [ ] 应用开通 `sheets:spreadsheet` 权限且**已发布版本**（§1.2）
- [ ] 机器人已加为目标表格**可编辑**协作者（§1.3）
- [ ] 环境变量已设置且当前终端生效（§2.2，自检输出 `True`）
- [ ] dry-run 出报告且匹配结果可接受（§3.2）
- [ ] `--apply` 写入，飞书表格里抽查 2–3 行（§3.3）

全部打勾 = 配置与链路全通。之后日常使用只需 §3.2 → §3.3 两步（环境变量会话内有效，重开终端需重设或已持久化）。

---

## 6. 与 CI / 其他工具共用凭据

- 若团队后续统一走 `.env` 或 CI 变量注入 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`，本脚本**零改动兼容**，无需 LARK_*/FEISHU_* 映射
- `feishu-project-native` MCP 的授权体系与本项目独立，互不影响
