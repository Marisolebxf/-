# CHANGELOG — GDF-ENT-WORKPACK（v4 目录）

> 本目录 CHANGELOG 自 v4.0 起新记；v3.x 历史见 `../GDF-ENT-WORKPACK-v3/CHANGELOG.md`。

## v4.0 — 2026-10-20

**基线切换**：三方承诺清单 219→176（10-19 版，架构师入仓变更纪要）+ live `gkx` 实证核验。v3 整包继承，以下为差异：

- **`dwd_org_stock_base` 移出**（拍板 2026-10-20）：10-19 清单不再收录（live 仍有 1,080 行仅备查）；`is_listed` 回归 `dwd_org_base_info.listing_status`；`listed_code`/`listed_market` 改源 `dwd_org_stock_finance_info`，`stock_noun` 置空（09 §3.1/§3.1.2 v4 注）。
- **国外母子换源**：`dwd_agg_subsidiary_info`（10-19 清单新表，live 19,810 行）替代从未存在的 `dwd_forg_subsidiary_info`——**A1 阻塞解除**；新增 09 §3.21（eid→org_id 实测命中率 6.3%，精确匹配+治理清单，禁造 ID）；ES `forg_relations` 母子段解冻。
- **专利 5 张新侧表扩入 mirror_only**（priority_filings 20,709 / claim 10,578 / description 15,900 / transfer 21,193 / family 16,235）：`enterprise_patent_detail` 无承接列，不 ADD 列；transfer 如需轨迹走 `detail_json` 另拍板。
- **融资/投资/并购改挂金融要素库**（10-19 清单归属调整；表名/数据/live 行数不变，贴源洗数口径全部继承 v3.1.6）。
- **10-19 纪要"Excel 多出字段"澄清**（live 实证）：`t_id` 分片键、`dwd_org_base_info.province_code/city_code/area_code` 等 153 表"Excel 多出"列 **live 库均不存在**——Excel 说明领先于库，**一律以 live 结构为准施工**，Excel 列不作源（02 头注已声明）。
- **16 号文移出本包**（v4.0 定稿前拍板：缺口回复留在 v3 包归档，v4 对外只带施工真源；README 索引同步）。
- **05/12/13 全卷对齐 v4 基线**：05 验收检查表按 02 v4.0 重做（62 张：P0=15/P1=33/P2=14；换源/移出/扩入全部体现 + 预填行数残留清除）；12 ES 卷 forg_relations 母子段解冻注记 + stock_base 移出后上市字段取值说明；13 差集卷 §2 forg_subsidiary 换源解除 + 开工顺序 v4 注。
- 原 16 号文相关：其中 B1"56 张结构已建"对应 v3.1.6 基线，v4 下 ODS 结构差异 = 移出 stock_base、新增 6 张（agg_subsidiary + 专利 5 张）→ **结构核对以本包 02 v4.0 清单为准重跑差集**（我方跟进，不阻塞 GDF 贴已有表）。
- 承诺清单内其余 52 张 ENT 现役表：行数/表名与 v3.1.6 一致（10-19 纪要"估数 0 变化"），02 全部继承。

## 继承基线

- v3.1.6（2026-10-20 同日）：缺口分析回复、产业/企业拆分对称声明、司法明细回补、年报资产洗数、财务单位门禁等全部加工逻辑——见 `../GDF-ENT-WORKPACK-v3/CHANGELOG.md`。
