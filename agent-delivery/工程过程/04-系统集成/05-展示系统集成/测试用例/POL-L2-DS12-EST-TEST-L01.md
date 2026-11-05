# POL-L2-DS12-EST-TEST-L01 · 政策效果推演 · 效果预估 · 集成测试用例

- 任务：`POL-L2-DS12-EST-TEST-L01`（WBS 行 `WBS-05-23-L2-08F`）
- 日期：2026-11-06
- 执行：`agent:qa-agent`；监管：`human:淮政玮`
- 被测链路：DS12 效果预估（SRS **232–236**）。只测效果预估，不测 237–242
- 设计真源：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS12-EST-API.md`、`sdd/l2/POL-L2-DS12-EST-DATA.md`
- 灌数脚本：`lumen-algo-py/scripts/seed_gapfill_policy_sim_forecast.py`（只覆盖 232–234）
- 强度：ponytail full
- 截图目录：`POL-L2-DS12-EST-TEST-L01/`（相对本文件）

## 0. 接口与链路总览（被测对象）

五叶共用一条同步读，一次请求只带一种类。不建任务，不进 `gkxlumen-topic-async-service`，不调 Python。

| 序号 | 公开资源 | 读法 |
|---|---|---|
| 232 未出台仿真 | `POST /display/v1/policy/simulation/jobs`，`kind=未出台仿真` | display → element → `gkxlumenx_gapfill.gapfill_policy_sim_forecast` 的未出台仿真行。四类参数至少一类才查；全空不发请求 |
| 233 新出台预测 | 同一条，`kind=新出台预测` | 同一张表按 `policy_id` 拣行。没有 `policy_id` 不发请求 |
| 234 区域空间 | 同一条，`kind=区域空间` | 同一张表。必须有 `region_name`；`policy_type` 只在选了时传。没有名为「全国」的行 |
| 235 多维评估 | 同一条，`kind=多维评估` | 只传 `kind`。读 `gapfill_policy_sim_result` 的多维评估行。本灌数脚本不写这张表 |
| 236 利益攸关方 | 同一条，`kind=利益攸关方` | 只传 `kind`。读 `gapfill_policy_sim_stakeholder` 的参与意见行。页面新提交的意见不写回。禁止文案「利益低关方」 |

空态契约（API 分册第 8 节）：无行或条件对不上则空，HTTP 成功，`records` 为空列表，不返回 501，不返回写死曲线、得分或意见。查询不灌数。不写 ODS / DWD / ADS。

---

## 1. 合规交付主路径数据准备

> 232–234 的预期行来自灌数脚本。本轮环境没有 `LUMEN_ALGO_MYSQL_PASSWORD`，**未执行 `--apply`，未连库，未把口令写入本文或 git**。235、236 不由本脚本灌入。

### DP-01 脚本校验（不连库）

| 项 | 内容 |
|---|---|
| 前置 | 仓 `repos/lumen-algo-py`，脚本 `scripts/seed_gapfill_policy_sim_forecast.py` |
| 操作 | `python scripts/seed_gapfill_policy_sim_forecast.py --check` |
| 实际 | 退出码 0。`{"mode":"check","ok":true,"db":"gkxlumenx_gapfill","rows":{"gapfill_policy_sim_forecast":6}}`。SQL 镜像 `scripts/mysql/gapfill_policy_sim_forecast.sql` 含 **6 条 INSERT**。git 对照该 SQL 与脚本无新差异。镜像中无「全国」、无「利益低关方」、无 `gkxlumenx_ods` / `gkxlumenx_dwd` / `gkxlumenx_ads` |
| `--apply` | **未执行**。本进程环境 `LUMEN_ALGO_MYSQL_PASSWORD` 未设置。不从其它文件取口令 |

### DP-02 预期行（6 行，未落库）

库 `gkxlumenx_gapfill`，表 `gapfill_policy_sim_forecast`。每种 2 行。`is_mock=1`，`metric_id=M_POLICY_SIMULATE`，`fill_method=manual`，`gapfill_batch_id=POL-L2-DS12-EST-GAPFILL-L01`，`generated_at=2026-11-06 01:00:00`。用不到的列是 NULL。

| row_kind | 行数 | 业务键 | gap_item |
|---|---|---|---|
| 未出台仿真 | 2 | 研发补助 × 广东省高新技术企业 × 按研发投入的20%补助 × 2026年至2028年；人才引进 × 深圳市重点实验室 × 每人每年30万元 × 2027年至2029年 | `232 未出台政策仿真模拟` |
| 新出台预测 | 2 | `policy_id` `18363390`（广东省科技型中小企业研发环境支持）、`18407696`（深圳市外国人来华工作许可） | `233 新出台政策效果预测` |
| 区域空间 | 2 | 广东省 × 研发补助；深圳市 × 人才引进。没有「全国」 | `234 区域经济发展空间模拟` |

### DP-03 预期核对 SQL（有口令后再执行，本轮未跑）

```sql
SELECT row_kind, COUNT(*) AS n
FROM gkxlumenx_gapfill.gapfill_policy_sim_forecast
GROUP BY row_kind;
-- 预期：未出台仿真 2、新出台预测 2、区域空间 2

