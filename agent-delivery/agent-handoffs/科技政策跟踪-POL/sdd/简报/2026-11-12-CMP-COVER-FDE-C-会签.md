# POL-L2-DS10-CMP-COVER-FDE · C 波次 · 四单会签闭合

- 总单：`POL-L2-DS10-CMP-COVER-FDE-L01`
- 日期：2026-11-12
- 档位：**中档**（B 裁定）
- 卡1=A、卡2=B 已锁定；不新造 `metric_id`；不改 D4

## 改写摘要

| 单 | 改动 |
|---|---|
| ARCH | §5.1 变化统计；§5.2 优缺点+差异柱图；§5.5 导出 = situation/report + OpenHTMLtoPDF（废止 trackingExport） |
| DATA | `gapfill_policy_detail_compare` 增 `pros_text`/`cons_text`；217 文件不进 gapfill、走态势存储 |
| API | detail 透传优缺点；217 导出走 `POST /display/v1/situation/report/generate` |
| METRIC | **不动**（无新指标） |

## 会签对抗（审稿硬清单 · 本会话代闭合）

| 角色 | 结论 |
|---|---|
| arch | 中档成立；优缺点只读 gapfill（免 D18）；217 复用已有 situation/report，不新加 jspdf |
| data | 扩列 + ALTER + 灌数脚本同改；空串合法 |
| api | 同一次 detail 贴列；导出经 display→topic-async 真字节 |
| frontend | live 柱图/优缺点/变化统计；217 双按钮走 useSituationReport |
| product | 界面必见与空态与 A 波次一致 |
| qa | 用例形态期望进 E |

分歧：无。**2026-11-12 晚修订**：原「trackingExport 打印另存」判定为非真实实现，已按专题/态势报告链回写四单；D 波次 217 代码须重做。

## 闭合结论

四单已按 COVER-FDE 改写（含 217 架构修订）；217 实现须对齐 situation/report。
