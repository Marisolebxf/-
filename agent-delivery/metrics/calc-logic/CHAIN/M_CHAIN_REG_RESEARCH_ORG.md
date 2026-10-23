# 科研机构（链维/区域维）（M_CHAIN_REG_RESEARCH_ORG）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_RESEARCH_ORG.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_RESEARCH_ORG.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_RESEARCH_ORG_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REG_RESEARCH_ORG |
| 指标名称 | 科研机构（链维/区域维） |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／区域协同／创新载体 |
| 更新频率 | 年度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 区域产业链对比页「科研机构」矩阵、深圳都市圈协同看板｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_REG_RESEARCH_ORG.md` |

## 口径定义

四市机构列合计 1,030 / 931 / 136 / 117 是真值，但 12 链 × 4 市的行内拆分只有 134 家可归属（2.4%），矩阵只能看列不能看行，判部分支持。

## 计算逻辑说明

```text
机构数 = COUNT(DISTINCT org) BY chain × city；机构桶 = 院所 ∪ 高校
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_RESEARCH_ORG.md` §二（M_CHAIN_REG_RESEARCH_ORG.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_heis_info`
- `dwd_research_institute_base_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：官方唯一桥 industry_chain_entity_rel 的 institution 行在 gkx 不存在，链维没有现成归属；但区域维所需的两张载体底册齐全（院所 2,074 + 高校 3,501，city 字段 100% 有值），四市列合计可直接数出、可对账。链维用机构名匹配环节名得到 134 家、10 链非零，只能作下限。区域完整 + 链维弱，判部分支持。
- **基期声明**：本件是截面计数（当前底册时点），不做年度序列，故无基期年份；底册不带历史版本，无法回溯往年机构数。若要做年度序列，院所侧有 incorporation_date（1,996 行），高校侧有 est_year，见 M_CHAIN_INSTITUTION_COUNT。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_RESEARCH_ORG.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_RESEARCH_ORG.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_RESEARCH_ORG_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

