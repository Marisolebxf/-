# POL-L2-DS12-SIM-238-COVER-FDE · C 波次 · 轻会签

- 总单：`POL-L2-DS12-SIM-238-COVER-FDE-L01`
- 日期：2026-11-12
- 档位：中（卡1=B）
- 依据：A product / B arch；说明书 #### 238 功能点表已回写

> 本波为**轻会签**：同会话按审稿硬清单自检并落异议；异议 ≠ 零。正式对抗会签若监管人要求可另开身份会话复审。

## 会签结论

**通过（可进 D）**：读法与说明书/四单一致；无新表新列；调用链不越层。下列异议均已 `采纳` 并写入 D/E 约束。

## 分身份清单（硬清单）

### product

| # | 核过 | 异议 / 风险 |
|---|---|---|
| 1–2 | 238-1…6 已编号且可截图验（导图/柱/明细） | — |
| 3 | 状态含未选/无行/无分/失败 | — |
| 4 | 柱落 `score_value`；明细落 `detail_text` | — |
| 5 | 差表「无数值列」已标已被取代 | **[product] R1**：样例四组分是 mock 展示分，关评审后界面不得出现「演示分」字样 · 依据 FDE §6 · **采纳**→ D FE 空态文案用「暂无得分」 |

### arch

| # | 核过 | 异议 / 风险 |
|---|---|---|
| 1 | FE→display→element 只读 gapfill；无 Python | — |
| 2 | 读 `gkxlumenx_gapfill`，非 ODS/DWD | — |
| 3 | 无 demo 服务 | — |
| 4 | 接口读表行，不直接返回写死数组（D18） | — |
| 5 | 中档成立 | **[arch] R1**：同组多行聚合「取非空最大」未写进 API 契约正文，仅 DATA/ARCH · 依据硬清单 api#2 · **采纳**→ D 前确认 FE 与样例一组一行一致即可；多行留预留 |

### data

| # | 核过 | 异议 / 风险 |
|---|---|---|
| 1 | `gkxlumenx_gapfill.gapfill_policy_sim_result.score_value`（重点行） | — |
| 2 | 样例行在；现 `score_value` 仍 NULL → 柱空 | **[data] R1**：线上库与 `gapfill_policy_sim_result.sql` 须同改四组分 · **采纳**→ D 波 UPDATE + 脚本 INSERT 对齐 |
| 3 | 不新表、不 ALTER | — |
| 4 | 只写 gapfill，不写 ODS/DWD/ADS | — |

### api

| # | 核过 | 异议 / 风险 |
|---|---|---|
| 1 | `policy_id` + `kind=重点可视化` | — |
| 2 | 响应已含 `scoreValue`/`score_value`（RESULT_COLUMNS） | — |
| 3 | 同步；无行空数组 | — |
| 4 | 复用 jobs | **[api] R1**：本 FDE 不改 Java；若 camel/snake 双键 FE 已兼容 `rowNumber` · 确认即可 |

### algorithm

| # | 核过 | 异议 / 风险 |
|---|---|---|
| 1 | 柱图数字无新 `metric_id`；行上 metric 空；D4 mock | — |
| 2 | 未改 D4 | — |
| 3 | 不挂 `M_POLICY_FOCUS_INDEX` | **[algo] R1**：业务用户可能把柱高误认为焦点指数 · 依据 D17/指标边界 · **采纳**→ 用例/评审 ⓘ 可注明「组重点展示分」；业务面不写 metric_id |

### doc

| # | 核过 | 异议 / 风险 |
|---|---|---|
| 1 | #### 238 正文 + 功能点表；差表已改；无新时序图（复用 jobs 链） | **[doc] R1**：storage ER 未展开 `score_value` 列（表已登记）· **采纳**→ CHANGELOG 记语义扩展一行，不强制改 mermaid |
| 2 | §12 变更记录已加 238 COVER-FDE | — |
| 3–4 | 无新表；DATA 与说明书列名一致 | — |

## 产物清单（C）

| 文件 | 动作 |
|---|---|
| `sdd/科技政策跟踪-系统详细设计说明书.md` | #### 238 功能点/状态/已定；§11 结果行；§12 变更记录 |
| `sdd/l2/POL-L2-DS12-SIM-{DATA,ARCH,API}.md` | B 波已回写（HEAD 含 238） |
| `data/.../POLICY/CHANGELOG.md` | 记 score_value 语义扩展（本波） |
| 本简报 | C 会签 |

## 下一跳

**D**：UPDATE 18363390 四组分 + FE `focusScoreOption` 读分；**E**：用例形态。
