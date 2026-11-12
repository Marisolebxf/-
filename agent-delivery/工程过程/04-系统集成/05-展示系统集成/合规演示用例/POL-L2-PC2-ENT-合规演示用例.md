# POL-L2-PC2-ENT · 政策实体关联 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技政策跟踪 · 智能政策拆解
- 需规序号：609
- 需规全文：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` §2 PC-2
- 日期：2026-11-13（PARSE-4JOB-FDE；原稿「设计无资源」废止）
- 调度核对：见文末

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 609 政策实体关联 | 智能政策拆解 · 实体 Tab + 页头关联度/完整度 | 政策 18363390 | 点「拆解」；本叶盯 `policy_parse_entity`。元信息级别/地区/部门另打 panorama/detail | POST /display/v1/policy/evaluation/jobs | {"sub_type":"policy_parse_entity","params":{"policy_id":"18363390"},"force":true} | 须见实体点/边或诚实空态；页头关联度、拆解完整度有数或「—」/「未抽取实体」。写回 `structured_elements.entities`+`links`。Java 不写 nGQL；KG 开关只控展示 | 可演（部署后） |

## 一条主路径

1. 选定 18363390，点「拆解」。
2. 实体 Tab 有图或空态；页头 KPI 随实体 Job 回填；级别/地区/部门可来自 detail。

## 调度核对

需规 609 一行可演。不再是「设计无资源」。
