# Handoff · DS10-12 核增四页 V1 高保真补齐

> agent: frontend-agent · 2026-08-07  
> 承接：`DS10-12-V1-HIFI-L01` 骨架缺口 `GAP-DS-PC-INTERACTION`

## 1. 范围

按 `Wireframe-DS10-12 §6` / `UX-SPEC §3.4 J-DS-PC` 将核增四页从骨架升级为可演示主路径：

| 页 | 关键交付 |
| --- | --- |
| 政策数据治理 | 四卡 KPI + 批次表 + 底座就绪闸门 |
| 智能政策拆解 | 选择器 / 摘要 / 条款树 / 指标表 / 实体图 / 送入对比 |
| 多维政策对比 | ≥2 对象、维度、运行对比、表+雷达+柱状、摘要、生成研报 |
| 智能研报生成 | 大纲 / 正文 / 洞察 / 溯源面板 / PDF·Word 演示导出 |

## 2. 产物

- `repos/demo-ui-science/src/pages/policy-tracking/PolicyPcPages.jsx`
- `repos/demo-ui-science/src/pages/policy-tracking/policyPcData.js`
- `repos/demo-ui-science/src/pages/policy-tracking/PolicyPcPages.css`
- `repos/demo-ui-science/src/pages/policy-tracking/mocks/policy-metrics-catalog.json`（补 4 个 metric）
- 交付覆盖：`implementation-coverage.yaml` / `page-packages.yaml` / `evidence/pol-pc-hifi.md` / `validation-report.md`

## 3. 偏离

- 仍为 demo2 **AntD** + Mock；算法/ADS 未接。
- 对比槽：`sessionStorage` key `display-policy-compare-slots`（非专题篮）。
- catalog 路由回写、QPOL 口径仍 🟡。

## 4. 架构合规

| 铁律 | 结果 |
| --- | --- |
| 算法只在 Python | ✅ 前端仅演示聚合 |
| 不直连 Nebula/Python | ✅ |
| demo 不 merge lumen | ✅ |
| D9 | ✅ ⓘ / 🧪 / ⚠️ |
| 分轨 | ✅ 页头说明条 |

## 5. 验收建议

1. 侧栏走通：治理 → 拆解「送入对比」→ 运行对比 → 生成研报 → 溯源
2. 治理页关闭「底座就绪」→ 对比/研报 CTA 禁用
3. 对比页仅选 1 对象 → 运行对比应警告
