# Demo 临时规则 `svc_rule_demo_kw_v1`（六类词表）

> **任务**：`DATA-SVC-STORAGE-GAP-L02`  
> **性质**：Q-SVC-010 🟡 **项目临时词典**。**不是** live 准入真源；**不关闭** Q-SVC-008 / Q-SVC-010。  
> **扫描列**：`name_cn` + `industry` + `industry_l1_name`…`industry_l4_name`（有则加 `industry_l*_code`，因 md-extract 名称/编码样例可能对调）+ 有则加 `business_scope`。  
> **禁止**：`org_type` 作服务机构语义。  
> **本单不灌数**；F-SEED / `svcseed` 须读本文件，不得另造第二套词。

```yaml
---
doc_id: SVC-RULE-DEMO-KW-V1
element: SVC
role: seed-config
status: draft
version: "svc_rule_demo_kw_v1"
updated: "2026-08-19"
task_id: DATA-SVC-STORAGE-GAP-L02
pending_client: true
---
```

## 圈定

1. 把扫描列拼成一个字符串（大小写不敏感；中文原样）。  
2. **任一**下表关键词子串命中 → 入 `svc_org_circle`。  
3. `rule_version=svc_rule_demo_kw_v1`；`pending_client_confirm=1`。  
4. `hit_fields`：记下命中的列名。  
5. 命中机构数 **&lt;10**：按决策表 **退回全表** 仍待核验；禁止静默灌伪池。  
6. 不要用光杆「服务」——过宽。

## 六类（先命中先得）

顺序 = 下表从上到下。一词可进圈定；分类取**第一条**命中的类。无类命中但因圈定词入池：`service_type_candidate` 空，仍待核验。

枚举对齐 v1 / DIM：`FINANCE` / `IP` / `HR` / `MKT` / `CONSULT` / `INNOV`。

招标 L01 六名（研发 / 技术转移 / 检验检测 / 知识产权 / 科技金融 / 综合科技服务）**映射进本六类**，不另开第七类。

| 类 | 中文 | 关键词（子串） |
|---|---|---|
| FINANCE | 金融服务 | 科技金融、创业投资、风险投资、融资担保、知识产权质押、小额贷款、小贷、创投、风投、担保、基金、证券、保险、银行、融资、投资 |
| IP | 知识产权服务 | 知识产权、专利代理、商标代理、版权代理、知产 |
| HR | 人力资源服务 | 人力资源、人才服务、劳务派遣、猎头、招聘 |
| MKT | 市场营销服务 | 市场营销、市场推广、广告、品牌、会展 |
| CONSULT | 咨询服务 | 管理咨询、规划咨询、顾问、咨询 |
| INNOV | 科技创新服务 | 检验检测、检测认证、技术转移、研发服务、科技服务、孵化器、众创、中试、计量认证、综合科技 |

「投资」偏宽，排在 FINANCE 末；若只想紧圈，F-SEED 可在 `ext` 记录命中词，**不得**擅自删表而不改 version。

## 与算法词典

Q-SVC-008 仍待 algorithm-agent 出 **business_scope→六类** 正式词典。本表是 Demo 圈定/候选的**文档真源**；正式 `svc_rule_v2.2` 另单，不把本表升 live。
