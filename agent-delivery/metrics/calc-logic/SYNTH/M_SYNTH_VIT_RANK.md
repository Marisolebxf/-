# 对比范围活力排名（M_SYNTH_VIT_RANK）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_VIT_RANK.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_RANK.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_RANK_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_VIT_RANK |
| 指标名称 | 对比范围活力排名 |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2024] |
| 缺失年份 | [2021, 2022, 2023, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_VIT_RANK.md` |

## 口径定义

本指标按四维（科技/产业/人才/政策）等权合成区域创新活力指数，在声明范围内的 11 城上排名。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_VIT_RANK.md` §二（M_SYNTH_VIT_RANK.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_tech_tag`
- `dwd_patent`
- `dwd_policy_base`
- `dwd_scholar_education_background`
- `dwd_zh_paper_citation`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：RANK 公式本身完整（指数降序 + 同分并列 + 无指数不进榜），四维也都能在四市上算出真值；但对比范围是 11 城：声明范围内只有 2 城达到数据充足度门槛（11 城被排除：北京市、上海市、杭州市、南京市、武汉市、重庆市、宁波市、成都市、合肥市、东莞市、惠州市），严格『四维齐全』口径下只剩 2 城（深圳市、广州市），排名退化为一次两两比较。根因是底册 99.82% 落在大湾区四市、高企与专利申请人名称两侧都无全国样本，扩量救不了，只能引入全国企业底册与全国专利申请人主数据后重做。
- **基期声明**：指数只取 2024 一个统计年（专利完整年），不做跨年均值；其余年份未进分母——专利 2025/2026 不完整、2021—2023 未参与本指标的任何比值；政策为存量全表，不按年截断。故 used=[2024]、missing 列出的是『本指标未取用』的年，不是『库内不存在』的年。
- **复现实测耗时**：约 2.4 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_VIT_RANK.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_RANK.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_RANK_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

