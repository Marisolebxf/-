# 政策效果预估 · LOOP 执行编排计划

- 状态：EQ 修复单已上线（2026-11-08，Java 过滤 + 库列 + 单测，CI 4286 全绿；handoff `POL-L2-DS12-INDUSTRY-EQ-FIX-L01.md`）。线上 HTTP 复核被 401 挡（token 过期，ENV）：待 human:淮政玮 换 token 后按 §3 从探测重入。前端半场（级联提交 target_industry）在工作区另一会话，未提交。上一轮（2026-11-08）8/8 PASS 见 handoff。
- 流程：`agent-delivery/产品实现规程.md` §6.5（用例 §6.4，SDD §4.1）
- 系统：科技信息展示系统。不打开页面。
- 监管人：`human:淮政玮`
- 日期：2026-11-07

## 1. 这一轮要证明什么

合规演示用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS12-EST-合规演示用例.md`。每条需规一行。

样本仍以 `测试用例/POL-L2-DS12-EST-TEST-L01.md` 第 1.1、1.2 节为准。经线上接口返回，并与右列一致。不另编期望。

通过线：

- 探测 HTTP 200。
- 未出台五类等值能拣到对应行。`target_industry` 用级联回显全文。没提交的项不加谓词。
- 新出台按 `policy_id`，区域按 `region_name`，多维评估和利益攸关方只传 `kind`。
- 对不上时接口仍是 HTTP 成功且 `records` 为空，不返回 501。这只说明过滤诚实，不算样本通过。
- 用例里已写下的 401、404 实测不改写。`POL-L2-DS12-EST-TEST-L01` 不标完成。

不纳入：237–242、区域空间的目标产业、页面文案、前端改动。

## 2. 验收单

沿用已有 `POL-L2-DS12-EST-ACCEPT-LOOP`（2026-11-07 起 `blocked`，`qa-agent`）。不另开第二张验收单，不把这张单签 `done`。映射恢复后，人说「按 LOOP 跑」再从 `blocked` 继续。一轮报告写进：

`agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS12-EST-ACCEPT-LOOP.md`

只追加「运行 YYYY-MM-DD」。

## 3. 后端调用

token 文件：`%USERPROFILE%\.gkx\display-loop-token`（一行 access_token，仓库外）。请求头 `Authorization: Bearer`、`systemCode: display`。不打印、不入库。

| 步骤 | 调用 | 作用 |
|---|---|---|
| 探测 | `POST https://edu.itic-sci.com/tid/api/display/v1/policy/simulation/jobs`，body `{"kind":"多维评估"}` | 只验 token 和映射 |
| 库 | 只读 `gkxlumenx_gapfill` 的 `gapfill_policy_sim_forecast`、`gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder` | 看行在不在 |
| 样本 | 同一 jobs 地址，按用例业务键逐条 POST | 看过滤结果是不是右列 |

探测 401、424，或正文为「访问令牌不存在」「用户凭证已过期」「token expired」：验收单 `blocked`，通知 `human:淮政玮`，不建子任务，不再开一轮。探测 404：同样停止，原因写「接口映射不存在」。

库只 `SELECT`。验收轮不 `--apply`。

## 4. 样本清单

第 1.1 节首批：

| 种类 | 业务键 | 右列要点 |
|---|---|---|
| 未出台仿真 | 研发补助 × 广东省高新技术企业 × 按研发投入的20%补助 × 2026年至2028年 × 新一代信息技术 | 约 128 亿元；2026年120、2027年146、2028年171 |
| 未出台仿真 | 人才引进 × 深圳市重点实验室 × 每人每年30万元 × 2027年至2029年 × 生物产业 | 约 46 亿元 |
| 新出台预测 | `18363390` | 短标题「广东省科技型中小企业研发环境支持」 |
| 新出台预测 | `18407696` | 短标题「深圳市外国人来华工作许可」 |
| 区域空间 | 广东省；政策类型可空 | 空间分布广州市42、深圳市38、佛山市21、东莞市16 |
| 区域空间 | 深圳市；政策类型可空 | 南山区28、福田区19、宝安区14、龙岗区11 |
| 多维评估 | 只传 kind | 经济 78.2500、社会 71.5000、环境 66.0000、创新 74.7500 |
| 利益攸关方 | 只传 kind | 三条参与意见，用字「利益攸关方」 |

第 1.2 节另加：未出台 5 条（目标产业依次为新能源、新材料、高端装备、绿色环保、海洋产业）、新出台 5 个政策编号、区域 5 个区域名、多维 5 个维度、参与意见 5 条。以用例表格为准，计划不改右列。

当前用例记载的表内行数是未出台 7、新出台 7、区域 7、多维 9、参与意见 8。`target_industry` 尚未落库。验收时按这个事实分类，不把缺列说成已经通过。

## 5. 缺口怎么派

每轮最多三张子任务，先去重。不改前端。

| 类 | 执行人 | 计划 ID | 挂靠 |
|---|---|---|---|
| DATA | `data-agent` | `POL-L2-DS12-EST-DEMO-FIX-R{YYYYMMDD}-DATA` | 无则新建 |
| QUERY | `api-agent` | 不新建 | 目标产业拣不中挂 `POL-L2-DS12-INDUSTRY-EQ-FIX-L01` |
| ALGO | `algorithm-agent` | `POL-L2-DS12-EST-DEMO-FIX-R{YYYYMMDD}-ALGO` | 仅当行在、键一致、算出的值对不上右列 |

同一缺口键连续两轮仍在：停止建单，交给 `human:淮政玮`。

子任务 handoff 落盘后，才把验收单拨回 `ready` 再开下一轮。note 不写「联调通过」。

## 6. 轮次顺序

2026-11-07 已探测并在 404 停止。下次从探测重入，不另开验收单。

1. 认领 `POL-L2-DS12-EST-ACCEPT-LOOP`，`supervised_by=human:淮政玮`。
2. 读本机 token，打探测。
3. 探测失败则停。
4. 探测成功则按第 4 节逐条核对库和 jobs。
5. 有缺口才建或挂第 5 节的子任务，验收当轮不改库。
6. 写 handoff 一节。样本全对上则停止，验收单留在 `ready`，不签 `done`。
