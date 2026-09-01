# 落地实效性（M_POLICY_IMPLEMENTATION_EFFECT）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-POLICY-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_IMPLEMENTATION_EFFECT |
| 指标名称 | 落地实效性 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 政策分析 |
| 三级模块 | 深圳政策现状分析 |
| 更新频率 | 季 |
| 对齐状态判定 | 待甲方QPOL-02；实施反馈无调查表 |
| 是否在数据库 | 否 |
| 关联Q编号 | QPOL-02 |

## 口径定义

对比城市（默认深圳，可选北京、上海、广州）政策落地实效综合评分，从落地执行启动、受益覆盖、实施反馈三维度评定，取值 0—100。分数越高表示落地执行越充分。

## 计算逻辑说明

入集：国内政策库 dwd_policy_base；status=有效且 expire_date 空或不早于统计日；按 id 去重。综合统计默认仅国内（QPOL-05），国际政策 dwd_global_policy_base 不进综合分。对比单位是城市。rank 含国家级可计入每个对比市。$N_c$=该市有效命中政策数，$N_c$=0 不输出。

第一步：三维原始值（见下表）。实施反馈无表则本维缺失。

第二步：合成：各维截面 min-max 到 [0,1]，缺维不补 0、不进平均；等权（权重待 QPOL-02）后 ×100。全样本同值取 0.5。N<3 标「样本不足」。 现行综合 = (启动得分+覆盖得分)/2×100。

第三步：需求未给维度，二级按科技部组织实施 / 范围和对象 / 效果与影响及 Sabatier 实施框架收口。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 落地实效性 | 落地执行启动 | 实施日填写率 | 从是否已填写实施日期评估政策落地是否启动，是启动率不是兑现率。 | COUNT(DISTINCT id WHERE implementation_date 非空) / $N_c$ × 100% | dwd_policy_base(id, implementation_date, status, expire_date) — 去重, 实施日, 有效, 失效 | 无 |
| 落地实效性 | 受益覆盖 | 支持对象种类数 | 从支持对象种类评估政策受益覆盖广度；无受益企业名单，不用企业数冒充覆盖。 | COUNT(DISTINCT support_object)，空值不计入 | dwd_policy_base(id, policy_support.support_object) — 去重, 支持对象 | benefit_enterprise_list-受益企业名单 |
| 落地实效性 | 实施反馈 | 实施反馈满意度 | 从实施反馈满意度评估政策落地后的对象评价；现库无调查表，本维不计算。 | 待建直读 | 无 | feedback_score-实施反馈满意度 |

## 源表字段

- dwd_policy_base(id, rank, city, implementation_date, policy_support, status, expire_date, title, keywords, keypoints, theme) — 去重, 国家级计入各市, 对比城市, 启动率, 受益对象, 有效, 失效, 四字段命中

## 待建字段

- benefit_enterprise_list-受益企业名单
- feedback_score-实施反馈满意度

## 参考资料

政策评估+中华人民共和国科学技术部+https://www.most.gov.cn/ztzl/zdzx/tztg/201612/t20161222_4804.html

落地实效性-落地执行启动、服务对象满意度|天祝藏族自治县卫生健康局.《2023年度天祝藏族自治县卫生健康局（汇总）部门决算》[EB/OL].（2024-09-26）.https://www.gstianzhu.gov.cn/art/2024/9/26/art_5585_1368776.html

落地实效性-受益覆盖|梓潼县财政局.[梓潼2024年重点绩效评价报告_梓潼县人民政府](https://www.zitong.gov.cn/ztxrmzf/c100156/202411/f54dacc6913548228b940b232dbed15d.shtml#30#5)

