# 创新机制指数（M_INNOV_GBA_MECH_INDEX）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_GBA_MECH_INDEX |
| 指标名称 | 创新机制指数 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 湾区创新监测 / 创新能力 |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

湾区各城协同创新与成果转化机制。统计对象为粤港澳大湾区 11 城，从联合专利、合作项目、成果转化综合评分，取值 0—100。分数越高，机制越活。

## 计算逻辑说明

湾区城市清单、入集与名称对齐同创新资源指数。转化率用转移件数除以专利件数，不另建转化率字段。

### 第一步：入集

该城存续机构集合同上。专利、项目用名称对齐，不用机构-专利、机构-项目关系表。

### 第二步：三个子项

同一维在**本批 11 城**内极值归一。

1. **联合专利**：统计年专利 `applicants` 拆出 ≥2 个机构名，且其中至少 1 个对齐到该城机构，`COUNT(DISTINCT pn)`。
2. **合作项目**：统计年 `dwd_zh_project` 中 `participating_institution` 拆出 ≥2 个机构，且 `funded_institution` 或参与机构对齐到该城，`approval_year` 落年窗，`COUNT(DISTINCT id)`。
3. **成果转化**：该城机构作为转移前或转移后权利人出现的专利转移去重件数 / 该城专利去重件数。分母为 0 则该维缺测。

### 第三步：合成

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
创新机制指数=\frac{norm(联合专利)+norm(合作项目)+norm(成果转化)}{3}\times 100
$$

缺测维不补 0，剩余维权重重归一。输出：一行一城，含三子项原始值、`mech_index`（0—100）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 创新机制指数 | 联合专利 | 多申请人专利件数。 | COUNT(DISTINCT 共申请人pn) | dwd_patent(pn, applicants, first_applicant_name, apdt_year) — 共申请人,申请人对齐,申请年 | 无 |
| 创新机制指数 | 合作项目 | 多机构项目件数。 | COUNT(DISTINCT 多机构项目id) | dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 受资助机构,参与机构,立项年 | 无 |
| 创新机制指数 | 成果转化 | 转移专利占专利比。 | 转移专利数 / 专利数 | dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移,生效日,转移前后权利人；dwd_patent(pn, first_applicant_name, apdt_year) — 专利分母,申请人对齐 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集
- dwd_patent(pn, applicants, first_applicant_name, apdt_year) — 专利去重,共申请人,申请人对齐,申请年
- dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移,生效日,转移前后权利人
- dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 受资助机构,参与机构,立项年

## 待建字段

- 无

## 参考资料

[1] 创新机制指数｜山西省科学技术厅｜省校合作科研机构建设运行与绩效评价管理办法｜2025-01-24｜https://www.shanxi.gov.cn/zcwjk/bmgfxwj/202501/t20250124_9758132.shtml.

[2]创新机制指数｜中国科学院成都文献情报中心，中国科学院大学｜中国科学院知识产权管理支撑专项项目（E4C00005）；中国科学院文献情报能力建设专项项目（E3201106）｜雷聪仪，张娴，等.基于三阶段DEA模型的科研机构专利技术转移效率评价研究[J]. 科技成果管理与研究, 2025, 20(1): 15-23.
