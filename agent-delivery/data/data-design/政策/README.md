# 政策维数据设计（旧目录）

> **现行入口**：[`../storage/POLICY/`](../storage/POLICY/)（S1–S4 文档闭环）。  
> 本目录旧稿仅历史对照。冲突以 `storage/POLICY` 为准。  
> 图谱目标态 = `demo_gkx_chain`，**不是** `gkx_policy`。

## 2026-10-23 三方 ODS

只读源固定两张表：`dwd_policy_base`（国内）、`dwd_global_policy_base`（海外）。字段以 `third-party-source/doc/md-extract/版权人才、企业机构、政策数据汇总表.md` 为准，各 35 列。业务键 `id`，`t_id` 是分片键。`dwd_zck_*` 不再使用。

## 2026-10-23 产业关联

贴源之后，`policy_base_info.related_entities.industry` **弃用**。主题仍只进 `ext5`。产业抽取（按钮 / 跑批）**不更新**这个 JSON 键，只写 DWD `policy_industry_rel`（`is_deleted` 逻辑删除），并按政策同步到 ADS 同名表。细表见 [`../storage/POLICY/stores/mysql/dwd.md`](../storage/POLICY/stores/mysql/dwd.md) 与 [`../storage/POLICY/stores/mysql/ads.md`](../storage/POLICY/stores/mysql/ads.md)。
