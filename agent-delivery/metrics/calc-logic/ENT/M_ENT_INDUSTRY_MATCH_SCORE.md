# 产业匹配度（M_ENT_INDUSTRY_MATCH_SCORE）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_INDUSTRY_MATCH_SCORE`
- **指标名称**：产业匹配度
- **一级模块**：企业分析
- **二级模块**：引育推荐
- **三级模块**：招引推荐
- **更新频率**：产业标签/目标画像更新后
- **对齐状态**：未对齐
- **是否在数据库**：部分
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q015

## 口径定义

衡量企业与目标产业链整体关联的紧密程度。

## 计算逻辑说明

```
先基于投入产出表算出产业链关联度和企业所属行业的上游度，再由上游度和行业收入占比定位产业链质心，计算企业与质心的相对距离得到质心度，最后将质心度与产业链关联度相乘得出融入度。
```

**计算公式文件**：`M_ENT_INDUSTRY_MATCH_SCORE.md`

## 源表字段

```
gkx.dwd_industry_chain_info(industry_code, industry_link_code, level, parent_code, industry_link_name, node_company_count) — 产业链层级结构
gkx.dwd_org_industry_tags(credit_code, industry_code, industry_link_code, company_name) — 企业与产业链节点关联
gkx.dwd_org_annual_financial_info(org_id, industry_name, main_business_revenue) — 行业主营业务收入及占比(c_i)
gkx.dwd_org_base_info(org_id, industry, industry_l1_code, industry_l2_code, industry_l3_code, city, province) — 企业行业归属+地级市限定
gkx.dwd_org_annual_financial_info(org_id, year, operating_revenue, main_business_revenue) — 企业产值/收入(production_f)
gkx.dwd_org_shareholder_info(org_id, inv_org_id, owners_name, ownership_percentage) — 股东/持股关系(边)
gkx.dwd_org_subsidiary_info(org_id, sub_org_id, sub_name_cn) — 母子公司关系(边)



【缺口】投入产出表(a_ij直接消耗系数, Y_i行业总产出, X_i行业最终消费) — 缺失，ind_link/c/d_f/ind_chain_f均无法计算
```

## 待建表字段

```
缺口：《中国投入产出表》
```

## 备注

1.1.1.2.4.2.3.6；

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
