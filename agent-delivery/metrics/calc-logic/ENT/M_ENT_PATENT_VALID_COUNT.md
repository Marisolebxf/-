# 有效专利数（M_ENT_PATENT_VALID_COUNT）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_PATENT_VALID_COUNT`
- **指标名称**：有效专利数
- **一级模块**：企业分析
- **二级模块**：企业查询
- **三级模块**：企业画像
- **更新频率**：日
- **对齐状态**：部分对齐
- **是否在数据库**：是
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q-E20

## 口径定义

企业当前法律状态有效的专利件数。

## 计算逻辑说明

```
从dwd_patent_legal筛选status为有效，关联dwd_patent匹配企业名，COUNT(DISTINCT patent_id)。
```

**计算公式文件**：`M_ENT_PATENT_VALID_COUNT.md`

## 源表字段

```
gkx.dwd_patent_legal(status,patent_id)
gkx.dwd_patent(patent_id,assignees)
gkx.dwd_org_base_info（org_id,name_cn）
gkx.dwd_forg_base_info（org_id,name_en)
assignees可能包括不止一个企业或个人，该值与企业基本表的企业名做mapping得的对应的org_id。
```

## 备注

1.1.1.2.4.2.3.3；需名称mapping

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
