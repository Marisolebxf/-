# 企业类型占比（M_ENT_TYPE_RATIO）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_TYPE_RATIO`
- **指标名称**：企业类型占比
- **一级模块**：企业分析
- **二级模块**：重点企业类型分析
- **三级模块**：类型与区域分析
- **更新频率**：月度/年度
- **对齐状态**：已对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：24

## 口径定义

某区域某企业类型数量 / 该区域企业总数 * 100%。

## 计算逻辑说明

```
先计算各类型企业数，再除以区域企业总数。
```

**计算公式文件**：`M_ENT_TYPE_RATIO.md`

## 源表字段

```
其他标签（高新/专精特新/小巨人）:gkx.dwd_org_tech_tag（org_id, org_tag）— 高新/专精特新/小巨人统一取科技型标签表，禁用 company_honor_tags；匹配值需按实际标签校准
外企：gkx.dwd_org_base_info.org_type
上市：gkx.dwd_org_stock_base.org_id
小微：gkx.company_basic_tags(id, scale_tag in("小型","微型"))
区域：gkx.dwd_org_base_info(org_id, province, city,area)
```

## 备注

1.1.1.2.4.2.3.1；简单统计类

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
