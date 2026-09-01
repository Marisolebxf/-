# 政策效果评分（M_POLICY_EFFECT_SCORE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-POLICY-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_EFFECT_SCORE |
| 指标名称 | 政策效果评分 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技政策跟踪 |
| 三级模块 | 政策分析评价 |
| 更新频率 | 季 |
| 对齐状态判定 | 待甲方QPOL-02；执行/宏观维无 ODS |
| 是否在数据库 | 否 |
| 关联Q编号 | QPOL-02 |

## 口径定义

从执行效果、社会经济效应、环境影响三维对政策实施成效综合评定的政策效果评估指数，取值 0—100。分数越高表示综合实施效果越好。

## 计算逻辑说明

入集：国内政策库 dwd_policy_base；status=有效且 expire_date 空或不早于统计日；按 id 去重。综合统计默认仅国内（QPOL-05），国际政策 dwd_global_policy_base 不进综合分。

第一步：各三级原始值（见下表）。社会经济两级无表则该维缺失，不进平均。

**环保关键词（环境影响，闭集，不得临时扩词）：**  
扫描 `title + keywords + theme + abstract + content`。子串计数；**长词优先、命中区间不重复计**。一条政策命中闭集任一词即计 1，不按词频加权。大小写与全半角不敏感。

- 导向：生态文明、生态环境保护、生态环境、环境保护、污染防治、节能减排、节能降碳、绿色低碳、绿色发展、清洁生产、循环经济、碳达峰、碳中和、双碳、低碳、环保。  
- 要素：大气污染、水污染、土壤污染、固体废物、危险废物、生物多样性、自然保护、碳排放、温室气体。  
- **不列入闭集（过宽）**：光杆「绿色」「环境」「生态」「清洁」（会误中绿色通道、发展环境、创新生态、产业生态、清洁能源口号中的光杆「清洁」）。

第二步：维内等权；三维再等权。合成：各维截面 min-max 到 [0,1]，缺维不补 0、不进平均；等权（权重待 QPOL-02）后 ×100。全样本同值取 0.5。N<3 标「样本不足」。

第三步：与算法库模型身份 M_POLICY_DEEP_168_1 同维。

| 一级指标 | 二级指标 | 三级指标 | 指标        说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 政策效果评分 | 执行效果 | 有效政策占比 | 从有效政策占比与实施及时性评估政策体系执行状态的健康程度。 | 有效政策数 / 政策总数 × 100% | dwd_policy_base(id, status) — 去重, 有效状态 | 无 |
| 政策效果评分 | 执行效果 | 政策及时性 | 从有效政策占比与实施及时性评估政策体系执行状态的健康程度。 | (统计日 − 实施日期) / (失效日期 − 实施日期) × 100%；失效日空则本级缺失 | dwd_policy_base(implementation_date, expire_date) — 实施日, 失效日 | 无 |
| 政策效果评分 | 社会经济效应 | 营业收入增长率 | 从政策关联企业营收增速与就业贡献评估社会经济效应。 | 待建直读（本期营收 − 上期营收）/ 上期营收 | 无 | operating_revenue_growth-政策关联企业营收增速 |
| 政策效果评分 | 社会经济效应 | 就业贡献率 | 从政策关联企业营收增速与就业贡献评估社会经济效应。 | 待建直读 就业人数增量 / 总就业人数 | 无 | employment_contribution-政策关联就业贡献率 |
| 政策效果评分 | 环境影响 | 绿色导向占比 | 从文本是否写明绿色/环保/低碳导向评估环境影响安排；是文本导向占比，不是实测排放或环评结论。 | I(title/keywords/theme/abstract/content 命中环保闭集任一词) 政策数 / 政策总数 × 100% | dwd_policy_base(title, keywords, theme, abstract, content) — 环保闭集检索 | 无 |

## 源表字段

- dwd_policy_base(id, status, expire_date, implementation_date, title, keywords, theme, abstract, content, keypoints) — 去重, 有效占比, 失效日及时性, 实施日及时性, 环保闭集检索, 要点不进环保维
- dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name) — 产业锚点定链（仅产业锚点）

## 待建字段

- operating_revenue_growth-政策关联企业营收增速
- employment_contribution-政策关联就业贡献率

## 参考资料

政策效果评分+上海市长宁区人民政府办公室+https://zwgk.shcn.gov.cn/xxgk/qzfwj-zfwj/2025/120/77489/4d78edd850f74679a72a397fa2e24eef.pdf

政策环境影响+生态环境部+https://www.mee.gov.cn/xxgk2018/xxgk/xxgk06/202011/t20201110_807267.html
