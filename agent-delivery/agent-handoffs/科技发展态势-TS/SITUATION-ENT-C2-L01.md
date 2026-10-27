# SITUATION-ENT-C2-L01 · display /map objectPoints 接线 + Feign 降级演练

> **任务**：科技全域态势·企业维度跑通 C2 叶（U3 接线）——`gkxlumen-display` `/v1/situation/map` 的 `objectPoints` 从恒空改为真实点位
> **角色**：`agent:api-agent` · 监管人：`human:李伟`（长任务授权，授权句已生效）
> **状态**：`backlog → claimed → in_progress → integration`（AV-1 目标态，待人工签收）
> **上位**：[SITUATION-ENT-长任务总控](./SITUATION-ENT-长任务总控.md) · 契约 [SITUATION-ENT-API-CONTRACT-01.md](./SITUATION-ENT-API-CONTRACT-01.md) §3
> **倚前端叶**：[C1 端点叶](./SITUATION-ENT-C1-L01.md)（integration） · [A0 体检](./SITUATION-ENT-A0-L01.md)（含 `/map` 基线存档）
> **挂接**：WBS §4.3（WBS-05-18-03） · 2026-10-27

---

## 一、交付内容

1. `RemoteElementClient#enterprisePoints(limit, city, district)`：新增 Feign 方法，**`@NoToken`**（与 element 侧 `@Inner` 配对——漏标会静默降级为「拿不到数据」，极易误判下游挂）。
2. `SituationController#map()`：`objectPoints` 由 `List.of()` 恒空改为 C1 端点 `records` **透传**（display 侧不二次装配）；**单独 try/catch 降级**，与 chips/区域/级联互不牵连。
3. `objectPointsEmptyReason`：**仅降级时出现**（正常路径不再吐该字段，符合契约 v1.1 §3）。
4. 新增常量 `OBJECT_POINT_LIMIT = 100`（注释标明是**工程口径非业务口径**，天花板由 element 侧 500 兜底，前端若要更少量自切片）。

## 二、自测证据（本地 element :7082 + display :7099，`from: Y`，2026-10-27 17:0x）

### 2.1 正常路径

| 项 | 结果 |
|---|---|
| HTTP | 200 |
| `objectPoints` | **100 条**（空一个月前 A0 基线的 0 条） |
| `objectPointsEmptyReason` | **不存在**（正常路径已移除） |
| 首条 | 深圳市京泉华科技股份有限公司 · 影响力 70.3 · 龙华区 · patents=198 · level=high · layerKeys=[enterprise, patent] |
| 原始 JSON 类型 | `"coordinates":[114.03262,22.746325]`、`"patents":198` —— **未被序列化成字符串**（Long→String 坑未在链路中出现） |

### 2.2 对照 A0 基线的字段级差分（`SITUATION-ENT-A0-L01-map-baseline.json`）

| 字段 | 结果 |
|---|---|
| `factorItems` | **identical = True** |
| `regions`（30 城市） | **identical = True** |
| `regionCascadeOptions` | **identical = True** |
| `legend` | **identical = True** |
| `objectPoints` | 0 → **100**（唯一预期变化） |
| `objectPointsEmptyReason` | True → **False**（唯一预期变化：正常路径移除） |

> 结论：**除 objectPoints 外零副作用**，契约 §3「其余字段不变」验证通过。

### 2.3 `/overview` 对照（本叶未动 overview，仅回归验证）

`enterprise_total=189,115 · high_tech=27,936 · little_giant=14,903 · gazelle=588 · unicorn=167`，
`trendYears=12 · domainRows=6 · factorCards=5 · isEmpty=false` —— 与 A0 基线一致。

### 2.4 降级演练（停 `gkxlumen-element`，最终产物包验证）

```
DEGRADED HTTP=200 objectPoints=0 regions=0 enterpriseChip=0
reason='要素服务不可达（UNREACHABLE）：对象级点位暂不可用——不以城市点冒充对象点'
```

满足分区降级铁律：**下游挂 → 仍 200 + 诚实空态 + emptyReason，不 5xx**。

## 三、过程中修正的一处不实陈述

降级文案初稿写了「对象级点位暂不可用，**区域舆图仍可用**」——演练时发现**element 整体不可达时 `regions` 也来自 element、同样为空**，该句是**暗示可用的不实陈述**。已改为「对象级点位暂不可用——不以城市点冒充对象点」并在代码注释里写明原因。诚实性铁律适用于 human 可读文案，不只是数据值。

## 四、给 C3 / D1 的输入

1. **C3（influence 端点）**：Feign 同样落在 element 侧（`enterprisePoints` 已验证 `@NoToken`/`@Inner` 配对链路可用），建议沿用本叶的「单独 try/catch + zero-structured 空态」模式，`/influence` 全降级时 `count=0 / averageScore=0 / items=[]`。
2. **D1（前端切换）**：`/map` 正常路径**不再返回** `objectPointsEmptyReason`，前端若有用该字段判断「降级」需兼容缺省（不能假设必存在）；建议 D1 在 api 层做缺省归一，不动视图。
3. **`parentRegionKey` 一致性已确认**：display 侧 `regions` 的 key 与 `regionCascadeOptions` 的 value **均为中文行政区划名**（如「深圳市」/「龙华区」），与 C1 输出的 `parentRegionKey` 同源，**无需映射层**——C1 handoff 里担心的「拼音 slug 不一致」问题在 display 这条链路上不存在。
4. **数量口径**：display 固定取 100；前端若只显示 Top50 请在 api/视图层切片，不作为后端契约。

## 五、本叶改动清单（git）

| 文件 | 类型 | 说明 |
|---|---|---|
| `gkxlumen-display/src/main/java/.../feign/RemoteElementClient.java` | 改 | 新增 `enterprisePoints`（`@NoToken`），口径写在 javadoc |
| `gkxlumen-display/src/main/java/.../controller/SituationController.java` | 改 | `/map` 接线 objectPoints + 独立降级 + `OBJECT_POINT_LIMIT` 常量 + 降级文案修正 |

> ⚠️ 工作区仍有前序任务的未提交改动（`gkxlumen-element/application*.yml`、`db/*.sql`、`scripts/local-seed-enterprise.sql` 等），**不属本叶范围**。按人工验收闸门，**本叶改动停本地，未 commit 未 push**。

## 六、Cost 四字段

| 字段 | 值 |
|------|-----|
| actual_tokens | ≈ 110k（估，含基线差分与降级演练两轮重启） |
| model_used | auto（CodeBuddy） |
| actual_cost | ≈ $0.8（估） |
| cost_warn | green（<$10） |

ponytail: full（降级文案的不实陈述、与 A0 基线逐字段差分都做了，未为省 token 省略）
