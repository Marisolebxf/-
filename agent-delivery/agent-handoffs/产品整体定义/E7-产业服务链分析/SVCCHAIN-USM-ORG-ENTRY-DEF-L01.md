# Handoff — SVCCHAIN-USM-ORG-ENTRY-DEF-L01

- **任务**：USM 服务机构分析 US-01 对象集入口定义修订：直选 → 对比篮两层组装（补 R2B 遗漏）
- **执行**：agent:frontend-agent · **监管**：human:淮政玮 · **类型**：definition
- **日期**：2026-10-20 · **强度**：ponytail off（定义产物完整性优先）

## 一、修订依据（口径链）

1. R2B 用户口径（2026-08-05 淮政玮）：服务机构检索/分析参照企业模式 + 落地对比篮
2. demo `98941fd`（2026-08-09）：分析页摘除直选 `OrgPickerModal`，对象组装切对比篮（1~50 / capability 2~5）——**代码改了、定义未跟**，即本任务补的遗漏
3. **产品侧 2026-10-20 确认**（淮政玮转述）：对象集入口 = 先弹对比篮，篮内点「新增」再弹对应企业/机构搜索框
4. lumen 已对齐（`LUMEN-SVC-FE-ORG-BASKET-ENTRY-L01`，commit `9ade25e`）

## 二、变更清单（gkx-orchestration，五件套目录 SVCCHAIN-ORG-ANALYSIS-服务机构分析/）

| 文件 | 变更 |
|---|---|
| `USM-…md` | 版本 v1.1-r2b → **v1.2-r2b-c**（头部修订记录）；US-01 业务结果 1~N→1~50 家经篮确认；主路径 2-4 步重写为两层组装（打开对比篮 → 篮内新增弹在库机构搜索框 → 勾选确定回填 org_ids[]+source）；异常表 6 行重写（篮空态/篮内过滤无匹配/新增搜索无匹配/勾选 0 家/持久化损坏/取消）；AC-01-01 重写为篮 picker 契约；AC-01-04 空态文案对齐；AC-01-05 取消对象改浮层；**新增 AC-01-06**（新增搜索框=在库只读检索，不做数据维护）；尾注改「篮提供选哪些、集合记录选中哪些，无绕篮第二入口，与 AC-08-06 互证」 |
| `IA-…md` | 结构图 `Modal: 机构选择器（分组/搜索/批量）` → `系统对比篮 picker（service_org Tab；篮内"新增"→在库机构搜索框）` |
| `Wireframe-…md` | F-SVC-01a 整节替换：直选分组 Modal → 对比篮 picker（0/50 计数、篮内过滤、新增第二层搜索框 ASCII 图、确定=唯一提交点）；状态机加 `adding`；上下文条按钮「选择机构」→「打开对比篮」 |
| `TRACE-…yaml` | 7.1.1 implementation 文本 `上下文区+选择器` → `上下文区+对比篮picker入口` |
| `UX-SPEC-…md` | 未动（仅 acceptance_source 引用 USM#4，无直选描述） |

残留核对：`grep 机构选择器|直选` 五件套内仅剩 USM 尾注否定句（「不再存在绕开篮的直选第二入口」），有意保留。

## 三、与实现的互证

- demo：`ServiceOrgAnalysisPage.tsx` `openCompareBasket`（1~50）+ `ServiceOrgCompareBasketPanel` 篮内「新增」→ `CompareBasketAddModal`（kind=service_org，在库检索）——与修订后主路径逐步对应
- lumen：`ServiceOrgAnalysisWorkspace.vue` `openCompareBasket` + 复用 `CompareBasketAddModal`，空态/角标/回传契约与 AC-01-01/04 一致
- US-08（篮故事）不受影响：AC-08-06「无第二套对比对象入口」与新 AC-01-01 互证关系已写入尾注

## 四、开放项

- 文档头仍标「AI 起草，待体验 Owner 确认」——本次修订依据含产品侧 2026-10-20 确认（淮政玮转述），正式会签建议随 E7 下次 PDR/评审一并收口
- US-06（技术力 2~5）主路径已是篮口径，无需改

## 五、验证

- `grep` 残留核对通过（见二）
- YAML/Markdown 结构未破坏（TRACE 仅改字符串值）
