# /goal B01 · 覆盖率对账（串行，全部 DONE-Axx 之后）

先读：`_ingest-loop/00-RULES.md`、`srs/INDEX.md`、`srs/SOURCE.yaml`、全部 `DONE-Axx.md`。

仍用 **officecli** 抽检，不要用 pandas 当主读取。

## 必做

1. 确认 `DONE-A01` … `DONE-A18` 都存在。缺哪个列哪个，**停止 cutover**。
2. 把各叶 `written_leaves` 加总，必须 = **2315**。
3. 每个系统目录应有 `README.md`；抽每个系统至少 3 个 `excel_row`：用

```powershell
$xlsx = "D:\深圳市国际科技信息中心\20、原型评审\国际科技信息中心项目_需求规格说明书功能清单(各子系统).xlsx"
officecli view $xlsx text --range "<Sheet>!M{row}:M{row}"
```

   与 MD 叶子「需规功能描述」**逐字**对比（深度挖掘用 N 列）。不一致记入 gaps。
4. 更新 `srs/INDEX.md`：补各系统 README 链接；若 2315 对齐且抽检无误，把 `SOURCE.yaml` `status` 改为 `coverage_ok`（**不要**改成 `cutover`，cutover 由人决定）。
5. 在根 `bid-reference/README.md` 顶部状态条改为「srs 覆盖已对账，待人宣布 cutover」。
6. 列出与旧招标 MD / `scope-baseline.yaml` 62 叶子的**差异备忘**（只记录，不改 baseline）。

产出：`_ingest-loop/DONE-B01.md`

禁止：删旧 MD、改 scope-baseline、commit。
