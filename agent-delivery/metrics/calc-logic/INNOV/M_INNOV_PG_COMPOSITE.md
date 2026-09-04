# 政策与条件保障力综合评估（M_INNOV_PG_COMPOSITE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PG_COMPOSITE |
| 指标名称 | 政策与条件保障力综合评估 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q-MO-DS07-01 |

## 口径定义

将引导力、扶持力度、经费、项目、效果五维加权，取值 0—100。对象为城市。引导力与 M_INNOV_PG_GUIDE 同一三级。

## 计算逻辑说明

选定城市入集。采用加权平均，五维：发展战略引导力（前瞻性/系统性/针对性，与 POLICY_GUARD_001 同一套覆盖率） / 政策扶持力度（政策数量/政策类型/政策覆盖面） / 经费支持（科研经费/产业基金） / 项目支持（项目数量/资助金额/实施效果） / 政策实施效果（实施前后对比）。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 发展战略引导力 |  | 从前瞻性、系统性、针对性评估政策引导力。 | 维内三项极值归一后等权。与 M_INNOV_PG_GUIDE、M_POLICY_DS_07_POLICY_GUARD_001 同一套覆盖率。 | dwd_policy_base(id, title, keywords, keypoints, theme, quote_policy, policy_support, city, province, publish_year, status, expire_date) — 四字段前瞻词,政策承接,扶持措施,有效,发布年,空间 |
| 发展战略引导力 | 前瞻性 | 政策是否包含规划/纲要/远景等顶层设计词。 | 四字段含「规划」或「纲要」或「远景」的政策数 ÷ 政策总数 | dwd_policy_base(title, keywords, keypoints, theme) — 四字段命中 |
| 发展战略引导力 | 系统性 | 政策是否明确引用或承接过往相关政策。 | quote_policy 非空且不为空数组的政策数 ÷ 政策总数 | dwd_policy_base(quote_policy) — 政策承接 |
| 发展战略引导力 | 针对性 | 政策是否包含明确扶持细则。 | policy_support.support_way 至少 1 条非空的政策数 ÷ 政策总数 | dwd_policy_base(policy_support.support_way) — 扶持措施 |
| 政策扶持力度 |  | 从政策数量、类型、覆盖面评估扶持广度。 | 维内三项极值归一后等权。 | dwd_policy_base(id, city, type, district, theme, status, expire_date, publish_year) — 政策件数,类型,区县,主题,有效 |
| 政策扶持力度 | 政策数量 | 有效政策去重件数。 | COUNT(DISTINCT id) | dwd_policy_base(id, city, status, expire_date, publish_year) — 政策件数,有效 |
| 政策扶持力度 | 政策类型 | 政策类型覆盖数。 | COUNT(DISTINCT type) | dwd_policy_base(id, city, type, status, expire_date, publish_year) — 政策类型 |
| 政策扶持力度 | 政策覆盖面 | 政策触及的区县广度。 | COUNT(DISTINCT district)；全空则 COUNT(DISTINCT theme) | dwd_policy_base(id, city, district, theme, status, expire_date, publish_year) — 区县,主题 |
| 经费支持 |  | 从科研经费、产业基金评估经费支持。 | 维内两项极值归一后等权。无补贴金额专表，不单列补贴。 | dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 机构入集,名称对齐,空间；dwd_industrial_fund_basic_info(industrial_fund_id, reg_region, est_date) — 产业基金注册地,设立日 |
| 经费支持 | 科研经费 | 该城机构上市研发投入合计。 | SUM(research_development_amount) | dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 机构入集,名称对齐,空间 |
| 经费支持 | 产业基金 | 注册地落在该城的产业基金数。 | COUNT(DISTINCT industrial_fund_id) | dwd_industrial_fund_basic_info(industrial_fund_id, reg_region, est_date) — 产业基金注册地,设立日 |
| 项目支持 |  | 从项目数量、资助金额、结题率评估项目支持。 | 维内三项极值归一后等权。 | dwd_zh_project(id, funded_amount, funded_institution, funded_province, approval_year, final_report_abstract) — 项目资助,机构对齐,立项年,结题 |
| 项目支持 | 项目数量 | 立项项目去重件数。 | COUNT(DISTINCT id) | dwd_zh_project(id, funded_institution, funded_province, approval_year) — 项目去重,立项年 |
| 项目支持 | 资助金额 | 项目资助额合计。 | SUM(funded_amount) | dwd_zh_project(id, funded_amount, funded_institution, funded_province, approval_year) — 资助金额,立项年 |
| 项目支持 | 实施效果 | 有结题摘要的项目占比。 | 结题项目数 / 项目数 | dwd_zh_project(id, final_report_abstract, funded_institution, funded_province, approval_year) — 结题摘要 |
| 政策实施效果 |  | 政策实施前后关键成果对比。 | 近窗相对基线的成果增幅。 | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 |
| 政策实施效果 | 实施前后对比 | 近窗成果相对基线的增幅。 | (近3年均值 − 前5年均值) / max(前5年均值, 1) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 |

## 源表字段

dwd_policy_base(id, city, province, district, status, expire_date, publish_year, rank, type, theme, quote_policy) — 政策去重,有效,级别,类型,主题,区县,引用；dwd_zh_project(id, funded_amount, funded_institution, funded_province, approval_year, final_report_abstract) — 项目资助,机构对齐,立项年,结题；dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 机构入集,名称对齐,空间；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_industrial_fund_basic_info(industrial_fund_id, reg_region, est_date) — 产业基金注册地,设立日；dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位

## 待建字段

无

## 备注

依照需求文档构建。02-科技信息展示系统|科技发展态势|科技创新评估.md|序号 157「将政策与条件保障力的各项指标进行综合展示，用户可自定义指标权重，系统根据权重计算综合得分，提供政策与条件保障力的综合评估结果和排名」。二级来自 seq 152-156（引导力/扶持力度/经费/项目/效果）。政策 9 叶无保障力综合专叶。禁止 mapped 167/168/185/186。权重待 Q-MO-DS07-01。
