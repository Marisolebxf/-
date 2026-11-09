# TOPIC-POL-REGION-DEMO-FIX-R20261107-ALGO · 区域政策对比缺信号与粤港澳归区

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 开工前已认领；本轮未再认领，registry 未另给 claim_type |
| 说明 | 任务保持 `in_progress` 期间只做判断。不改为 `done`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 没有改代码。相对指数 0 与字段选择都不该动公式或词表。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本轮只读结果板与 demo 库政策行，没有压缩上下文。 |

## 图即契约

本轮不改调用链，没有图。

## 问题清单

- 缺口键：`compare_rows` 里粤港澳（除深）的 `scores`。已签发 `POLICY-20261107-008`：`industry_vid=chain:INB1303`，五区五维，`policy_regional`。该区 `policy_count=0`，`scores=[0,0,0,0,0]`，`composite=0`。
- 要分清这组 0 是「该区没有政策，但每维都有别的区命中，所以相对指数为 0」，还是「整维无峰却写成 0」或「缺信号填了 50 / 读了 weights」。
- 另核对：有没有地区文本按 `assign_zone` 自己的规则应进粤港澳（除深），却因为 `zone_of` 用错字段没进去。

## 判断

**是相对指数 0。不改公式。**

`build_regional_board` 里，某一维 `peak==0`（五区都没命中）时该列写 `None`；有峰时本区命中次数为 0 就写 `100 * 0 / peak = 0`。综合分只对非空分做等权均值，函数不读 `weights`。创建体里的 34/33/33 没有入口。

008 五维都有别的区顶到 100，所以粤港澳五格都是相对指数 0，综合分是五格 0 的等权均值 0。深圳 `(28.6+100+0+50+75)/5=50.7`，长三角 80，京津冀 34.3，成渝 5，都是等权均值。人才政策上的 50、25 是相对该维最高的指数，不是缺信号填的 50。

用 demo 库 `chain:INB1303` 的 57 条政策在本地重跑 `build_regional_board`（不新签发、不带 force），五行与 008 逐格一致：关联 57 条，归入 38 条，未归入 19 条，粤港澳 0 条且五维为 0、综合分 0。

`POLICY-20261105-026` 的税收优惠整列已是 null、综合分不计入该列，对应的就是 `peak==0 → None` 这条分支。本轮再 GET 该任务时 `resultData` 为空，没有重解结果体；这条以任务说明和代码分支为准。

## 归区核对

`assign_zone` 先认「深圳」，再认广州/佛山等或「广东」进粤港澳（除深）。对不上的返回 `None`。`zone_of` 先读 `region`，空或字面 `NULL` 时改读 `publish_organization`。

这 57 条的 `region` 全空，实际都走发文机构。省字段单独看有 7 条是「广东省」，但市都是「深圳市」，发文机构也都含「深圳」。按函数自己的顺序，拼上市之后仍是深圳（大湾区），不是粤港澳（除深）。没有一条的省、市、区、地区或发文机构按现行词表应进粤港澳却没进去。

未归入的 19 条是福建、青海、黑龙江、山西、山东、湖南长沙、贵州、广西，以及工信部、财政部、国家知识产权局、发改委等。词表对不上，不放宽，不塞进五区。

## 修改内容

- 没有改代码。没有改前端，没有改 Java，没有新签发线上任务。

## 测试结果

- 未改代码，未跑 `tests/test_regional_board.py`。
- 本地重算（只读 demo 库，假 `load_fn` 不回库外政策）与 008 已签发分数一致，见上。

## 遗留风险

- 粤港澳（除深）在这张集成电路结果里是 0 条，矩阵显示相对指数 0。这是现行口径「该维最高=100，无命中=0」，不是缺数。
- 若以后出现「省/市写了广州或广东、发文机构却不含这些词、且 `region` 仍空」的政策，`zone_of` 仍只看发文机构，可能归不进去。本批 57 条没有这种行，所以这次不改字段选择。

## CI/CD（必填）

- 分支：`lumen-algo-py` 未改，无提交
- commit：无
- pipeline URL / ID：未跑
- 部署 namespace / 镜像 tag：无
- K8s rollout：未部署
- dev 测试 URL / 命令与结果：未发新任务。只读核对 demo 库 `policy_base_info` × `policy_industry_rel`（`industry_link_code=chain:INB1303`）并本地重算结果板。

## 可观测性（建议）

- 本轮无新请求，无新 traceId。

## 涉及文件

- 只读：`repos/lumen-algo-py/vendor/entan-py/polan/regional_board.py`
- 只读：`repos/lumen-algo-py/tests/test_regional_board.py`
- 本交接：`agent-handoffs/政策模块-E7/TOPIC-POL-REGION-DEMO-FIX-R20261107-ALGO.md`
