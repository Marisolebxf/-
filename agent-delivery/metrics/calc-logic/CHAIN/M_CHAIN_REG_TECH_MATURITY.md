# M_CHAIN_REG_TECH_MATURITY 区域技术成熟度（技术力叶子）计算口径细稿

- **版本**：v0.2.0（2026-10-14，链路升级随 Seq17 同拍板；增速映射保留原稿；正式签名待 human:唐绍祖 会签）
- **口径拍板**：human:徐滕强 2026-10-14（链路 org_id 全键 + 名称过渡轨；kind 语义 DDL 钉死但本指标**不过滤 kind**）
- **类型**：MODEL（增速→生命周期映射 0–100）
- **is_mock**：true（rel 0 行走名称过渡轨）

## 1. 原始定义档案

- **页面语境**：区域产业评价页 `TOPIC-REG-013`，技术力叶子（权重 8/100）。页面约束：**不得用周期侧 M_CHAIN_TECH_MATURITY_SCORE 顶替**。A1 需规 `ALGO-CHAIN-DEEP-126`。
- **白话**：深圳这条链上的技术处在生命周期哪个位置——公开专利量增速趋缓=成熟，陡增=成长，负增长=衰退，输出 0–100 分。
- **原稿口径**（王惠调研迁移版，**保留不变**）：时间戳 pbdt_year（不用授权年）、不要求 granted_number、patent_id 去重。P_t=该区域该年公开专利去重件数；窗口 k 优先 3、否则 2、仅 1 年同比；g_t=(P_t/P_{t-k})^(1/k)-1。P 连续 0→0 分；上期 0 本期有量→25（萌芽）；g>5% 且加速或缺上期 g→50（成长）；g>5% 且减速→70（趋于成熟）；|g|≤5%→90（成熟）；g<-5%→90×P_t/P_{t-k} 截断 [0,90)（衰退）。

## 2. 链路变更（v0.2.0 唯一改动）

老链路 `dwd_org_industry_tags`（demo 库与主档 0 命中，废）→ 新链路 **org_id 全键**：
`enterprise_industry_chain`(chain_code) → `dwd_org_base_info`(org_id + city) → 专利关联（过渡 `first_current_assignee_name = name_cn`；rel 灌数后切 `enterprise_patent_org_rel`.org_id + party_role IN ('APPLICANT','ASSIGNEE')）。

## 3. 实核（2026-10-14 demo）

pbdt_year 2021–2026（6 年窗，k=3 可支撑两期）；其余同 Seq17 §4（链桥 2000 行已灌、深圳×INB1309=1004、rel 0 行待灌）。

## 4. 缺口分型

同 Seq17 §5（rel 0 行=数据未灌；collation 统一待办；ADS fact 表待产出）。
