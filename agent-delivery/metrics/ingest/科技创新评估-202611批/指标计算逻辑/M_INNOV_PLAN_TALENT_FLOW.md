# 科技人才流动（产业界↔学术界）（M_INNOV_PLAN_TALENT_FLOW）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_PLAN_TALENT_FLOW |
| 指标名称 | 科技人才流动（产业界↔学术界） |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技发展规划 / 综合发展规划 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

核心技术人才在产业界与学术界之间的流动趋势与预警。对象=学者。任职性质由工作经历机构名对齐现表判定，不另建性质标识或流动方向字段。只统计学术界↔产业界的跨界变动；同界跳槽不计。按流动发生年聚合人数，近窗相对基线增速超阈预警。

## 计算逻辑说明

核心技术人才入集。按工作经历相邻任职性质变化识别流动。二维：学界→产业 / 产业→学界。近窗相对基线增速超阈预警。

### 第一步：入集

页面年窗、空间（可选）。

学者：`dwd_scholar` 按 `scholar_id` 去重。核心人才：`dwd_scholar_talent_flag.academician=1`，或 `h_index` ≥ 本批学者第 70 百分位（有效学者 < 5 时改为 `h_index≥10`）。

工作经历：`dwd_scholar_work_experience`，`status=1`；按 `scholar_id`、`start_time`、`seq_no` 排序。`start_time` / `end_time` 为 `YYYY` 或 `YYYY.MM`，取左 4 位为年。

空间：当前经历 `org_name_zh` 对齐机构名后取 `province`/`city`；无命中不剔除该学者，只缩小可落图的流动。

### 第二步：任职性质

每段经历的机构名（优先 `org_name_zh`，空则 `org_name_en`）判定产业界 / 学术界。对齐顺序：

1. 命中 `dwd_research_institute_base_info.name_cn` / `name_en`，或 `dwd_forg_university_org_info` 的 `name_std` / `name_alias`（且 `org_type` 不含「企业」）→ **学术界**。
2. 命中 `dwd_org_base_info.name_cn`：`industry` / `industry_l1_code` 含教育、高等教育、研究与试验发展 → **学术界**；其余工商主体 → **产业界**。
3. 未对齐：名称含「大学」「学院」「研究所」「研究院」「高校」→ **学术界**；含「有限公司」「股份」「集团」→ **产业界**。
4. 仍无法判定：该段经历跳过，不参与相邻比较。

不用作者-机构关系表，不另建 `org_type_flag`。

### 第三步：识别流动

同一学者相邻两段**已判定**经历，性质不同记一次跨界流动：

- 学术界 → 产业界
- 产业界 → 学术界

流动发生年 = 新经历 `start_time` 年；年无法解析则该次不计。`is_current=1` 的经历可作为新经历一端。

### 第四步：趋势与预警

按发生年计两类流动的去重学者数。近窗 \((T-2,\ldots,T)\) 相对基线 \((T-7,\ldots,T-3)\)：

$$
\mathrm{burst}=\frac{\bar{y}_{\mathrm{recent}}-\bar{y}_{\mathrm{base}}}{\max(\bar{y}_{\mathrm{base}},1)}
$$

两类分别算 burst，再取人数加权平均得总体 burst。

| 条件 | 等级 |
| --- | --- |
| 总体 burst ≥ 1 | 2 预警 |
| 总体 burst ≥ 0.5 | 1 关注 |
| 其他 | 0 无 |

输出：按年的两类流动人数、近窗 burst、`alert_level`；可选学者清单含旧/新机构名与方向。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 科技人才流动（产业界↔学术界） | 学界→产业 | 学术界转入产业界的去重学者数。 | COUNT(DISTINCT scholar_id) WHERE 旧=学术 AND 新=产业 | dwd_scholar_work_experience(scholar_id, org_name_zh, org_name_en, start_time, seq_no, is_current, status) — 工作经历；dwd_org_base_info(org_id, name_cn, industry, industry_l1_code, city, province) — 工商主体对齐；dwd_research_institute_base_info(org_id, name_cn, name_en) — 科研机构对齐；dwd_forg_university_org_info(name_std, name_alias, org_type) — 海外高校对齐 | 无 |
| 科技人才流动（产业界↔学术界） | 产业→学界 | 产业界转入学术界的去重学者数。 | COUNT(DISTINCT scholar_id) WHERE 旧=产业 AND 新=学术 | 同上工作经历与机构对齐 | 无 |
| 科技人才流动（产业界↔学术界） | 流动预警 | 近窗流动人数相对基线突增。 | burst≥1 为 2；burst≥0.5 为 1；否则 0 | 上两年序列 — 近窗相对基线 | 无 |

## 源表字段

- dwd_scholar(scholar_id, name_zh, name_en, scholar_org_name_zh, h_index, paper_nums) — 学者入集,H指数
- dwd_scholar_talent_flag(scholar_id, academician) — 院士标识
- dwd_scholar_work_experience(scholar_id, org_name_zh, org_name_en, start_time, end_time, seq_no, is_current, status) — 工作经历,任职机构,起止年
- dwd_org_base_info(org_id, name_cn, industry, industry_l1_code, city, province, reg_status) — 工商主体名称对齐,行业,空间
- dwd_research_institute_base_info(org_id, name_cn, name_en) — 科研机构名称对齐
- dwd_forg_university_org_info(name_std, name_alias, org_type) — 海外高校名称对齐

## 待建字段

- 无

## 参考资料

[1]科技人才流动｜全国人民代表大会｜全国人大代表袁玉宇｜推进跨体制人才流动融合｜2025-09-18｜http://www.npc.gov.cn/c2/c30834/202509/t20250918_448081.html.

[2]科技人才流动（产业→学界）｜人民政协网｜全国政协委员李书鹏｜为人才流动“架桥”｜2026-05-13｜http://www.rmzxw.com.cn/c/2026-05-13/3914093.shtml.

[3]科技人才流动｜山东财经大学工商管理学院｜教育部人文社会科学研究一般项目（18YJA630122）；山东省社会科学规划重点研究项目（19BJCJ132019）；山东省社会科学规划优势学科项目（19BYSJ15）｜徐茜，崔霞，罗文卿. 区域科技人才流失风险预警机制研究[J]. 经济与管理评论, 2023, 39(1): 30-41. DOI: 10.13962/j.cnki.37-1486/f.2023.01.003.
