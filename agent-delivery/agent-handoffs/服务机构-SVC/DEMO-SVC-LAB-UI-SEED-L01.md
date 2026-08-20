# DEMO-SVC-LAB-UI-SEED-L01 · 50100 灌数据接到 circle/card/A1–A6

> 日期：2026-08-20  
> Task：`DEMO-SVC-LAB-UI-SEED-L01`  
> 仓：`demo-ui-system-test`  
> 与 `DEMO-SVC-LAB-SEED-L01` 同批。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只改基础指标页文案/状态/读 ADS；未重做十模型页 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SVC-STORAGE-LINEAGE`（消费） |
| 图 diff | 无  
| 会签态 | 流图 approved 2026-08-19 |

## 范围与实现

1. `BasicPage.vue`：离开 `dwd_service_org` / `service_org`；状态读 ODS `dwd_org_base_info`、圈定、卡面。  
2. replace 确认框写明 **不碰 ODS 33 表**。  
3. `BasicIndicators.vue`：有灌数读 ADS；A2 用省分布（`CN_PROVINCE_CENTROIDS`），不造国家。未灌数保留演示序列。

## 偏离说明

- 无。未改 lumen / 50892。

## 产物清单

| 产物 | 路径 |
|---|---|
| 灌数页 | `src/views/industry-service/pages/BasicPage.vue` |
| 指标 | `src/views/industry-service/components/BasicIndicators.vue` |

## 验收证据

- [x] 文案/状态对齐 circle/card  
- [x] 重建不清空 ODS  
- [x] A2 诚实降级到省  

## CI/CD

- 分支：`origin/dev`

## Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 25000 |
| actual_tokens | 35000 |
| model_used | `cursor-grok-4.6` |
| actual_cost | 0.18 |
| cost_warn | green |
