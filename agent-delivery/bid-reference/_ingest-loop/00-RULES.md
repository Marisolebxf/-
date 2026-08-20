# 00-RULES · SRS 拆解子 agent 必读

角色：doc / product 文档拆解。定义类任务，**禁止** ponytail 压短需规原文。

## 真源

- Excel（只读）：`D:\深圳市国际科技信息中心\20、原型评审\国际科技信息中心项目_需求规格说明书功能清单(各子系统).xlsx`
- 目录约定：`agent-delivery/bid-reference/srs/INDEX.md`、`SOURCE.yaml`
- 本叶范围：只做 `prompts/Axx.md` 写明的 **sheet + 三级/四级过滤**。范围外的行 **一行都不要写**。

## 必须用 officecli（禁止 pandas/openpyxl 当主读取）

1. 读 Cursor skill：`C:\Users\25456\.cursor\skills\officecli-xlsx\SKILL.md`（若无：`officecli skills install excel cursor`）
2. 不确定属性先 `officecli help xlsx`
3. 定向读取（PowerShell，路径必须双引号）：

```powershell
$oc = (Get-Command officecli).Source
$xlsx = "D:\深圳市国际科技信息中心\20、原型评审\国际科技信息中心项目_需求规格说明书功能清单(各子系统).xlsx"
& $oc view $xlsx outline
& $oc view $xlsx text --range "科技信息展示系统!A4:N18"
```

4. **分块**：每次 `--range` 不超过 **15 个数据行**。读完写入 MD，再拉下一块。禁止一次 dump 整表。
5. 单元格换行必须保留（`需规功能描述` 里的 (1)(2)(3) 不得拍扁成一句）。
6. 禁止改 Excel。禁止 `officecli set/add` 打到该 xlsx。

## 写入规则

- 只写 `agent-delivery/bid-reference/srs/` 下本叶目录 + 本 loop 的 `DONE-Axx.md`
- 每个 Excel 数据行 → 恰好一个 `###` 叶子（见 `srs/INDEX.md` §2）
- `excel_row` 用 officecli 路径里的 `row[N]`（表头占 1–3，数据从 4 起）
- `I`/`J`/`K`/`L` 空字符串：仍建叶子，标题用 `（空）`，不要丢行
- 招标列 F（或深度挖掘的 G）经常只在组首行有字：有则抄；空则写「（本行空）」**不要**自行从上组复制进正文，可在叶子加 `bid_desc_inherited: true` 并注明上一非空行号
- 文件名：四级功能名；Windows 非法字符 `\/:*?"<>|` 换成 `_`
- 同一四级很多叶子：仍放**同一个** `{四级}.md`，不要 1 行 1 文件
- 系统 `README.md`：列出本叶写过的四级文件、每个文件叶子数、对应 Excel 行号闭区间

## 禁止

- git commit / push
- 改 `task-registry.yaml`、`scope-baseline.yaml`、根目录旧招标 MD
- 发明验收标准、合并「相似」功能、删除核增/核减行
- 把「数据需求清单」行丢掉（它们也是需规行）

## 完工

在 `_ingest-loop/DONE-Axx.md` 写：

| 项 | 值 |
|----|----|
| sheet | |
| filter | |
| excel_rows | 闭区间列表，如 4–199 |
| expected_data_rows | 见 Axx |
| written_leaves | 必须 = expected |
| files | 相对 `srs/` 的路径列表 |
| gaps | 空单元格 / 超长单元格截断 / officecli 读失败 |

`written_leaves != expected` → 不得标完成，继续补块。
