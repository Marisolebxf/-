# Handoff — E-TECH-NEWS-ENTITY-M3-L03

> **status**: done  
> **claimed_by**: agent:frontend-agent  
> **supervised_by**: human:孙英哲  
> **claim_type**: pull  
> **completed_at**: 2026-07-29T12:00:00+08:00  
> **repo**: lumen-ui-science-pc  

---

## 1. 范围与实现

| DoD | 证据 |
|-----|------|
| 从 Java 拉取实体扩展历史列表 / 回看，展示 entities / event_type | `listTechNewsEntityExtractions` → `GET /innov/v1/tech-news/entity-extractions`；`getTechNewsEntityExtraction` → `…/entity-extractions/{id}`；回看加载 `response`（含 `entities[]`、`events[].event_type`） |
| 仅调 Java | 未直连 Python `/internal/*` |
| Design.md §14 + D9 | 复用既有 Arco 页；MockBadge + MetricSpecHint（事件数/实体数）保留 |
| handoff | 本文件 |

### 改动文件

- `src/api/tech-news/index.ts` — 新增 entity-extractions list/get
- `src/types/tech-news.ts` — 列表/详情补 `entity_count` / `mode` / ADS 辅证字段
- `src/views/tech-news/index.vue` — 实体模式下历史走 ADS 查询；列展示实体数；模式切换刷新历史

---

## 2. 偏离

- 登录态联机截图 / 网关在线 E2E 待环境（与 M2-L03 残留同类）；本期以 type-check 绿 + 契约对齐为准。
- 四要素历史仍走 `/extractions`；实体扩展历史走 `/entity-extractions`（按抽取模式切换）。

---

## 3. 验收命令

```powershell
cd repos/lumen-ui-science-pc
npm run type-check
# 手工：科技新闻抽取复核 → 实体扩展 → 刷新历史 → 回看（需后端 entity persist 有数据）
```

---

## 4. 架构合规自检

1. 前端→Java REST only ✅  
2. 不直连 Python ✅  
3. Arco Design ✅  
4. D9 MockBadge / MetricSpecHint ✅  

---

## 5. 开放项

- 网关登录态截图补进 handoff  
- 可选：历史分页 / 筛选  

---

## 6. Cost

| 字段 | 值 |
|------|-----|
| model_used | cursor-grok-4.5 |
| actual_tokens | ~估 40k |
| actual_cost | ~$0.25 |
| cost_warn | green |


---

## 7. 验收关单

- **accepted_by**: human:孙英哲
- **accepted_at**: 2026-07-29T11:53:42+08:00
- **result**: PASS
- **commit**: lumen-ui-science-pc e796e475
