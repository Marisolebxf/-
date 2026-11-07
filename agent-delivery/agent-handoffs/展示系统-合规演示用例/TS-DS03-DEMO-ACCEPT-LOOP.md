ponytail: full

# TS-DS03-DEMO-ACCEPT-LOOP · DS-03 技术发展跟踪演示样本循环验收记录

> **验收单**：TS-DS03-DEMO-ACCEPT-LOOP（技术发展跟踪 / qa-agent）　|　**监管人**：human:李伟
> **依据**：`产品实现规程.md` §6.5；计划 `agent-delivery/工程过程/04-系统集成/05-展示系统集成/编排计划/TS-L2-DS03-LOOP计划.md`；用例真源 `agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/TS-L2-DS03-合规演示用例.md`
> **性质**：只读验收（GET/POST 查询体），零代码改动、零 commit/push；token 不落盘、不进本文档。

## 运行 2026-11-07 R1

- **执行**：qa-agent　|　**轮次**：R1（第一轮）
- **探测（第一笔）**：`POST http://10.50.69.111:30895/display/v1/tracking/meta`，头 `Authorization: Bearer <本机 token>`（读 `%USERPROFILE%\.gkx\display-loop-token`，len=32，内容不记录）+ `systemCode: display`，body `{}`，curl.exe `--max-time 40`。
  - 返回 **HTTP 401**：`{"code":401,"msg":"访问令牌不存在","data":"sso check-token failed","ok":false}`
  - 命中计划 §1 熔断（401/令牌失效文案）→ **停止，不进逐行对照、不建子任务**；验收单 `blocked`，note「token 失效，已通知 human:李伟」。
- **诊断补充（只读）**：同端点不带 token 复测亦 401（`Full authentication is required to access this resource`），说明网关当前为强制鉴权、且本机令牌在 SSO 查无记录；与用例文件 2026-11-07 M2/M3 实测注记「网关 StripPrefix=1，无 token」不一致——鉴权策略或令牌注册状态已变化，换发后须以新探测为准。（与同日 TS-DS01-DEMO-ACCEPT-LOOP R1 现象一致。）
- **逐行对照表（7 行可演）**：因探测熔断，7 行全部未发起请求，无接口证据，不判「对得上/对不上」，登记如下。

| 行 | 内容 | 端点 | 条件 | HTTP | 关键返回 | 判定 |
|---|---|---|---|---|---|---|
| 1 | meta/筛选维度（100 城市、26 年、15 集群枚举） | tracking/meta | body {} | 401 | 访问令牌不存在 | 未执行（探测熔断） |
| 2 | dataset 主查询（isEmpty=false、基线 20 条、currentYear=2025） | situation/tracking/dataset | — | 未发起 | 熔断（探测 401） | 未执行 |
| 3 | 年份/集群切换（timeRange 2020–2025、fieldValues CL-SEI-01） | situation/tracking/dataset | — | 未发起 | 熔断（探测 401） | 未执行 |
| 4 | Top-20 榜单（全局模型产出，有榜单数据；不随筛选变化为设计行为不判负） | situation/tracking/dataset | — | 未发起 | 熔断（探测 401） | 未执行 |
| 5 | 9 参数模板（模板可取、参数值域齐） | situation/tracking/parameter-templates | — | 未发起 | 熔断（探测 401） | 未执行 |
| 6 | 趋势/对比（26 年范围可取、返回有数） | situation/tracking/dataset | — | 未发起 | 熔断（探测 401） | 未执行 |
| 7 | 主路径端到端（开页→筛选→看榜→切年份 全链有数） | 上述串行 | — | 未发起 | 熔断（探测 401） | 未执行 |

- **覆盖不到 1 行（行 55 报告产物 items=0）**：已知不判行，本轮不涉及、不建补数单。
- **结论**：**blocked** —— 本机 `display-loop-token` 已被 SSO 判定不存在（令牌失效）。对得上 **0/7**（熔断未对照，**非样本缺口**，不做 DATA/QUERY/ALGO 分类、不建补数单）。
- **下一步建议**：监管人 human:李伟 换发新 token 写入 `%USERPROFILE%\.gkx\display-loop-token` 后触发 R2；R2 仍为只读全量 7 行对照，计划与用例不变。
