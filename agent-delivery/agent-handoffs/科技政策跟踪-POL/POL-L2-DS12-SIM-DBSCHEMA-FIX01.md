# POL-L2-DS12-SIM-DBSCHEMA-FIX01 · 仿真空结果线上热修（gapfill 缺列）· hotfix

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent`（口头派单 hotfix，不建 task-id、不走 task-claim/task-update-status，按派单指令执行） |
| supervised_by | `human:淮政玮`（当次会话批准执行线上 DDL） |
| 状态流转 | 无 registry 单（hotfix 口头派单）；DDL 已在线上执行并端到端验证，本 handoff 即交付证据 |

## 现象（2026-11-11，用户报告）

232 合规演示用例（未出台政策仿真模拟：知识产权 / 广东省高新技术企业 / 每人每年30万元 / 2026年至2028年）点「运行仿真模拟」返回空态「尚未运行仿真模拟」；多维评估、利益攸关方同样空。

## 根因（实证）

`gkxlumen-element` `PolicySimulationReadController.FORECAST_COLUMNS`（POL-SIM-VIS-FDE-L01 图序列契约新增 `medium_effect_text`、`auto_tags` 两列），但线上库 `10.50.11.76` `gkxlumenx_gapfill.gapfill_policy_sim_forecast` **缺这两列**（仓库种子 SQL `scripts/mysql/gapfill_policy_sim_forecast.sql` 第 48–49 行的 ALTER 从未在线上执行）。

故障链：

1. 每次 `未出台仿真` 查询：`Unknown column 'medium_effect_text' in 'field list'`
2. `ElementDao.listOrEmpty()` 捕获 `DataAccessException`，只打 WARN 返回 `List.of()` → element 以 HTTP 200 返回 `records: []`
3. display `PolicyPanoramaService.recordsBody()` 对 `code=0` 空记录直接透传 → 前端空态

element pod 日志实证（02:44）：`gapfill 读表失败，返回空列表: Unknown column 'medium_effect_text' in 'field list'`。库内 26 行数据完好，id=64 即 232 用例行。

## 修复（只动线上库 DDL，不改代码）

用户批准后，对 `10.50.11.76` 执行与仓库种子 SQL 第 48–49 行**逐字一致**的 DDL（幂等：先查 information_schema 再加列；只加列不动数据）：

```sql
ALTER TABLE `gapfill_policy_sim_forecast` ADD COLUMN `medium_effect_text` text AFTER `short_effect_text`;
ALTER TABLE `gapfill_policy_sim_forecast` ADD COLUMN `auto_tags` varchar(512) DEFAULT NULL AFTER `similar_basis_text`;
```

## 验证（2026-11-11 14:4x，公网全链路）

| kind | 结果 |
|---|---|
| 未出台仿真（232 四参数） | ✅ 返回 id=64 完整推演（经济 74 亿 / 就业 1.6 万 / 发明专利 0.9 万件等字段齐全） |
| 多维评估 | ✅ 有数据 |
| 利益攸关方 | ✅ 有数据 |
| 页面得分 | 空 = 设计内诚实空态（得分表未发布，前端「得分待发布」） |

集群内 port-forward 直打 element（`from: Y`）同样返回 id=64，display→element 链路无异常。仓库种子 SQL 与线上库列集现已一致，无遗留漂移。

## 教训（记入沟通流水）

1. **种子 SQL 迁移与代码部署不同步**：POL-SIM-VIS-FDE-L01 发代码（element 列契约扩了）没发 DDL（线上缺列）。gapfill 表的 ALTER 属线上变更，需要会话内人工批准——但「代码上线前提线上列齐」这一步没有闸门。
2. **吞错观察性**：`ElementDao.listOrEmpty` 只打 WARN 不告警；display `payload()` 对下游 `code != 0` 静默塌缩成空、零日志。这次定位花在「先证明链路里谁在撒谎」。防再发：display `payload()` 加下游失败 WARN（另派）。
3. **PowerShell 5.1 中文 JSON 测试假象**：`Invoke-WebRequest -Body '中文'` 按 GBK 发送，服务端按 UTF-8 解析 → `kind` 乱码不在白名单 → 静默空。排查期间一度误判为「display→element 断了」。复测规范：UTF-8 无 BOM 文件 + `curl.exe --data-binary @file`。
