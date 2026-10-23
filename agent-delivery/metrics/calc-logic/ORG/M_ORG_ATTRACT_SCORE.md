# 科研机构招引推荐指数（M_ORG_ATTRACT_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ORG-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ORG_ATTRACT_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_ATTRACT_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_ATTRACT_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ORG_ATTRACT_SCORE |
| 指标名称 | 科研机构招引推荐指数 |
| 所属域 | ORG（科研机构） |
| 一级模块 | 科研机构 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | ["2016", "2017", "2018", "2021", "2022", "2023"] |
| 缺失年份 | ["2019", "2020", "2024"] |
| calc-logic 引用 | `metrics/calc-logic/ORG/M_ORG_ATTRACT_SCORE.md` |

## 口径定义

需求序号 154「科研机构引入推荐模型」在算法库 §1.1.1.1.1.1.1.6.6 里对应的产物就是「招引推荐指数」。也就是说，本件与已入库的 `M_ORG_DEEP_154_1` **同属一个需求项**，不是两个指标。二者的差别是实现分工：154 件是候选清单模型（只算 1,060 家省内非深机构、五维含学科契合 Q 与稀缺 S、输出 9 家名单），本件是全体 2,074 家的单值指数（含深圳本地机构、含动量维 R、输出 0–100 与 A/B/C）。

## 计算逻辑说明

```text
score = (0.35A + 0.35S + 0.30T + 0.15R 在缺失维重归一) × 证据覆盖折减(0.80+0.05×维数)；≥2 维出分
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ORG_ATTRACT_SCORE.md` §二（M_ORG_ATTRACT_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_industry_tags`
- `dwd_scholar`
- `dwd_zh_paper`
- `dwd_zh_paper_citation`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：需求序号 154「科研机构引入推荐模型」在算法库 §1.1.1.1.1.1.1.6.6 里对应的产物就是「招引推荐指数」。也就是说，本件与已入库的 `M_ORG_DEEP_154_1` **同属一个需求项**，不是两个指标。二者的差别是实现分工：154 件是候选清单模型（只算 1,060 家省内非深机构、五维含学科契合 Q 与稀缺 S、输出 9 家名单），本件是全体 2,074 家的单值指数（含深圳本地机构、含动量维 R、输出 0–100 与 A/B/C）。
- **基期声明**：作者已声明基期：used=['2016', '2017', '2018', '2021', '2022', '2023']，missing=['2019', '2020', '2024']。缺失年不计入分母、未按 0 摊入。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ORG_ATTRACT_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_ATTRACT_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_ATTRACT_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

