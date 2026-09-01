# 派单包：企业维 GDF 工作包 v3（贴源 + Mapping + 写 ES）

- **状态**：2026-09-01 `human:淮政玮` 口头目标已收
- **派发角色**：coordinator-agent
- **承接 / Owner**：`human:徐滕强`（可带 `data-agent`；监管人必须是徐滕强）
- **协作**：GDF 导入 = `human:辜少彬`；CDC 预填 = `human:胡森泉`（本叶出 v3 包，不代替导入）
- **仓**：`gkx-orchestration`（`agent-delivery/data/GDF/派单包/企业/`）
- **Epic**：`E-PLATFORM-P1`
- **Sprint**：`2026-W36`
- **task-id**：`GDF-ENT-WORKPACK-V3-L01`
- **强度**：definition，**禁止** ponytail 行

---

## 0. 已拍板（勿再议）

| # | 决策 | 值 |
|---|------|-----|
| 1 | 版本 | **必须出 v3**。v2.1 改为历史包，施工只认 v3 |
| 2 | 范围 | **Wave A 贴源 + Wave B Mapping + DWD→ES 写索引**（别名 `gkx_enterprise` 双索引） |
| 3 | 目标库 | 产线 `gkxlumenx_ods` / `gkxlumenx_dwd`；检索别名 `gkx_enterprise`。禁止把 Demo 库当产线目标 |
| 4 | ES 写方 | 作业边界写清：`lumen-etl-es-py` 写 ES；Java/前端只读搜索，不直写 ES |
| 5 | v2.1 开放项 | 财务单位、`dwd_org_industry_chain_dtl` 未检出、融资表或已迁金融库、专利权限——**在 v3 `00`/`11` 收口或登记客户决策清单**，不得再「暂缓」却不写原因 |

---

## 1. 产物落点

新建：`agent-delivery/data/GDF/派单包/企业/GDF-ENT-WORKPACK-v3/`

在 v2.1 目录结构上 **加 ES 卷**（建议 `12-DWD到ES.md` 或 README 指定的 `09` 续章），至少写清：

- 别名 `gkx_enterprise` → `gkx_enterprise_v1`（国内 IK）+ `gkx_enterprise_global_v1`（国外 standard）
- DWD 表 → ES 字段对照（指针可到 `企业搜索-ES索引设计.md` + `storage/ENT/etl/pipeline-dwd-to-es.md`）
- 门禁：DWD 验收通过后才允许 bulk；失败不发布半成品索引
- 调度/SLA 若仍开 `OPEN-ENT-FLOW-01/04`，在包内点名，禁止假装已关

回写：

- v2 `README.md` 顶部改为 **历史 / 禁止施工**
- `派单包/README.md` 现行企业包改指 **v3**
- `GDF-ENT-WORKPACK-v2-投递说明.md` 加一行「已被 v3 替代」

**本叶不要求** GDF 已导入绿；CDC 预填可另派胡森泉。

---

## 2. 必读

| 序 | 路径 |
|---:|---|
| 1 | `data/GDF/GDF协作指南.md` |
| 2 | `data/GDF/派单包/企业/GDF-ENT-WORKPACK-v2/`（继承，不要从 v1 抄） |
| 3 | `agent-handoffs/企业战略分析-ENT/GDF-ENT-WORKPACK-v2-投递说明.md`（开放项清单） |
| 4 | `data/data-design/企业/企业域-ETL-Mapping明细-源表到DWD.md` |
| 5 | `data/data-design/企业/企业搜索-ES索引设计.md` · `企业搜索-ES更新机制.md` |
| 6 | `data/data-design/storage/ENT/etl/pipeline-dwd-to-es.md` |
| 7 | `repos/lumen-etl-es-py/README.md`（只读对照写库方，本叶不改业务仓除非缺指针） |

---

## 3. `/goal`

```
/goal GDF-ENT-WORKPACK-V3-L01
监管人：human:徐滕强
仓：gkx-orchestration
图：本叶不改 ENT 存储流图拓扑；写库方=GDF Wave A/B + lumen-etl-es-py 写 ES（禁止 Java/前端直写）
范围：新建 派单包/企业/GDF-ENT-WORKPACK-v3；覆盖贴源、Mapping、DWD→ES。v2.1 降为历史。
禁止：把 Demo 库当产线；用短版 Mapping 当全文；本叶改检索 Java/前端；密钥进 Git。
DoD：见 registry。
```

---

## 4. 验收对照（摘）

- v3 包 `02` + `09` 明细 + `10` DDL + **ES 卷** 齐全
- v2.1 开放项每条：已关 / 决策清单 ID / 明确不洗原因
- 总 README 现行企业包 = v3
- handoff：`agent-handoffs/企业战略分析-ENT/GDF-ENT-WORKPACK-V3-L01.md`
