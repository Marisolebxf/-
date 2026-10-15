# M_CHAIN_REG_PAPERS 高校论文（链维 / 区域维）计算口径细稿

- **版本**：v0.2.0（2026-10-14，路径A：口径前置写实；正式签名待 human:唐绍祖 会签）
- **口径拍板**：human:徐滕强 2026-10-14
- **类型**：STAT（去重计数）
- **is_mock**：true（机构挂链 0 行，D4=mock；目标态走 P0-6 后转 live）

## 1. 指标定义

指定区域内、指定产业链链上**高校+科研院所**所属学者发表的**论文去重件数**。

- 机构范围沿用定义层既定口径：`dwd_org_heis_info`（高校）+ `dwd_research_institute_base_info`（科研院所）双桶 UNION，与 `M_CHAIN_REG_COMP_ACADEMIC`、`M_CHAIN_INSTITUTION_COUNT` 三处自洽；**不含**企业研究院（`××研究院有限公司` 归 ENTERPRISE 口径）。
- 区域过滤：`inst.city = :region_city`（同族 KPI 一致）。
- 挂链（过渡桥）：`dwd_org_industry_tags.credit_code = inst.external_id AND industry_code = :chain`；目标桥 = `industry_chain_entity_rel`（entity_type=institution，待 CHAIN-P0-6）。
- 学者归属：`dwd_scholar.scholar_org_name_zh = inst.name_cn`（名称匹配，REG_COMP_ACADEMIC 先例）。
- 论文计数：`COUNT(DISTINCT r.paper_id)`，跨桶/跨机构合作论文只计 1。

## 2. Formula（SQL）

```sql
SELECT COUNT(DISTINCT r.paper_id) AS paper_cnt
FROM (
  SELECT external_id, name_cn, city FROM demo_gkxlumenx_ods.dwd_org_heis_info WHERE is_deleted = 0
  UNION
  SELECT external_id, name_cn, city FROM demo_gkxlumenx_ods.dwd_research_institute_base_info WHERE is_deleted = 0
) inst
JOIN demo_gkxlumenx_ods.dwd_org_industry_tags t
  ON t.credit_code = inst.external_id AND t.industry_code = :chain
JOIN demo_gkxlumenx_ods.dwd_scholar s
  ON s.scholar_org_name_zh = inst.name_cn AND s.is_deleted = 0
JOIN demo_gkxlumenx_ods.dwd_scholar_paper_relation r
  ON r.scholar_id = s.scholar_id AND r.is_deleted = 0
WHERE inst.city = :region_city;
```

## 3. 表依赖与实核（2026-10-14 demo 库）

| 表 | 角色 | 实核 |
|---|---|---|
| `dwd_scholar_paper_relation` | 分子（paper_id 去重） | 388,615 行 |
| `dwd_scholar` | 学者↔机构名称匹配 | 21,316 位 |
| `dwd_org_heis_info` / `dwd_research_institute_base_info` | 机构桶双键载体（external_id / name_cn / city） | 3,501 / 2,074 行 |
| `dwd_org_industry_tags` | 过渡桥（credit_code↔external_id） | CHAIN-P0-5 缺上链时间 |
| `dwd_scholar_papers` | **弃用**（2026-10-14 实核：status 唯一值 1，无过滤价值；未来灌入非 1 值时加回） | 738,106 行 |

## 4. 已知缺口（如实 0 + ⚠️，不造数）

1. **机构挂链 0 行**（CHAIN-P0-6）：`industry_chain_entity_rel` 无 entity_type=institution 数据 → 真数 0。
2. **企业桥缺上链时间**（CHAIN-P0-5）：过渡桥沿用；NEW 同族 KPI 需上链时间。
3. **名称匹配覆盖误差**：`scholar_org_name_zh = name_cn` 匹配面 32,215 行，同名校漏配风险；升级路径 = 供方补 `scholar_org_id ↔ org_id` 结构化映射。

## 5. 验证记录（2026-10-14）

- 端到端已验证：深圳 heis 路径真数 **1,791 篇**（不带链过滤、city=深圳市）。
- relation/papers/scholar 三表行数实核如上表。
