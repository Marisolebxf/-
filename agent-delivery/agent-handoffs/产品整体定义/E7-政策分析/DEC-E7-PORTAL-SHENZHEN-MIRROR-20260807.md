# DEC-E7-PORTAL-SHENZHEN-MIRROR · 深圳政策 Tab 镜像四能力 + 各区对照（S1）

| 字段 | 值 |
|---|---|
| id | `DEC-E7-PORTAL-SHENZHEN-MIRROR-20260807` |
| 日期 | 2026-08-07 |
| 确认人 | human:高颖（会话确认 S1 + 共享产业 + 地图/列表；同日确认**不含力度榜**） |
| approval_status | `approved` |
| source_relation | product_interpretation |
| 上级 | `DEC-E7-PORTAL-TAB-MERGE-A-20260807` |
| Bid | P-22（§1.1.1.1.1.1.2.6） |

## 决策

1. **S1 四段镜像（贴招标四能力）**：深圳政策 Tab 内 Segmented = `政策数量对比 | 政策地图 | 产业覆盖 | 最新动态`，复用对应 Panel，范围预置深圳市。
2. **不含力度榜**：招标 P-22 无「力度排名」叶子；**不**挂各区力度 / P-20 镜像。力度榜仅留在「政策概览 · rank」。
3. **共享产业**：概况 / 地图共享产业 Cascader。
4. **地域控件锁深圳**：地域 Cascader 仅展示「深圳 → 深圳市各区 → 各区」，全国/区域等不可选项不展示。
5. **对照 = 深圳各区**：stats 对照候选为各区（≤5，不含焦点）；去掉「深圳 vs 标杆城雷达 / 三维摘要」作为 P-22 主路径。
6. **地图双视图**：政策地图主区支持 **地图 | 列表**（概览与深圳镜像同步）。
7. **深度评估**：三维现状分析经对比篮**产业 Tab**发起（对象=产业）→ P-73；见 `DEC-E7-POLICY-LAUNCH-FROM-INDUSTRY-BASKET-20260807`。

## URL

`?tab=shenzhen&szView=stats|map|coverage|latest&industry=&geo=shenzhen…&compare=`

## scope_effect

不增删 Bid 叶子；P-22 四能力镜像 + 各区对照；明确排除力度榜。
