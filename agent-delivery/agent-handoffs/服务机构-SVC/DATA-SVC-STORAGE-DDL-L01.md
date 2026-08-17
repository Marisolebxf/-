# DATA-SVC-STORAGE-DDL-L01 · 服务机构存储 — 字段级结构（排除数据口径）

> **日期**：2026-08-17  
> **确认**：待 `human:侯佳伟` 结构走查（非 live / 非 Q-SVC-010 关闭）  
> **本地签**：仅本地产物；**不 commit / 不 push**  
> **前置**：S3 stores 清单已本地签收；数据准入仍无法定 → **结构先行**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `lite` |
| 说明 | 文档 + DDL 草稿；未伪闭合 Q-SVC-010；未跳过 ADS / 待核验列 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 task-registry MCP；本叶未改 registry |

## 问题清单

- 数据灌入 / 圈定规则 / 关键词 **刻意排除**（Q-SVC-010 仍开放）
- Demo 物理建表未自动执行（有 SQL 草稿，需 Owner 指示再 APPLY `demo_*`）
- ADS 其余 `svc_metric_*` 等表仅列契约，SQL 先落 profile/ranking 两表骨架
- 六类中文名：结构采用 Q-ALGO-006 码；与产品文案若不一致 → 另轨改 label，不改码列

## 修改内容

| 路径 | 内容 |
|---|---|
| `stores/mysql/dwd-svc.md` | 5 表字段级 + 键索引；`verification_status` 预留 |
| `stores/mysql/ads.md` | `svc_*` 十表列契约；**ADS 单轨**；对比篮/`org_id` 下钻键 |
| `stores/mysql/dim.md` | 六类 / verification / `CHAIN_STAGES` 唯一来源 |
| `etl/demo_gkxlumenx_dwd_svc_tables.sql` | CREATE 草稿（禁默认真正式库） |
| `README.md` / `CHANGELOG.md` / `stores/mysql/README.md` | 登记 DDL-L01 |

## 测试结果

- 文档自检：DWD 不复制 ENT 全量列；ADS Java 只读；环节码不另造树
- 未对任何 MySQL 实例执行 DDL

## 遗留风险

- 结构会签前 Java/算法若按旧 v1 38 字段接线会漂移 → 以本目录为准
- 甲方关闭 Q-SVC-010 后可能增列（规则痕迹字段已预留 `rule_version`）

## CI/CD（必填）

- 分支：本地工作区（未 commit）
- commit：无
- pipeline / 部署：N/A（文档）

## 可观测性

- N/A（存储设计稿）

## 涉及文件

- `agent-delivery/data/data-design/storage/SVC/stores/mysql/dwd-svc.md`
- `agent-delivery/data/data-design/storage/SVC/stores/mysql/ads.md`
- `agent-delivery/data/data-design/storage/SVC/stores/mysql/dim.md`
- `agent-delivery/data/data-design/storage/SVC/etl/demo_gkxlumenx_dwd_svc_tables.sql`
- `agent-delivery/data/data-design/storage/SVC/README.md`
- `agent-delivery/data/data-design/storage/SVC/CHANGELOG.md`
- `agent-delivery/agent-handoffs/服务机构-SVC/DATA-SVC-STORAGE-DDL-L01.md`

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 / Java 不扫 DWD | ✅ |
| Nebula 不复制 CHAIN | ✅（本叶未改图谱） |
| 不伪闭合 Q-SVC-010 | ✅ |
| 不默认写正式 ODS/DWD | ✅ |
| demo→lumen merge | N/A |

## 下一步（可选）

1. 侯佳伟结构走查后标「结构 draft 冻结」（仍非 approved live）
2. 指示后对 `demo_gkxlumenx_dwd/_ads` APPLY SQL 草稿
3. 数据口径另开叶，不挡结构
