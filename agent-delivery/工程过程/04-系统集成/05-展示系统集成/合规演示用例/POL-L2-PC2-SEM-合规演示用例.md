# POL-L2-PC2-SEM · 政策语义理解 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技政策跟踪 · 智能政策拆解
- 需规序号：606
- 需规全文：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` §2 PC-2
- 日期：2026-11-13（PARSE-4JOB-FDE 卡 AAA；原稿 2026-11-07 501 口径废止）
- 调度核对：见文末

一点「拆解」并行起四 Job；本叶只验收语义路。样例政策与 SIM 共用 `18363390`（有正文）。真算依赖 LLM/密钥；无密钥则 `generated=0`、不造假行（可仍读预灌/既有 gapfill 行）。

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 606 政策语义理解 | 智能政策拆解 · 语义 Tab | 检索/选定政策（样例 18363390） | 点「拆解」：并行 `evaluation/jobs`×4；本叶盯 `policy_parse_semantic`。禁浏览器直连 Python | POST /display/v1/policy/evaluation/jobs | {"sub_type":"policy_parse_semantic","params":{"policy_id":"18363390"},"force":true}（另有 analysis_fp） | 须见核心主旨 / 适用场景 / 约束 非空（或诚实空态「暂无语义结果」）；条款分类可空。业务面不出现 gapfill / Job 黑话。关评审零泄漏 | 可演（部署后）。D4 mock；真算 upsert `gapfill_policy_semantic` |

## 一条主路径

1. 打开「智能政策拆解」，选定政策 18363390，点「拆解」。进行中按钮 loading。
2. 网络可见四条 `evaluation/jobs`（含 `policy_parse_semantic`）与并行 `panorama/.../detail`。
3. 语义 Tab：主旨 / 适用场景 / 约束有文或诚实空态；不因另三路失败而整页清空已成功块。

## 调度核对

需规 606 一行可演。可进演示样本循环。无密钥时允许空态，不造假。
