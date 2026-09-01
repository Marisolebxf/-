# 科技创新服务机构技术力评价模型（M_SVC_DEEP_179_1）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SVC-seed.yaml。

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_SVC_DEEP_179_1 |
| 指标名称 | 科技创新服务机构技术力评价模型 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 产业服务链分析 |
| 三级模块 | 服务机构技术力评估分析 |
| 更新频率 | 按需 |
| 对齐状态判定 | 已按算法库9.8展开；四维均可落现表 |
| 是否在数据库 | 否 |
| 关联Q编号 |  |

## 口径定义

选定科技创新服务机构在统计年度的技术力指数，从合作科研机构数、合作企业数、科技创新成果数量、技术转化成果数量四个维度评定，取值 0—100。

## 计算逻辑说明

demo_gkxlumenx_ads.svc_org_card(service_type_candidate=INNOV) — 科技创新服务机构认定。

第一步：各指标标准化

各指标原始数据通过极值归一化法转换为 0—100 之间的标准化得分：
$$
指标得分_{ij} = \frac{x_{ij} - \min(x_j)}{\max(x_j) - \min(x_j)} \times 100
$$

$$
其中，x_{ij}为第 i个机构在第 j个指标上的原始值，\min(x_j)和 \max(x_j)分别为该指标在所有机构中的最小值和最大值。
$$

第二步：技术力综合得分

四个指标加权汇总（可采用等权重，各指标权重 = 1/4；也可根据评估重点自行制定各指标权重）：
$$
技术力得分 = \sum_{j=1}^{4} w_j \times 指标得分_{ij}
$$
其中，w_j 为第 j个指标的权重，可采用等权重（各占 25%），也可根据评估重点自行制定，\sum w = 1。得分越高，表明该科技创新服务机构的技术力越强。

| 指标             | 指标说明                                                     | 计算方法                            | 源表字段 | 待建字段 |
| :--------------- | :----------------------------------------------------------- | :---------------------------------- | -------- | -------- |
| 合作科研机构数 | 机构建立合作关系的科研机构（高校、科研院所等）数量 | 统计近三年累计合作科研机构总数 | dwd_patent(patent_id, first_applicant_name, applicants) — 联合申请人；dwd_org_heis_info(name_cn, univ_type) — 高校识别；dwd_zh_project(id, funded_institution) — 项目承担单位 | 无 |
| 合作企业数 | 机构建立合作关系的中小企业或规模以上企业数量 | 统计近三年累计合作企业总数 | dwd_patent(patent_id, applicants) — 联合企业申请人；dwd_org_invest_info(org_id, inv_org_id) — 投资连接 | 无 |
| 科技创新成果数量 | 机构累计有效发明专利、实用新型专利、软件著作权等知识产权总数 | 统计近三年累计知识产权授权/登记总数 | dwd_patent(patent_id, first_applicant_name, kind) — 专利类型,申请人对齐；dwd_patent_legal(pn, status, isdt_year) — 授权有效 | software_copyright_count-软件著作权数 |
| 技术转化成果数量 | 机构科技成果转化项目数（含技术转让、许可、作价投资等） | 统计近三年累计科技成果转化项目总数 | dwd_patent_transfer(pn, transfer_effective_date) — 专利转移生效 | 无 |

## 源表字段

- demo_gkxlumenx_ads.svc_org_card(org_id, name_cn, service_type_candidate) — 服务机构清单,科技创新类型筛选
- dwd_patent(patent_id, first_applicant_name, applicants, kind) — 联合申请人,成果专利
- dwd_org_heis_info(name_cn, univ_type) — 高校识别
- dwd_zh_project(id, funded_institution, title) — 国内项目承担单位
- dwd_patent_legal(pn, status, isdt_year) — 专利授权有效
- dwd_patent_transfer(pn, transfer_effective_date) — 专利转移
- dwd_org_invest_info(org_id, inv_org_id) — 合作企业代理

## 待建字段

- software_copyright_count-软件著作权数

## 参考资料

[2]科技创新服务机构技术力评价模型｜洛阳市科学技术局、洛阳市财政局｜洛阳市新型研发机构备案和绩效评价办法（试行）｜2024-02-28｜[洛阳市科学技术局 洛阳市财政局 关于印发《洛阳市新型研发机构备案和绩效评价办法（试行）》的通知_市科学技术局_洛阳市人民政府](https://www.ly.gov.cn/2024/05-07/118645.html)

[3]科技创新服务机构技术力评价模型｜三门峡市科学技术局｜省级新型研发机构绩效考核｜2025-09-19｜[文章详情-三门峡市科学技术局](http://kjj.smx.gov.cn/4/2025/9/2126236.html)
