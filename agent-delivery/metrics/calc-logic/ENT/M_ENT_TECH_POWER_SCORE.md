# 技术力得分（M_ENT_TECH_POWER_SCORE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_TECH_POWER_SCORE |
| 指标名称 | 技术力得分 |
| 一级模块 | 企业分析 |
| 二级模块 | 企业评估 |
| 三级模块 | 技术力评估 |
| 更新频率 | 年度/模型版本发布时 |
| 对齐状态判定 | 未对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | Q014 |


## 口径定义

企业技术力评估的综合得分，满分0—100分，综合反映企业技术人才储备、技术创新产出、技术转化效率、技术合作能力及研发投入水平。

## 计算逻辑说明

| 一级维度     | 权重 | 三级指标                           | 指标说明                                         | 源表字段 |
| :----------- | :--- | :--------------------------------- | :----------------------------------------------- | -------- |
| **技术人才** | 20%  | 研发人员占职工总数的比重           | 反映企业技术人力投入规模                         | gkx.dwd_org_annual_financial_info(org_id, development_employee, employees_number, year) — 研发人员占比=研发人员数÷从业人数×100% |
|              |      | 高级研发人才数量                   | 副高级及以上职称或硕士及以上学历的专职研发人员数 | gkx.dwd_org_annual_financial_info(org_id, development_employee, year) — 研发人员总数（分母参考）<br>gkx 现库无学历/职称结构字段（待建）— 高级研发人才数 |
| **技术创新** | 25%  | 有效发明专利数量                   | 企业拥有的有效发明专利总量                       | gkx.dwd_org_rd_achiev_info(org_id, inv_pat_auth_num) — 有效发明专利授权数（累计预聚合） |
|              |      | 发明专利占比                       | 有效发明专利 ÷ 有效专利总数                      | gkx.dwd_org_rd_achiev_info(org_id, inv_pat_auth_num, util_pat_auth_num, des_pat_auth_num) — 发明专利占比=发明专利授权数÷(发明+实用新型+外观设计)×100% |
|              |      | 当年新增发明专利申请数             | 衡量核心技术产出活跃度                           | gkx.dwd_patent(patent_id, first_applicant_name, application_reference) — 专利申请信息<br>gkx.dwd_patent_legal(patent_id, status, isdt_year) — 法律状态与申请年份筛选 |
| **技术转化** | 20%  | 新产品销售收入占主营业务收入的比重 | 反映技术成果的市场化水平                         | gkx.dwd_org_annual_financial_info(org_id, operating_revenue, year) — 主营业务收入（分母）<br>gkx 现库无新产品销售收入字段（待建）— 新产品销售收入 |
|              |      | 技术合同成交额                     | 反映技术对外转移和交易活跃度                     | gkx 现库无技术合同成交额字段（待建）— 技术合同交易数据 |
| **技术合作** | 15%  | 产学研合作项目数量                 | 企业与高校/科研院所合作项目数                  | gkx.dwd_zh_project(id, project_host, participating_institution) + gkx.dwd_en_project(id, project_host, participating_institution) — 产学研合作项目 |
|              |      | 外部专家参与研发的人月数           | 来企业从事研发工作的外部专家工作量               | gkx 现库无外部专家人月数字段（待建）— 外部专家工作量数据 |
| **技术投入** | 20%  | 研发经费支出占主营业务收入的比重   | 衡量企业研发投入强度                             | gkx.dwd_org_annual_financial_info(org_id, `arch development am`, operating_revenue, year) — 研发投入强度=`arch development am`÷营业收入×100% |
|              |      | 研发人员人均研发经费支出           | 反映人均研发资源保障水平                         | gkx.dwd_org_annual_financial_info(org_id, `arch development am`, development_employee, year) — 人均研发经费=`arch development am`÷研发人员数 |

## 源表字段

gkx.dwd_org_annual_financial_info(org_id, development_employee, employees_number, `arch development am`, operating_revenue, year) — 技术人才维度（研发人员占比）、技术投入维度（研发经费强度、人均研发经费），优先年报，覆盖非上市企业
gkx.dwd_org_rd_achiev_info(org_id, inv_pat_auth_num, util_pat_auth_num, des_pat_auth_num) — 技术创新维度（有效发明专利数、发明专利占比，专利授权累计预聚合）
gkx.dwd_patent(patent_id, first_applicant_name, application_reference) — 技术创新维度（当年新增发明专利申请数，按申请年份筛选）
gkx.dwd_patent_legal(patent_id, status, isdt_year) — 技术创新维度（法律状态过滤有效专利、申请年份筛选）
gkx.dwd_zh_project(id, project_host, participating_institution) — 技术合作维度（中文产学研合作项目）
gkx.dwd_en_project(id, project_host, participating_institution) — 技术合作维度（英文产学研合作项目）
高级研发人才数字段 — 现库无学历/职称结构字段，待建
新产品销售收入字段 — 现库无此字段，待建
技术合同成交额字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建

注：技术力得分由技术人才(20%)、技术创新(25%)、技术转化(20%)、技术合作(15%)、技术投入(20%)五个维度加权汇总，各指标经极值归一化后按权重加权计算，权重待甲方确认（Q014）。结果表 ads_ent_tech_score(tech_score, org_id, 待建)。

## 待建字段

高级研发人才数字段 — 现库无学历/职称结构字段，待建
新产品销售收入字段 — 现库无此字段，待建
技术合同成交额字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建
