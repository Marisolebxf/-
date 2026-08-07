# DEC-E7-POLICY-LAUNCH-FROM-INDUSTRY-BASKET · 政策三项经产业对比篮发起

| 字段 | 值 |
|---|---|
| id | `DEC-E7-POLICY-LAUNCH-FROM-INDUSTRY-BASKET-20260807` |
| 日期 | 2026-08-07 |
| 确认人 | human:高颖（会话确认：对象=产业/技术领域；若用对比篮则挂产业 Tab 发起） |
| approval_status | `approved` |
| source_relation | `direct_requirement` |
| 上级 | 修订/取代 `DEC-E7-COMPARE-ACTIVATE` 中「政策文档为篮对象且唯一经政策 Tab 发起」条款 |
| Bid | `科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.2.6（P-70/P-72/P-73） |

## 背景

招标写明：用户**选定产业或技术领域**后，系统**自动关联**相关政策，再做时序 / 区域对比 / 深圳三维。  
原四件套将对比篮对象定为 `policy` 文档并以政策 Tab 唯一发起，与招标对象语义不一致。

## 决策

1. **分析对象** = `industry`（产业；技术领域后续同构扩展）。政策文档是任务内自动关联语料，**不是**对比篮分析对象。
2. **对比篮若使用**：在系统对比篮 **产业 Tab**「发起分析」任务选择器中增加分组「政策分析」，含三项：
   - 政策时序分析 → `/policy/overview`
   - 区域政策对比 → `/policy/analysis`
   - 深圳政策现状分析 → `/policy/recommendation`
3. **分发契约**：`object_type=industry` + `object_ids[]` / `object_names[]` + `analysis_type` + `source=compare-basket`；单次 **1** 个产业对象（与招标「选定领域」一致）。
4. **移除对比篮「政策」Tab**（2026-08-07 确认）：系统篮不再展示政策文档 Tab；查询/门户不再提供「加入对比篮（政策文档）」。
5. **分析页空态**：轻量对象条 +「打开对比篮」→ 产业 Tab；`compare_object_type=industry`。
6. **页面直选产业/领域**（不经篮）仍允许作为增强路径，与本 DEC 不冲突；细则见 `DEC-E7-POLICY-SCOPE-MUTEX-20260807`（产业 XOR 技术领域；技术领域可多选且暂不进篮）。

## 明确废止/降级

| 原条款 | 处理 |
|---|---|
| 篮对象 = `policy_id`；分发 `policy_ids[]` | 废止 |
| 对比篮政策 Tab（含暂存） | **移除**（非降级占位） |
| 「唯一经政策 Tab 发起」 | 废止；改为产业 Tab |
| IA「产业/技术领域不进篮、进页再配」 | 废止；产业为篮对象，区域/粒度/权重仍为页内配置 |
| 查询/门户「加入对比篮」写政策文档 | 废止 |

## scope_effect

不增删 Bid 叶子；纠偏对象与发起路径，贴 §1.1.1.2.4.2.6。
