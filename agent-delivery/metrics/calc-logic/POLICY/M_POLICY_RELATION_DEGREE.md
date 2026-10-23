# 政策关联度（M_POLICY_RELATION_DEGREE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_RELATION_DEGREE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_RELATION_DEGREE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_RELATION_DEGREE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_RELATION_DEGREE |
| 指标名称 | 政策关联度 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 政策图谱页「关联度」节点大小映射（设计位）、政策详情页「相关政策」排序（设计位） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_RELATION_DEGREE.md` |

## 口径定义

关联度是**一个数**，这个数由**边**决定。两类边源都核过：结构化的边表在 gkx 与 live 都没有（live 那张是造数面），文本里的引用边 `quote_policy` 真值只有 2 行、标签边 `theme` 2 行、`keywords`/`keypoints` 0 行。没有边，度数只能是 0；对 99% 以上的节点都给 0，不是「关联度低」，是「没有定义」。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_RELATION_DEGREE.md` §二（M_POLICY_RELATION_DEGREE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_policy_base`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：关联度=图谱节点加权度中心性，依赖政策实体关系图谱的四类边。gkx 280 表里没有任何边表或实体表；注册表给的临时口径（pedigree 引用 + 标签共现）同样不成立：引用字段真值 2 行、标签字段 0—2 行、pedigree 列不存在。结构与数据两端都不具备可算闭环 → 完全不支持。
- **基期声明**：截面指标：关联度按当前政策集合的图结构一次性计算，不按年出值；故无基期年。发布年只作节点属性，不进入度数的分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_RELATION_DEGREE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_RELATION_DEGREE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_RELATION_DEGREE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

