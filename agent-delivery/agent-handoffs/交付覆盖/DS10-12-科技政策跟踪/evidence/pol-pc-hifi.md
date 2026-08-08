# Evidence · DS-PC-01~04 V1 高保真（非骨架）

日期：2026-08-07  
范围：`repos/demo-ui-science/src/pages/policy-tracking/PolicyPcPages.jsx` + `policyPcData.js`

## 验收对照（Wireframe §6 / UX-SPEC §3.4 · §4.5）

| Frame | 关键交互 | 结果 |
| --- | --- | --- |
| PC01 | 四状态卡 + 批次明细 + 底座未就绪禁用下游 CTA | ✅ Switch 可演示禁用 |
| PC02 | 政策选择 / 摘要 / 条款树 / 指标表 / 实体图 / 送入对比 | ✅ |
| PC03 | ≥2 对象、维度勾选、运行对比、表/雷达/柱状、摘要、生成研报 | ✅ 单对象禁止运行 |
| PC04 | 大纲 / 正文 / 洞察 / 双向溯源 / PDF·Word | ✅ 演示导出 |

## D9

- KPI 挂 ⓘ MetricSpecTrigger + 🧪 MockBadge；QPOL 项挂 ⚠️ PendingBadge
- 新增 catalog：`M_POLICY_VALIDITY_RATE` / `INTENSITY_INDEX` / `RELATION_DEGREE` / `INDUSTRY_FIT`

## 分轨

- 页头分轨说明条；对比槽 key=`display-policy-compare-slots`（非专题篮）

## 预览

```bash
cd repos/demo-ui-science && npm run dev
# 侧栏：科技政策跟踪 → 政策数据治理 / 智能政策拆解 / 多维政策对比 / 智能研报生成
```
