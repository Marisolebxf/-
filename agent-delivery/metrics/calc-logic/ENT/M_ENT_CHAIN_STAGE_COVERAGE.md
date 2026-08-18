# 产业链环节覆盖（M_ENT_CHAIN_STAGE_COVERAGE）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_CHAIN_STAGE_COVERAGE`
- **指标名称**：产业链环节覆盖
- **一级模块**：企业分析
- **二级模块**：深圳企业现状分析
- **三级模块**：产业链定位
- **更新频率**：产业标签更新后
- **对齐状态**：部分对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：24

## 口径定义

企业在目标产业链各环节（上游/中游/下游）的覆盖数量。

## 计算逻辑说明

```
从dwd_org_industry_tags关联dwd_industry_chain_info按level分组（上游/中游/下游），COUNT(DISTINCT industry_link_code)。
```

**计算公式文件**：`M_ENT_CHAIN_STAGE_COVERAGE.md`

## 源表字段

```
gkx.dwd_org_industry_tags(credit_code, industry_code, industry_link_code)
gkx.dwd_industry_chain_info(industry_code, industry_link_code, level, parent_code)
```

## 备注

1.1.1.2.4.2.3.5.1

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
