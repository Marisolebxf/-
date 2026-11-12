# POL-L2-DS10-CMP-COVER-FDE · A 波次 · product

- 总单：`POL-L2-DS10-CMP-COVER-FDE-L01`
- 日期：2026-11-12
- 身份：product（本会话代写）
- 裁定真源：卡1=A、卡2=B；矩阵 `2026-11-12-政策重点比对-需规分句闭合.md`
- 档位建议：中档（不退定义规程）

## 1. 功能点 · 界面必见

| 分句 | 界面必见 | 空态 / 失败 |
|---|---|---|
| 213-3 变化统计 | 新旧对比 live：查询出 diff 行后，同屏见「新增 / 修改 / 删除」计数（由 diff 行 `change_type` 聚合） | 无分析列、无 diff 行 → 一句空态，不造 0 之外的口径 |
| 214-5 差异柱图 | 详情对比 live：与 mock 同结构出现柱图（支持力度 / 条件门槛 / 材料复杂度轴） | 力度无分 → 该轴空；门槛/材料无数值模型 → 轴空；**不造演示分** |
| 214-6 优缺点 | 详情对比 live 弹窗：每策一块「优点 / 缺点」 | 缺项列空 → 该策空态一句；live **禁** mock fixture 填数 |
| 217-5 PDF/Word | 标杆对标报告 live：分「导出 Word」「导出 PDF」；内容来自当次 `benchmark-report` 行 | 无行不产文件；不做 text/plain 冒充 |

不扩 216 主路径；不重开已闭合六维表读面。

## 2. 状态清单

| 状态 | 表现 |
|---|---|
| 未选够对象 / 未点开始 | 空态引导，不自动起 Job、不自动查 diff/报告 |
| 读中 | 按钮 loading；不清已返回块 |
| 读失败 | Alert；保留已读行 |
| 有行无分 / 无优缺点 | 图轴空或优缺点空态；诚实不造数 |
| 导出 | Word=.doc HTML 下载；PDF=可打印页另存（与检索导出同款） |

## 3. 影响清单

| 层 | 影响 |
|---|---|
| 说明书 / 四单 | 回写 213-3、214-5/6、217-5；DATA 扩 `pros_text`/`cons_text` |
| gapfill | `gapfill_policy_detail_compare` 加列 + 灌数 |
| element / display | DETAIL_SQL + `attachCompare` 透传优缺点 |
| FE | `ComparisonModal` / `VersionCompareModal` / `BenchmarkCompareModal`；217 → `useSituationReport`（禁 trackingExport 打印） |
| 合规用例 | G3 形态期望：213 Tag 计数、214 图+优缺点、217 真 PDF/Word、218 三图种 |

## 4. 回写说明书要点（交 C 会签定稿）

- 214：live 必见差异柱图 + 每策优缺点（读 gapfill，免 D18 写死接口）
- 217：导出落点 = 态势/专题同构（FE HTML → `situation/report` → OpenHTMLtoPDF；Word=html→.doc）；废止 trackingExport 打印另存
- 213：变化统计 = diff 行聚合，非独立分析列
