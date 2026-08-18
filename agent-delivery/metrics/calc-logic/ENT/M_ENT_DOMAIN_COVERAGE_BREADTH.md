# 领域覆盖广度（M_ENT_DOMAIN_COVERAGE_BREADTH）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_DOMAIN_COVERAGE_BREADTH`
- **指标名称**：领域覆盖广度
- **一级模块**：企业分析
- **二级模块**：重点企业领域分布分析
- **三级模块**：领域分布分析
- **更新频率**：产业标签更新后
- **对齐状态**：未对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q013

## 口径定义

企业集合覆盖的产业链节点广度，取去重节点数；可同时除以目标产业链节点全集得到0—1覆盖率。

## 计算逻辑说明

```
从dwd_org_industry_tags按industry_link_code去重计数(分子)，从dwd_industry_chain_info取全量节点数(分母)，相除。
```

**计算公式文件**：`M_ENT_DOMAIN_COVERAGE_BREADTH.md`

## 源表字段

```
gkx.dwd_org_industry_tags（credit_code, industry_link_code）
gkx.dwd_industry_chain_info（industry_code, industry_link_code）
```

## 备注

1.1.1.2.4.2.3.2；需求文档未明确构建方法，参考V3方案

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
