# 入站数据源表（已确认表结构 · 工作面）

> **范围**：供应方 MySQL `gkx` 库中，对本项目正式开放的 **`dwd_*` 表**（已落 DDL 沙箱）。  
> **不含**：加工规则、字段映射、自建 DWD/ADS 设计（见 `GDF/派单包/`、`data-design/`）。  
> **不含**：`ods_*`（供应方不暴露为正式输入）、`*_bak_*`（备份，勿进映射主路径）。

## 1. 数据源身份

| 项 | 值 |
|----|-----|
| 库 | MySQL `gkx` |
| 连接 | 见 [CONNECTION.md](CONNECTION.md) |
| 工作约束 | 见 [SUPPLIER-WORK-CONSTRAINTS.md](加工/SUPPLIER-WORK-CONSTRAINTS.md) |
| DDL 沙箱 | [gkx_schema_ddl.sql](gkx_schema_ddl.sql) |
| 结构落盘日 | 2026-07-15（后续供应方变更以新批次覆盖） |

## 2. 工作面定义

| 集合 | 是否工作面 | 说明 |
|------|------------|------|
| `dwd_*` 活跃（排除 bak） | **是** | 入站贴源原料；约 **206** 张（自 table_list 解析） |
| `dwd_*` 含 `_bak_` | 否 | 仅结构对照；**50** 张 |
| `ods_*` | 否 | 库内可见但正式不暴露；**165** 张 |

## 3. 已确认结构的入站表清单（`dwd_*` 活跃）

下列表名来自本目录 `加工/table_list.txt` / DDL 沙箱，表示**表结构已落盘**。字段级业务口径仍可能 🟡（见供应方约束 §业务字段未定稿）。

