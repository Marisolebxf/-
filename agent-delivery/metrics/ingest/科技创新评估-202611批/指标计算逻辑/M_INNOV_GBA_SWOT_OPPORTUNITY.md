# 湾区创新能力机会因素（M_INNOV_GBA_SWOT_OPPORTUNITY）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_GBA_SWOT_OPPORTUNITY |
| 指标名称 | 湾区创新能力机会因素 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 湾区创新监测 / 创新能力分析（SWOT） |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

识别选定湾区城市的外部机会：政策窗口、新兴技术、外溢合作。输出机会清单与利用建议。

## 计算逻辑说明

湾区 11 城、机构入集与名称对齐同创新能力总指数。机会看**近窗相对基线的变化**，不与优势因素共用「高分项」规则。

基线窗 \($T-7,\ldots,T-3$\)，近窗 \($T-2,\ldots,T$\)。

### 第一步：三个子项

1. **政策窗口**：该城近窗有效政策件数 / max(基线年均政策件数, 1)。≥ 1.5 记入机会。利用建议：对接近窗新增主题的政策申报。
2. **新兴技术**：该城专利按 IPC 前 4 位做突现（规则同创新点发现：burst ≥ 1 且近窗专利 ≥ 3）。入选 IPC4 个数 ≥ 1 记入机会。利用建议：沿突现 IPC 加大布局。
3. **外溢合作**：近窗联合专利中，`applicants` 含该城机构且另有至少一个**非本城**机构的去重件数。相对基线年均增幅 ≥ 0.5 记入机会。利用建议：扩大跨城联合申请。

### 第二步：清单

三个子项分别计算信号值；达标则输出一行，含 `factor`、`signal`、`advice`。皆未达标则输出信号最大的 1 项并标记 `weak_signal=1`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 湾区创新能力机会因素 | 政策窗口 | 近窗政策相对基线是否放量。 | 近窗政策数 / max(基线年均政策数, 1) ≥ 1.5 | dwd_policy_base(id, city, province, status, expire_date, publish_year, theme) — 政策去重,湾区城市,有效,发布年,主题 | 无 |
| 湾区创新能力机会因素 | 新兴技术 | 该城突现 IPC 领域。 | burst≥1 且近窗专利≥3 的 IPC4 个数 | dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 申请人对齐,IPC领域,申请年 | 无 |
| 湾区创新能力机会因素 | 外溢合作 | 跨城联合专利是否加速。 | (近窗跨城联合专利年均 − 基线年均) / max(基线年均, 1) ≥ 0.5 | dwd_patent(pn, applicants, first_applicant_name, apdt_year) — 共申请人,申请人对齐,申请年 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集
- dwd_policy_base(id, city, province, status, expire_date, publish_year, theme) — 政策窗口,主题
- dwd_patent(pn, applicants, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,共申请人,IPC突现,申请年

## 待建字段

- 无

## 参考资料

[1] 湾区创新能力机会因素｜华中科技大学管理学院，华中科技大学法学院｜教育部人文社会科学基金青年基金项目（20YJC630201）｜纪亚琨，余翔，张奔，彭文波. 专利网络视角下的潜在颠覆性技术识别——以自动驾驶领域为例[J]. 情报杂志, 2022, 41(12): 46-50, 139.

[2]湾区创新能力机会因素｜北京理工大学珠海学院｜广东省哲学社会科学规划2023年度青年项目（GD23YJY01）；北京理工大学珠海学院粤港澳大湾区高质量发展重大问题研究课题（XK-2023-034）｜马静娴. 粤港澳大湾区产学协同创新网络结构特征及优化对策[J]. 科技和产业, 2024, 24(22): 230-240.
