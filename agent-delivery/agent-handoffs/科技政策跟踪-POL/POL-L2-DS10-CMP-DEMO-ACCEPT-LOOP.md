# POL-L2-DS10-CMP-DEMO-ACCEPT-LOOP · 演示样本验收 handoff

- 流程：`agent-delivery/产品实现规程.md` §6.5
- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS10-CMP-合规演示用例.md`
- 系统：科技信息展示系统 · 科技政策跟踪 · 科创政策全景 · 政策重点比对（213–218）
- 监管人：`human:淮政玮`（口令「按 LOOP 跑」，2026-11-10 会话）
- 执行：`agent:qa-agent`（本会话代跑）
- 令牌：本机 `%USERPROFILE%\.gkx\display-loop-token`，不进 git、不打印。请求头 `Authorization: Bearer` + `systemCode: display`。
- 背景：序号 213 前端修复（`lumen-ui-science-pc` `a255d94`，初始政策值裸值渲染）已推 origin/dev，待 CI/K8s dev 部署后复验界面；本轮为数据侧 LOOP 验收。

## 运行 2026-11-10（首轮）

- 用例：覆盖表 213–218 六行全 `可演`
- 库：未读（探测未通过，没有进入样本对照，也没有 SELECT）
- 样本满足：否
- 停止：token 失效

### 探测

| 请求 | HTTP | 正文 |
|---|---|---|
| GET `/display/v1/policy/panorama/version-diff?policy_id=18363390&publish_date_a=2022-04-06&publish_date_b=2022-06-15`（兼 213 断言） | 401 | `{"code":401,"msg":"访问令牌不存在","data":"sso check-token failed","ok":false}` |

网关本体可达（返回结构化 401 JSON，非超时/DNS 失败），排除 ENV 映射不存在。本机文件当前令牌（`5af83d33…`）与 2026-11-09 第三轮会话旧令牌（`00e0ccb0…`）核对均失效。

### 缺口

无 DATA/QUERY/ALGO 缺口。本轮属 §6.5「token 失效」停止分支：不建子任务，验收单 `blocked`。已通知 `human:淮政玮` 重新登录展示系统，覆盖 `%USERPROFILE%\.gkx\display-loop-token`，再说一次「按 LOOP 跑」后开第二轮。

断言脚本已备好：本机 `%TEMP%\gkx_loop\cmp_round1.py`（不进 git），含 213 逐字摘要、214 两政策四列、215 六行部门+头条 20000、216 对象码/力度 58、217 两行四段原文全部断言；218 的 POST jobs 为写型任务（先 `intensity.run()`），验收轮默认不签发，脚本按 SKIP 处理。换 token 后直接重跑。

## 运行 2026-11-10 第二轮（令牌已换新）

- 令牌：`human:淮政玮` 当次会话换发，探测 HTTP 200。
- 库：接口只读对照（响应即库读面），未直连、未 SELECT、未写库。落盘证据 `%TEMP%\gkx_loop\cmp\`（probe_213 / detail_18363390 / detail_18407696 / stats_all / stats_bench / bench_report）。
- 样本满足：否
- 停止：继续（FAIL 全归 DATA，根因为用例期望冻结快照过期，已派重冻结单）

### 逐行结果（第二轮）

| 需规 | 请求 | HTTP | 实测 | 判定 |
|---|---|---|---|---|
| 213 | GET `/panorama/version-diff?policy_id=18363390&publish_date_a=2022-04-06&publish_date_b=2022-06-15`（兼探测） | 200 | records 3 行；新增/修改/删除三句摘要逐字一致；日期对 `2022-04-06`/`2022-06-15` | ✅ 通过（用户报障项；前端修复 a255d94 配合后界面可演） |
| 214 | GET `/panorama/18363390/detail?dimensions=申报条件,申报材料`；同 18407696 | 200 | 两政策申报时间/受理部门/申报条件/申报材料四项逐字一致 | ✅ 通过 |
| 215 | GET `/panorama/stats?kind=all` | 200 | 北京/广东四键行（件数+清单）仍在且一致；但总行数 6→14（BTN-panorama 合法扩充：北京市人民政府/深圳市南山区人民政府/深圳市福田区人民政府/苏州市人民政府等）；头条 `M_POLICY_TOTAL_COUNT` 20000→20184 | ❌ DATA（期望过期） |
| 216 | GET `/panorama/stats?kind=all&benchmark_scope=国内先进地区&benchmark_object=北京市&benchmark_object=广东省&compare_field=支持力度` | 200 | 省级对象 31 行、北京 110000/广东 440000 在列、`metric_value=58.0`、`dim_key=支持力度`、裸 `kind=all` 力度块为空——全对；仅 `stat_date` 2026-11-05→2026-11-10（mock_20260623 批次重跑） | ❌ DATA（期望过期，单字段） |
| 217 | GET `/panorama/benchmark-report?benchmark_object=北京市&benchmark_object=广东省&compare_field=支持力度` | 200 | 两行结构/对象/字段在；四段文案被 BTN-panorama 批次重写为引用具体政策文件名的新模板句（如「北京市《…新型储能…措施》的通知」），用例冻结原文不再匹配 | ❌ DATA（期望过期） |
| 218 | POST `/panorama/jobs` `policy_intensity` | 未发 | 写型任务（先 `intensity.run()`），验收轮默认不签发；表内现数用例已冻结，不重复提交 | ⏭ SKIP |

### 缺口与去重（第二轮）

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| `gapfill_policy_impl_dept` 总行数（6→14，BTN-panorama 扩充；北京/广东四键未变） | DATA | 14 行 | 用例 215 重冻结现行读面并注明查库时间 | 同根因合一张 | POL-L2-DS10-CMP-DEMO-FIX-R20261110-DATA |
| `demo_gkxlumenx_ads.policy_level_dist` 头条（20000→20184） | DATA | 20184 | 用例 215 头条重冻结 | 同上 | 同上 |
| `ads.policy_metric_timeseries.stat_date`（2026-11-05→2026-11-10，值 58 不变） | DATA | 2026-11-10 | 用例 216 重冻结 | 同上 | 同上 |
| `gapfill_policy_benchmark_report` 四段文案（BTN-panorama 重写） | DATA | 新模板句（含具体政策文件名） | 用例 217 按现行行重冻结 | 同上 | 同上 |

去重：`task-query` 无未完成的 CMP 期望刷新单；本批为合法并行灌数（`BTN-panorama`、`mock_20260623`）覆盖冻结快照，非行丢失——四键归一派一张 DATA 单，不派症状单。

脚本勘误：本轮 `cmp_round1.py` 首跑汇总 49/14 中含 2 处脚本自身 bug（217 camelCase 错拼报 got:None；「裸 kind=all 力度块」误读 bench 响应），已用 `cmp_round1b.py` 按落盘 JSON 复断言修正——真实 FAIL 即上表 12 项，213/214 判定不受影响。

### 结论（第二轮）

验收单 `POL-L2-DS10-CMP-DEMO-ACCEPT-LOOP` 回 `ready`（未收尾，不签 done）。第三轮待 `POL-L2-DS10-CMP-DEMO-FIX-R20261110-DATA` 完成并签收后重测 215/216/217（断言脚本改期望即用）。**重点：用户报障的 213 新旧对比数据侧已验证通过**，前端下拉修复（`a255d94`）部署生效后即可演示。
