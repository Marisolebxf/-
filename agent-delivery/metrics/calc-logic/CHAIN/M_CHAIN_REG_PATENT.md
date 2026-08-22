# 专利（M_CHAIN_REG_PATENT）

## 基本信息

- 指标ID: M_CHAIN_REG_PATENT
- 指标名称: 专利
- 一级模块: 产业链分析
- 二级模块: 区域产业分析
- 三级模块: 区域产业指数评价
- 更新频率: 季度
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-CHAIN-07

## 口径定义

专利产出与布局强度。

## 计算公式

COUNT(专利) 后标准化。

## 源库表字段

gkxlumenx_dwd.enterprise_chain_patent（0 行）；gkxlumenx_ods.dwd_org_industry_chain_pat_dtl（888 行）

## 待建表字段

企业/机构关联键缺失，专利无法按主体关联

## 参考文献 / 依据

区域产业指数预设指标，原型归属技术力。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
