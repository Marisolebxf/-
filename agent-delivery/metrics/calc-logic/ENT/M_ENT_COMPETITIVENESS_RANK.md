# 企业竞争力排名（M_ENT_COMPETITIVENESS_RANK）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_COMPETITIVENESS_RANK.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_COMPETITIVENESS_RANK.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_COMPETITIVENESS_RANK_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_COMPETITIVENESS_RANK |
| 指标名称 | 企业竞争力排名 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业服务／企业评价／竞争力排名 |
| 更新频率 | 建议年度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业竞争力榜单、企业画像「竞争力」卡、区域企业实力对比｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_COMPETITIVENESS_RANK.md` |

## 口径定义

创新 0.35 + 广度 0.20 + 资本 0.25 + 年龄 0.10 − 风险 0.10（本期按 0）在 139,189 家候选上排序，比亚迪 0.644 居首，但经营与风险两维缺失，判部分支持。

## 计算逻辑说明

```text
score = 0.35*创新 + 0.20*技术广度 + 0.25*资本活跃 + 0.10*经营年限 − 0.10*风险（风险维本期未逐企业接入，见 proxy_deviation）
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_COMPETITIVENESS_RANK.md` §二（M_ENT_COMPETITIVENESS_RANK.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_invest_info`
- `dwd_org_shareholder_info`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：enterprise_score 与 enterprise_ranking 两张结果面都不存在，但排名所需的大头可从原始表算：专利、IPC 广度、投资与股东关系、成立年限覆盖 13 万级企业，四维加权即可出完整名次与分项。缺的是经营维（营收覆盖 0.73%）与风险维（无逐企业记录），两维占旧稿权重的一部分，本件只能按 0 处理。可排名但不完整，判部分支持。
- **基期声明**：专利侧窗口 2021—2024（2025/2026 残年不计），经营年限按 2025 减成立年；营收维因覆盖 0.73% 不进入排名，故不列营收年份。本件是截面排名，不做年度序列。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_COMPETITIVENESS_RANK.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_COMPETITIVENESS_RANK.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_COMPETITIVENESS_RANK_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