SELECT COUNT(*) FROM gkxlumenx_gapfill.gapfill_policy_sim_forecast
WHERE is_mock = 1 AND metric_id = 'M_POLICY_SIMULATE' AND fill_method = 'manual';
-- 预期：6

SELECT COUNT(*) FROM gkxlumenx_gapfill.gapfill_policy_sim_forecast
WHERE region_name = '全国' OR policy_id IN ('18363390', '18407696');
-- 全国行预期 0；两条 policy_id 预期各 1，且都在新出台预测

SELECT policy_id, policy_title FROM gkxlumenx_gapfill.gapfill_policy_sim_forecast
WHERE row_kind = '新出台预测' ORDER BY policy_id;
-- 预期：18363390、18407696
```

脚本 `--apply` 会先 `DELETE FROM gapfill_policy_sim_forecast` 再插入这 6 行，可重复。只写 `gkxlumenx_gapfill`。

### DP-04 环境

| 环境 | 本轮 |
|---|---|
| 本机前端 | `lumen-ui-science-pc` 已在 `http://127.0.0.1:3000`。`.env.development` 为 `VITE_APP_USE_MOCK=false`、`VITE_ENABLE_MOCK_AUTH=true`，接口代理到 `http://127.0.0.1:7099`。截图时地址带 `review=1`，页头有「演示数据」角标 |
| 线上 | `https://edu.itic-sci.com/tid/policy/policy-effect-simulation`。登录按新人引导第 6 节，机构「某某大学」。账号口令不写入本文 |
| 库 | 未灌。见 DP-01 |

---

## 2. 关键路径验证用例

> 实际结果只记本轮看到的响应。接口没有返回「HTTP 成功且 records 为空」时，不记通过。

### TC-API-01 未出台 · 四参数全空

| 列 | 内容 |
|---|---|
| 编号 | TC-API-01 |
| 前置 | `USE_MOCK=false` |
| 步骤 | 打开效果预估，进入「未出台政策仿真模拟」，四个输入都空。再点「运行仿真模拟」 |
| 预期 | 不发 `POST /display/v1/policy/simulation/jobs`。页面文案「四类参数都空，未发起仿真」 |
| 实际结果 | **前端符合**。本机网络没有这条 POST。按钮 `disabled=true`。见 TC-02 截图。线上同一文案也曾出现，未单独留图 |

### TC-API-02 未出台 · 只填一类

| 列 | 内容 |
|---|---|
| 编号 | TC-API-02 |
| 步骤 | 只填政策类型「研发补助」 |
| 预期 | 只传已填项：`{"kind":"未出台仿真","policy_type":"研发补助"}`。对不上行则该次模拟空，HTTP 成功，records 空，不返回 501 |
| 实际结果 | **请求体符合，HTTP 成功空列表未测到**。本机发出上述 JSON，响应 HTTP **401**，`msg=访问令牌不存在`。页面显示「没有对得上的仿真行」。这是失败降级，不是 200 空列表。见 TC-03 |

### TC-API-03 新出台 · 无政策编号

| 列 | 内容 |
|---|---|
| 编号 | TC-API-03 |
| 步骤 | 进入「新出台政策效果预测」，政策编号留空 |
| 预期 | 不发请求。文案「未选择政策，不可预测效果」 |
| 实际结果 | **符合**。无 POST。见 TC-04 |

### TC-API-04 新出台 · 必须 policy_id

| 列 | 内容 |
|---|---|
| 编号 | TC-API-04 |
| 步骤 | 填 `18363390` |
| 预期 | body 只有 `kind` 与 `policy_id`。有行则带回该政策预测；无行则空，HTTP 成功，不返回 501 |
| 实际结果 | **请求体符合，成功空列表未测到**。body `{"kind":"新出台预测","policy_id":"18363390"}`。本机 HTTP **401**，`访问令牌不存在`。页面「没有该政策的预测行」。见 TC-05。库未灌，即使接口通也不应把未落库说成已读到这两行 |

### TC-API-05 区域 · 无区域名

| 列 | 内容 |
|---|---|
| 编号 | TC-API-05 |
| 步骤 | 进入「区域经济发展空间模拟」，区域留空 |
| 预期 | 不发请求。文案「未选择区域，不可模拟区域经济发展」。不补全国 |
| 实际结果 | **符合**。无 POST。政策类型占位为「选了才传政策类型」。见 TC-06 |

