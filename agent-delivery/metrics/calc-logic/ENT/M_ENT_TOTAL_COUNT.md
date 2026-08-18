# 企业总数（M_ENT_TOTAL_COUNT）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_TOTAL_COUNT`
- **指标名称**：企业总数
- **一级模块**：企业分析
- **二级模块**：企业总览
- **三级模块**：企业整体概况
- **更新频率**：日
- **对齐状态**：已对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q-E32

## 口径定义

在选定的未来产业范围内，按企业统一社会信用代码去重的企业数量。

## 计算逻辑说明

```
COUNT(DISTINCT credit_code WHERE 属于目标未来产业)。从dwd_org_industry_tags按industry_name正则匹配归类。
```

**计算公式文件**：`M_ENT_TOTAL_COUNT.md`

## 源表字段

```
gkx.dwd_org_industry_tags（credit_code, industry_code, industry_name）
gkx.dwd_org_base_info(org_id,external_id)
gkx.dwd_forg_base_info(org_id,external_id)
```

## 备注

1.1.1.2.4.2.3；简单统计类

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
