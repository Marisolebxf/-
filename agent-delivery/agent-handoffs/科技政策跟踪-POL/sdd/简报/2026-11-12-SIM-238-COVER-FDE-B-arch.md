# POL-L2-DS12-SIM-238-COVER-FDE · B 波次 · arch

- 总单：`POL-L2-DS12-SIM-238-COVER-FDE-L01`
- 日期：2026-11-12
- 身份：arch（本会话代写）
- 输入：A 波 product；监管人卡1=**B**

## 1. 定档

**中档**：不退定义规程；**不 ALTER**；不新造列；不新 `metric_id`；不改 `jobs` URL / SELECT；D4 仍 mock。

## 2. 要动的层

| 层 | 动作 | 不动 |
|---|---|---|
| `gapfill_policy_sim_result` | **UPDATE** 重点样例行填 `score_value`（D 波） | 不加列、不建第二表 |
| element / display | 无 | `RESULT_COLUMNS` 已含 `score_value` |
| FE focus live | `focusScoreOption` 读 `score_value`+`group_name`；禁 `namedScorePoints(detail_text)` | mock 轨可并行对齐 |
| DATA / ARCH / API / 说明书 | 已回写 238 柱图口径（见下） | 不挂 `M_POLICY_FOCUS_INDEX` |
| 合规用例 | E 波补导图+柱形态与样例分 | — |

## 3. 读法钉死

- 种类：`重点可视化` → `row_kind=重点`；必选 `policy_id`
- 柱：横轴 `group_name`（闭集四组），纵轴 `score_value`；同组多行取非空最大
- 空：无行 → 全区空；有行无分 → 导图/明细可出，柱「暂无得分」
- **禁止**用 `detail_text` 解析「名+分」顶替柱高
- 与 235 同列分流：多维=`dimension_name`+分；重点=`group_name`+分

## 4. 样例分（D 波默认）

`policy_id=18363390`：政策目标 88 / 支持领域 82 / 实施路径 75 / 资金安排 80。

## 5. 已改文稿

| 文件 | 状态 |
|---|---|
| `sdd/l2/POL-L2-DS12-SIM-DATA.md` §列说明 + §4 | 本波已改，可提交 |
| `sdd/l2/POL-L2-DS12-SIM-API.md` §4 | 本波已改，可提交 |
| `sdd/l2/POL-L2-DS12-SIM-ARCH.md` §5.2 + 灌数表 | 本波已改；工作区另有 **240 WIP**（邻会话），**勿单独把 240 半成品冒充本 FDE**——提交时若带上需与 240 责任人对齐，或只提交 DATA/API |
| `sdd/科技政策跟踪-系统详细设计说明书.md` §238 + 差表 | 同上（含 240 WIP） |

## 6. B 波收口

定档中 + 读法钉死 → 进 **C** 轻会签（审稿硬清单对 ARCH/DATA/说明书 238 段）→ **D** 灌数 + FE。
