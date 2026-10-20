# GDF 派单包（人类可读）

> GDF 数据中台团队**不使用 Cursor**。对外沟通用本目录工作包 + 飞书/例会，不用智能体派单话术。
> **2026-10-20 基线切换**：三方承诺清单更新为 10-19 版（176 表，架构师入仓 `gkx-mysql-raw/加工/GKX数据源表差异分析摘要-20261019.md`）；企业、产业链两包随之升版。

| 工作包 | 范围 | 版本 |
|--------|------|------|
| [企业/GDF-ENT-WORKPACK-v4](企业/GDF-ENT-WORKPACK-v4/) | 贴源 + Mapping + **写 ES**（`gkx_enterprise`）+ 图谱日批触发；**10-19 基线**（stock_base 移出 / 国外母子换源 `dwd_agg_subsidiary_info` / 专利侧表 +5 mirror_only） | **v4.0**（2026-10-20）· **现行企业包（可对外投递）** · Owner **徐滕强** · 含 `16-缺口分析回复工作包`（继承） |
| [产业链/GDF-CHAIN-WORKPACK-v2](产业链/GDF-CHAIN-WORKPACK-v2/) | 产业链四表贴源+洗链树/`entity_rel`；分析六表只贴不洗；**10-19 基线对齐**（四表行数不变；链树 live 实证 `parent_name` 列） | **v2.0**（2026-10-20）· **现行产业链包（可对外投递）** |
| [企业/GDF-ENT-WORKPACK-v3](企业/GDF-ENT-WORKPACK-v3/) | v3.1.6（2026-10-20 同日早间）：缺口分析回复 + ODS 建表 + 加工逻辑补遗 | **历史包**（加工逻辑被 v4 全继承；仅 stock_base/国外母子/专利侧表三项被覆盖） |
| [政策/GDF-POLICY-WORKPACK-v1](政策/GDF-POLICY-WORKPACK-v1/) | **只**贴源 + Mapping → `policy_base_info`（不含 ES） | **v1.0.1**（2026-09-01）· **Mapping 已冻结可投递；MAP-01 已关（永远分 UK）** · Owner **淮政玮** · 厚包 [`GDF-POLICY-WORKPACK-V1-DISPATCH.md`](../../agent-handoffs/政策模块-E7/GDF-POLICY-WORKPACK-V1-DISPATCH.md) |
| [企业/GDF-ENT-WORKPACK-v2](企业/GDF-ENT-WORKPACK-v2/) | 贴源 + MySQL DDL + Mapping 明细 | **v2.1**（2026-08-13）· **历史 / 禁止施工** |
| [企业/GDF-ENT-WORKPACK-v1](企业/GDF-ENT-WORKPACK-v1/) | 历史包；DWD 指针误指旧 PG 稿 | v1.3 · **建表已作废** |
| [产业链/GDF-CHAIN-WORKPACK-v1](产业链/GDF-CHAIN-WORKPACK-v1/) | v1.0 原版 | **历史包**（v2.0 继承） |

企业建表 / ALTER：**只认企业 v4 包内 `10-DWD-MySQL-DDL/`**（与 v3.1 快照一致）。
Mapping：各域只认各自现行包 README 指定的 `09-*Mapping明细*`；短版导读不作施工真源。
**三方源结构以 live `gkx` 为准**；10-19 Excel 纪要中"Excel 多出"列（t_id/区划码等）live 库不存在，不作源（ENT v4 CHANGELOG / CHAIN v2 09 头注均已声明）。
