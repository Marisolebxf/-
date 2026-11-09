# TOPIC-POL-SZ3D-DEMO-FIX-R20261107-EFFECT-DATA · 深圳政策现状回填真实实施日与支持对象

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人要求领取并执行。MCP `task-claim` 没有 `claim_type` 参数，该值写在任务 note 里。锁 4 小时。不改 `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-DATA`。 |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `full` |
| 说明 | 只回填正文已经写明的施行日和适用对象。不建反馈表，不把发布日抄成实施日。 |

## 图

不改调用链。只更新 `demo_gkxlumenx_dwd.policy_base_info` 的 `implementation_date` 与 `policy_support`。

## 扫描

与金额单同一次只读扫描。深圳政策 879 行。

| 位置 | 写库前 |
|---|---|
| demo `implementation_date` | 879 行都有日期，且 879 行等于 `publish_date`。NULL 0，零日期 0 |
| 正式库 `implementation_date` | 879 行都是 NULL。本轮不改正式库 |
| demo `policy_support` | 879 行 SQL NULL |
| 正式库 `policy_support` | 879 行 JSON null |

正文只认两种实施日：「自 YYYY年M月D日 起施行/实施/执行/生效」，或带「施行日期 / 实施日期」标签的公历日期。「自发布之日起」不算。适用对象只认「适用对象 / 支持对象 / 扶持对象：」或「本办法/本规定适用于」后面的原文。

| 结果 | 条数 |
|---|---|
| 深圳政策扫描 | 879 |
| 正文写明施行日 | 79 |
| 其中与现列不同、可以回填 | 77 |
| 现列是 NULL 或零日期 | 0，因此没有触碰这类单元格 |
| 正文写明适用对象 | 21 |

## 写库

只更新 demo 库，且只更新抽到原文的行。

- `implementation_date`：77 行改成正文里的施行日。写后 `implementation_date <> publish_date` 的深圳行是 77。其余 802 行仍等于发布日，没有改。
- `policy_support`：21 行从 SQL NULL 写成 `{"适用对象":"<正文>"}`。没有对象的行保持 NULL。
- 反馈调查表：没建。
- 正式库深圳实施日仍是 879 行 NULL。

## 测试

写后计数与上表一致。正式库没有被加上金额表，实施日空值行数仍是 879。

## 遗留

- 802 条深圳政策正文没有公历施行日，实施日仍是发布日的副本。
- 858 条适用对象仍空。
- 反馈维没有表，本轮按口径不进平均。
- 结果板还没读这两列。

## CI/CD

- 无业务仓代码提交，无流水线，无镜像。
- 数据落在 demo MySQL，不经 K8s。
- 注册表提交 `4dd593202`，推送到 `origin/dev` 的合并提交 `b8dde9489`。

## 架构合规

| 项 | 结果 |
|---|---|
| 不写 ODS / 正式 DWD / 供应方库 | 是 |
| 零日期和 JSON null 不编成假值 | 是 |
| 不建反馈表 | 是 |
| 不把本单签成 done | 是 |
