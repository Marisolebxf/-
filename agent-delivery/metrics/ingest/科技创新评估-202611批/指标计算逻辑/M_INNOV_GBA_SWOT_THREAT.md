# 湾区创新能力威胁因素（M_INNOV_GBA_SWOT_THREAT）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_GBA_SWOT_THREAT |
| 指标名称 | 湾区创新能力威胁因素 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 湾区创新监测 / 创新能力分析（SWOT） |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

识别选定湾区城市的外部威胁：政策退坡、竞争挤压、结构风险。输出威胁清单与应对策略。本指标不是 0—100 评分。

## 计算逻辑说明

湾区 11 城、机构入集与名称对齐同创新能力总指数。威胁看**近窗相对基线的恶化**，不与短板因素共用「低分项」规则。

基线窗 \(T-7,\ldots,T-3\)，近窗 \(T-2,\ldots,T\)。

### 第一步：三个子项

1. **政策退坡**：近窗 `status` 含「失效」或 `expire_date` 落入近窗的政策件数 / max(近窗仍有效政策件数, 1)。≥ 0.3 记入威胁。应对：补位即将到期政策，稳住有效供给。
2. **竞争挤压**：该城近窗专利占 11 城近窗专利合计的份额 − 基线份额。下降 ≥ 0.02（2 个百分点）记入威胁。应对：对照份额上升城市补齐对应 IPC 布局。
3. **结构风险**：该城近窗专利按 IPC 前 4 位的赫芬达尔指数 \(HHI=\sum s_i^2\)（\(s_i\) 为 IPC4 件数占比）。≥ 0.25 记入威胁（过度集中）。应对：向第二、第三 IPC 领域分流申请。

### 第二步：清单

三个子项分别计算信号值；达标则输出一行，含 `factor`、`signal`、`advice`。皆未达标则输出信号最大的 1 项并标记 `weak_signal=1`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 湾区创新能力威胁因素 | 政策退坡 | 失效政策相对有效政策的比例。 | 近窗失效政策数 / max(近窗有效政策数, 1) ≥ 0.3 | dwd_policy_base(id, city, province, status, expire_date, publish_year) — 政策去重,湾区城市,有效失效,到期日 | 无 |
| 湾区创新能力威胁因素 | 竞争挤压 | 该城专利份额是否下滑。 | 近窗份额 − 基线份额 ≤ −0.02 | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年 | 无 |
| 湾区创新能力威胁因素 | 结构风险 | 专利领域是否过度集中。 | HHI(IPC4) ≥ 0.25 | dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 申请人对齐,IPC领域,申请年 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集
- dwd_policy_base(id, city, province, status, expire_date, publish_year) — 政策有效失效,到期日
- dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC集中度,申请年

## 待建字段

- 无

## 参考资料

[1] 湾区创新能力威胁因素｜西北政法大学经济学院，中南财经政法大学经济学院｜陕西省科技厅项目（2021JM-454）｜徐梅，张露. 补贴退坡对新能源企业技术创新的影响研究[J]. 重庆社会科学, 2025(8): 85-100. DOI: 10.19631/j.cnki.css.2025.008.006.

[2]湾区创新能力威胁因素｜知识产权出版社有限责任公司｜王彦嫱，张聿文，姚长利. 基于HHI指数的中国类脑智能产业专利集中度研究[J]. 中国发明与专利, 2026, 23(6): 15-22.
