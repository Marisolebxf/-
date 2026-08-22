# 卡脖子环节数（M_CHAIN_CHOKE_LINK_COUNT）

## 基本信息

- 指标ID: M_CHAIN_CHOKE_LINK_COUNT
- 指标名称: 卡脖子环节数
- 一级模块: 产业链分析
- 二级模块: 产业诊断
- 三级模块: 瓶颈堵点识别
- 更新频率: 按需
- 对齐状态判定: 部分对齐
- 是否在数据库: 部分
- 关联Q编号: Q-CHAIN-06

## 口径定义

统计当前演示结果中标记为卡脖子的产业链环节数，与图谱节点卡脖子点位一致。

## 计算公式

COUNT WHERE chain_panorama_nodes.position/status=卡脖子 或 chain_bottleneck 判定。

## 源库表字段

gkxlumenx_ads.chain_bottleneck（8 行）；gkxlumenx_ads.chain_panorama_nodes（41 行）

## 待建表字段

卡脖子标签字段未在 panorama_nodes 中显式存在

## 参考文献 / 依据

瓶颈堵点识别；需与图谱节点卡脖子标签对齐。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