### TC-API-06 区域 · 只传区域名

| 列 | 内容 |
|---|---|
| 编号 | TC-API-06 |
| 步骤 | 只填区域「广东省」，政策类型留空 |
| 预期 | body 为 `{"kind":"区域空间","region_name":"广东省"}`，不含 `policy_type` |
| 实际结果 | **请求体符合，HTTP 完成态未测到**。浏览器 XHR **status 0**，无响应体。页面「没有对得上的区域行」。见 TC-07 |

### TC-API-07 区域 · 选了政策类型才传

| 列 | 内容 |
|---|---|
| 编号 | TC-API-07 |
| 步骤 | 区域「广东省」，政策类型「研发补助」 |
| 预期 | body 含 `region_name` 与 `policy_type` |
| 实际结果 | **请求体符合，HTTP 完成态未测到**。body `{"kind":"区域空间","region_name":"广东省","policy_type":"研发补助"}`。XHR **status 0**，无响应体。见 TC-08 |

### TC-API-08 多维评估 · 只传 kind

| 列 | 内容 |
|---|---|
| 编号 | TC-API-08 |
| 步骤 | 进入「多维度效果评估」 |
| 预期 | body 只有 `{"kind":"多维评估"}`。无行则雷达和柱状空，HTTP 成功，不返回 501 |
| 实际结果 | **请求体符合，成功空列表未测到**。首次进入本机 HTTP **401**，`访问令牌不存在`。再次进入 body 仍只有 `{"kind":"多维评估"}`，XHR status 0。页面「没有多维评估行」，没有用种子雷达填数。见 TC-01、TC-09 |

### TC-API-09 利益攸关方 · 只传 kind

| 列 | 内容 |
|---|---|
| 编号 | TC-API-09 |
| 步骤 | 进入「利益攸关方参与评估」 |
| 预期 | body 只有 `{"kind":"利益攸关方"}`。页面不得出现「利益低关方」 |
| 实际结果 | **请求体与用字符合，成功空列表未测到**。body `{"kind":"利益攸关方"}`。XHR status 0。页内文案是「利益攸关方」「本接口只返回参与意见」。整页文本无「利益低关方」。见 TC-10 |

### TC-API-10 页面提交的意见不写回

| 列 | 内容 |
|---|---|
| 编号 | TC-API-10 |
| 步骤 | 在利益攸关方填写意见 `QA-EST-LOCAL-OPINION`，点「提交反馈」 |
| 预期 | 意见只留在浏览器。请求不插入。不出现带这段意见正文的 jobs |
| 实际结果 | **符合**。提示「意见留在本页，未写入接口」。列表出现该条。提交后没有 jobs body 含这段文字。见 TC-11 |

### TC-API-11 线上 jobs 与未知 kind

| 列 | 内容 |
|---|---|
| 编号 | TC-API-11 |
| 步骤 | 登录后对 `POST https://edu.itic-sci.com/tid/api/display/v1/policy/simulation/jobs` 依次提交：未出台全空、未出台一项、四参数对档、新出台无编号、`18363390`、`18407696`、区域空、广东省、广东省+研发补助、对不上的类型、`region_name=全国`、多维评估、利益攸关方、`利益低关方`、未知 kind、空 body |
| 预期 | 空表或未知 kind：HTTP 成功，records 空，不返回 501。对得上的 232–234 在灌库后返回对应行 |
| 实际结果 | **未测到成功空列表**。未带登录的同一 URL 为 HTTP 401。带登录后上述 body **全部 HTTP 404**，Spring 体 `path=/v1/policy/simulation/jobs`，`error=Not Found`。响应里没有 501，也没有 records。说明网关把 `/display` 剥掉后，当前 display 进程没有这条映射。未登录打 `https://edu.itic-sci.com/api/display/v1/policy/simulation/jobs` 为 HTTP 500。本机直连 `http://127.0.0.1:7099/v1/policy/simulation/jobs`（body `{"kind":"多维评估"}`，无登录）为 HTTP **401** 未经授权，约 59 秒后返回。这条路径在本机网关存在，但仍不是 200 空列表 |

### 用例汇总

| 编号 | 一句话 | 状态 |
|---|---|---|
| TC-API-01 / 03 / 05 | 条件不齐不发请求 | 本机已测到 |
| TC-API-02 / 04 / 06 / 07 / 08 / 09 | 请求体按种类收口 | 请求体已测到；HTTP 200 空列表未测到 |
| TC-API-10 | 意见不写回 | 本机已测到 |
| TC-API-11 | 空表与未知 kind 不返回 501 | 线上 404，未测到该契约 |
| 灌库 6 行 | 未出台 2、新出台 2、区域 2 | `--check` 通过；`--apply` 未执行 |

