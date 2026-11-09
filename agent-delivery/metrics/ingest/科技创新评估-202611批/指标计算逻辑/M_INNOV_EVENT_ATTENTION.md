# 事件关注度（M_INNOV_EVENT_ATTENTION）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_EVENT_ATTENTION |
| 指标名称 | 事件关注度 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技全域态势 / 科创事件 |
| 口径版本 | V1.3-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

科技政策事件被关注的程度。统计对象为选定范围内的政策事件（代理科技事件），从正文规模、主题覆盖、引用政策数综合，取值 0—100。

## 计算逻辑说明

第一步至合成：入集：`dwd_policy_base` 按 `id` 去重；`publish_year`/`publish_date` 落统计窗；空间用 `province/city`。子项：正文规模取 `LENGTH(content)`（空则 `LENGTH(abstract)`）；主题覆盖取 `theme` 去重主题点数；引用政策数取 `quote_policy` 去重条数。三子项本窗极值归一后等权 ×100。

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
事件关注度=\frac{norm(正文规模)+norm(主题覆盖)+norm(引用政策数)}{3}\times 100
$$

输出：按二级子项给出原始值与合成结果（评分类为 0—100；聚类/异常/预测输出标签或期次）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 事件关注度 | 正文规模 | 政策正文/摘要规模。 | LENGTH(content)；空则 LENGTH(abstract) | dwd_policy_base(id, abstract, content) — 正文规模 | 无 |
| 事件关注度 | 主题覆盖 | 主题点数量。 | COUNT(DISTINCT theme) | dwd_policy_base(id, theme) — 政策主题 | 无 |
| 事件关注度 | 引用政策数 | 引用政策条数。 | COUNT(DISTINCT quote_policy) | dwd_policy_base(id, quote_policy) — 引用政策 | 无 |

## 源表字段

- dwd_policy_base(id, title, publish_date, publish_year, province, city, abstract, content, theme, quote_policy) — 政策事件入集,统计窗,正文,主题,引用

## 待建字段

- 无

## 参考资料

[1]事件关注度｜湖北宏泰集团，中南财经政法大学统计与数学学院，杭州银行股份有限公司｜无基金项目资助｜黄骏飞，张博文，熊霖霏. 中国科技创新政策的演化与量化评价[J]. 统计与决策, 2023, 39(14): 168-173. DOI: 10.13546/j.cnki.tjyjc.2023.14.031.

[2]事件关注度｜清华大学公共管理学院｜国家自然科学基金重点项目（71233005）；国家自然科学基金面上项目（71173184）｜黄萃，任弢，张剑. 政策文献量化研究：公共政策研究的新方向[J]. 公共管理学报, 2015, 12(2): 129-137.
