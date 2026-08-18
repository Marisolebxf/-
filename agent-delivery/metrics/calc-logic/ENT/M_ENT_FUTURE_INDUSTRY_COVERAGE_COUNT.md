# 覆盖未来产业数（M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT`
- **指标名称**：覆盖未来产业数
- **一级模块**：企业分析
- **二级模块**：企业总览
- **三级模块**：企业整体概况
- **更新频率**：产业标签更新后
- **对齐状态**：未对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q-E32-02

## 口径定义

当前企业集合实际覆盖的未来产业一级分类数量。

## 计算逻辑说明

```
从dwd_org_industry_tags按industry_name正则匹配归类到8个未来产业，统计有企业覆盖的数量。
```

**计算公式文件**：`M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT.md`

## 源表字段

```
gkx.dwd_org_industry_tags（credit_code, industry_code, industry_name）
```

## 备注

1.1.1.2.4.2.3

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
