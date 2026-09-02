# GDF-ENT-WORKPACK-v2 投递说明

> **2026-09-02**：已被 **`GDF-ENT-WORKPACK-v3`** 替代（`GDF-ENT-WORKPACK-V3-L01`）。本文件不再作为投递入口。开放项转到 v3 `00` §8，未关。

> **日期**：2026-08-13（v2.1 修订）  
> **作者**：agent:data-agent  
> **状态**：**暂不投递** — 先以仓内 Mapping 明细对齐工作包；对外发送前再改本文件状态  
> **工作包**：`agent-delivery/data/GDF/派单包/企业/GDF-ENT-WORKPACK-v2/` · **v2.1**  
> **ponytail:** off（文档）

## 1. 当前结论

| 项 | 说明 |
|----|------|
| Mapping 真源 | `data-design/企业/企业域-ETL-Mapping明细-源表到DWD.md`（v1.2）；包内已嵌快照 |
| 相对 v2.0 | 短版 `09` 字段表**不再**当施工全文；Wave A / DDL 已按明细加宽 |
| 投递 | **先不派**；定稿后 zip 名建议 `GDF-ENT-WORKPACK-v2.1-YYYYMMDD.zip` |

## 2. v2.1 包内要点（给本侧）

- `09-企业域-ETL-Mapping明细-源表到DWD.md` = 施工全文  
- `09-…-v4.md` = 导读 + 相对旧短版差集  
- `02`：financing / invest / tag / subsidiary / chain_dtl / patent / forg_subsidiary；mirror_only 表已标  
- `10/`：刷新快照；含 recruit + forg_*  

## 3. storage/ENT/etl 已同步

- `pipeline-ods-to-dwd.md` → Mapping 明细为真源；包 v2.1 暂缓投递  
- `pipeline-dwd-to-es.md` → 双索引别名口径（明细 §1.4）  
- `etl/README.md` 状态行已改  
- `stores/mysql/dwd-entity.md` 补 recruit + forg 指针  

## 4. 待你确认后再投递

- [ ] Mapping 明细 §5 开放问题（财务单位等）是否接受「带病投递」  
- [ ] `05` Wave A 验收表是否按新 `02` 重出一版勾选表  
- [ ] 专利 `dwd_patent` 供应方权限 / 工作簿路径是否写进 `03`  
- [ ] **`dwd_org_industry_chain_dtl`**：md-extract **未检出**，与明细 §1.3 不一致——确认源表实名或改洗 `industry_tags`  
- [ ] **`dwd_org_financing_info`**：承诺注「或已迁金融库」——贴源可行性  
- [ ] 飞书话术改「v2.1 + 停用短版 Mapping」  

## 5. 飞书话术（**定稿后再用**，现勿发）

```text
【企业维 GDF 工作包】GDF-ENT-WORKPACK-v2.1（待发）

Mapping 以「企业域-ETL-Mapping明细-源表到DWD」为准（包内 09-企业域-…）；
建表只认 10-DWD-MySQL-DDL/（含 enterprise_recruit、enterprise_forg_*）。
请停用 v1、三方参考 PG 9 表、以及任何短版 Mapping 字段表当全文。
```
