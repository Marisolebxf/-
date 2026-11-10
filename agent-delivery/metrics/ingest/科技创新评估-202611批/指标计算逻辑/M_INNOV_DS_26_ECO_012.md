# 协同绩效与影响力智能评估（M_INNOV_DS_26_ECO_012）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_26_ECO_012 |
| 指标名称 | 协同绩效与影响力智能评估 |
| 使用位置 | 科技专题服务系统 / 科技专题战略分析 / 服务生态分析 |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

生态内机构的协同绩效与影响力。统计对象为选定范围内存续机构，从产出规模、网络协同综合评分，取值 0—100。分数越高，协同与影响越强。

## 计算逻辑说明

节点用规范化机构名，边用共现，不用关系表和待建协同分。

### 第一步：入集

`dwd_org_base_info` 与 `dwd_research_institute_base_info` 按 `org_id` 去重；`reg_status` 含「存续」。名称用 `name_cn`。空间用 `province`/`city`。

### 第二步：三个子项

同一维在**本批机构**内极值归一。

1. **产出规模**  
   统计年专利去重件数 + 中英文论文去重件数。专利 `first_applicant_name` 对齐；论文作者 `institution` 对齐；年键分别为 `apdt_year`、`cover_year_start`。

2. **网络协同**  
   合作邻居去重数：同一专利 `applicants` 中其他机构、同一论文其他作者单位、同一项目 `participating_institution` 中其他机构。

3. **协同绩效**  
   有合作的成果件数 / 该机构成果件数（专利 + 论文 + 项目，项目用 `funded_institution` 对齐）。分母为 0 则该维缺测。

### 第三步：合成

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
协同影响力=\frac{norm(产出规模)+norm(网络协同)+norm(协同绩效)}{3}\times 100
$$

缺测维不补 0，剩余维权重重归一。

输出：一行一个机构，含三子项原始值、`score`（0—100）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 协同绩效与影响力智能评估 | 产出规模 | 机构专利与论文件数。 | COUNT(DISTINCT pn)+COUNT(DISTINCT 论文id) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 协同绩效与影响力智能评估 | 网络协同 | 合作邻居数。 | COUNT(DISTINCT 合作机构名) | dwd_patent(pn, applicants, first_applicant_name) — 共申请人；dwd_zh_project(id, funded_institution, participating_institution) — 项目合作机构 | 无 |
| 协同绩效与影响力智能评估 | 协同绩效 | 合作成果占自身成果比。 | 合作成果数 / 成果数 | 同上专利论文项目 — 合作占比 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 机构入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_patent(pn, first_applicant_name, applicants, apdt_year) — 专利去重,申请人对齐,共申请人,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐
- dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 受资助机构,参与机构,立项年

## 待建字段

- 无

## 参考资料

[1] 协同绩效与影响力智能评估｜东莞理工学院图书馆｜东莞理工学院高等教育研究重点项目（GJKY20220）｜楼晶. 研究型高校与应用型高校学科科研产出评价体系差异研究——以工程学学科为例[J]. 图书情报导刊, 2023, 8(10): 71-79.

[2]协同绩效与影响力智能评估 ｜兰州大学管理学院｜中央高校基本科研业务专项资金（2022016zrbr07）｜邵瑞华，沙勇忠，李亮. 机构合作网络与机构学术影响力的关系研究——以图书情报学科为例[J]. 情报科学, 2017, 35(3): 42-46, 86. DOI: 10.13833/[j.cnki.is](https://j.cnki.is/).2017.03.008.
