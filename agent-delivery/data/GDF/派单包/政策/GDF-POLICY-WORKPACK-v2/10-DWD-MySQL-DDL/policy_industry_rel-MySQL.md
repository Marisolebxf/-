# `policy_industry_rel`（Wave C 建表，不参与 Wave B Mapping）

> **日期**：2026-10-26  
> **谁写**：POLICY-C1 抽取产业。Wave B 的 CDC **不要**洗这张表，也不要从 ODS 灌主题名进来。  
> DWD 与 ADS **同结构**。抽取写 DWD 后，按 `policy_id` 把该政策的行替换进 ADS（`id` 一致）。

结构真源：[dwd.md 的 `policy_industry_rel` 节](../../../../../data-design/storage/POLICY/stores/mysql/dwd.md)。库名 `demo_gkxlumenx_dwd`。

ADS 同结构，只换库名，见 [ads.md](../../../../../data-design/storage/POLICY/stores/mysql/ads.md)。库名 `demo_gkxlumenx_ads`。

产线执行时把 `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads` 换成 `gkxlumenx_dwd` / `gkxlumenx_ads`。表结构不另写。
