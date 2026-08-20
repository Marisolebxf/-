# DATA-SVC-STORAGE-PATCH-L02 · SVC 圈定规则 A + 列清单（不灌数）

> 日期：2026-08-20  
> Task：`DATA-SVC-STORAGE-PATCH-L02`  
> 总控：`DEMO-SVC-REOPEN-长任务总控.md`（阶段 F）  
> 拍板：`human:淮政玮` 规则 A；卡面 B 维持；看列清单就过，**不再会签流图**  
> **本单未执行 DDL、未灌数。** F-SEED 另叶 `DEMO-SVC-LAB-SEED-L01`。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `lite` |
| 说明 | 定义叶：升词表 version + 一页列清单；未改 §1 工厂拓扑边 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机 task-registry 走 CLI |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SVC-STORAGE-FLOW` / `SVC-STORAGE-LINEAGE` |
| 图 diff | §1 工厂 `flowchart LR` **边未动**。§1.1 血缘边未改。§7 Demo 灌数图圈定标签改为 `svc_rule_demo_kw_v1.1`（不是工厂拓扑）。 |
| 会签态 | `signoff_status=approved`（2026-08-19）；本叶不再会签 |
| 说明 | 真源仍 `01-data-flow.md` |

## 范围与实现

1. 词表升 **`svc_rule_demo_kw_v1.1`**：圈定从宽、分类从紧；有行业不把科研 L1 余量倒进 INNOV；无行业去掉光杆投资/咨询/广告/银行/基金/保险。  
2. 一页列清单 `seeds/svc-column-checklist.md`：扫描列 + `svc_org_circle` + `svc_org_card`。  
3. 交叉：`ods-to-dwd-mapping.md` / `dwd-svc.md` / SVC README 读序。细表仍 **draft**。

## 偏离说明

- 无。未开 50892；未改 lumen。

## 产物清单

| 产物 | 路径 |
|---|---|
| 规则 A | `data-design/storage/SVC/seeds/svc_rule_demo_kw_v1.md` |
| 列清单 | `data-design/storage/SVC/seeds/svc-column-checklist.md` |
| 本 handoff | `agent-handoffs/服务机构-SVC/DATA-SVC-STORAGE-PATCH-L02.md` |

## 验收证据

- [x] v1.1 规则 A 落盘；禁止 org_type / tech_tag  
- [x] 列清单含 circle + card（卡面 B 维持）  
- [x] §1 工厂边未改；细表 draft；本单不灌数  
- [x] Q-SVC-010 仍黄  

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ N/A（文档） |
| 7 | 方案 A / D12 | ✅ 50892 不施工 |
| 10 | D9 | ✅ 待核验不伪闭合 |

## 决议

列清单给淮总看一眼即可。灌数见 F-SEED。

## CI/CD

- 分支：`origin/dev`
- pipeline：`cicd: skip_design_only`
- 连库 / 灌数：未执行（本叶）

## Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 30000 |
| actual_tokens | 55000 |
| model_used | `cursor-grok-4.6` |
| actual_cost | 0.28 |
| cost_warn | green |
