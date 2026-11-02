# POL-DISPLAY-SURVEY-DS10-L01 · 科创政策全景存量调研

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 总控已授权。本叶只写调研分册，不改注册表状态 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | 定义任务，不缩文档。未用 YAGNI 跳过指标身份与任务回指 |

## 范围

只覆盖 DS-10 科创政策全景。

- 用户故事：`US-DS-POL-01`～`04`
- SRS：`bid-reference/srs/02-科技信息展示系统/科技政策跟踪/科创政策全景.md` 序号 197～218
- 对照任务：`FE-POL-01A`、`FE-POL-01B`
- 不写政策分析评价、政策效果推演、核增四页

指标用 `metric-query`（domain=政策）和 `metric-get`。任务用 `task-get`、`task-query`。未读 `cfg_metric-POLICY-seed.yaml`、`metric-readiness-matrix-POLICY.yaml`、`task-registry.yaml`。

## 产物路径

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/survey/DS-10.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-DISPLAY-SURVEY-DS10-L01.md`（本文件）

未改对照初稿、WBS、task-registry、lumen 仓、demo 仓。未 commit，未 push。

## 三档计数

全景能力 24 行：可接统计读面 9，501 为 13，跨项索引 2。

边界索引 3 行，全部是跨项索引。

合计：可接统计读面 9，501 为 13，跨项索引 5。

政策域查询 35 条，D4 全部 `mock`。可接统计读面的数值仍是 mock。

## 未见清单

- 情感分布：政策域未见对应 metric_id；全景组件未见 `metric-id`
- 页面未见挂接：`M_POLICY_SZ_DIST`、`M_POLICY_INDUSTRY_COVERAGE`；序号 206、208、214、215、216 的面板未见字面挂接
- `srs_refs` 为空：`M_POLICY_VALIDITY_RATE`、`M_POLICY_MATCH`、`M_POLICY_INDUSTRY_FIT`、`M_POLICY_RELATION_DEGREE`、`M_POLICY_INDUSTRY_COVERAGE`
- 不挂本叶：`M_POLICY_GRAPH_106_1`（推演页）、`M_POLICY_DEEP_168_1`（不挂序号 211）、`M_POLICY_INTENSITY_INDEX`（只挂专题）、`M_POLICY_BASE_100_1`（只挂专题）
- 未见任务：收藏与检索历史的用户态服务、订阅邮件短信、受众反馈采集、检索导出服务、版本对比模型、序号 205 的热点与深度报告模型

## 修改内容

- 新增全景调研分册与本 handoff
- 判定回指 2026-11-03 的任务注册表与指标注册表

## 测试结果

- 文档叶。未跑业务仓测试，未改代码

## 遗留风险

- `FE-POL-01B` note 写联调通过，状态仍是 integration
- 9 条 501 没有对应 MODEL 条目，是按未注册归入，定稿时不要改写成统计读面
- `GDF-POLICY-MOCK-GATE-L01` 仍 blocked，统计读面不能写成已上线

## CI/CD（必填）

- 分支：编排仓本地工作区，未 commit
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：文档叶，无

## 涉及文件

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/survey/DS-10.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-DISPLAY-SURVEY-DS10-L01.md`

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 未计 |
| model_used | 未计 |
| actual_cost | 未计 |
| cost_warn | green |
