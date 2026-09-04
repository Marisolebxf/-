# 产业政策匹配度（M_CHAIN_POLICY_MATCH_SCORE）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-CHAIN-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_POLICY_MATCH_SCORE |
| 指标名称 | 产业政策匹配度 |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 三级模块 | - |
| 更新频率 | 月度 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | - |

## 口径定义

指定产业链与当前政策导向的匹配程度综合评分，从政策标签匹配度、政策支持覆盖度、政策支持强度三维加权评定，取值 0—100。分数越高表示该产业链越契合政策扶持方向。对象=产业链与政策体系的匹配关系，需跨政策域数据。权重与口径待甲方确认。

## 计算逻辑说明

采用加权平均。三维：政策标签匹配度 / 政策支持覆盖度 / 政策支持强度。算法库「产业实体关系抽取」（1.1.1.1.1.1.1.2.2）与「政策实体关系抽取」（.2.6）明确需构建「产业-政策」关系，但无独立匹配度评分专叶；按政策匹配度测度惯例补齐三维，默认等权（ΣW=1）。

### 第一步：入集

- 按 `dwd_industry_chain_info.industry_code`/`industry_name` 定链。
- 有效政策取 `dwd_policy_base` 中 `status` 含「有效」的记录。

### 第二步：三个子项

1. **政策标签匹配度**：产业链名称/环节名命中政策 `title`/`keywords`/`keypoints`/`theme` 的政策数，归一。
2. **政策支持覆盖度**：政策 `policy_support` 支持对象/支持行为命中该产业链主体的覆盖程度。
3. **政策支持强度**：命中的政策按级别（`rank`：国家级/省级/市级）加权后的强度分。

### 第三步：综合评分

各子项 min-max 归一到 0—100，等权求和：
$$
产业政策匹配度 = \frac{1}{3}(标签匹配度得分 + 支持覆盖度得分 + 支持强度得分)
$$

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 产业政策匹配度 | 政策标签匹配度 | 标签命中政策数 | 产业名称/环节命中政策文本的有效政策数归一 | min-max(COUNT 有效政策 WHERE 产业名∈title/keywords/keypoints/theme) | dwd_policy_base(id, title, keywords, keypoints, theme, status) — 政策标签；dwd_industry_chain_info(industry_code, industry_name, industry_link_name) — 产业/环节标签 | 无 |
|  | 政策支持覆盖度 | 支持对象覆盖数 | 政策支持对象/行为命中该产业主体的覆盖度 | min-max(COUNT 政策 WHERE policy_support 命中产业主体) | dwd_policy_base(id, policy_support, status) — 政策支持目标；dwd_org_industry_tags(industry_code, company_name) — 产业主体 | 支持对象结构化字段 |
|  | 政策支持强度 | 级别加权强度分 | 命中政策按级别加权后的强度分 | Σ(级别权重) 归一 | dwd_policy_base(id, rank, status) — 政策级别；policy_match(subject_id, match_score) — 匹配分 | 级别权重配置 |

## 源表字段

- dwd_policy_base(id, title, keywords, keypoints, theme, policy_support, rank, status, city) — 政策文本/标签/级别
- dwd_industry_chain_info(industry_code, industry_name, industry_link_code, industry_link_name) — 产业链/环节标签
- dwd_org_industry_tags(industry_code, company_name, credit_code) — 产业主体
- policy_match(id, subject_type, subject_id, subject_name, policy_id, match_score, match_reasons) — 政策匹配结果（gkxlumenx_ads / demo_gkxlumenx_ads）
- policy_entity_relation(policy_id, entity_id, relation_type, relation_weight, confidence) — 政策-实体关系
- policy_entity(id, entity_type, entity_name) — 政策实体

## 待建字段

- 产业-政策图谱关系（`industry_chain_entity_rel` entity_type=政策）的匹配度评分字段
- `policy_match` 的 subject_type 是否覆盖「产业链」的确认（当前多为企业/用户画像）
- 匹配度权重与口径（待甲方确认）

## 参考资料

[1] 产业实体关系抽取 / 政策实体关系抽取｜科技专题服务算法库 1.1.1.1.1.1.1.2.2 / 1.1.1.1.1.1.1.2.6（产业-政策关系）。

[2] 政策匹配度测度｜国家信息中心｜产业政策匹配度评估方法（标签匹配/支持覆盖/支持强度加权）。
