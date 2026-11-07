# POL-L2-DS11-VIZ-DEMO-ACCEPT-LOOP · 演示样本验收 handoff

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS11-VIZ-合规演示用例.md`
- 系统：科技信息展示系统 · 政策分析评价 · 可视化呈现（219–222）
- 监管人：`human:淮政玮`（口令「按 LOOP 跑」，2026-11-08 会话）
- 执行：`agent:qa-agent`（本会话代跑，验收单留 `ready`）
- 令牌：本机 `%USERPROFILE%\.gkx\display-loop-token`，不进 git、不打印。请求头 `Authorization: Bearer` + `systemCode: display`。禁写 8 字符以下无意义口令，正文不出现令牌值。

## 运行 2026-11-08

- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS11-VIZ-合规演示用例.md`
- 库：只读对照未直连库，对照物为线上接口返回 + 既有 GAPFILL/TEST 记录（`gkxlumenx_gapfill`，10.50.11.76:3306，账号 `gkxlumenx`；本轮未连库，QA 已有 2026-11-04 连库核实记录沿用）。不写口令。
- 样本满足：否
- 停止：继续（有 QUERY 缺口，挂在在办单 POL-L2-DS11-BE-L01）

### 逐行结果

| 需规 | 请求 | HTTP | 结果 | 判定 |
|---|---|---|---|---|
| 219 趋势 | POST jobs `{"kind":"趋势","switch":["时间"],"metric":["科技政策连续出台数"]}` | 200 | 2021–2026 六点 48/62/75/83/79(isFluctuation=1)/91(isKeyPoint=1) | ✅ 通过 |
| 220 分区·行业 | POST jobs `{"kind":"分区","subject":"行业"}` | 200 | 10 行（电子信息3、生物医药2、高端装备2、新能源2、新材料1） | ✅ 通过 |
| 220 投向过滤 | POST jobs `{"kind":"分区","subject":"行业","allocation":"财政资金"}` | 200 | 5 行：新材料96.5、新能源104、生物医药121、高端装备118、电子信息132.5，与 TEST-L01 DP-02 SQL3 逐行一致 | ✅ 通过 |
| 222 模板选用 | GET shells?kind=模板选用&template=区域政策效果季度对比 | 200 | `records: []` 空列表。库内有 10 行（TC-03a 已判红，GAP-01） | ❌ 不通过（GAP-01） |
| 221 多维结构关联图 | 设计无资源，不请求 | — | — | 不判 |

探测即 219 请求（计划第 3 节），HTTP 200，非 401/424/404。首笔 `curl -d` 内联中文曾返回 400（Windows 控制台 GBK 编码所致，网关与令牌均正常）；改 UTF-8 文件体后 200，属本机工具链问题，非接口缺口。

### 缺口

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| `gapfill_policy_eval_template.kind=模板选用` shells 过滤 | QUERY | 返回空列表；库内 10 行（6 模板）2026-11-04 已连库核实 | 模板「区域政策效果季度对比」2 行：季度/地区/柱状、季度/地区/热力 | 修 shells 端点模板选用分支的列名/过滤（同 READ BUG-01 同根因：旧列名拣不中） | POL-L2-DS11-BE-L01（in_progress，DoD 已含 shells 读面） |

去重：`task-query` POL 模块无未完成的 DS11-VIZ QUERY 修复单；`POL-L2-DS11-BE-L01` DoD 覆盖「趋势段与分区段同步读缺项表」与 shells 读面，本轮缺口整单挂靠，不新建。

### 结论

可演行 4 笔请求：3 笔通过、1 笔 GAP-01 缺口（QUERY，挂 `POL-L2-DS11-BE-L01`）。样本未满足，验收单留 `ready`。下一轮待该单签收后重测 222。

## 运行 2026-11-08（第二轮 · 修复后复测）

- 修复单：`POL-L2-DS11-BE-L01`，commit `0a6b0d9`（element 新增 /evaluation/template + display kind=模板选用 路由）与 `e0ede48`（shells 绑定 template 参数）已 push，`0a6b0d9` 已部署，`e0ede48` CI 部署中。
- 样本满足：待 `e0ede48` 部署后终测 222

### 逐行结果

| 需规 | 请求 | HTTP | 结果 | 判定 |
|---|---|---|---|---|
| 219 趋势 | POST jobs `kind=趋势` | 200 | 首轮已过（6 点），本轮未回归 | ✅ 通过 |
| 220 分区 | POST jobs `kind=分区` | 200 | 首轮已过（10 行 + 财政资金过滤 5 行），本轮未回归 | ✅ 通过 |
| 221 多维结构关联图 | 设计无资源，不请求 | — | — | 不判 |
| 222 模板选用 | GET evaluation/shells `kind=模板选用&template=区域政策效果季度对比` | 200 | element 侧已验证返回 2 行（季度/地区/柱状、季度/地区/热力）；display 参数绑定修复 `e0ede48` 部署后终测 | ⏳ 待终测 |

### 结论

VIZ 三笔已过、222 待 `e0ede48` 部署完成后终测。element 侧读面证据：集群内直测 `gkxlumen-platform-element:7082/v1/element/policy/evaluation/template` 返回模板 2 行。