1. `dwd_author_affiliation`
2. `dwd_author_en_paper_rel`
3. `dwd_author_en_project_rel`
4. `dwd_author_en_report_rel`
5. `dwd_author_foreign_org_base_info_rel`
6. `dwd_author_global_patent_rel`
7. `dwd_author_info`
8. `dwd_author_org_base_info_rel`
9. `dwd_author_zh_paper_rel`
10. `dwd_author_zh_project_rel`
11. `dwd_author_zh_report_rel`
12. `dwd_calculation`
13. `dwd_clinical`
14. `dwd_clinical_trial`
15. `dwd_company`
16. `dwd_company_base`
17. `dwd_company_basic_tags`
18. `dwd_company_branch`
19. `dwd_company_brief_tags`
20. `dwd_company_change`
21. `dwd_company_contact_tags`
22. `dwd_company_diy_tags`
23. `dwd_company_history_name`
24. `dwd_company_honor_tags`
25. `dwd_company_industry_tags`
26. `dwd_company_license`
27. `dwd_company_location_tags`
28. `dwd_company_nei_code`
29. `dwd_company_recruit`
30. `dwd_company_reg_cap_change`
31. `dwd_company_shareholder`
32. `dwd_company_staff`
33. `dwd_company_transition_clean`
34. `dwd_crystal_structure`
35. `dwd_deal`
36. `dwd_drug`
37. `dwd_drug_profile`
38. `dwd_drug_substance`
39. `dwd_en_author`
40. `dwd_en_journal`
41. `dwd_en_paper`
42. `dwd_en_paper_abstract`
43. `dwd_en_paper_citation`
44. `dwd_en_paper_cited_by`
45. `dwd_en_paper_classification`
46. `dwd_en_paper_funding`
47. `dwd_en_paper_info`
48. `dwd_en_paper_reference`
49. `dwd_en_paper_related`
50. `dwd_en_paper_title`
51. `dwd_event`
52. `dwd_forg_agg_identifier`
53. `dwd_forg_base_info`
54. `dwd_forg_beneficiary_info`
55. `dwd_forg_contact`
56. `dwd_forg_executive_info`
57. `dwd_forg_industry`
58. `dwd_forg_investment`
59. `dwd_forg_profile`
60. `dwd_forg_shareholder`
61. `dwd_forg_ultimate_control`
62. `dwd_hycy_aquaculture_veterinary_drugs_enterprise_list`
63. `dwd_hycy_aquatic_new_species`
64. `dwd_hycy_china_classification_society_marine_product_list`
65. `dwd_hycy_china_mainland_submarine_cable`
66. `dwd_hycy_china_major_city_lng_receiving_capacity`
67. `dwd_hycy_china_ocean_large_model`
68. `dwd_hycy_china_offshore_field`
69. `dwd_hycy_china_offshore_production`
70. `dwd_hycy_china_offshore_production_growth`
71. `dwd_hycy_csad_ship`
72. `dwd_hycy_enterprise_indicators`
73. `dwd_hycy_gas_supply`
74. `dwd_hycy_global_alternative_marine_fuel_market_demand_scale`
75. `dwd_hycy_global_cruise_capacity_distribution`
76. `dwd_hycy_green_fuel_enterprise`
77. `dwd_hycy_index`
78. `dwd_hycy_industry`
79. `dwd_hycy_international_shipping_agency_enterprises_registration`
80. `dwd_hycy_international_shipping_certificate_effective_enterprise`
81. `dwd_hycy_leading_maritime_capitals`
82. `dwd_hycy_marine_alternative_fuel_cost`
83. `dwd_hycy_marine_energy_industry_carrier`
84. `dwd_hycy_marine_forecast_data`
85. `dwd_hycy_marine_observation_data`
86. `dwd_hycy_marine_remote_sensing_data`
87. `dwd_hycy_methanol_production_cost_trend_prediction`
88. `dwd_hycy_nvocc_operator_list`
89. `dwd_hycy_offshore_fishing_company_evaluation`
90. `dwd_hycy_pelagic_fishery_enterprise_eval_results`
91. `dwd_hycy_port_operation_license_form`
92. `dwd_hycy_shanghai_domestic_water_transport_directory`
93. `dwd_hycy_ship_management_enterprise_trustee_ship`
94. `dwd_hycy_shipping_capacity`
95. `dwd_hycy_submarine_cable_distribution`
96. `dwd_hycy_sz_maritime_law_attorneys`
97. `dwd_industry_chain_info`
98. `dwd_industry_chain_news_info`
99. `dwd_industry_code`
100. `dwd_information`
101. `dwd_job`
102. `dwd_market`
103. `dwd_material_virtual_structure`
104. `dwd_medical_device`
105. `dwd_molecular_spectrum`
106. `dwd_multi_omics`
107. `dwd_org_annual_financial_info`
108. `dwd_org_bankruptcy_public_cases`
109. `dwd_org_bankruptcy_public_cases_list`
110. `dwd_org_base_info_en_paper_rel`
111. `dwd_org_base_info_financing_meta_rel`
112. `dwd_org_base_info_financing_metadata_rel`
113. `dwd_org_base_info_patent_rel`
114. `dwd_org_base_info_zh_policies_rel`
115. `dwd_org_base_info_zh_project_rel`
116. `dwd_org_bid_info`
117. `dwd_org_change_record_info`
118. `dwd_org_changerecord_info`
119. `dwd_org_company_abnormal`
120. `dwd_org_company_chattel`
121. `dwd_org_company_illegal`
122. `dwd_org_company_justice`
123. `dwd_org_company_pledge`
124. `dwd_org_company_punish`
125. `dwd_org_executive_info`
126. `dwd_org_financing_info`
127. `dwd_org_hels_info`
128. `dwd_org_important_news_info`
129. `dwd_org_industry_chain_dtl`
130. `dwd_org_industry_chain_pat_dtl`
131. `dwd_org_industry_chain_prod_dtl`
132. `dwd_org_innovation_carrier`
133. `dwd_org_invest_info`
134. `dwd_org_merger_acquisition_info`
135. `dwd_org_opt_judicial_case`
136. `dwd_org_org_product_info`
137. `dwd_org_product_info`
138. `dwd_org_recruit_info`
139. `dwd_org_reg_info`
140. `dwd_org_risk_court_announcement`
141. `dwd_org_risk_court_announcement_list`
142. `dwd_org_risk_court_filed_case`
143. `dwd_org_risk_court_filed_case_litigant`
144. `dwd_org_risk_court_notice`
145. `dwd_org_risk_court_notice_list`
146. `dwd_org_risk_lawsuit`
147. `dwd_org_risk_lawsuit_list`
148. `dwd_org_risk_shixin`
149. `dwd_org_risk_tax_punish`
150. `dwd_org_risk_xianxiao`
151. `dwd_org_risk_zhixing`
152. `dwd_org_risk_zhongben`
153. `dwd_org_shareholder_info`
154. `dwd_org_stock_base`
155. `dwd_org_stock_finance_info`
156. `dwd_org_tag_info`
157. `dwd_org_tb_judicial_sale`
158. `dwd_org_tb_judicial_sale_info_company`
159. `dwd_patent`
160. `dwd_patent_abstract`
161. `dwd_patent_family`
162. `dwd_patent_legal`
163. `dwd_patent_title`
164. `dwd_protein`
165. `dwd_quantum_chain_link`
166. `dwd_quantum_frontier_talent`
167. `dwd_quantum_market_scale`
168. `dwd_quantum_product`
169. `dwd_quantum_rd_progress`
170. `dwd_quantum_tech_trend`
171. `dwd_react_detail`
172. `dwd_rel_project_paper`
173. `dwd_rel_project_patent`
174. `dwd_rel_project_scholar`
175. `dwd_rel_reaction_substance`
176. `dwd_rel_report_paper`
177. `dwd_rel_report_project`
178. `dwd_rel_report_scholar`
179. `dwd_rel_substance_paper`
180. `dwd_rel_substance_patent`
181. `dwd_safety`
182. `dwd_scholar`
183. `dwd_scholar_coauthor`
184. `dwd_scholar_paper_relation`
185. `dwd_scholar_papers`
186. `dwd_scholar_research_direction`
187. `dwd_scholar_talent_flag`
188. `dwd_series_metadata`
189. `dwd_series_timepoints`
190. `dwd_similar_substance`
191. `dwd_small_molecule_screening`
192. `dwd_substance`
193. `dwd_zck_intl_policy`
194. `dwd_zck_policy`
195. `dwd_zh_author`
196. `dwd_zh_journal`
197. `dwd_zh_paper`
198. `dwd_zh_paper_abstract`
199. `dwd_zh_paper_citation`
200. `dwd_zh_paper_classification`
201. `dwd_zh_paper_reference`
202. `dwd_zh_paper_related`
203. `dwd_zh_paper_title`
204. `dwd_zh_project`
205. `dwd_zh_project_output`
206. `dwd_zh_report`

