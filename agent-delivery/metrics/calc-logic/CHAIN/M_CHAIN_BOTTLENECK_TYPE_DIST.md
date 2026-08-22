# 瓶颈类型分布（M_CHAIN_BOTTLENECK_TYPE_DIST）

## 基本信息

- 指标ID: M_CHAIN_BOTTLENECK_TYPE_DIST
- 指标名称: 瓶颈类型分布
- 一级模块: 产业链分析
- 二级模块: 产业诊断
- 三级模块: 瓶颈堵点识别
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-CHAIN-06

## 口径定义

按技术、人才、市场、资本和政策类型统计瓶颈分布。

## 计算公式

展开 chain_bottleneck.bottleneck_dims 后 GROUP BY 类型 COUNT。

## 源库表字段

gkxlumenx_ads.chain_bottleneck（8 行；bottleneck_dims）

## 待建表字段

无；bottleneck_dims 为 JSON/文本，解析规则需固化

## 参考文献 / 依据

瓶颈堵点识别；ADS 有 bottleneck_dims。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
