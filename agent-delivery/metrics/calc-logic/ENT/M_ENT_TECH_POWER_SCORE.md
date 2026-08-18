# 技术力得分（M_ENT_TECH_POWER_SCORE）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 本指标含 12 行子指标（L1+L2+L3），已合并为单文件。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## L1 指标元数据

- **指标ID**：`M_ENT_TECH_POWER_SCORE`
- **指标名称（一级）**：技术力得分
- **一级模块**：企业分析
- **二级模块**：企业评估
- **三级模块**：技术力评估
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **是否在数据库（L1）**：部分
- **关联Q编号**：Q014

## L1 口径定义

企业技术力评估的综合得分，满分0-100分，综合反映企业在技术人才、技术创新、技术转化、技术合作、技术投入五个维度的综合水平。

## L1 计算逻辑说明

```
采用加权平均。五维：技术人才/技术创新/技术转化/技术合作/技术投入。
```

**计算公式文件**：`M_ENT_TECH_POWER_SCORE.md`

## L1 源表字段

```
gkx.dwd_org_annual_financial_info(org_id, development_employee, employees_number, `arch development am`, operating_revenue, year) — 技术人才维度（研发人员占比）、技术投入维度（研发经费强度、人均研发经费），优先年报，覆盖非上市企业
gkx.dwd_org_rd_achiev_info(org_id, inv_pat_auth_num, util_pat_auth_num, des_pat_auth_num) — 技术创新维度（有效发明专利数、发明专利占比，专利授权累计预聚合）
gkx.dwd_patent(patent_id, first_applicant_name, application_reference) — 技术创新维度（当年新增发明专利申请数，按申请年份筛选）
gkx.dwd_patent_legal(patent_id, status, isdt_year) — 技术创新维度（法律状态过滤有效专利、申请年份筛选）
gkx.dwd_zh_project(id, project_host, participating_institution) — 技术合作维度（中文产学研合作项目）
gkx.dwd_en_project(id, project_host, participating_institution) — 技术合作维度（英文产学研合作项目）
```

## L1 备注

1.1.1.2.4.2.3.3 + 算法库5.5；依照需求文档提供的构建方法

## 子指标详情（L2 / L3）

### L2：技术人才

#### L3：研发人员占职工总数的比重

- **口径定义**：从研发人员占比、高级研发人才数量等维度评估企业技术人才储备规模与结构。
- **计算逻辑**：`研发人员数 / 职工总数`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, development_employee, employees_number, year) — 研发人员占比=研发人员数÷从业人数×100%`
- **待建表字段**：`高级研发人才数字段 — 现库无学历/职称结构字段，待建
新产品销售收入字段 — 现库无此字段，待建
技术合同成交额字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.3 + 算法库5.5；依照需求文档提供的构建方法；研发人员优先取年报development_employee

#### L3：高级研发人才数量

- **口径定义**：从研发人员占比、高级研发人才数量等维度评估企业技术人才储备规模与结构。
- **计算逻辑**：`高级研发人才数量（副高级及以上职称或硕士及以上学历专职研发人员数）`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, development_employee, year) — 研发人员总数（分母参考）<br>gkx 现库无学历/职称结构字段（待建）— 高级研发人才数`
- **待建表字段**：`高级研发人才数字段 — 现库无学历/职称结构字段，待建
新产品销售收入字段 — 现库无此字段，待建
技术合同成交额字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：否
- **备注**：1.1.1.2.4.2.3.3 + 算法库5.5；依照需求文档提供的构建方法；研发人员优先取年报development_employee

### L2：技术创新

#### L3：有效发明专利数量

