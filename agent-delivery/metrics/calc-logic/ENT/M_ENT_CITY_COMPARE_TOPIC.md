# 多城市企业群对标值（M_ENT_CITY_COMPARE_TOPIC）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CITY_COMPARE_TOPIC.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CITY_COMPARE_TOPIC.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CITY_COMPARE_TOPIC_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_CITY_COMPARE_TOPIC |
| 指标名称 | 多城市企业群对标值 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 区域分析／城市对标／议题生成 |
| 更新频率 | 建议半年 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 城市对标页议题卡、区域协同看板「差距提示」｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_CITY_COMPARE_TOPIC.md` |

## 口径定义

四市对标可出（技术力、企业规模、投资活跃、链覆盖四维），但北京 163 家、上海 16 家、苏州 1 家不可比，商业力无代理、密度无面积分母，判部分支持。

## 计算逻辑说明

```text
city_value = GROUP BY city 的均值/计数；技术力=专利三维分均值；投资活跃度=关系边/千家企业
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CITY_COMPARE_TOPIC.md` §二（M_ENT_CITY_COMPARE_TOPIC.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_invest_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三类对标值里两类有代理（技术力→专利三维分均值、投资活跃度→关系边密度），企业密度只能出企业数（缺面积分母），商业力整维无源。更硬的约束是对标城市：北京 163 家、上海 16 家、苏州 0 家，需求点名的三个城市在本库不可比，对标只能落在深圳都市圈四市。两维可算、一维缺分母、一维整缺、对标集不完整，判部分支持。
- **基期声明**：本件是截面城市对标（当前底册时点），不是年度序列，故无基期年份；底册不带历史版本，无法做「某年对标」。专利侧年份窗口 2021—2024 仅影响专利计数口径，不构成城市对标的基期。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CITY_COMPARE_TOPIC.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CITY_COMPARE_TOPIC.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CITY_COMPARE_TOPIC_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

