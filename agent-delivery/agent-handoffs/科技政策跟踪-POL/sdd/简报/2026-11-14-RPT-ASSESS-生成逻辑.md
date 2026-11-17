# 政策效果评估报告（需规 seq 211）· 生成逻辑草稿

- 日期：2026-11-14
- 状态：待 `human:淮政玮` 确认。确认前不写代码、不改菜单、不改表、不改接口、不改 task-registry
- 相对 `2026-11-14-POL-报告缓存架构.md`：该文第 2 节把 211 写成「下一刀、本刀不改表不改接口」。本次只把生成逻辑写成可确认的草稿；未确认前那一句仍然有效
- 需规（`科创政策全景.md` seq 211）：基于政策实施数据和受众反馈，自动生成报告，内容含政策达成度、社会影响、存在问题、改进建议，用户可查看和下载

已拍板、本稿遵守：这是正文缓存，不是图表。不改 lumen 现有页面展现。旧内容在新正文写成功前仍在，失败不删旧行。中台 `demo-ui-system-test` 单独一个菜单「效果评估报告」。本波只写 demo 库，不写 `gkxlumenx`。Java 不写正文、不调模型。前端不直连 Python。`is_mock=1`。

## 1. 现状

展示读面已经有，生成没有。

| 位置 | 事实 |
|---|---|
| 表 | `gkxlumenx_gapfill.gapfill_policy_assessment_report`。DDL 在 `lumen-algo-py/scripts/mysql/gapfill_policy_assessment.sql`。Java `PolicyGapfillController.REPORT_SQL` 选的列与 DDL 一致 |
| 列 | `id`，`scope_text`，`achievement_text`，`social_impact`，`problem_text`，`suggestion_text`，`report_body`，`is_mock`，`metric_id`，`gap_item`，`fill_method`，`gapfill_batch_id`，`generated_at`。没有 `policy_id`，没有评分列，没有 `fill_model` |
| 已灌行 | 灌数单 `POL-L2-DS10-SENT-MOCK-211` 于 2026-11-03 写入 2 行，`fill_method=manual`，`gap_item='211 政策效果评估报告'`，`metric_id` 空，`is_mock=1`，正文以「缺项演示」开头。本稿没有重查线上行数 |
| 读接口 | `GET /display/v1/policy/panorama/assessment-report`。display 委托 element 只读上表，`ORDER BY generated_at DESC, id DESC`。无行则 `records` 空。查询不插入 |
| 生成 | `lumen-algo-py` 里没有 211 的生成任务。全景 jobs 现有 `sub_type` 不含评估报告。`demo-ui-system-test` 里没有「效果评估报告」菜单 |
| 页面 | `lumen-ui-science-pc` 的 `SentimentTab.vue`：`USE_MOCK=false` 时列表显示 `scope_text`、`generated_at`，查看把达成度与社会影响拼成结论，问题与建议按换行或 `；` 拆开，`report_body` 作报告正文。下载走 `situation/report`，`reportType=policy-assessment-report`。不造分 |

可作取材、但现在不参与 211 生成的表：

| 表 | 库（代码默认） | 能用的列 | 对不上的地方 |
|---|---|---|---|
| `policy_base_info` | `polan.common.db` 的 `conn.dwd`，默认 `demo_gkxlumenx_dwd` | `policy_id`，`title`，`abstract`，`content`，`keywords` | 评估报告行上没有 `policy_id`，不能按键关联 |
| `gapfill_policy_audience_feedback` | 只见到 `gkxlumenx_gapfill` | `subject_name`，`channel`，`opinion_text`，`score`，`policy_id`，`feedback_at` | 种子行的 `policy_id` 是 `GF-POL-SENT-210-*`，不是 `policy_base_info.policy_id` |
| `policy_effect` | `conn.ads`，默认 `demo_gkxlumenx_ads`；`scope_type='region_effect'` | `scope_name`，`impl_effect`，`ext` | 一行是一个区域的落地实效，数据分册写明这不是 211 的报告。`effect_score` 属于 `M_POLICY_EFFECT_SCORE`，不写入本报告 |

`demo_gkxlumenx_gapfill` 这个库名在别的域出现过。政策这条链路的说明是：应用账号没有该库授权，政策缺项表现在写在 `gkxlumenx_gapfill`。本稿没有找到政策 211 已经在用的另一张 demo 评估报告表。

## 2. 生成逻辑

一行仍是一份报告。不新建表，不加列，不写文件进表，不写 `gkxlumenx_gapfill`。

