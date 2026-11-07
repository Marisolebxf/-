# TOPIC-POL-REGION-DEMO-ACCEPT-LOOP · 区域政策对比演示实例反复验收

## 任务

| 字段 | 值 |
|---|---|
| claimed_by | （未认领） |
| supervised_by | `human:淮政玮` |
| 状态 | `ready` |
| 说明 | 2026-11-07 第一轮。集成电路五区五维读已签发结果，可演字段对上。不签完成。 |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `N/A` |
| 说明 | 本轮只读接口，没有改业务代码，没有连库。 |

## 图

本轮不改调用链，没有图。

## 运行 2026-11-07

- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/区域政策对比-合规演示用例.md`
- 库：结果不是全空，本轮没有连 `demo_gkxlumenx_dwd.policy_base_info`
- 样本满足：是
- 停止：通过
- 探测：`POST http://10.50.69.111:30892/api/topicAsync/topic/v1/analysis/tasks/list`，body `user_id=guest`、`analysisType=policy_regional`、`status=success`、`page=1`、`size=5`。HTTP 200，`code=0`。当时本机还没有 token 文件，第一次没有带 Bearer。返回不是 401、424、404，正文也不是令牌不存在或过期，所以没有把验收单改成阻塞
- 补探：token 已写入 `%USERPROFILE%\.gkx\topic-loop-token`（仓库外，不入库）。带 `Authorization: Bearer` 和 `systemCode: topic` 再打列表和 `POLICY-20261107-008` 结果，都是 HTTP 200、`code=0`。列表仍是 008、007、006、005、026。没有令牌失效文案。结论不变
- 样本：列表共 26 条成功任务。最新一条对得上集成电路五区五维的是 `POLICY-20261107-008`（`industry_vid=chain:INB1303`，五区，五维，`scope_kind=industry`）。同页 005、006、007 与 008 创建体相同。验收只读 008 的 `GET .../tasks/POLICY-20261107-008/result?user_id=guest`，HTTP 200，`code=0`，状态 `success`。没有新签发，没有 `force=true`
- 技术领域：同页还有 `POLICY-20261105-026`（`industry_codes=INB2505`，`industry_name=合成生物`，无 `industry_vid`）。只读了这一条，用来核覆盖表第二行，没有把它当成集成电路的结果
- 008 综合分按五维里的非空分等权。深圳 `(28.6+100+0+50+75)/5=50.7`。没有改去读创建体里的 `weights`（34/33/33）。008 五维都有区域命中，所以没有出现「整列应为 null」的列。026 的税收优惠整列是 null，综合分没有把这列算进去，也没有填 50
- 补贴标准、准入条件仍按覆盖表 `覆盖不到`。008 里多数抽取为空，不派补数

### 可演行

| 行 | 结论 |
|---|---|
| 序号 112 · 指定产业 | 008 类型 `policy_regional`，创建体为集成电路 `chain:INB1303`、五区、五维 |
| 序号 112 · 指定技术领域 | 026 按关联产业取政策，结果里没有「技术锚点不可算」。条数不跟 008 对死 |
| 序号 112 · 长三角与粤港澳 | 008 的 `compare_rows.region` 含深圳（大湾区）、长三角、粤港澳（除深）。`summary` 含「关联政策」和「归入对比区域」。不核 57 与 38 |
| 序号 113 · 对比矩阵 | `dims` 为五维。五行区名与请求一致。`headline.region_count` 为 5。缺信号没有写成 0 或 50 |
| 序号 113 · 雷达图与热力图 | 008 有非空 `scores`，图用 `compare_rows` 和 `dims`。未开页面 |
| 序号 113 · 差异与竞争优势 | 有「计分口径」，`pending_ref` 为 `QPOL-02`。五个维都有「领先」。有「深圳与长三角」 |
| 序号 112 · 政策条款列 | 008 里有政策的四区都在 `extracts`。粤港澳（除深）0 条，没有抽取行。`clause` 允许为空 |

### 缺口

无。不建子任务。

## 签收 2026-11-07

计划状态行已回写。可演行已对上。数据单、算法单已签收。验收单改为 `done`。
