# CHANGELOG — GDF-FIN-WORKPACK

## v1.0 — 2026-11-09

首版成包（`GDF-FIN-WORKPACK-L01` / WBS-06-04B）。

- 范围：金融要素库物理表 31 张（行数报告 32 行含 `dwd_corp_basic_info` 重复）。
- 分期：P0 9 张 + P1 10 张洗入 11 张 `gkxlumenx_dwd.fin_*`；P2 6 张与公募基金 0 行 3 张只贴不洗；融资 / 投资 / 并购 3 张归 ENT-v4，本包不重复配贴源。
- 声明：市场研究红标优先级第 2；与落地实效无关；不与 MACRO 并包；结构以 live `gkx` 为准。
- ② 金融 ADS：4 张草稿（产业基金汇总、债券发行汇总、A 股上市公司快照、主营构成最新期），SQL 口径未在库上执行，未会签。
- DDL：DWD 11 张、ADS 4 张均为**草稿**，`storage/FIN/` 尚不存在（OPEN-FIN-01），`gkx-gdf-ddl-signoff` 未跑。
- 开放项：OPEN-FIN-01 ~ 11（见 `00` §7、`09` §6）。
- 不含：Java / 前端、指标 8 件套登记、写 ES / 图谱 / 向量库、任何作业已建或已跑的宣称。
