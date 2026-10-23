# 政策匹配推送（M_POLICY_MATCH）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_MATCH.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_MATCH.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_MATCH_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_MATCH |
| 指标名称 | 政策匹配推送 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业详情页「政策推荐」列表、政策详情页「适合我的政策」侧栏、政策库首页「为你匹配」卡片 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_MATCH.md` |

## 口径定义

四维里产业维依赖「政策侧产业词」，而产业词的两个来源（`theme`、`keypoints`）分别只有 2 行与 0 行；诉求维依赖 `policy_support` 与企业诉求标签，前者全表 JSON null、后者库内不存在。地区维可算但主体侧恒为同一个市，有效性维因 `status` 单值而恒真。**三维能算、一维不能算，且能算的三维里两维没有方差**，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_MATCH.md` §二（M_POLICY_MATCH.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_tech_tag`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：四维里产业维依赖「政策侧产业词」，而产业词的两个来源（`theme`、`keypoints`）分别只有 2 行与 0 行；诉求维依赖 `policy_support` 与企业诉求标签，前者全表 JSON null、后者库内不存在。地区维可算但主体侧恒为同一个市，有效性维因 `status` 单值而恒真。**三维能算、一维不能算，且能算的三维里两维没有方差**，故判**部分支持**。
- **基期声明**：截面件：政策池取 20,000 条存量全表（publish_year 跨 1981—2024），企业池取当期底册。匹配是「当期政策 × 当期企业」的横截面，不设基期；不得把「某年没有新政策」读成匹配度为 0。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_MATCH.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_MATCH.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_MATCH_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

