# 重点企业总数（M_ENT_KEY_TOTAL）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_KEY_TOTAL`
- **指标名称**：重点企业总数
- **一级模块**：企业分析
- **二级模块**：企业总览
- **三级模块**：企业整体概况
- **更新频率**：按名单更新
- **对齐状态**：部分对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：24

## 口径定义

选定范围内重点企业（高企/专精特新/上市等）去重总数。

## 计算逻辑说明

```
高企/专精特新/小巨人从dwd_org_tech_tag筛选，上市从dwd_org_stock_base筛选，去重COUNT(DISTINCT org_id)。
```

**计算公式文件**：`M_ENT_KEY_TOTAL.md`

## 源表字段

```
gkx.dwd_org_tech_tag(org_id, org_tag)
gkx.dwd_org_stock_base(org_id, stock_code)
```

## 备注

1.1.1.2.4.2.3；简单统计类

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
