# SYSINT-06-04-L01 · 市场研究金融数据同步（CDC 预填阶段）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full`（复用 gdf-cdc 解析/填充；只加金融包 09 格式解析 + UNION 作业写法；企业 v2/v4、宏观 v1 重解析与既有 inventory 一致） |

## 状态说明

**本叶未完成。** 只完成 CDC 预填草稿。GDF 导入回传与 ② ADS 仍待办；DoD「执行结果回传后 Java 只读 ADS」未满足，不是跑通。Q-SVC-006（金融要素库是否纳入交付）🟡 仍待甲方。

## 修改内容

- 产物：`agent-delivery/data/GDF/派单包/金融数据/GDF-FIN-WORKPACK-v1/预填作业/`
  - `1、贴源_预填-DRAFT.xlsx`：28 张（P0=9；wash 19 + mirror_only 9）；ENT-v4 三表不含
  - `2、明细数据_预填-DRAFT.xlsx`：11 张 `fin_*`（单源 7 + UNION ALL 4）
  - `inventory.json`、`GENERATION-REPORT.md`
- 模板来源：金融包无模板，借 `企业/GDF-ENT-WORKPACK-v1/执行结果/` 布局壳，内容全清重写。
- 脚本：`scripts/gdf-cdc/parse_workpack.py`（02 多 owner 拆分、识别 09 `目标列` 矩阵、`reg_capital_wan` SQL）、`fill.py`（UNION 写法、目标类型列）。另：HEAD 上 `parse_workpack.py` 尾部被上一提交截断（`len(wave` 处），本次提交补全。

## 待 GDF 导入核对

1. `SRC_ENT` 沿用企业数据源名；业务主题 `FIN`；作业频率/运行区间未填。
2. 单位待确认（OPEN-FIN-03）：`sub_capital` / `lp_real_capital` / `cum_inv_amount` 原样不换算。
3. 大表（sec 124 万、估值 322 万、主营三表）增量策略回签前不得宣称 CDC 闭环。
4. 类型列以 `10-DWD-MySQL-DDL/` 预建表为准（草稿未签收）。

## 架构合规自检

D1 算法仅 Python：✅ 无涉及；D12 demo/lumen 隔离：✅ 仅 `gkxlumenx_*` 占位符；D16/D18：✅ 无 gapfill/mock 表。

## cost

actual_tokens 未精确统计；预估内（< $10）。

## 遗留风险

- 未在 GDF 实际导入验证；预填表只做了与 09 的字段数、顺序、过滤、联合分支抽检（officecli 全表 outline 未跑通：本机 officecli 缺依赖，改用 openpyxl 抽检）。