---

## 3. 界面操作过程（lumen-ui-science-pc · 政策效果推演 · 效果预估）

前置：`VITE_APP_USE_MOCK=false`。入口：科技政策跟踪 → 政策效果推演 → 效果预估工作台。无数据时截空态，不用 fixture 填这五块。页头 86.5 / 78 / 7 / 3 是页面壳上的数字，不是这五叶 jobs 的返回，见 OBS-01。

| 步骤 | 操作 | 预期 | 实际 | 截图 |
|---|---|---|---|---|
| S1 | 打开页面 | 默认在效果预估；多维评估无行则空 | 默认「多维度效果评估」，「没有多维评估行」 | TC-01 |
| S2 | 未出台，四参数全空 | 不发请求 | 文案「四类参数都空，未发起仿真」，无 POST | TC-02 |
| S3 | 未出台只填政策类型 | 只带这一项去查；无行则空 | 发出仅含 `policy_type` 的 body；401 后显示「没有对得上的仿真行」 | TC-03 |
| S4 | 新出台不填编号 | 不发请求 | 「未选择政策，不可预测效果」 | TC-04 |
| S5 | 新出台填 `18363390` | 只带 policy_id | body 符合；401 后「没有该政策的预测行」 | TC-05 |
| S6 | 区域不填名称 | 不发请求 | 「未选择区域，不可模拟区域经济发展」 | TC-06 |
| S7 | 区域只填广东省 | 不传政策类型 | body 只有 kind 与 region_name；空态「没有对得上的区域行」 | TC-07 |
| S8 | 区域再填研发补助 | 此时才传 policy_type | body 含这两项；空态仍空 | TC-08 |
| S9 | 多维评估 | 只传 kind，无种子雷达 | 「没有多维评估行」 | TC-09 |
| S10 | 利益攸关方 | 只传 kind，用字正确 | 「本接口只返回参与意见」「未汇总各方意见」 | TC-10 |
| S11 | 提交一条意见 | 不写回接口 | 列表出现本地意见，提示未写入接口 | TC-11 |

![TC-01 打开页面](POL-L2-DS12-EST-TEST-L01/TC-01-open-page.png)

![TC-02 未出台四参数全空](POL-L2-DS12-EST-TEST-L01/TC-02-unreleased-empty.png)

![TC-03 未出台只填政策类型](POL-L2-DS12-EST-TEST-L01/TC-03-unreleased-one-param.png)

![TC-04 新出台未填政策编号](POL-L2-DS12-EST-TEST-L01/TC-04-new-empty.png)

![TC-05 新出台填写政策编号](POL-L2-DS12-EST-TEST-L01/TC-05-new-policy-id.png)

![TC-06 区域未填区域](POL-L2-DS12-EST-TEST-L01/TC-06-region-empty.png)

![TC-07 区域只填广东省](POL-L2-DS12-EST-TEST-L01/TC-07-region-name-only.png)

![TC-08 区域加上政策类型](POL-L2-DS12-EST-TEST-L01/TC-08-region-with-type.png)

![TC-09 多维评估](POL-L2-DS12-EST-TEST-L01/TC-09-multi.png)

![TC-10 利益攸关方空列表](POL-L2-DS12-EST-TEST-L01/TC-10-stakeholder-empty.png)

![TC-11 意见留在本页](POL-L2-DS12-EST-TEST-L01/TC-11-stakeholder-local-opinion.png)

---

## 4. 观察

| 编号 | 说明 |
|---|---|
| OBS-01 | `USE_MOCK=false` 时五叶结果区是空态，没有种子曲线。页头「预估综合效果 86.5」「落地成效维 78」「布局建议 7」「利益攸关反馈 3」仍显示。截图带 `review=1` 时这些卡还有「演示数据」。这四张卡不是本轮 jobs 的 records |
| OBS-02 | 本机 401 和后来未完成的 XHR，页面都落成「没有对得上的…行 / 没有多维评估行」。不能把这句文案当成接口已返回 200 空列表 |
| OBS-03 | 线上 display 当前没有 `POST /v1/policy/simulation/jobs`（404）。232–236 的成功空列表与灌库后的有行分支都还不能在这条 URL 上复测 |

## 5. 结论

- `--check` 通过，预期 6 行。`--apply` 未执行，表未由本轮写入。
- 前端在 `USE_MOCK=false` 下：四参数全空、未选政策、未选区域都不发请求；有条件时 body 按种类收口；意见提交不写回；页面无「利益低关方」。
- `POST /display/v1/policy/simulation/jobs` 的「HTTP 成功、records 空、不返回 501」本轮没有测到。线上是 404，本机是 401 或 XHR 未完成。
