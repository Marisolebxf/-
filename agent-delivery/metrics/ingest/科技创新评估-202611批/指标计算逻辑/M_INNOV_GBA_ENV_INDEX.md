# 创新环境指数（M_INNOV_GBA_ENV_INDEX）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_GBA_ENV_INDEX |
| 指标名称 | 创新环境指数 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 湾区创新监测 / 创新能力 |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

湾区各城政策与科技型市场主体构成的创新环境。统计对象为粤港澳大湾区 11 城，从政策供给、政策覆盖、高企密度综合评分，取值 0—100。分数越高，环境越好。

## 计算逻辑说明

湾区城市清单、机构入集同创新资源指数。融资事件表不用，金融环境改用高企密度代理。

### 第一步：入集

政策：`dwd_policy_base` 按 `id` 去重；`city`/`province` 命中该城；`status` 含「有效」或 `expire_date` 晚于统计年末；`publish_year` 落年窗（国家级政策 `rank` 含「国家级」且未标其他城市时，11 城共享计入）。

机构：该城存续机构集合同上。

### 第二步：三个子项

同一维在**本批 11 城**内极值归一。

1. **政策供给**：该城有效政策 `COUNT(DISTINCT id)`。
2. **政策覆盖**：该城政策 `theme` 去重主题点数。
3. **高企密度**：该城 `org_tag` 含「高新技术」的机构数 / 该城存续机构数。分母为 0 则该维缺测。

### 第三步：合成

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
创新环境指数=\frac{norm(政策供给)+norm(政策覆盖)+norm(高企密度)}{3}\times 100
$$

缺测维不补 0，剩余维权重重归一。输出：一行一城，含三子项原始值、`env_index`（0—100）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 创新环境指数 | 政策供给 | 该城有效政策件数。 | COUNT(DISTINCT id) | dwd_policy_base(id, city, province, status, expire_date, publish_year, rank) — 政策去重,湾区城市,有效,发布年,级别 | 无 |
| 创新环境指数 | 政策覆盖 | 政策主题点数。 | COUNT(DISTINCT theme) | dwd_policy_base(id, city, theme) — 政策主题 | 无 |
| 创新环境指数 | 高企密度 | 高企占存续机构比。 | 高企数 / 存续机构数 | dwd_org_tech_tag(org_id, org_tag) — 高新技术标签；dwd_org_base_info(org_id, city, province, reg_status) — 存续机构分母 | 无 |

## 源表字段

- dwd_policy_base(id, city, province, status, expire_date, publish_year, rank, theme) — 政策去重,湾区城市,有效过滤,发布年,级别,主题
- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,高企分母
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, country, city) — 港澳机构入集
- dwd_org_tech_tag(org_id, org_tag) — 高新技术等科技型标签

## 待建字段

- 无

## 参考资料

[1] 创新环境指数｜上海交通大学安泰经济与管理学院｜国家社会科学基金项目（23BJY108）｜石桂峰，李蕙均，李娜. 地方政府创新政策强度与企业创新[J]. 会计与经济研究, 2024, 38(6): 3-32. DOI: 10.16314/j.cnki.31-2074/f.2024.06.002.

[2]创新环境指数｜湖北宏泰集团，中南财经政法大学统计与数学学院，杭州银行股份有限公司｜黄骏飞，张博文，熊霖霏. 中国科技创新政策的演化与量化评价[J]. 统计与决策, 2023(14): 168-173.
