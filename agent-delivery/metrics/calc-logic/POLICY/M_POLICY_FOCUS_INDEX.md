# 政策焦点指数（M_POLICY_FOCUS_INDEX）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-POLICY-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_FOCUS_INDEX |
| 指标名称 | 政策焦点指数 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 政策分析 |
| 三级模块 | 政策时序分析 |
| 更新频率 | 周 |
| 对齐状态判定 | 待甲方QPOL-02；四维已对extract |
| 是否在数据库 | 否 |
| 关联Q编号 | QPOL-02 |

## 口径定义

单条政策在制定背景、政策目标、适用范围、措施执行情况四维上的焦点强度综合评分，取值 0—100。分数越高表示文本焦点越清晰、可执行信息越完整。

## 计算逻辑说明

入集：国内政策库 dwd_policy_base；status=有效且 expire_date 空或不早于统计日；按 id 去重。

第一步：四维原始值（见下表）。词频维用正文 `content` 字符数作分母（空则该维缺失）；`keypoints` 按分号/换行/序号切分条目。三类关键词均为**闭集**，只计下表所列词，不得临时扩词。

**匹配规则：** 在指定字段做子串计数；**长词优先、命中区间不重复计**（例如已计「为贯彻落实」则不再计「贯彻落实」）。同一词多次出现累加。大小写与全半角不敏感；中文数字年份「到20XX年」按正则 `到20\d{2}年` 计 1 次/处。

**依据类关键词（制定背景，扫描 content + abstract + theme）：** 
为贯彻落实、深入贯彻落实、贯彻落实、根据有关法律法规、国务院决策部署、有关规定、有关要求、根据、依据、依照、遵照、按照。

**目标类关键词（政策目标，扫描 content + keypoints）：** 
总体目标、发展目标、预期目标、主要目标、工作目标、到20XX年、目标、预期、力争、确保、实现。

**对象/范围类关键词（适用范围，扫描 content）：** 
- 范围标记：适用于、适用对象、适用范围、覆盖、面向。 
- 对象类型：中小微企业、中小企业、高新技术企业、专精特新、制造业、高校、科研院所、事业单位、社会组织、创业服务机构。 
- 另加结构化字段：`policy_support.support_object` 至少 1 条非空记 1，不与词频重复归一前先相加。不把光杆「企业」列入闭集（过宽）。

**措施完备性：** 
解析 `policy_support` JSON 数组，摊平每条对象的 `support_behavior`、`support_way` 列表；空串/空数组不计；同词去重。原始值 = `COUNT(DISTINCT support_behavior) + COUNT(DISTINCT support_way)`。

第二步：合成：各维截面 min-max 到 [0,1]，缺维不补 0、不进平均；等权（权重待 QPOL-02）后 ×100。全样本同值取 0.5。N<3 标「样本不足」。

第三步：四维等权平均 ×100。与算法库模型身份 M_POLICY_DEEP_166_1 同维、同词表，本 ID 为指数产出。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 政策焦点指数 | 制定背景 | 制定依据完备性 | 从制定依据与背景说明完整程度评估政策文本是否具备充分的出台依据。 | 依据类闭集词频（为贯彻落实/深入贯彻落实/贯彻落实/根据有关法律法规/国务院决策部署/有关规定/有关要求/根据/依据/依照/遵照/按照）/ 正文字数，截面 min-max 到 0—100 | dwd_policy_base(content, abstract, theme) — 正文依据词, 摘要, 主题 | 无 |
| 政策焦点指数 | 政策目标 | 目标表述清晰度 | 从目标表述是否清晰评估政策是否设定了可识别的预期结果。 | 目标类闭集词频（总体目标/发展目标/预期目标/主要目标/工作目标/到20XX年/目标/预期/力争/确保/实现）/ 正文字数，截面 min-max 到 0—100 | dwd_policy_base(content, keypoints) — 正文目标词, 要点 | 无 |
| 政策焦点指数 | 适用范围 | 对象范围明确度 | 从适用对象与地域范围是否写明评估政策边界清晰度。 | 对象/范围类闭集词频（适用于/适用对象/适用范围/覆盖/面向/中小微企业/中小企业/高新技术企业/专精特新/制造业/高校/科研院所/事业单位/社会组织/创业服务机构）+ I(support_object 非空)，截面 min-max 到 0—100 | dwd_policy_base(content, policy_support.support_object, province, city) — 正文范围词, 支持对象, 省, 市 | 无 |
| 政策焦点指数 | 措施执行情况 | 措施完备性 | 从可执行措施是否写全评估政策落地信息完整度。 | COUNT(DISTINCT support_behavior)+COUNT(DISTINCT support_way)，截面 min-max 到 0—100；behavior 与 way 均为空则本维缺失 | dwd_policy_base(policy_support.support_behavior, policy_support.support_way) — 支持行为去重数, 支持方式去重数 | 无 |

## 源表字段

- dwd_policy_base(id, content, abstract, theme, keypoints, policy_support, province, city, title, keywords, status, expire_date) — 去重, 正文词频, 摘要背景, 主题背景, 要点与目标词扫描（不进措施维）, 对象与措施, 省范围, 市范围, 四字段命中, 有效, 失效
- dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name) — 产业锚点定链（仅产业锚点）

## 待建字段

- 无

## 参考资料

政策焦点指数+清华大学公共管理学院+国家自然科学基金重点项目（71233005）+黄萃, 任弢, 张剑. 政策文献量化研究：公共政策研究的新方向[J]. 公共管理学报, 2015, 12(2): 129-137.
