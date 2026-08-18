# 专利授权量（M_ENT_PATENT_GRANT_COUNT）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_PATENT_GRANT_COUNT`
- **指标名称**：专利授权量
- **一级模块**：企业分析
- **二级模块**：企业评估
- **三级模块**：技术力评估
- **更新频率**：月度/年度
- **对齐状态**：部分对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：24

## 口径定义

报告期内企业作为第一专利权人获得授权的专利件数，含发明、实用新型、外观设计三类。

## 计算逻辑说明

```
从dwd_patent_legal筛选status为授权，关联dwd_patent匹配企业名，COUNT(DISTINCT patent_id)。
```

**计算公式文件**：`M_ENT_PATENT_GRANT_COUNT.md`

## 源表字段

```
gkx.dwd_patent（patent_id, pn, assignees, first_current_assignee_name）— 专利基本信息与权属
gkx.dwd_patent_legal（patent_id, pn, status, isdt）— 专利法律状态与授权日期（status 为授权状态，isdt 为授权日期）
gkx.dwd_org_base_info（org_id, name_cn）— 国内企业名称关联
gkx.dwd_forg_base_info（org_id, name_en）— 海外企业名称关联
关联说明：
- 通过 dwd_patent_legal.status 筛选已授权专利
- dwd_patent.assignees 或 first_current_assignee_name 与企业基本表 name_cn/name_en 做 mapping 获取 org_id
```

## 备注

1.1.1.2.4.2.3.3；简单统计类

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
