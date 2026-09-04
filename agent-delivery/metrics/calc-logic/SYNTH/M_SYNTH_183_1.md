# 区域产业创新成果综合评价模型（M_SYNTH_183_1）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SYNTH-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_183_1 |
| 指标名称 | 区域产业创新成果综合评价模型 |
| 一级模块 | 综合智能分析 |
| 二级模块 | 区域创新活力分析 |
| 三级模块 | 产业创新成果 |
| 更新频率 | 年度 |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

选定区域内、统计年度的产业创新成果指数，从产品服务创新、企业创新、服务机构创新三维评定，取值 0—100。分数越高表示产业创新成果越强。对象=区域产业创新主体。

## 计算逻辑说明

采用加权平均。三维：产品服务创新 / 企业创新 / 服务机构创新。算法库序号 183 已给这三维，不另起维度。

- 产品服务创新维：产品名称覆盖数、第三产业增加值占比重分别极值归一后等权。
- 企业创新维：高新技术企业数、企业授权专利数分别极值归一后等权。
- 服务机构创新维：区域内创新服务机构绩效均值，沿用 M_SVC_ORG_COVERAGE_DEPTH。
- 三维极值归一后等权合成（也可按评估重点改权，ΣW=1）。

### 第一步：入集

统计窗默认自然年。区域落到 `dwd_org_base_info.city` / `province` / `area`。存续：`reg_status` 含「存续」。专题可选：`dwd_org_industry_tags.industry_code` 命中当前产业链，`credit_code` 对齐 `external_id`。无专题则该区域存续企业全入。

### 第二步：三个子项

1. **产品服务创新**  
   需求要产品服务创新质量与市场表现。本维由两个三级指标组成：

   a. 产品名称覆盖数：`product_name` 去重数。无产品标签的企业不进分子、仍在分母企业集。

   b. 第三产业增加值占比重：第三产业增加值（`gmjj_jjzl_01_03`）÷ 地区生产总值（`gmjj_jjzl_01`）× 100%。两码均取同一 `area_code`、`{统计年}12`、`JDZ`、`DNLJ` 的绝对事实。该指标反映区域产业服务/市场结构背景，不是企业级产品收入。

   **新产品销售收入口径说明**：宏观 `a77234` 是规上工业研究与试验发展（R&D）新产品销售收入，不是「全部规上工业企业新产品销售收入（标准全口径）」，因此不用于本模型；当前宏观六表也未发现标准全口径指标码，故不新增 `new_product_revenue` 待建。若供应方后续补全口径，可再评估是否恢复为产品服务创新维三级指标。

2. **企业创新**  
   科技型企业与专利产出。高企去重数（`dwd_org_tech_tag.org_tag` 含高新技术企业）+ 企业名对齐的授权专利去重数。两子值分别极值归一后等权。本维现表可算，不代理。

3. **服务机构创新**  
   需求要服务机构创新绩效。服务机构入集采用 `demo_gkxlumenx_ads.svc_org_card(service_type_candidate='INNOV')`，区域值沿用产业服务链 `M_SVC_ORG_COVERAGE_DEPTH`：机构得分=服务广度与服务深度等权，区域绩效=区域内机构得分均值。

### 第三步：归一与汇总

先在各三级指标上对目标区域集合做极值归一；无有效宏观事实的三级指标记为缺失，不填 0、不用同比/指数代替。随后按上述维内等权、三维等权汇总得 0—100 综合指数。

