# 缺口清单

只写方法和表名。本包不建表，不灌数，不写 ODS，不写供应方库，不写久新分析库。库名若要用，只允许 `gkxlumenx_gapfill`，表名以 `gapfill_` 开头。

第一批能对上的三张表不走缺口表：`gkxlumenx_dwd.enterprise_base`、`enterprise_supply_chain`、`enterprise_parent_subsidiary`。缺稳定 ID 的行跳过，不用企业名称生成 VID。

## 先加工，再考虑缺口表

| 缺什么 | 落在哪一层 | 缺口表（仅当没有第二来源） | 本版 |
|---|---|---|---|
| 供给边对端没有 `related_org_id`，或对端不在 `enterprise_base` | 先在 DWD 映射里补已经存在的 `org_id` | `gapfill_enterprise_supply_endpoint` | 第一批跳过这些行，不建表 |
| 母子边没有 `parent_org_id` 或子企业 `org_id`，或对端不在企业主表 | 同上 | `gapfill_enterprise_parent_endpoint` | 第一批跳过，不建表 |
| 合作边没有 `partner_org_id`，或对端不在企业主表 | 同上。双向规则另见下表 | `gapfill_enterprise_cooperate_endpoint` | 合作边本版不入库 |
| `cooperate` 必须双向，现有行只够写一个方向 | ADS 映射或入图脚本：同一对企业各写一条有向边，边名仍是 `cooperate` | 不需要缺口表 | 规则没落地之前不写 |
| 企业挂到产业链环节，边名必须是 `participates` | 优先用产业链仓已经能对上的关系表做映射，方向企业 → `segment:`。企业产业表写出的 `industry_belong` 不算这条边 | 映射仍对不上环节 ID 时，才用 `gapfill_enterprise_segment_rel`，列是企业 `org_id` 和环节 ID | 本版不灌 |

缺口表里只放人工确认过的稳定 ID 对。确认不了的行继续不进图。

## 不放进本包的缺口

政策适用到企业、服务机构指向企业，归其他要素的上图路径。不在本包新造边名，也不在这里建对应的 `gapfill_` 表。

分批和燕大的小版本对齐：v0.1 只调通企业点、`supply`、`parent_sub`。上表里标成「本版不建表」的，留到写明下一版再开。
