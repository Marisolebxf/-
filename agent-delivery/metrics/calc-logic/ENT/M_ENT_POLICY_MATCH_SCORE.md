# 政策匹配度（M_ENT_POLICY_MATCH_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_POLICY_MATCH_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_POLICY_MATCH_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_POLICY_MATCH_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_POLICY_MATCH_SCORE |
| 指标名称 | 政策匹配度 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业详情页「政策适配」、招商推荐列表「可申报政策」、政策详情页「匹配企业」 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_POLICY_MATCH_SCORE.md` |

## 口径定义

公式 $Score=\sum_d W_d\cdot Norm(子项_d)$ 的三个子项各自都有承载字段，但其中两个字段整列不可用：`theme` 20,000 行里只有 2 行有值，`keywords` 与 `keypoints` 全 0，`policy_support` 20,000 行全是字符串占位符 `'null'`。三个子项因此只能退化为「政策标题里有没有这个词」的文本匹配，分数可算、可排序，但它度量的是「政策标题用词」而不是「政策内容适配」。语义维缺，故按 §〇 判**部分支持**。

## 计算逻辑说明

```text
score = 100 × (0.40·industry + 0.35·object + 0.25·way)，地域为适用性门槛
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_POLICY_MATCH_SCORE.md` §二（M_ENT_POLICY_MATCH_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_tech_tag`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：政策侧 theme/keywords/keypoints 三列不可用、policy_support 全为 JSON null 占位，三个子项只能退化为标题文本匹配；权重 Q015 未签，0.4/0.35/0.25 为本件默认值。分数可算、可排序，但不是甲方定义的政策匹配度。
- **基期声明**：截面件：政策池取 20,000 条存量全表（publish_year 1990—2025 混合），企业标签取当期快照，不按年度切分；政策维不设基期，也不得把「今年没有新政策」读成匹配度为 0。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_POLICY_MATCH_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_POLICY_MATCH_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_POLICY_MATCH_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

