# 科研关注度（M_ORG_ATTENTION_TREND）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ORG-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ORG_ATTENTION_TREND.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_ATTENTION_TREND.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_ATTENTION_TREND_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ORG_ATTENTION_TREND |
| 指标名称 | 科研关注度 |
| 所属域 | ORG（科研机构） |
| 一级模块 | 科研机构 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | ["2016", "2017", "2018", "2021", "2022", "2023"] |
| calc-logic 引用 | `metrics/calc-logic/ORG/M_ORG_ATTENTION_TREND.md` |

## 口径定义

有人会提议「用论文数代理被引」，但这两者度量的是不同东西：论文数度量产出规模，被引度量同行认可。一家机构可以年产 200 篇但篇均被引 0.3，另一家年产 20 篇但篇均被引 30，前者「关注度高」后者「影响力高」，用论文数代理会把后者彻底埋掉。本件选择**不设被引维**，把论文数明确标为「学术产出曝光量」，并在 §四 把「不能读作学术影响力」写成硬约束。这比造一个看起来很专业的代理值更负责。

## 计算逻辑说明

```text
A_i = 0.65·pct(论文 2016–2023 合计) + 0.20·pct(政策提及) + 0.15·pct(项目数)，缺维重归一
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ORG_ATTENTION_TREND.md` §二（M_ORG_ATTENTION_TREND.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_important_news_info`
- `dwd_policy_base`
- `dwd_zh_paper`
- `dwd_zh_paper_citation`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：有人会提议「用论文数代理被引」，但这两者度量的是不同东西：论文数度量产出规模，被引度量同行认可。一家机构可以年产 200 篇但篇均被引 0.3，另一家年产 20 篇但篇均被引 30，前者「关注度高」后者「影响力高」，用论文数代理会把后者彻底埋掉。本件选择**不设被引维**，把论文数明确标为「学术产出曝光量」，并在 §四 把「不能读作学术影响力」写成硬约束。这比造一个看起来很专业的代理值更负责。
- **基期声明**：作者已声明基期：used=['2016', '2017', '2018', '2021', '2022', '2023']，missing=[]。缺失年不计入分母、未按 0 摊入。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ORG_ATTENTION_TREND.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_ATTENTION_TREND.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_ATTENTION_TREND_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

