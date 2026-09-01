# 派单包：政策维 GDF 工作包 v1（贴源 + Mapping）

- **状态**：2026-09-01 `human:淮政玮` 口头目标已收
- **派发角色**：coordinator-agent
- **承接 / Owner**：`human:淮政玮`（可带 `data-agent`；监管人必须是淮政玮）
- **协作**：GDF 导入核对 = `human:辜少彬` / CDC 预填 = `human:胡森泉`（本叶只出包，不代替他们导入）
- **仓**：`gkx-orchestration`（`agent-delivery/data/GDF/派单包/政策/`）
- **Epic**：`E-PLATFORM-P1`
- **Sprint**：`2026-W36`
- **task-id**：`GDF-POLICY-WORKPACK-V1-L01`
- **强度**：definition，**禁止** ponytail 行

---

## 0. 已拍板（勿再议）

| # | 决策 | 值 |
|---|------|-----|
| 1 | 范围 | **只做 Wave A 贴源 + Wave B Mapping**。本叶 **不含** 写 ES、不含 ADS/算法、不含 Nebula/图谱 |
| 2 | 源 | 三方 `gkx.dwd_policy_base`（国内）+ `gkx.dwd_global_policy_base`（国际），只读 |
| 3 | 目标 ODS | `gkxlumenx_ods` 同名表（产线）。Demo `demo_gkxlumenx_ods` 仅对照，**禁止**写进本包当产线目标 |
| 4 | 目标 DWD | **一张** `gkxlumenx_dwd.policy_base_info`；国内+国际同表，用平面/来源字段切片，不建第二张明细表 |
| 5 | 对照 | Demo「数据同步」=`polan/ods_sync.py` 只是算子级 Demo，**不是** GDF DAG。正式编排仍关 `OPEN-POLICY-FLOW-01`，由本包第一次写成可投递给 GDF 的形状 |

---

## 1. 产物落点

新建目录（对标产业链 v1 / 企业 v2 结构，缺文件不许用「目录在」冒充完成）：

`agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v1/`

| 文件 | 必须 |
|------|------|
| `README.md` + `00-派单说明书.md` | 投递状态、作废清单、DoD |
| `01-命名与分层词典.md` | `gkx.dwd_*` = 本项目 ODS，不是项目 DWD |
| `02-WaveA-贴源表清单.yaml` | 至少两张 P0 表 + 过滤 `is_deleted=0` / 非历史 |
| `03` / `04` | 连接（口令线下）+ 技术字段 |
| `06-WaveB-Mapping派工.md` | 洗入 `policy_base_info` |
| `09-政策域-ETL-Mapping明细-源表到DWD.md` | **施工真源**。可从 `storage/POLICY/etl/ods-to-dwd-mapping.md`（draft）升格，须收口列级规则 |
| `10-DWD-MySQL-DDL/` | 指针或快照到现行 `policy_base_info` 正式 DDL（禁止旧 v1 37 列当贴源） |
| `11-作废与误源对照.md` | 禁：`dwd_zck_*`、PG、Demo `ods_sync` 当产线、宽表第二套政策主表 |
| 回写 | `data/GDF/派单包/README.md` 增加政策现行包一行 |

**本叶不要求**生成 CDC 预填 xlsx（那是胡森泉下一叶）。包不齐则禁止喊「可以预填」。

---

## 2. 必读

| 序 | 路径 |
|---:|---|
| 1 | `data/GDF/GDF协作指南.md` |
| 2 | `data/GDF/派单包/产业链/GDF-CHAIN-WORKPACK-v1/`（目录样板） |
| 3 | `data/data-design/storage/POLICY/etl/pipeline-source-to-ods.md` |
| 4 | `data/data-design/storage/POLICY/etl/pipeline-ods-to-dwd.md` |
| 5 | `data/data-design/storage/POLICY/etl/ods-to-dwd-mapping.md` |
| 6 | `data/data-design/storage/POLICY/sources/ods-ddl.md` |
| 7 | `data/data-design/storage/POLICY/01-data-flow.md`（`OPEN-POLICY-FLOW-01`） |

---

## 3. `/goal`

```
/goal GDF-POLICY-WORKPACK-V1-L01
监管人：human:淮政玮
仓：gkx-orchestration
图：本叶不改 POLICY-STORAGE-FLOW 拓扑；写库方正式=GDF Wave A/B（禁止把 Demo ods_sync 写进产线 DAG）
范围：新建 派单包/政策/GDF-POLICY-WORKPACK-v1；Wave A 贴源两张 gkx 政策表→gkxlumenx_ods；Wave B Mapping→policy_base_info。
禁止：写 ES；写 ADS；写 Nebula；改 lumen-ui-*；把 demo_gkxlumenx_* 当产线目标；用旧 v1 37 列当贴源。
DoD：见 registry。
```

---

## 4. 验收对照（摘）

- 包内 `02` + `09` 明细 + `10` 指针齐全，README 标明现行、可投递或剩余开放项清单
- 国内/国际两源都进同一 `policy_base_info`，主键 `policy_id`←ODS `id`
- 派单包总 README 已挂政策行
- handoff：`agent-handoffs/政策模块-E7/GDF-POLICY-WORKPACK-V1-L01.md`
