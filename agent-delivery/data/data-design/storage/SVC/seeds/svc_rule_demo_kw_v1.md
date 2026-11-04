# Demo 临时规则 `svc_rule_demo_kw_v1.1`（规则 A）

> **任务**：`DATA-SVC-STORAGE-PATCH-L02`（升版；原 GAP-L02 v1 不删）  
> **拍板**：`human:淮政玮` 2026-08-20 **规则 A**；卡面 **B 维持**。  
> **性质**：Q-SVC-010 🟡 **项目临时词典**。**不是** live 准入真源；**不关闭** Q-SVC-008 / Q-SVC-010。  
> **扫描列**：`name_cn` + `industry` + `industry_l1_name`…`industry_l4_name`（有则加 `industry_l*_code`）+ 有则加 `business_scope`（Demo 主表仍无此列）。  
> **禁止**：`org_type` 作服务机构语义；`dwd_org_tech_tag` 作圈定路径。  
> **本单不灌数**；F-SEED / `svcseed` 须读本文件，不得另造第二套词。

```yaml
---
doc_id: SVC-RULE-DEMO-KW-V1
element: SVC
role: seed-config
status: draft
version: "svc_rule_demo_kw_v1.1"
updated: "2026-08-20"
task_id: DATA-SVC-STORAGE-PATCH-L02
pending_client: true
amendment: "规则 A：圈定从宽、分类从紧"
---
```

写入 `svc_org_circle.rule_version` 用 **`svc_rule_demo_kw_v1.1`**。文件名仍叫 `svc_rule_demo_kw_v1.md`（文档 ID 未改）。

## 原则（规则 A）

1. **圈定从宽、分类从紧。**  
2. **有行业**：国标白名单只用于**分类**；**禁止**把「科学研究和技术服务业」L1 余量整筐倒进 `INNOV`。  
3. **无行业**：只用**收紧名称词**；去掉光杆「投资 / 咨询 / 广告 / 银行 / 基金 / 保险」。  
4. 六类只在**有把握的叶子**上写 `service_type_candidate`；否则候选**空** + `pending_client_confirm=1`。  
5. 名单按类截断（如 40–80）只允许 UI 展示，**禁止**灌数造假均衡。  
6. 一律 `pending_client_confirm=1`（Q-SVC-010 不伪闭合 live）。  
7. `hit_fields` 记下命中的 ODS 列名。命中很少或为 0：**诚实空/少池**，禁止静默灌伪小池，也**禁止**整表回退入池（2026-11-04 Q9 / `GDF-SVC-WORKPACK-R1A-L01`）。

## 圈定（入 `svc_org_circle`）

把扫描列拼成字符串（大小写不敏感）。满足任一即入池：

| 条件 | 做法 |
|---|---|
| `industry` / `industry_l*` **有值** | L1=`科学研究和技术服务业` **或** L1 含「金融」**或** 行业串命中下表「圈定宽词」 |
| 行业全空 | **仅**名称命中「名称收紧词」；不扫光杆投资/咨询/广告/银行/基金/保险 |

圈定宽词（行业侧，**不等于**六类）：上表分类叶子 + 「咨询」「广告」等宽子串（只决定进池，不自动分类）。

不要用光杆「服务」。不要用 `org_type` / 资质标签表。

## 六类（先命中先得 · 从紧）

顺序：`FINANCE` → `IP` → `HR` → `MKT` → `CONSULT` → `INNOV`。

枚举对齐 DIM：`FINANCE` / `IP` / `HR` / `MKT` / `CONSULT` / `INNOV`。招标 L01 六名映射进本六类，不另开第七类。

### 有行业：只认叶子 / 明确国标，不倒余量

| 类 | 中文 | 行业侧（子串，须有把握） |
|---|---|---|
| FINANCE | 金融服务 | L1 含「金融」；或 投资与资产、货币金融、资本市场、保险、证券、非金融机构支付 |
| IP | 知识产权服务 | 知识产权 |
| HR | 人力资源服务 | 人力资源、劳务派遣、职业中介 |
| MKT | 市场营销服务 | 广告业、广告服务、会展、会议展览、市场调查、市场营销 |
| CONSULT | 咨询服务 | 管理咨询、规划咨询、商务咨询、科技咨询、社会经济咨询、咨询与调查 |
| INNOV | 科技创新服务 | 检验检测、检测认证、质检、技术推广、研究和试验、科技推广、技术转移、孵化、中试、计量认证 |

**禁止**：`industry_l1_name=科学研究和技术服务业` 且无上表 INNOV 叶子 → **候选空**（仍可因圈定从宽入池）。

裸「咨询 / 广告 / 投资」出现在行业串、但够不上上表叶子 → 入池、候选空。

### 无行业：名称收紧词（分类＝圈定）

| 类 | 关键词（子串） |
|---|---|
| FINANCE | 科技金融、创业投资、风险投资、融资担保、知识产权质押、小额贷款、小贷、创投、风投 |
| IP | 知识产权、专利代理、商标代理、版权代理、知产 |
| HR | 人力资源、人才服务、劳务派遣、猎头、招聘 |
| MKT | 市场营销、市场推广、会展 |
| CONSULT | 管理咨询、规划咨询 |
| INNOV | 检验检测、检测认证、技术转移、研发服务、科技服务、孵化器、众创、中试、计量认证、综合科技 |

无类命中但已入池：`service_type_candidate` 空，仍待核验。

## 与算法词典

Q-SVC-008 仍待 algorithm-agent 出 **business_scope→六类** 正式词典。本表是 Demo 圈定/候选的**文档真源**；正式 `svc_rule_v2.2` 另单，不把本表升 live。
