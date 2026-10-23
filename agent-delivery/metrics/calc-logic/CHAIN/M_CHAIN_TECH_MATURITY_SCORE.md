# 技术成熟度评分（M_CHAIN_TECH_MATURITY_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_TECH_MATURITY_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_TECH_MATURITY_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_TECH_MATURITY_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_TECH_MATURITY_SCORE |
| 指标名称 | 技术成熟度评分 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业链全景／技术能级 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链详情页「技术成熟度」刻度条、链间技术能级对比 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_TECH_MATURITY_SCORE.md` |

## 口径定义

指定产业链上，以链上企业专利按公开年汇总的近 3 年复合增速判定技术所处生命周期位置，输出 0—100 分；分值越高表示公开量增速越趋缓、技术越接近成熟。

> 一句话口径（源件 §0.3）：「技术成熟度」在文献里是**技术就绪度（TRL）**一类的多维评估，本库没有 TRL 字段、没有专利引证、没有权利要求数；能拿到的只有「申请年 × 申请人」的件数。本件用「件数增速趋缓 = 技术趋于成熟」这一条单因子代理，方法可执行、结果可复算，但三个前提（公开年、足够长的历史窗口、链级申请人的完整匹配）都只能降级满足，故判 **部分支持**。

## 计算逻辑说明

```text
g_t=(P_t/P_{t-k})^(1/k)-1；P 连续为 0 评 0；上期 0 且本期有量评 25；g>5% 且（加速或缺上期）评 50；g>5% 且减速评 70；|g|<=5% 评 90；g<-5% 评 90×P_t/P_{t-k} 并截断到 [0,90)
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_TECH_MATURITY_SCORE.md` §二（M_CHAIN_TECH_MATURITY_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：「技术成熟度」在文献里是**技术就绪度（TRL）**一类的多维评估，本库没有 TRL 字段、没有专利引证、没有权利要求数；能拿到的只有「申请年 × 申请人」的件数。本件用「件数增速趋缓 = 技术趋于成熟」这一条单因子代理，方法可执行、结果可复算，但三个前提（公开年、足够长的历史窗口、链级申请人的完整匹配）都只能降级满足，故判 **部分支持**。
- **基期声明**：统计年 2024，主窗口 k=3（2021→2024），上期增速用 2021→2023 的 k=2 年化值。2017—2020 在 dwd_patent 零行，未按 0 摊入任何分母或均值；2025/2026 为采集残年（2026 仅 74,810 件）且不在面板 app_year 窗口内，主动排除，不参与涨跌判定。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_TECH_MATURITY_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_TECH_MATURITY_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_TECH_MATURITY_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

