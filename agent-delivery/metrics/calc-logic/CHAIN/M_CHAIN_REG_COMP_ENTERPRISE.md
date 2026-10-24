# 竞争力-企业能力（M_CHAIN_REG_COMP_ENTERPRISE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_COMP_ENTERPRISE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_COMP_ENTERPRISE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_COMP_ENTERPRISE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REG_COMP_ENTERPRISE |
| 指标名称 | 竞争力-企业能力 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | CHAIN |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 / 产业链分析 / 区域产业竞争力评价 / 企业能力 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_REG_COMP_ENTERPRISE.md` |

## 口径定义

三个三级指标里，C（有效发明专利）用 2,939,895 件真实专利满覆盖；B（研发投入强度）只有 875 家上市主体、占 4 市链上企业 35,046 家的 2.5%；A（人均产值）只有 850 家有效配对，且 64.8% 的公司-年比值低于 1,000 元/人（量纲不一致）。有二维始终拿不到足够数据 → **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_COMP_ENTERPRISE.md` §二（M_CHAIN_REG_COMP_ENTERPRISE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_stock_finance_info`
- `dwd_patent`
- `dwd_patent_legal`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三个三级指标中 C 满覆盖（2,939,895 件专利按第一申请人现转，发明授权 kind=B 353,020 件）；B 仅覆盖 875 家上市主体（40,239 行财务），占 4 市链上企业 35,046 家的 2.5%；A 仅 850 家有营收+人数有效配对（90,926 行年报），最新年度集中在 2025 及以前（2013–2018 为主），且 64.8% 的公司-年「营收÷人数」低于 1,000 元/人（量纲不一致，疑为万元与元混用），A 在单位确认前不可用。故只能给部分支持：C 可正式出数，A/B 只能出「有样本单元」的参考值并须标注覆盖率。
- **基期声明**：由产物中实际出现的年度键反推：used=[2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]；未见其他年度，缺失年未按 0 摊入。此项为机械反推，需人工确认取数窗口。
- **复现实测耗时**：约 0.85 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_COMP_ENTERPRISE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_COMP_ENTERPRISE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_COMP_ENTERPRISE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

