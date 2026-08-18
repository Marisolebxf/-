# 国有企业数（M_ENT_STATE_OWNED_COUNT）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_STATE_OWNED_COUNT`
- **指标名称**：国有企业数
- **一级模块**：企业分析
- **二级模块**：企业总览
- **三级模块**：企业整体概况
- **更新频率**：日
- **对齐状态**：部分对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：否
- **是否在原型代码**：否
- **关联Q编号**：Q-E32

## 口径定义

统计范围内国有且当前有效状态的在营企业去重数量。

## 计算逻辑说明

```
（待补充）
```

**计算公式文件**：`M_ENT_STATE_OWNED_COUNT.md`

## 源表字段

```
gkx.dwd_org_shareholder_info（org_id, owners_type, ownership_percentage）— 股东类型与持股比例
gkx.dwd_org_base_info（org_id, city, province）— 企业所在地筛选（深圳）
gkx.dwd_forg_shareholder_info（org_id, ownership_percentage）— 海外企业股东持股（补充）
判定逻辑：
- 国有独资：owners_type = 单位 且 ownership_percentage = 100%
- 国有控股：owners_type = 单位 且 ownership_percentage > 50%
- 需进一步通过股东名称判断是否为国有主体（如国资委、国有资产监督管理部门等）
```

## 备注

1.1.1.2.4.2.3；国有判定规则待确认

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
