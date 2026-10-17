# 全库「六级 ↔ catalog 页」错挂排查清单（L13 事件后）

> **触发**：L13 曾整库误挂 chain/entan/policy/svc 构建 API，而非 `comp.graph`。  
> **要求**：合表 F4 前由人 + 父控跑一遍；发现错挂按 L13 同级严重处理。

## 1. 自动粗扫（父控可跑）

```bash
# 在 fp-split-by-api-run/ 下
python3 scripts/audit_l6_catalog_binding.py   # 待建：对照 _l6-to-catalog-map.yaml + work 内 endpoint_id 前缀
```

当前已有：

- `scripts/rewrite_l13_l05_12.py` 生成后 **3c**（`endpoint_id`+`field_key` 全库唯一）应为 **0 重复**。
- work 表行 **禁止单元格含未转义的 `|`**（会破坏合表解析）。

## 2. 人工对照表（60 六级 × 页 title）

| 风险级 | 六级示例 | 期望 catalog 页 | 常见误挂 |
|--------|----------|-----------------|----------|
| P0 | L13 | `comp.graph` · 产业全要素图谱 API | `chain.panorama` / `entan.graph` 等构建页 |
| P0 | L05–L12 | 见 `L13-comp-graph-closure.md` 分挂表 | 仍写「契约见 L13」但 L13 已是 comp |
| P1 | L14 | `chain.panorama.main`（非 ops） | 与 L05 重复 ops |
| P1 | L42 | `svc.relation` | 与 L12 `svc.graph` 混 path |
| P2 | L15+ chain 分析 | `chain.*` 各独占页 | 挂到 `chain.panorama` 或 `comp.graph` |

**操作**：打开 `_l6-to-catalog-map.yaml` 一行六级 → 打开 `work/Lxx.md` → 抽查 `endpoint_id` 是否落在 `pages[]` 对应 JSON 页内。

## 3. 需规语义 vs 接口语义

- 六级名含 **「API 服务开发」** → 优先 **查询/对外 REST** 页（如 `comp.graph`），不是 `graph/ops` 写入。
- 六级名含 **「实体识别/关系抽取/构建」** → **构建** 页（`*.graph` / `panorama.ops`），不是 `comp.graph` COMP_*。

## 4. 签收闸门

- [ ] L13 work/review **人复核**（6 COMP_* + 39 行量级）
- [ ] L05–L12 抽检至少 L05、L09、L14 各 1 份
- [x] 全库 3c = 0（`audit_l6_catalog_binding.py` 2026-10-17）
- [x] `_l6-to-catalog-map` L13=comp.graph（原则/playbook **未同步**，见 audit memo）
- [x] 父控自动扫已记入 `memo/audit-parent-run-20261017.md` + `00-control.md`
- [ ] **不进 F4** 直至人签收 + 文档 drift 处理（可选派单语义 spot-check）
