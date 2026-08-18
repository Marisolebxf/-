# 专利总量（M_ENT_PATENT_TOTAL）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_PATENT_TOTAL`
- **指标名称**：专利总量
- **一级模块**：企业分析
- **二级模块**：企业总览
- **三级模块**：企业整体概况
- **更新频率**：日
- **对齐状态**：部分对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q-E34

## 口径定义

选定企业集合内各企业作为第一专利权人的有效专利件数。

## 计算逻辑说明

```
从dwd_patent_legal筛选status为有效，关联dwd_patent按assignees匹配，COUNT(DISTINCT patent_id)。
```

**计算公式文件**：`M_ENT_PATENT_TOTAL.md`

## 源表字段

```
gkx.dwd_patent（patent_id, pn, assignees,）— 专利基本信息与权属
gkx.dwd_patent_legal（patent_id, pn, status）— 专利法律状态（有效/授权/失效）
gkx.dwd_org_base_info（org_id, name_cn）— 国内企业名称关联
gkx.dwd_forg_base_info（org_id, name_en）— 海外企业名称关联
关联说明：
- dwd_patent.assignees  与 dwd_org_base_info.name_cn 做企业名映射获取 org_id
- assignees 可能包含多个企业或个人，需与企业基本表的企业名做 mapping 得到对应 org_id
```

## 备注

1.1.1.2.4.2.3；assignees需mapping到org_id

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