- **口径定义**：从有效发明专利存量、发明专利占比及当年新增申请量等维度评估企业核心技术产出能力与创新活跃度。
- **计算逻辑**：`有效发明专利数量`
- **源表字段**：`gkx.dwd_org_rd_achiev_info(org_id, inv_pat_auth_num) — 有效发明专利授权数（累计预聚合）`
- **待建表字段**：`高级研发人才数字段 — 现库无学历/职称结构字段，待建
新产品销售收入字段 — 现库无此字段，待建
技术合同成交额字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.3 + 算法库5.5；依照需求文档提供的构建方法

#### L3：发明专利占比

- **口径定义**：从有效发明专利存量、发明专利占比及当年新增申请量等维度评估企业核心技术产出能力与创新活跃度。
- **计算逻辑**：`有效发明专利数 / 有效专利总数`
- **源表字段**：`gkx.dwd_org_rd_achiev_info(org_id, inv_pat_auth_num, util_pat_auth_num, des_pat_auth_num) — 发明专利占比=发明专利授权数÷(发明+实用新型+外观设计)×100%`
- **待建表字段**：`高级研发人才数字段 — 现库无学历/职称结构字段，待建
新产品销售收入字段 — 现库无此字段，待建
技术合同成交额字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.3 + 算法库5.5；依照需求文档提供的构建方法

#### L3：当年新增发明专利申请数

- **口径定义**：从有效发明专利存量、发明专利占比及当年新增申请量等维度评估企业核心技术产出能力与创新活跃度。
- **计算逻辑**：`当年新增发明专利申请数`
- **源表字段**：`gkx.dwd_patent(patent_id, first_applicant_name, application_reference) — 专利申请信息<br>gkx.dwd_patent_legal(patent_id, status, isdt_year) — 法律状态与申请年份筛选`
- **待建表字段**：`高级研发人才数字段 — 现库无学历/职称结构字段，待建
新产品销售收入字段 — 现库无此字段，待建
技术合同成交额字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.3 + 算法库5.5；依照需求文档提供的构建方法

### L2：技术转化

#### L3：新产品销售收入占主营业务收入的比重

- **口径定义**：从新产品销售收入占比、技术合同成交额等维度评估企业技术成果的市场化与对外转化水平
- **计算逻辑**：`新产品销售收入 / 主营业务收入`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, operating_revenue, year) — 主营业务收入（分母）<br>gkx 现库无新产品销售收入字段（待建）— 新产品销售收入`
- **待建表字段**：`高级研发人才数字段 — 现库无学历/职称结构字段，待建
新产品销售收入字段 — 现库无此字段，待建
技术合同成交额字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：否
- **备注**：1.1.1.2.4.2.3.3 + 算法库5.5；依照需求文档提供的构建方法；专利许可表待建

#### L3：技术合同成交金额

- **口径定义**：从新产品销售收入占比、技术合同成交额等维度评估企业技术成果的市场化与对外转化水平
- **计算逻辑**：`技术合同成交额`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, development_employee, employees_number, `arch development am`, operating_revenue, year) — 技术人才维度（研发人员占比）、技术投入维度（研发经费强度、人均研发经费），优先年报，覆盖非上市企业
gkx.dwd_org_rd_achiev_info(org_id, inv_pat_auth_num, util_pat_auth_num, des_pat_auth_num) — 技术创新维度（有效发明专利数、发明专利占比，专利授权累计预聚合）
gkx.dwd_patent(patent_id, first_applicant_name, application_reference) — 技术创新维度（当年新增发明专利申请数，按申请年份筛选）
gkx.dwd_patent_legal(patent_id, status, isdt_year) — 技术创新维度（法律状态过滤有效专利、申请年份筛选）
gkx.dwd_zh_project(id, project_host, participating_institution) — 技术合作维度（中文产学研合作项目）
gkx.dwd_en_project(id, project_host, participating_institution) — 技术合作维度（英文产学研合作项目）`
- **待建表字段**：`高级研发人才数字段 — 现库无学历/职称结构字段，待建
新产品销售收入字段 — 现库无此字段，待建
技术合同成交额字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.3 + 算法库5.5；依照需求文档提供的构建方法；专利许可表待建

### L2：技术合作

#### L3：产学研合作项目数量

- **口径定义**：从产学研合作项目数量、外部专家参与研发工作量等维度评估企业外部技术协作与开放创新程度。
- **计算逻辑**：`产学研合作项目数量`
- **源表字段**：`gkx.dwd_zh_project(id, project_host, participating_institution) + gkx.dwd_en_project(id, project_host, participating_institution) — 产学研合作项目`
- **待建表字段**：`高级研发人才数字段 — 现库无学历/职称结构字段，待建
新产品销售收入字段 — 现库无此字段，待建
技术合同成交额字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.3 + 算法库5.5；依照需求文档提供的构建方法；供应链合作表待建

