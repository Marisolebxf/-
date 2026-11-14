# 205 政策影响评估 · 生成逻辑（待确认）

- 日期：2026-11-14
- 状态：草稿。`human:淮政玮` 确认前不写代码、不改菜单、不改库、不改 task-registry
- 范围：只这一类。不改深度分析报告、热点识别、DS11、说明书、bugfix-runs、zmate
- 对齐：`sdd/简报/2026-11-14-POL-报告缓存架构.md`、`POL-L2-DS10-TREND-ARCH.md` §7.4、`POL-报告缓存-长任务总控.md`
- 本波相对 §7.4 的收窄：生成不从 lumen 页面发起。中台单独菜单先写 demo 库。lumen 页保持现在的同步读

## 1. 现状

`gkxlumenx_gapfill.gapfill_policy_trend_impact` 已有表，没有 `is_mock` 列，`domain_name` 没有唯一约束。列是领域名、`impact_object`（128）、`impact_direction`（64）、`conclusion`（512），外加 `metric_id` / `gap_item` / `fill_method` / `gapfill_batch_id` / `generated_at`。

库里三行，`fill_method=manual`，`gap_item=205 政策影响评估`，`metric_id` 空，结论都以「缺项演示」开头：

| 领域 | 对象 | 方向 |
|---|---|---|
| 科创发展 | 科技型企业 | 支持范围扩大 |
| 人才引进 | 科研人员 | 流入条件放宽 |
| 资金扶持 | 早期硬科技企业 | 资金来源增加 |

展示页「影响评估」只提交 `{ kind: 政策影响评估, domain }`。`PolicyPanoramaService.jobs` 见 `kind` 就走 `syncTrendKind`，委托 element `GET /trend/impact` 读上表，不建任务、不调 Python。`kind` 与 `sub_type` 同时出现时返回空 `records`。异步 `sub_type` 闭集里没有 `policy_trend_cache`。§7.4 的生成任务还没落地。

弹窗在请求返回前会先清空本地列表，再用当次读到的行填对象、方向、结论。进度是定时器，不是任务状态。`MockBadge` 常显，不读 `is_mock`。页面副标题还有「技术发展方向」，缺项表没有这一行。

Python 没有这条缓存写入。`seed_gapfill_policy_trend.py` 把演示行灌进 `gkxlumenx_gapfill`。中台 `POLICY_SUB_MENU` 没有「政策影响评估」。现有政策算法页多数走 `/policy/v1` 直达 Python，本菜单不沿用这条。

demo 侧没有 `demo_gkxlumenx_gapfill` 授权（`entan/common/db.py`：demo 的 gapfill 过渡落 ADS）。正文列是 `policy_base_info.content`（力度抽取已在用），检索列有 `title` / `abstract` / `keywords`。

## 2. 生成逻辑

只由中台这一菜单触发，一次一个领域。不从展示页按钮触发。

调用链：中台页面 → demo Java 只转发 → Python 已有 `POST /internal/policy/jobs/execute`。不新开给前端的 Python 地址。不复用 display `panorama/jobs`（那条见 `kind` 只读正式缺项表）。Java 不拼对象、方向、结论，不调模型。

1. 目标库名必须以 `demo_` 开头。`gkxlumenx_gapfill` 以及任何不带 `demo_` 的 `gkxlumenx_*` 直接拒绝，不连写。顶栏政策面为 live 时菜单按钮不可用。
2. 读该领域现有行。命中：存在 `fill_method=llm` 且结论不以「缺项演示」开头，且本次不是强制重算。命中则返回该行，不调模型。演示行、没有行、或强制重算，都算未缓存。
3. 未缓存时取材与深度报告相同：领域名当关键词，在标题、摘要、关键词里找，`content` 非空，按发布日最近 8 条。一条都没有、没有模型密钥、模型失败、或三项里有空：停。不删旧行，不插入新行，不写以「缺项演示」开头的句子。
4. 模型只产出一组：对象、方向、结论。成功后同一事务先插入新行，再删掉该领域其余行，然后提交。提交前读到的仍是旧行。提交后该领域只剩一行。
5. 新行：`gap_item` 仍是 `205 政策影响评估`，`metric_id` 仍空，`fill_method=llm`，`is_mock=1`，`gapfill_batch_id` 用新批次，不用灌数批次 `POL-L2-DS10-TREND-GAPFILL-L01`。不写热点表、深度报告表、主题表，不写文件。

## 3. 中台菜单看见什么

`demo-ui-system-test` 单独一项，标签就是「政策影响评估」。不挂在「政策 Mock」「效果评估」或深度报告下面。

- 领域单选。本波闭集是科创发展、人才引进、资金扶持。
- 主按钮「生成这一条」。已命中时主区只显示那一行，旁边另有「重新生成」。
- 结果表列：领域、对象、方向、结论、`fill_method`、生成时间。成功后只有一行。
- 进度跟任务：受理、生成中、完成、失败。不用定时器假装在读材料。
- 失败：提示原因，再读一遍表。旧行还在就继续显示旧行；本来没行就空表。不出现新的演示句。
- 政策面切到正式库：按钮禁用，文案写明不写正式库。
- 不出现热点、深度报告正文、导出 PDF / Word。

## 4. 迁 lumen 时页面怎么保持

本波 `lumen-ui-science-pc` 与 display / element 的读路径 diff 为空。展示页继续只提交 `{ kind, domain }`。`syncTrendKind` 继续同步读 `gkxlumenx_gapfill`。不要给这个按钮加 `sub_type`，否则现有代码会返回空列表。

正式库里的三句演示结论留到迁移叶。迁移只换表里的字：某个领域的新行在 demo 已成功，才在正式表用同一事务「先插入、再删该领域旧行」。没成功的领域不动。失败不删正式库旧行。

页面模板、按钮、空态、导出、弹窗里的定时进度都不改。弹窗仍会先清本地列表再填当次读到的行；因为表上不会先被删空，这次填上的要么是旧结论，要么是已经提交的新结论。对象、方向、结论仍走现有三列，`MockBadge` 仍常显。本波不给 `IMPACT_SQL` 加 `is_mock`。

## 5. 待确认

每条只选一项。第一项是推荐。

1. 中台写哪张库。
   - 推荐：`demo_gkxlumenx_ads.gapfill_policy_trend_impact`。与现有注释一致：demo 没有 gapfill 库授权，过渡表落 demo ADS。库名必须 `demo_` 开头。
   - 另一项：先授权 `demo_gkxlumenx_gapfill`，表只建在该库，不进 ADS。
2. `is_mock=1` 落在哪。现表没有这一列。
   - 推荐：只在 demo 这份表加列，成功行写 1。正式表本波不加列，Java 查询不加列。
   - 另一项：不加列。`is_mock=1` 只记在任务回执，表列与正式表逐列相同。
3. 最近 8 条怎么摘。🟡 领域名不是库里的分类列。
   - 推荐：领域名整词出现在 `title` / `abstract` / `keywords`，`content` 非空，按 `publish_date` 最近 8 条。0 条则失败不写。摘要列与深度报告用同一列 `abstract`。
   - 另一项：先做同义词（页面上科创发展的检索锚是「科创」，不是全名）再摘。本波不生成。
4. 菜单领域闭集。
   - 推荐：只有缺项表已有的三个名字。不生成「技术发展方向」。
   - 另一项：把「技术发展方向」加进闭集。该领域现在没有演示行，失败时正式页仍是空，不补演示句。
5. 模型若返回多组对象。
   - 推荐：只留第一组三项都非空的，写成该领域唯一行。
   - 另一项：不是恰好一组就失败，不写。
