# TS-L2-DS09 科技发展规划 · 演示样本循环(LOOP)计划(常规型,R2)

> 依据:`产品实现规程.md` §6.5(含 §6.5.7)。用例真源:`../合规演示用例/TS-L2-DS09-合规演示用例.md`(R2,2026-11-11:19 叶 20 行,16 可演/3 部分或条件,0 覆盖不到)。
> 验收单:`TS-DS09-DEMO-ACCEPT-LOOP`。监管人:human:王梓真(沿 DS-09 菜单负责人;R1 期监管人 human:李伟 的 blocked 判定已被 R2 解除)。
> 版本:R2(2026-11-11)。R1(2026-11-08)为阻塞型——`planning/dataset` 404;11-09 起 11 端点上线、30 表实灌,转常规 LOOP。R1 原文以 git 历史为准。

## 状态行(每轮回写)

| 轮次 | 日期 | 探测 | 对得上 | 缺口 | 子任务 | 结论 |
|---|---|---|---|---|---|---|
| R0(pre) | 2026-11-08 | `POST .../planning/dataset` → 404 | 0/19 | BLOCKED-DS09-01 | 待开发 | blocked,不进 LOOP(R1 历史行) |
| R0.5(重制) | 2026-11-11 | 9 端点匿名实测全 200 | 16 可演行填值就绪 | G1/G2/G3 | 见缺口节 | 用例 R2 落盘,具备开 LOOP 条件;验收单未建 |
| R0.7(缺口闭合) | 2026-11-13 | simulate 200 / export 401(需登录)/ 推送链路全通(registry 双执行器、调度 15+ 次 200/200、推送 16+ 行 3 用户、通知双写) | **20/20 全可演** | G1/G2/G3 全闭合(G1 系 11-12 晚间 1045 自行消解,期间累计修复均为净改进并保留) | 无 | **用例终态 R2.2:20 行全可演,0 缺口;具备建验收单条件,待监管人说「按 LOOP 跑」** |

## 1. 要证明什么

可演行的填好请求(覆盖表「按界面值填好的请求」列),返回用例写明的期望输出。通过线:探测 HTTP 200,且可演行与期望一致。对不上时按 §6.5.4 分类。

以下保持现状,不算本 LOOP 的失败,也不为此建子任务(演示话术如实声明,详见用例「保持现状不派单」节):预警 200/501 双态语义(dev 当前注册开、61 行 model_output);预警 region 仅全球;tracking 深圳档 1 城 5 点;186 三块不随区域筛选;carrier_count 与 carrier_total 双口径;local_adv 合同草稿示例抽样;人才流动 talent_fill_demo 机构级聚合;192 阈值 draft;196 派生建议与静态方案模拟;装饰按钮(查看全部/查看联动指标/图例说明/缩放控件)。

## 2. 验收单

人说「按 LOOP 跑」之后再建,本文件不建。

| 项 | 值 |
|---|---|
| ID | `TS-DS09-DEMO-ACCEPT-LOOP` |
| 类型 | `tech_task` |
| 执行 | `qa-agent` |
| 协作 | `data-agent`、`algorithm-agent`;G2/G3 类查询缺口再加 `api-agent` |
| 状态 | 建为 `ready`,不认领 |
| 报告 | `agent-delivery/agent-handoffs/科技发展态势-TS/TS-DS09-DEMO-ACCEPT-LOOP.md`(只追加) |

样本满足且状态行已回写(操作人 `human:淮政玮`)后改 `done`。

## 3. 后端调用

token 文件:`%USERPROFILE%\.gkx\display-loop-token`(一行 access_token,仓库外)。请求头 `Authorization: Bearer`、`systemCode: display`。不打印、不入档。**本模块 9 个数据端点在网关 `/v1/situation/**` 放行清单内,匿名可读;token 仅 183a 订阅写面与 183b 个人清单必需。**

| 步骤 | 调用 | 作用 |
|---|---|---|
| 探测(轮首一笔) | `GET http://10.50.69.111:30895/display/v1/situation/planning/hot-technologies?range=12m` | 200 且 items=8 即过;404=接口映射不存在,停止并通知 |
| 样本(逐可演行) | 覆盖表「接口+请求」列:hot-technologies(3m/6m/12m)、metric-system、tracking(space_mode=shenzhen/gba/global)、local-advantage、talent-flow(range 三档)、direction-warnings、key-areas(无参 + `?cluster=ai` + `?carrier_type=lab` + 组合)、research-analysis;183a/183b 带 token 调 resource-push 与 subscriptions(POST 写面在 R1 验证后即回滚为原值,不留脏订阅) | 核对期望输出(具体值见用例) |
| G3 探测(首轮) | `POST /display/v1/situation/export/jobs` body `{"format":"doc","content_keys":["planning-research-intelligence"],"filter":{"title":"<intelligence_rows 首行 title>"}}`(带 token) | 200→195 转可演;404/501→按「导出服务未就绪」记录,不回退 |
| 库(只读) | `gkxlumenx_ads`(10.50.11.76):`ts_plan_*` 30 表;`gkxlumenx`:`sys_user_subscription_rule`(scope_type=planning_resource)、`sys_user_planning_push_record` | 库侧真值核对:行数/枚举/批次与接口值对账(底稿 `TS-DS09-数据调研-20261111.md` 为基线) |

熔断:探测 401/424/「访问令牌不存在」→ blocked,通知 `human:淮政玮`(注:本模块匿名端点不受此影响,仅写面/个人块需要 token);探测 404 → 停止,通知「接口映射不存在」。库只 SELECT,不写 ODS/DWD/ADS/缺项库,不执行 `--apply`。

## 4. 缺口怎么派

只比较用例里数据情况为「可演」的行(G1 涉及的 183b 为「部分可演」,其缺口分类仍按 §6.5.4)。每轮最多三张。

| 缺口 | 类 | 派法 |
|---|---|---|
| G1 推送产物 0 行(admin 连库 1045) | DATA(链路修复) | **不建新单**——沿用 OPS-SEQ183-XXLJOB-DEPLOY-L01 链(运维定位集群密码改写后,`subscriptionPushJob` 整点自产;LOOP 复测 183b)。若该链关闭而 183b 仍 0 行,再建 `TS-DS09-PUSH-RECORD-DATA-L01`(data-agent) |
| G2 `key-areas/simulate` 404 | QUERY | 先产品/契约裁定(契约三册无此端点):补契约→api-agent 实现单;或裁定 FE 公式为 V1 终态→用例 190 改口径注记,缺口关闭。建 `TS-L2-DS09-SIM-ENDPOINT-L01` 裁定单(definition) |
| G3 export/jobs 未实测 | QUERY(探测) | 并入 LOOP R1 探测项,不单独建单;404 且 M1 §3.8 已声称上线时,升级为 `TS-DS09-EXPORT-PROBE-L01`(api-agent) |

同页同条件单飞;不签发新分析任务;不动前端;不改已写下的实测。
