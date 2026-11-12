# KG-COMPLY-LOAD-T06 · 四条现存边语义对齐交接

## 认领

- claimed_by：agent:data-agent；supervised_by：human:陈芸飞；claim_type：pull。
- 2026-11-12 用户明确授权启动。开工前通过 MCP 确认 ready、T02/T03/T04 全部 done，认领后转 in_progress。
- 4 小时锁定窗口：2026-11-12 15:39:42–19:39:42 +08:00。
- ponytail：full。复用现有序列化与结果工具，新增一个只读核验脚本；本次为调研报告，不上线服务或变更图结构。

## 交付

- 报告：`agent-delivery/工程过程/04-系统集成/07-图数据库集成/T06-四条现存边语义对齐报告-20261112.md`。
- 脚本：`scripts/t06_semantics.py`。
- 证据：同图数据库集成目录下 `对接文档/燕大/T06/audit.json`、`verification.json`、`samples.md`。
- 全量原始快照留本机 `_local/t06-20261112/`，SHA256 在证据中；未提交凭据。

## 验证结论

apply_to/support 各 10,957 条，端点交集 10,957、双向覆盖率及 Jaccard 均 100%，独有 0。**但全部 10,957 条 weight 不同：0.6 vs 0.8；props 解析后完全一致。** 报告明确建议停读 support、单读 apply_to，保留权重口径待裁定，不删不改图。

participates 拆分为 M17 enterprise→segment 178,731 及 institution→institution 34,769（不得映射 M02/M19/M17/M18，候选 service_relate 另行确认）。belongs_to 为 segment→chain 359 条，覆盖 359/1,414 个环节，1,055 个未挂链，不强行映射或补边。

五组各 20 条样本，共 100 条；政策边分页全量对比，前后分组计数一致。独立 SQLite PRIMARY KEY/JOIN 验证交集与属性差异通过，快照摘要通过；部分交集/双空集合边界检查通过。正式结果基于最后一次成功运行（15:43:28–15:44:07 +08:00）。

## 风险与待裁定

- 仅对已知源 Tag 锚定，未全图扫描，未证明其他源类型的异常边为零；非事务快照。
- 旧 T06 文件中“M02=0”及政策边空属性的历史说法不再符合当前数据。本报告按最新 T02 签收与本次实测说明，不修改历史裁定正文。
- 两条政策边是端点重复、非全属性相同，权重处理需负责人确认；不能擅自求和、取最大值或回写。
- service_relate 仅建议，接口停读、物理迁移、补链都未实施，需后续授权。
- 高水位风险仍存在，本次按类型串行小批读取成功，不代表环境问题修复。

## CI/CD 与流程

- 分支 dev，开工与执行器提交 d26bcea8c；最终交付版本以本文件 Git 历史为准。
- 本机图库只读实跑及离线验证通过。未查询 CI Pipeline，不宣称 CI 绿；无镜像发布、K8s rollout 或 API 部署。
- 日志与证据有查询耗时、起止时间、源码摘要；图库执行仅 USE/MATCH，无 DDL/DML。
- 提交 review，由唐绍祖 / 徐滕强裁定、coordinator 签收 done；执行 Agent 不自行关闭，亦不提前启动 T07。
- 实际 token / 费用平台未提供，不虚填；cost_warn=yellow 表示计量缺失。
