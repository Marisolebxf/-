# 招引推荐评分（M_ENT_ATTRACT_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_ATTRACT_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_ATTRACT_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_ATTRACT_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_ATTRACT_SCORE |
| 指标名称 | 招引推荐评分 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业服务／招引推荐／企业评分 |
| 更新频率 | 建议季度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 招引推荐列表、企业画像「招引价值」卡、招商线索池｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_ATTRACT_SCORE.md` |

## 口径定义

四维代理分（技术 0.4 / 广度 0.2 / 资本 0.3 / 属地 0.1）在 127,015 家候选企业上出分，比亚迪 0.855 居首，但三维是代理、风险未扣分、权重未裁定，判部分支持。

## 计算逻辑说明

```text
score = 0.40*minmax(log1p专利) + 0.20*minmax(IPC4广度) + 0.30*minmax(log1p(融资+投资边)) + 0.10*属地适配
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_ATTRACT_SCORE.md` §二（M_ENT_ATTRACT_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_financing_info`
- `dwd_org_invest_info`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：上游指数与 enterprise_score 都不存在，但招引排序要的信号在 gkx 有真实载体：专利、IPC 广度、融资事件、投资/股东边、企业城市归属，覆盖 13 万级企业。四项加权可出名单、分项分与「深圳以外候选」子表，故不判完全不支持；但三维修正为单指标代理、风险维未接入、权重未裁定，故判部分支持。
- **基期声明**：专利窗口 2021—2024（2025/2026 残年不计）；融资事件不按年切，只数条数；属地适配取当前城市。截面评分，不做年度序列。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_ATTRACT_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_ATTRACT_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_ATTRACT_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

