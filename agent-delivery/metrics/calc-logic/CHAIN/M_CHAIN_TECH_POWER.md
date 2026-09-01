# 技术能力（M_CHAIN_TECH_POWER）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_TECH_POWER |
| 指标名称 | 技术能力 |
| 一级模块 | 产业链分析 |
| 二级模块 | 区域产业指数评价 |
| 三级模块 | 区域产业指数 |
| 更新频率 | 周 |
| 对齐状态判定 | 待闭合/待甲方确认 |
| 是否在数据库 | 否/待确认 |
| 关联Q编号 | Q055+QC05 |


## 口径定义

指定区域在指定产业链上的技术能力得分，取值0—100。由区域专利（M_CHAIN_REG_PATENT）、区域技术壁垒（M_CHAIN_REG_TECH_BARRIER）、区域技术成熟度（M_CHAIN_REG_TECH_MATURITY）三维合成。

## 计算逻辑说明

三维等权。先按各子指标口径计算区域、链、年原始值，再在同一产业链、同一统计年度对全部对比区域做截面min-max归一化到[0,1]，算术平均后乘100。某维全部区域取值相同则该维取0.5。默认等权，前端可调权重但不另建权重表。区域用机构所在省、市过滤，深圳场景取city="深圳市"。从dwd_industry_chain_info确定目标产业链，关联dwd_org_industry_tags取链上企业，再关联dwd_org_base_info筛区域。

区域技术壁垒为负向指标（壁垒越高，技术能力越低）：该维先按壁垒原始值min-max到[0,1]，再取 \(1-x\) 后参与合成。区域专利、区域技术成熟度为正向指标。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 区域产业指数 | 技术能力 | 区域专利 | 对齐M_CHAIN_REG_PATENT：区域链上企业专利去重件数。筛区域后，用company_name匹配dwd_patent.first_applicant_name或first_current_assignee_name，按patent_id去重；公开年pbdt_year≤统计年 | dwd_patent(patent_id, first_applicant_name, first_current_assignee_name, pbdt_year) | 无 |
| 区域产业指数 | 技术能力 | 区域技术壁垒 | 对齐M_CHAIN_REG_TECH_BARRIER：断链壁垒=（核心技术空白得分+核心技术封锁得分）÷2。空白为连续3年发明专利授权量为0取1否则取0；封锁为区域企业与同链其他企业IPC占比向量的平均欧氏距离。合成时作负向处理 | dwd_patent(kind, granted_number, pbdt_year, main_classification_ipcr, first_applicant_name, first_current_assignee_name) | 无 |
| 区域产业指数 | 技术能力 | 区域技术成熟度 | 对齐M_CHAIN_REG_TECH_MATURITY：按公开年pbdt_year汇总近k年复合增速并映射到0—100。 | dwd_patent(patent_id, first_applicant_name, first_current_assignee_name, pbdt_year) | 无 |

子指标计算步骤与对应md相同，此处不重复公式。

## 源表字段

- dwd_industry_chain_info(industry_code, industry_name) — 目标产业链范围, 产业链名称
- dwd_org_industry_tags(industry_code, credit_code, company_name) — 链上企业筛选, 信用代码关联, 企业名称匹配专利权人
- dwd_org_base_info(external_id, province, city) — 企业信用代码关联, 省份, 城市(区域筛选)
- dwd_patent(patent_id, first_applicant_name, first_current_assignee_name, kind, granted_number, pbdt_year, main_classification_ipcr) — 专利去重, 申请人匹配, 专利权人匹配, 发明识别, 授权判定, 公开年, IPC主分类

## 待建字段

- 无

## 参考文献

- 技术能力｜耶拿大学｜Haupt R, Kloyer M, Lange M. Patent indicators for the technology life cycle development[J]. Research Policy, 2007, 36(3): 387-398. DOI: 10.1016/j.respol.2006.12.004.
- 技术能力｜经济合作与发展组织（OECD）；欧盟委员会联合研究中心（JRC）｜OECD, European Commission Joint Research Centre. Handbook on constructing composite indicators: methodology and user guide[R]. Paris: OECD Publishing, 2008. DOI: 10.1787/9789264043466-en.
- 技术能力｜北京理工大学管理与经济学院，清华大学公共管理学院｜常晓涵, 何海燕, 孙磊华, 李浩然. 关键核心技术壁垒对中国产业链升级的影响[J]. 北京理工大学学报（社会科学版）, 2023, 25(6): 184-198.
