# 推荐企业数（M_ENT_RECOMMEND_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_RECOMMEND_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_RECOMMEND_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_RECOMMEND_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_RECOMMEND_COUNT |
| 指标名称 | 推荐企业数 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 招引/培育名单规模、首页推荐卡片｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_RECOMMEND_COUNT.md` |

## 口径定义

计数链路可跑，但招引指数标度只到 0.561、阈值 70 不可达；按最大值拉到 100 才有 2 家过线，培育指数无企业分，只能给 null。

## 计算逻辑说明

```text
count(DISTINCT org_id) WHERE index >= 70；招引/培育分开，不 UNION；无分不进分子
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_RECOMMEND_COUNT.md` §二（M_ENT_RECOMMEND_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_invest_info`
- `dwd_org_shareholder_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：计数链路可跑通：95,652 个节点有度中心度，去重键 org_id 齐备，重算最大值 0.561416 与上游 0.561416 一致；但阈值 70 在原始 0—1 标度上不可达（最大 0.5614），严格计数只能得 0；按最大值拉到 0—100 才有 2 家过线，这一步是标度修复、需甲方确认；培育指数完全没有企业级分数，只能输出 null。上游只覆盖有投资/股东边的企业，未建边的企业不参与，属覆盖缺口。故判部分支持，且拒绝把 0 当业务结论。
- **基期声明**：本指标是截面阈值计数：度中心度由当前投资/股东边一次性算出，上游指数与口径均无年度键、无年份窗口，不存在年度分母；used/missing 为空表示无年度基期，不是「缺年按 0 摊入」。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_RECOMMEND_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_RECOMMEND_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_RECOMMEND_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

