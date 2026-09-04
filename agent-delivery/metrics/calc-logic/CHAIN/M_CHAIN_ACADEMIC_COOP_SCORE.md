# 产学研合作强度（M_CHAIN_ACADEMIC_COOP_SCORE）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_ACADEMIC_COOP_SCORE |
| 指标名称 | 产学研合作强度 |
| 一级模块 | 产业链分析 |
| 二级模块 | 区域产业竞争力评价 |
| 三级模块 | - |
| 更新频率 | 季度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

指定产业链上，企业与高校、科研机构之间的产学研合作强度综合评分，从联合专利、联合项目（合作论文）、人才流动三维加权评定，取值 0—100。对象=产业链层面的产学研合作，不是单次合作事件、也不是单个机构。

## 计算逻辑说明

采用加权平均。三维：联合专利 / 联合项目 / 人才流动。算法库「产业实体关系抽取」（1.1.1.1.1.1.1.2.2，约 378 行）明确需构建「产业-科研机构」关系，但未给出独立匹配度评分公式，故按产学研合作测度学术惯例补齐三维，默认等权（ΣW=1），甲方可改。

### 第一步：入集

- 先按 `dwd_org_industry_tags.industry_code` 定链，链上企业以 `credit_code` 去重。
- 高校以 `dwd_org_heis_info` 对齐，科研机构以 `dwd_research_institute_base_info` 对齐（`external_id`/`name_cn` 匹配）。

### 第二步：三个子项

1. **联合专利**：专利申请人主体同时包含「链上企业」与「高校/科研机构」的专利去重数。用 `dwd_patent.applicants`/`first_applicant_name` 与企业、机构名称做共现判定。
2. **联合项目（合作论文）**：链上企业与高校/科研机构共同署名的论文去重数。用 `dwd_zh_paper.author_info_list` 做机构共现判定（英文论文 `dwd_en_paper` 无作者单位明细，不计入本子项）。
3. **人才流动**：高校/科研机构学者与链上企业存在任职/合作关联的学者去重数。用 `dwd_scholar.scholar_org_id`/`scholar_org_name_zh` 与企业/机构名称匹配判定。

### 第三步：综合得分

各子项在统计窗内 min-max 归一到 0—100，等权求和：
$$
产学研合作强度 = \frac{1}{3}(联合专利得分 + 联合项目得分 + 人才流动得分)
$$

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 产学研合作强度 | 联合专利 | 联合专利数 | 企业与高校/科研机构共同申请的专利去重数 | COUNT(DISTINCT pn WHERE 申请人含企业且含高校/科研机构) | dwd_patent(pn, first_applicant_name, applicants, first_current_assignee_name, pbdt_year) — 申请人共现判定；dwd_org_industry_tags(industry_code, company_name, credit_code) — 链上企业；dwd_org_heis_info(name_cn, external_id) — 高校；dwd_research_institute_base_info(name_cn, external_id) — 科研机构 | 联合专利共现标记字段 |
|  | 联合项目 | 合作论文数 | 企业与高校/科研机构共同署名的论文去重数 | COUNT(DISTINCT paper_id WHERE 作者单位含企业与高校/科研机构) | dwd_zh_paper(id, author_info_list, cover_year_start) — 作者单位共现；dwd_org_industry_tags(industry_code, company_name) — 链上企业；dwd_org_heis_info(name_cn) — 高校；dwd_research_institute_base_info(name_cn) — 科研机构 | 合作项目/技术合同成交额表；英文论文作者单位明细 |
|  | 人才流动 | 校企人才关联数 | 高校/科研机构学者与链上企业存在任职关联的去重学者数 | COUNT(DISTINCT scholar_id WHERE 学者机构含企业与高校/科研机构) | dwd_scholar(scholar_id, scholar_org_id, scholar_org_name_zh) — 学者所属机构；dwd_org_industry_tags(industry_code, company_name) — 链上企业；dwd_org_heis_info(name_cn) — 高校；dwd_research_institute_base_info(name_cn) — 科研机构 | 人才流动轨迹表 |

## 源表字段

- dwd_org_industry_tags(industry_code, industry_name, company_name, credit_code) — 链上企业入集
- dwd_org_heis_info(org_id, name_cn, external_id, city) — 高校机构
- dwd_research_institute_base_info(org_id, name_cn, external_id, city) — 科研机构
- dwd_patent(pn, first_applicant_name, applicants, first_current_assignee_name, pbdt_year) — 联合专利判定
- dwd_zh_paper(id, author_info_list, cover_year_start) — 合作论文判定（中文）
- dwd_scholar(scholar_id, scholar_org_id, scholar_org_name_zh) — 人才流动判定
- industry_chain_entity_rel(chain_id, node_id, entity_type, entity_id, relation_type, confidence) — 产业-科研机构图谱关系（demo_gkxlumenx_dwd）

## 待建字段

- 联合专利共现标记字段（申请人「企业×机构类型」判定结果）
- 合作项目/技术合同成交额表（产学研项目维度）
- 人才流动轨迹表（学者跨校企任职/合作记录）
- industry_chain_entity_rel 中 entity_type=科研机构 的关系抽取结果标准化

## 参考资料

[1] 产业实体关系抽取｜科技专题服务算法库 1.1.1.1.1.1.1.2.2（产业-科研机构关系）。

[2] 产学研合作强度测度｜教育部、科学技术部｜《关于促进产学研用深度融合的指导意见》，以联合专利、合作论文、人才流动为核心测度维度。

[3] 产学研协同创新｜国家发展改革委｜《关于推动产业创新能力提升的指导意见》，产学研合作以联合专利/联合项目/人才流动加权评价。
