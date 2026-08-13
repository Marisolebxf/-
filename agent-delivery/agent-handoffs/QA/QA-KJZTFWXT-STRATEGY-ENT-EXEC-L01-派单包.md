# 派单包：QA-KJZTFWXT-STRATEGY-ENT-EXEC-L01

- **派单方**：coordinator（本会话 · 2026-08-13）
- **执行 / 监管**：`human:黄敬洲`（可带 `qa-agent`；claimed_by 写真人）
- **Agent 角色**：`qa-agent`
- **状态**：`in_progress` · `claim_type` 语义 = coordinator_dispatch
- **仓 / 产物落点**：`agent-delivery/qa/`
- **Sprint**：未挂（勿 silent 加活；需进 Sprint 请 PM 写入）
- **强度**：ponytail full（写记录 / 证据 / BUG 清单）

---

## 1. 目标

对 **科技专题战略分析 · 企业分析** 已拆好的总集 FUNC 用例做 **R0 执行**，产出：

1. **测试记录**（总集 Excel，编号与用例一致）
2. **BUG 清单**（`BUG-ZNFWJQ-KJZTFWXT-YYYYMMDD-nnn`）

输入用例（勿改用例正文，只填记录）：

`qa/total-set/KJZTFWXT/科技专题战略分析-v1.3/6.国际科技信息中心项目_企业分析_测试用例.xlsx`（538 条）

拆分单 `QA-KJZTFWXT-STRATEGY-TOTALSET-L01` 仍为 in_progress（基础完成待 handoff），本单 **不** 等其 `done`。

## 2. 产物

| 产物 | 建议路径 |
|------|----------|
| 测试记录 Excel（R0 空壳） | `qa/total-set/KJZTFWXT/科技专题战略分析-v1.3/7.国际科技信息中心项目_企业分析_测试记录-R0.xlsx` |
| 模板真源 | `原始文档/7.国际科技信息中心项目_xx_测试记录.xlsx` |
| 工作区 MD（可选） | `qa/test-records/KJZTFWXT/STRATEGY-ENT/FUNC-企业分析-记录-R0.md` |
| BUG 清单 | 记录 Excel 内 §BUG 表，或同目录 `BUG-企业分析-R0.md` |
| 失败截图 | `qa/evidence/{用例编号}-Fail-*.png` |
| handoff | `agent-handoffs/QA/QA-KJZTFWXT-STRATEGY-ENT-EXEC-L01.md` |

列：总集记录 17 列 + 右侧 GKX 扩展（实际结果 / 是否通过 / BUG编号 / traceId / 复测轮次 **R0** / 阻塞跳过原因）。

「是否通过」交付仅允许：`通过` / `不通过`。工作区可暂记阻塞/跳过，定稿前消化。

## 3. 执行顺序与范围

1. **P0 先跑**：重点企业类型分析、重点企业领域分布分析（KEYENT，对照 `USM-ENT-KEYENT`）
2. 再跑企业分析其余 L5（评估 / 深圳现状 / 招引培育 / 供应链 / 痛难点 / 竞争力 + 通用质量属性）
3. 538 条都应在记录中有结论；未测 **不得** 标「通过」，须写跳过依据

**测试环境（本轮）**：[http://111.198.38.90:50892/](http://111.198.38.90:50892/)（深圳国际科技专题服务系统，HTTP 200）。记录头已预填该 URL。

登录测试环境后开跑；不用「登录原型」话术。

## 4. BUG 规则

- 编号：`BUG-ZNFWJQ-KJZTFWXT-{YYYYMMDD}-{001起}`
- 不通过：必须有 BUG 号 + 截图；联调失败尽量补 traceId
- 不改业务代码；缺陷派给对应开发 agent / 记责任方
- 清单字段：BUG编号 / 关联用例 / 严重级别 / 标题 / 发现日 / 状态

## 5. DoD（与 registry 一致）

1. R0 记录 Excel，编号与 v1.3 企业分析用例一致  
2. BUG 清单；不通过有号+图  
3. KEYENT P0 本轮必须跑完；其余未测有跳过依据  
4. handoff 含通过率、BUG 列表、偏离、cost 四字段、`ponytail:` 行  
5. 经 MCP 推进；**勿自行 `done`**；勿 silent 加 Sprint  

## 6. 必读

- `agent-delivery/qa-test-case-spec.md` §5 / §8  
- `agent-delivery/templates/test-record-template.md`  
- `USM-ENT-KEYENT.md` + demo-ui-topic 企业分析页  
- `Design.md` §14（界面规范抽样，不扩范围）

## 7. 进度

| 日期 | 状态 |
|------|------|
| 2026-08-13 | 建单 ready → claimed（黄敬洲）→ in_progress；派单包落盘 |
| 2026-08-13 晚 | pull 后 registry 被覆盖，已重建并重新认领；环境 http://111.198.38.90:50892/ HTTP 200；已生成 R0 记录空壳 |
