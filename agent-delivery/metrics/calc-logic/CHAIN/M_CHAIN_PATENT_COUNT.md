# 产业链关联专利数（M_CHAIN_PATENT_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_PATENT_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_PATENT_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_PATENT_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_PATENT_COUNT |
| 指标名称 | 产业链关联专利数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 链详情页「创新」卡片主数字 + 12 链对比柱 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | ["2021", "2022", "2023", "2024"] |
| 缺失年份 | ["2025", "2026"] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_PATENT_COUNT.md` |

## 口径定义

专利池 `gkx.dwd_patent` 当日 **2,939,895 件**、企业底册 189,116 家、链标签 2,283,762 行，三段数据齐备；按「企业名精确桥接第一申请人 + 链标签归属 + 申请年 ≤2024 截断」端到端跑通，12/12 链全部非零（16,300—537,046 件），合计 **3,026,291 件** → **完全转换支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_PATENT_COUNT.md` §二（M_CHAIN_PATENT_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：专利池 2,939,895 件、机构底册 189,116 家、链标签 2,283,762 行三段真实数据齐备，12/12 链全部算出非零值（16,300—537,046 件），截断与去重规则可执行、脚本可复跑；名称桥的已知漏计（非第一申请人、更名、同名）写入 gaps，属口径下界而非数据缺口。
- **基期声明**：统计期 2025 年，专利按申请年 ≤2024 截断：发明专利公开滞后 18 个月，2025—2026 年申请量不完整，纳入会系统性低估近年值；池内 2021—2026 全覆盖，2025/2026 两年仅作观察不入正式值。
- **复现实测耗时**：约 0.01 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_PATENT_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_PATENT_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_PATENT_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-24: 初版 v0.1.0（表名漂移稿）
- 2026-10-14: v0.2.0 口径重写（human:徐滕强 拍板：全量/去重/时间轴/窗口参数化/量级不进口径）
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

