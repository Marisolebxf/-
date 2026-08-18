# 产业链完整度（M_ENT_CHAIN_COMPLETENESS）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_CHAIN_COMPLETENESS`
- **指标名称**：产业链完整度
- **一级模块**：企业分析
- **二级模块**：深圳企业现状分析
- **三级模块**：产业链定位
- **更新频率**：产业标签/链图更新后
- **对齐状态**：已对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：24

## 口径定义

目标产业已被企业覆盖的有效节点数占该产业标准节点总数的比例，反映区域内某产业链的覆盖广度。

## 计算逻辑说明

```
完整度 = 有企业覆盖的节点数k / 标准节点总数K * 100%。从dwd_industry_chain_info取K，从dwd_org_industry_tags取k。
```

**计算公式文件**：`M_ENT_CHAIN_COMPLETENESS.md`

## 源表字段

```
gkx.dwd_industry_chain_info（industry_code, industry_link_code）
gkx.dwd_org_industry_tags（industry_code, industry_link_code, credit_code）
```

## 备注

1.1.1.2.4.2.3.5.1；简单统计类

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