1. 中台选中一条已有报告（按 `id`）。`scope_text` 当作这份报告的身份，生成时不改它。
2. 该行已经是 `fill_method=llm`，且五段正文都不是「缺项演示」开头：只显示，不生成。现在的 2 行手工演示句算未缓存。
3. 点「生成」或「重新生成」（`force=true`）后，Java 只受理任务并转给 Python。Java 不拼正文、不调模型。
4. Python 取材（推荐组合，见第 5 节）：用 `scope_text` 里的政策名在 `demo_gkxlumenx_dwd.policy_base_info` 的标题、摘要、关键词里取最近 8 条且 `content` 非空的政策；再在受众反馈里用同一段政策名对 `opinion_text` 做包含匹配，取最近 8 条。对不上就不编。不按 `policy_id` 关联，因为两边键不一致。不读 `policy_effect.effect_score`，不把区域分写进报告。
5. 一条政策正文都摘不到，或没有模型密钥，或模型失败、或五段里有空：不 UPDATE、不 DELETE、不 INSERT 演示句。旧行原样留下，任务记失败。
6. 模型只输出 JSON，键固定为 `achievement_text`、`social_impact`、`problem_text`、`suggestion_text`、`report_body`。五段都非空才算成功。问题和建议在各自字符串里用 `；` 分开，方便现有页面拆行。达成度是一段文字，不是分数，不新造指标。
7. 成功后只 UPDATE 这一行的五个正文列，外加 `fill_method='llm'`、`is_mock=1`、`metric_id` 仍空、`gap_item` 仍为 `211 政策效果评估报告`、`gapfill_batch_id` 改为当次批次、`generated_at` 改为写入时间。一次语句写完。不先删后插。表上没有 `fill_model`，模型名不入行。
8. 本波写入库不选 `gkxlumenx_gapfill`（展示正在读它）。推荐库见第 5 节第 1 项。

## 3. 中台菜单看见什么

`demo-ui-system-test` 单独一个菜单，标题「效果评估报告」。不挂到深度报告、对标报告或研报。

- 列表：评估范围（`scope_text`）、生成时间、来源（手工演示 / 已生成）。点一行看到达成度、社会影响、问题、建议、正文。不显示分数，不显示图。
- 按钮：「生成」「重新生成」。进行中只显示任务状态（已受理、生成中、完成、失败）。
- 成功：同一行五段换成新正文，列表仍是这一条。
- 失败：原五段还在，旁边一句失败原因。不出现新的演示句。
- 每条标明 mock。菜单不提供「写入 lumen 库」。

## 4. 迁 lumen 时页面怎么保持

迁的时候只把已经写成功的行复制进 `gkxlumenx_gapfill.gapfill_policy_assessment_report`，列名不变。展示继续 `GET /display/v1/policy/panorama/assessment-report`。

`SentimentTab.vue` 的列表、弹窗和下载字段映射不动：范围、达成度、社会影响、问题、建议、正文、生成时间。不增加维度得分，不改 `situation/report` 的导出壳。复制完成前，页面仍显示库里原来的手工行。本波不在打开页面时自动生成。

## 5. 待确认

1. **写入哪张 demo 表（推荐）**：在 `demo_gkxlumenx_ads` 建同名表 `gapfill_policy_assessment_report`，列与第 1 节相同，只给中台读写。展示的 `{gapfill}` 默认仍是 `gkxlumenx_gapfill`，所以 lumen 页面看不到这批新行。不选 `demo_gkxlumenx_gapfill`：政策账号没有该库授权的记录还在。不选直接写 `gkxlumenx_gapfill`：那会在确认迁之前换掉展示正在读的两行。
2. **粒度（推荐）**：只重写选中的那一行，`scope_text` 不动。备选：成功后插入新行再删旧行。备选会在失败窗口里出现两行，与「失败不删旧行、旧内容一直在」更难对齐，不推荐。
3. **取材（推荐）**：政策正文用 `demo_gkxlumenx_dwd.policy_base_info`；受众意见用 `gkxlumenx_gapfill.gapfill_policy_audience_feedback` 的 `opinion_text`，只读、按政策名包含匹配。实施数据若对不上区域名就不摘。备选：再把 `demo_gkxlumenx_ads.policy_effect` 里名称能对上的 `scope_name` 与 `impl_effect` 写进提示词，仍不写 `effect_score`。
4. **未缓存判定（推荐）**：`fill_method=manual` 或正文以「缺项演示」开头视为未缓存；成功改为 `fill_method=llm`。不新增 `fill_model` 列。这与数据分册「211 的 `fill_method` 固定 manual」不一致，确认后才改那句。
5. **谁触发（推荐）**：本波只有中台按钮。展示页不发起任务。迁 lumen 时若要「打开未缓存才生成」，另确认，不放进本波。