### 3.1 资讯相关表使用裁定（2026-08-25）

结构在清单里 ≠ 可以进业务 Mapping。资讯只认下面三行：

| 表 / 库 | 使用 | 说明 |
|---------|------|------|
| `dwd_org_important_news_info` | **可用** | 企业重点资讯明细 |
| 行业分析要素库（`dwd_industry_analysis_*` 六表） | **可用** | 行业分析文档 / 资讯正文与关联维；清单见 `data-design/storage/CHAIN/sources/inventory-industry-analysis.md`。本目录 2026-07-15 编号表可能未列入，以 `gkx` live 为准 |
| `dwd_industry_chain_news_info` | **不可用** | 合规交付，无实用价值；禁止进入资讯功能与 Mapping 主路径 |

## 4. 明确不在本工作面的对象

- **`ods_*`**：供应方贴源层，不对项目正式开放（即使库中可见）。
- **`*_bak_*`**：历史备份表，禁止进入 Mapping 主路径。
- **项目自建 DWD/ADS**：在 `data-design/{垂向}/`，不是本目录内容。
- **字段映射 / ETL 加工**：在 `GDF/派单包/{域}/` 的 `09-*Mapping*`。

## 5. 相关但不混写

| 文档 | 关系 |
|------|------|
| `加工/table_inventory.md` | 全量盘点（含 ods/bak），作对照用 |
| `加工/ANALYSIS.md` | 与旧要素库差异 + 对映射任务含义 |
| `../../../GDF/派单包/` | 各域工作包（含 Mapping `09`） |
