# 粤港澳大湾区技术合同成交额（M_INNOV_GBA_TECH_CONTRACT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_TECH_CONTRACT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_TECH_CONTRACT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_TECH_CONTRACT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_TECH_CONTRACT |
| 指标名称 | 粤港澳大湾区技术合同成交额 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 创新／大湾区指标 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 大湾区创新指标页「技术交易」卡片、创新要素总览的金额榜 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_GBA_TECH_CONTRACT.md` |

## 口径定义

「技术合同成交额」的分子是**经科技部门认定登记的合同金额**，这个金额只存在于登记台账；gkx 里与「合同」语义最近的四张表分别是药品许可（10 行）、专利转让（22,809 行）、期权行情（20,000 行）、招投标公告（39,962 行），**没有一张记录技术合同的对价**。没有底表、没有金额列、没有属地与年份，退到哪一级都构不成指标，按 §〇 落**完全不支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_TECH_CONTRACT.md` §二（M_INNOV_GBA_TECH_CONTRACT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_bid_base_out`
- `dwd_deal`
- `dwd_deal_bak_20260912`
- `dwd_en_report`
- `dwd_en_report_v3bad`
- `dwd_high_tech_industry_bonds`
- `dwd_market`
- `dwd_option_basic_info`
- `dwd_option_daily_quotation`
- `dwd_org_base_info`
- `dwd_org_tech_tag`
- `dwd_patent_transfer`
- `dwd_policy_base`
- `dwd_sci_tech_inno_bonds`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：需求要的是粤港澳大湾区技术合同的「成交额」（及项数），其唯一权威来源是科技部火炬中心的技术合同认定登记系统。gkx 全库表名扫描（contract/hetong/deal/trade/transfer/bargain 六个模式）只命中 dwd_deal（10 行药品许可）与 dwd_patent_transfer（22809 行专利权人变更），两者都没有价格列；含 contract/amount/price 的列扫描也没有一列是合同金额。四个候选表逐一实测：专利转让无对价、药品许可只有 10 行、期权行情是权利金、招投标是采购额且技术类标题仅 912 行。库内唯一出现「技术合同成交额」实数的地方是一份政策通知正文里的全国 2020 单年总量（549353 项 / 28251.51 亿元），无大湾区拆分、无技术领域拆分、无年度序列。既无表、又无金额字段、又无地区与年份维度，退到哪一级都构不成指标，故判完全不支持。
- **基期声明**：本件不产出任何数值，故不声明基期。反向验证中引用的全国锚点是 2020 单年（政策正文自述「截至 2020 年 12 月 31 日」），仅用于说明库内唯一实数的时间落点，不进入任何计算；也不把缺失年份摊 0。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_TECH_CONTRACT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_TECH_CONTRACT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_TECH_CONTRACT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

