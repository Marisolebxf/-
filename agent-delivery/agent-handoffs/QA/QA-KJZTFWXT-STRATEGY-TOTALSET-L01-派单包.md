# 派单包：QA-KJZTFWXT-STRATEGY-TOTALSET-L01

- **派单方**：coordinator（本会话 · 2026-08-13）
- **执行 / 监管**：`human:黄敬洲`（可带 `qa-agent`；claimed_by 已写真人）
- **Agent 角色**：`qa-agent`
- **状态**：`in_progress`（2026-08-13 黄敬洲已开工） · `claim_type` 语义 = coordinator_dispatch
- **仓 / 产物落点**：`agent-delivery/qa/total-set/KJZTFWXT/`
- **Sprint**：未挂 `2026-W32` committed（避免 silent 加活；需进 Sprint 请 PM 写入 stretch）
- **强度**：ponytail full（写测 / 生成脚本）

---

## 1. 目标

为 **科技专题战略分析**（L3）五个四级编写 **符合总集模板** 的 FUNC 用例 Excel，并交付可签收 handoff。

四级：综合智能分析 / 政策分析 / 企业分析 / 产业链分析 / 产业服务链分析。

**KEYENT（E-20/E-21/E-22）为 P0 标杆**：对照 `USM-ENT-KEYENT.md` 验收场景 + `demo-ui-topic` 原型交互，禁止只用功能清单两句话来回组合。

## 2. 产物（本单约定：仅总集 Excel；MD 可选）

| 产物 | 路径 |
|------|------|
| 五份 Excel | `qa/total-set/KJZTFWXT/科技专题战略分析-v1.3/` |
| 编号 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-#####`（每四级文件独立起编） |
| 列 | 总集 17 列 + 右侧 GKX 扩展列（用户故事 / USM-AC / bid / TRACE / route / 任务ID） |
| handoff | `agent-handoffs/QA/QA-KJZTFWXT-STRATEGY-TOTALSET-L01.md`（尚未定稿） |

基线：v1.0–v1.2 归档；当前工作稿 **v1.3**。生成：`_gen_zt_testcases_v13.py` + `product-pack-index-zt-strategy.yaml` + `prototype-catalog-zt-strategy.yaml`。

## 2.1 当前进度（2026-08-13 晚）

| 版本 | 目录 | 规模 | 含义 | 本单用法 |
|------|------|------|------|----------|
| v1.0 | `qa/total-set/KJZTFWXT/科技专题战略分析-v1.0/` | ~1322 | 功能清单拆分 + 通用质量属性 | 基线归档 |
| v1.1 | `…/科技专题战略分析-v1.1/` | 1696（非通用 1300 + 通用 396） | 需规全覆盖 + bid-reference 设计句 | 覆盖对照 |
| v1.2 | `…/科技专题战略分析-v1.2/` | 1661（非通用 1265 + 通用 396；原型向 ~59） | 原型 UI 优先，八件套未系统进用例 | 对照稿 |
| **v1.3** | `…/科技专题战略分析-v1.3/` | **1696**（非通用 **1300** + 通用 396；原型向 **235**；八件套向 **985**） | 功能清单定数量；八件套出要点；冲突以原型为准 | **当前工作稿** |

v1.3 分册：综合智能 180（原型 54 / 八件套 72）/ 政策 294（21 / 231）/ 企业 538（90 / 302）/ 产业链 384（36 / 258）/ 产业服务链 300（34 / 122）。

**已完成（v1.3）：** 总集列 + GKX 扩展列；L5/L6 配额非通用 1300；USM 故事/主路径/AC/异常 + TRACE/IA/UX；KEYENT 侧栏类型/领域分析；产业链/服务链原型点已挂 catalog；无「布局区块-N」。

**v1.3 文案修订（2026-08-13 晚）：** 前置改为「测试环境可访问」；步骤改为登录测试环境 + 业务控件名；去掉「确认路由」「观察 Drawer/URL」「与八件套冲突时以原型为准」「每条都写非白屏」。路由仅保留在 GKX 扩展列。

**拆分基础完成（2026-08-13 晚）：** v1.3 五册已出且文案已按评审修订。本单正式 handoff 未交，仍 `in_progress`，勿自行 `done`。

**执行已拆出：** `QA-KJZTFWXT-STRATEGY-ENT-EXEC-L01`（企业分析 R0：测试记录 + BUG 清单）。

**本单还要继续：**

1. 写正式 handoff `QA-KJZTFWXT-STRATEGY-TOTALSET-L01.md`（含 cost / ponytail: full）。  
2. 勿 silent 加入 Sprint；勿自行 `done`。

## 3. 编写原则

1. 设计来源：USM → bid-reference → TRACE/IA → Design §14（不扩范围）
2. 先在 `demo-ui-topic` 找对应路由 / Tab / Drawer / ContextBar，再写步骤
3. 步骤写导航路径与控件；预期写可观察 UI 状态
4. 通用质量属性每六级模块保留（入口 / 权限 / 加载 / 空态 / 异常 / 一致性）
5. KEYENT 注意最新导航：`/enterprise-center/key-enterprise-analysis?workspace=type|domain&view=type|domain`（侧栏两项，兼容旧 `view=`）

## 4. DoD（与 registry 一致）

1. 五份总集 FUNC Excel，列与编号合规  
2. 拆分按 USM/原型；KEYENT P0 标杆  
3. 步骤可执行、预期可判定；Mock 边界可辨  
4. handoff 含范围 / 偏离 / 产物 / 架构合规 / cost 四字段 / `ponytail:` 行  
5. 经 MCP 推进状态；**勿自行 `done`**

## 5. 必读

- `agent-delivery/qa-test-case-spec.md`（编号 FUNC；本单产物裁剪为 Excel-only）
- `agent-delivery/agent-handoffs/产品整体定义/E-20_E-22-重点企业分析/USM-ENT-KEYENT.md`
- `bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.2
- `Design.md` §14（筛选控件 ≤400px；二级圆角 Tab class）
- `repos/demo-ui-topic`（原型真源）