#### L3：外部专家参与研发的人数

- **口径定义**：从产学研合作项目数量、外部专家参与研发工作量等维度评估企业外部技术协作与开放创新程度。
- **计算逻辑**：`外部专家参与研发人数（人月）`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, development_employee, employees_number, `arch development am`, operating_revenue, year) — 技术人才维度（研发人员占比）、技术投入维度（研发经费强度、人均研发经费），优先年报，覆盖非上市企业
gkx.dwd_org_rd_achiev_info(org_id, inv_pat_auth_num, util_pat_auth_num, des_pat_auth_num) — 技术创新维度（有效发明专利数、发明专利占比，专利授权累计预聚合）
gkx.dwd_patent(patent_id, first_applicant_name, application_reference) — 技术创新维度（当年新增发明专利申请数，按申请年份筛选）
gkx.dwd_patent_legal(patent_id, status, isdt_year) — 技术创新维度（法律状态过滤有效专利、申请年份筛选）
gkx.dwd_zh_project(id, project_host, participating_institution) — 技术合作维度（中文产学研合作项目）
gkx.dwd_en_project(id, project_host, participating_institution) — 技术合作维度（英文产学研合作项目）`
- **待建表字段**：`高级研发人才数字段 — 现库无学历/职称结构字段，待建
新产品销售收入字段 — 现库无此字段，待建
技术合同成交额字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.3 + 算法库5.5；依照需求文档提供的构建方法；供应链合作表待建

### L2：技术投入

#### L3：研发经费支出占主营业务收入的比重

- **口径定义**：从研发经费投入强度、研发人员人均研发经费等维度评估企业研发资源投入水平与保障能力。
- **计算逻辑**：`研发经费支出 / 主营业务收入`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, `arch development am`, operating_revenue, year) — 研发投入强度=`arch development am`÷营业收入×100%`
- **待建表字段**：`高级研发人才数字段 — 现库无学历/职称结构字段，待建
新产品销售收入字段 — 现库无此字段，待建
技术合同成交额字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.3 + 算法库5.5；依照需求文档提供的构建方法

#### L3：研发人工人均研发经费支出

- **口径定义**：从研发经费投入强度、研发人员人均研发经费等维度评估企业研发资源投入水平与保障能力。
- **计算逻辑**：`研发经费支出 / 研发人员数`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, development_employee, employees_number, `arch development am`, operating_revenue, year) — 技术人才维度（研发人员占比）、技术投入维度（研发经费强度、人均研发经费），优先年报，覆盖非上市企业
gkx.dwd_org_rd_achiev_info(org_id, inv_pat_auth_num, util_pat_auth_num, des_pat_auth_num) — 技术创新维度（有效发明专利数、发明专利占比，专利授权累计预聚合）
gkx.dwd_patent(patent_id, first_applicant_name, application_reference) — 技术创新维度（当年新增发明专利申请数，按申请年份筛选）
gkx.dwd_patent_legal(patent_id, status, isdt_year) — 技术创新维度（法律状态过滤有效专利、申请年份筛选）
gkx.dwd_zh_project(id, project_host, participating_institution) — 技术合作维度（中文产学研合作项目）
gkx.dwd_en_project(id, project_host, participating_institution) — 技术合作维度（英文产学研合作项目）`
- **待建表字段**：`高级研发人才数字段 — 现库无学历/职称结构字段，待建
新产品销售收入字段 — 现库无此字段，待建
技术合同成交额字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.3 + 算法库5.5；依照需求文档提供的构建方法

---
*生成自王惠 20260816 Excel 底稿（12 行），data-agent 正式化 2026-08-18*
