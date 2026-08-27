# 领域覆盖深度（M_ENT_DOMAIN_COVERAGE_DEPTH）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_DOMAIN_COVERAGE_DEPTH |
| 指标名称 | 领域覆盖深度 |
| 一级模块 | 企业分析 |
| 二级模块 | 重点企业领域分布分析 |
| 三级模块 | 领域分布分析 |
| 更新频率 | 产业标签更新后 |
| 对齐状态判定 | 未对齐 |
| 是否在数据库 | 是 |
| 关联Q编号 | Q013 |


## 口径定义

企业在目标产业链图谱中**所覆盖节点的最大层级深度**，反映企业向产业链纵深环节的渗透程度。

产业链图谱为树形结构（`dwd_industry_chain_info` 中 `level` 字段表示层级，`parent_code` 表示父子关系），层级越大表示越靠近产业链下游/末端环节。覆盖深度取企业集合命中的所有节点中的最大 `level` 值，并除以该产业链的最大层级做归一化，结果为 0~1。

## 计算逻辑说明

企业集合命中的节点j在产业链图谱中的层级/该产业链（industrycode）下所有节点的最大层级

## 源表字段

gkx.dwd_org_industry_tags（credit_code, industry_link_code, industry_code）gkx.dwd_industry_chain_info（industry_code, industry_link_code, level）
