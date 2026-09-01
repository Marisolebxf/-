# 政策焦点识别模型（M_POLICY_DEEP_166_1）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-POLICY-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_DEEP_166_1 |
| 指标名称 | 政策焦点识别模型 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 政策分析 |
| 三级模块 | 政策时序分析 |
| 更新频率 | 周 |
| 对齐状态判定 | 待甲方GAP-ALGO-TYPE-UNSIGNED；与焦点指数同维 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

对有效政策文本做焦点/堵点识别的模型综合结果，从制定背景、政策目标、适用范围、措施执行情况四维提取焦点与堵点清单，并输出与 M_POLICY_FOCUS_INDEX 同构的 0—100 指数。

## 计算逻辑说明

入集：国内政策库 dwd_policy_base；status=有效且 expire_date 空或不早于统计日；按 id 去重。综合统计默认仅国内（QPOL-05），国际政策 dwd_global_policy_base 不进综合分。本 ID 为算法库模型，原型页不挂本 metricId。

第一步：四维原始值与 M_POLICY_FOCUS_INDEX 相同，词表闭集如下，不得临时扩词。长词优先、命中区间不重复计。

**依据类关键词（制定背景，扫描 content + abstract + theme）：** 
为贯彻落实、深入贯彻落实、贯彻落实、根据有关法律法规、国务院决策部署、有关规定、有关要求、根据、依据、依照、遵照、按照。

**目标类关键词（政策目标，扫描 content + keypoints）：** 
总体目标、发展目标、预期目标、主要目标、工作目标、到20XX年（正则 `到20\d{2}年`）、目标、预期、力争、确保、实现。

**对象/范围类关键词（适用范围，扫描 content）：** 
适用于、适用对象、适用范围、覆盖、面向、中小微企业、中小企业、高新技术企业、专精特新、制造业、高校、科研院所、事业单位、社会组织、创业服务机构。另加 I(support_object 非空)。不把光杆「企业」列入闭集。

**措施完备性（不用 keypoints 条目数）：** 
解析 `policy_support` JSON，摊平 `support_behavior`、`support_way`；空串不计、同词去重。原始值 = `COUNT(DISTINCT support_behavior) + COUNT(DISTINCT support_way)`。行为与方式均为空：本维记缺失。`keypoints` 语义是章节标题/原则/现状/任务/产业混合摘录，不是措施清单，不进本维。

第二步：低于阈值（待 QPOL-02）的维输出堵点；四维等权得焦点指数。

第三步：输出焦点列表、堵点清单、优化建议模板。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 | 数据质量情况 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 政策焦点识别模型 | 制定背景 | 制定依据完备性 | 从制定依据与背景说明完整程度评估政策文本是否具备充分的出台依据。 | 依据类闭集词频（为贯彻落实/深入贯彻落实/贯彻落实/根据有关法律法规/国务院决策部署/有关规定/有关要求/根据/依据/依照/遵照/按照）/ 正文字数，截面 min-max 到 0—100 | dwd_policy_base(content, abstract, theme) — 正文依据词, 摘要, 主题 | 无 | 源表 47,050 行（20260824）；content/abstract/theme 均允许空。content 空则本维缺失。theme V1 记缺失约 96%，辅助扫描几乎无效，主靠 content。 |
| 政策焦点识别模型 | 政策目标 | 目标表述清晰度 | 从目标表述是否清晰评估政策是否设定了可识别的预期结果。 | 目标类闭集词频（总体目标/发展目标/预期目标/主要目标/工作目标/到20XX年/目标/预期/力争/确保/实现）/ 正文字数，截面 min-max 到 0—100 | dwd_policy_base(content, keypoints) — 正文目标词, 要点 | 无 | content/keypoints 均允许空。keypoints 为 varchar(1000) 易截断；语义混合，不是纯目标清单，只作目标词扫描辅字段。 |
| 政策焦点识别模型 | 适用范围 | 对象范围明确度 | 从适用对象与地域范围是否写明评估政策边界清晰度。 | 对象/范围类闭集词频（适用于/适用对象/适用范围/覆盖/面向/中小微企业/中小企业/高新技术企业/专精特新/制造业/高校/科研院所/事业单位/社会组织/创业服务机构）+ I(support_object 非空)，截面 min-max 到 0—100 | dwd_policy_base(content, policy_support.support_object, province, city) — 正文范围词, 支持对象, 省, 市 | 无 | content、policy_support、province、city 均允许空。国家级省市区常空。support_object 嵌在 JSON，整段空则结构化项不得分。 |
| 政策焦点识别模型 | 措施执行情况 | 措施完备性 | 从可执行措施是否写全评估政策落地信息完整度。 | COUNT(DISTINCT support_behavior)+COUNT(DISTINCT support_way)，截面 min-max 到 0—100；behavior 与 way 均为空则本维缺失 | dwd_policy_base(policy_support.support_behavior, policy_support.support_way) — 支持行为去重数, 支持方式去重数 | 无 | policy_support 为 JSON、允许空；样例结构完整。behavior/way 均空则本维缺失。keypoints 语义非措施清单，不进本维。非空率未做全库实查。 |

## 源表字段

- dwd_policy_base(id, content, abstract, theme, keypoints, policy_support, province, city, title, keywords, status, expire_date) — 去重, 正文词频, 摘要背景, 主题背景, 要点与目标词扫描（不进措施维）, 对象与措施, 省范围, 市范围, 四字段命中, 有效, 失效
- dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name) — 产业锚点定链（仅产业锚点）

## 待建字段

- 无

## 参考资料

政策焦点指数+清华大学公共管理学院+国家自然科学基金重点项目（71233005）+黄萃, 任弢, 张剑. 政策文献量化研究：公共政策研究的新方向[J]. 公共管理学报, 2015, 12(2): 129-137.