输出区域一行，含三维得分与综合分。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 区域产业创新成果综合评价模型 | 产品服务创新 | 产品名称覆盖数 | 区域企业产品名称去重数。 | COUNT(DISTINCT product_name) | dwd_org_industry_product_tags(credit_code, industry_code, product_name) — 产品覆盖；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, external_id) — 区域入集,名称对齐,信用代码 | 无 |
| 区域产业创新成果综合评价模型 | 产品服务创新 | 第三产业增加值占比重 | 区域统计年第三产业增加值占地区生产总值比重，作为产业服务/市场结构背景。 | 第三产业增加值（`gmjj_jjzl_01_03`）÷ 地区生产总值（`gmjj_jjzl_01`）× 100% | dwd_macro_index_data(index_code, occur_period, area_code, dim_cal, dim_dur, index_value, unit_use, source_code, update_time) — 宏观事实,12位area_code,{统计年}12,JDZ,DNLJ；dwd_dim_index_attribute(index_code, index_name, data_freq, unit_use, unit_show) — 指标字典,gmjj_jjzl_01地区生产总值/gmjj_jjzl_01_03第三产业增加值；dwd_dim_admin_area(area_code, area_name) — 行政区划；dwd_dim_index_cal(dim_cal, cal_name) — 计量口径；dwd_dim_index_dur(dim_dur, dur_name) — 时间跨度；dwd_dim_source_code(source_code, source_name) — 数据来源 | 无 |
| 区域产业创新成果综合评价模型 | 企业创新 | 高新技术企业数 | 区域内高企去重数。 | COUNT(DISTINCT 高企) | dwd_org_tech_tag(org_id, org_tag) — 高新技术企业等科技型标签；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
|  |  | 企业授权专利数 | 企业名对齐授权专利去重数。 | COUNT(DISTINCT 授权专利) | dwd_patent(pn, kind, granted_number, first_applicant_name, pbdt_year) — 授权专利,申请人对齐,年窗；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
| 区域产业创新成果综合评价模型 | 服务机构创新 | 创新服务机构绩效 | 服务机构创新绩效，沿用 M_SVC_ORG_COVERAGE_DEPTH。 | 区域机构得分均值；机构得分=(服务广度+服务深度)/2 | demo_gkxlumenx_ads.svc_org_card(org_id, name_cn, city, service_type_candidate) — 科技创新服务机构,INNOV；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, external_id) — 区域入集,名称对齐,信用代码；dwd_org_industry_tags(credit_code, industry_code, industry_link_code) — 覆盖产业领域,覆盖环节；dwd_industry_chain_info(industry_code, industry_link_code) — 标准产业领域,标准环节 | 无 |

## 宏观取数要点

- 事实表使用 12 位 `area_code`。深圳=`440300000000`；区县用对应 12 位区划码，不用中文名关联。
- 第三产业增加值与地区生产总值必须同一 `area_code`、同一 `occur_period`、同一计量口径和时间跨度：`dim_cal='JDZ'`、`dim_dur='DNLJ'`，年度值取 `{统计年}12`。
- `source_code` 优先 `LBS`；同一业务键多行时取 `update_time` 最新一行。
- 当前样例覆盖有限：深圳市级 `gmjj_jjzl_01_03` 未见可用 `JDZ+DNLJ` 事实；部分区/年可算，如南山 `202212` 同时存在 GDP 与第三产业增加值。无同口径同时事实时记缺失，不改用 `TB` 或指数型指标。

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, external_id) — 区域入集,名称对齐,机构类型,存续,信用代码
- dwd_org_industry_tags(credit_code, industry_code, industry_name, industry_link_code) — 专题产业链筛选,服务机构覆盖产业领域/环节
- dwd_org_industry_product_tags(credit_code, industry_code, product_name) — 产品覆盖
- dwd_org_tech_tag(org_id, org_tag) — 高新技术企业等科技型标签
- dwd_patent(pn, kind, granted_number, first_applicant_name, pbdt_year) — 企业授权专利
- dwd_industry_chain_info(industry_code, industry_name, industry_link_code) — 标准产业领域,标准环节
- demo_gkxlumenx_ads.svc_org_card(org_id, name_cn, city, service_type_candidate) — 科技创新服务机构,INNOV
- dwd_macro_index_data(index_code, occur_period, area_code, dim_cal, dim_dur, index_value, unit_use, source_code, update_time) — 宏观事实
- dwd_dim_index_attribute(index_code, index_name, data_freq, unit_use, unit_show) — 宏观指标字典
- dwd_dim_admin_area(area_code, area_name) — 行政区划
- dwd_dim_index_cal(dim_cal, cal_name) — 计量口径
- dwd_dim_index_dur(dim_dur, dur_name) — 时间跨度
- dwd_dim_source_code(source_code, source_name) — 数据来源

## 待建字段

- 无
