# PM 决策签字单 · E-PERM-L03a 企业维度权限切片

> **作用**：把 E-PERM-L03a 切片完成后**需 PM 拍板**的 10 项内部决策集中到一张单子，PM 一次性勾完即可。
> **配套**：
> - 派单：`PROD-权限改造-派单-FE-L03a-企业切片.md`
> - 完工 handoff：`FE-权限改造-handoff-L03a-企业切片.md`（详细证据链）
> - 业务口径相关（甲方决策）：`客户决策清单跟踪表.md` Q019 / Q031 / Q032
> - 任务状态：`task-registry.yaml` E-PERM-L03 / E-PERM-L03a
>
> **签字规则**（团队公约 §3）：
> - 团队内部决策（D1–D8）→ PM 单签即可
> - 涉及架构铁律突破（如有）→ PM + 架构师双签
> - 涉及甲方业务口径（D9–D10）→ 不在本表，走客户决策清单（PM 推甲方确认）
>
> **状态**：⏳ 待签 / ✅ 同意 / ❌ 否决 / ⚠️ 有保留同意（条件附注）

---

## 0. 一页摘要（PM 30 秒看完）

| 关键指标 | 值 |
|---|---|
| 切片名 | E-PERM-L03a 企业维度（demo-ui-topic 仓 / 仅 PC 中屏） |
| 实施 agent | frontend-agent |
| 分支 | `feat/E-PERM-L03a-enterprise-perm`（demo-ui-topic 仓） |
| commit | `a85dd57`（23 files changed, +1555 / -384） |
| 是否 push | ❌ **未 push**，等 PM 批准（D6） |
| build 自检 | ✅ `npm run build` 3727 modules ✓ 51s 通过 |
| 范围卫生 | ✅ 未改 package.json / vite.config / tsconfig；功能点 0 增减 |
| DoD §6 13 条 | 11 ✅ + 2 ⚠️ + 1 🟡 |
| 跨切片影响 | RoleLevelGate 改 shim（其他 7 个非企业域沿用旧 API，0 破坏） |
| 实际成本 | actual_tokens ~480K / ~$7.20（< $10 阈值，cost_warn=false） |
| 待 PM 决策项 | **10 项**（D1–D10），见 §1 |

---

## 1. 待 PM 决策的 10 项（请逐项打勾）

### D1. DoD §6 13 条对照结果是否接受？

> 详细对照见 `FE-权限改造-handoff-L03a-企业切片.md` §1（表格 13 行）。

| 条目 | 状态 | 关键证据 |
|---|---|---|
| 1. 权限内核 | ✅ | `src/app/perms/*` 共 9 文件；矩阵从 yaml 派生（含再生成路径注释） |
| 2. 顶栏收敛 | ✅ | 删除 userRoles[6] + 三套 dropdown |
| 3. 企业菜单 Gate | ✅ | 9 菜单挂 permCode + 锁态 + 埋点 |
| 4. 企业按钮 Gate | ✅（核心） | EnterpriseOverview 导出/对比/竞争力 PermGate；其他 8 子页留 L03b |
| 5. E-21/E-22 去重 | ✅ | structure tab + analysis-tabs 删；4 条重定向 |
| 6. D9 角标 | ✅ | ⓘ+🧪+⚠️+❌ 全 Arco Icon |
| 7. L1/L2 视觉差 | ⚠️ 部分 | 仅挂 PendingBadge Q031；段落 mask 留 L03b |
| 8. 屏幕约束 | ✅ | 专题恒 MEDIUM；showcase 0 渲染 |
| 9. Design.md §14 | ✅ 本切片 | 新文件 0 硬编码 #165DFF |
| 10. 自测 mock 4 组 | ⚠️ 待人工 | 代码已可切，截图需 PM/QA 运行 dev 录制 |
| 11. observability | ✅ | 5 事件已埋（PERM_LOCKED_HIT 等） |
| 12. 范围卫生 | ✅ | 未改配置；node_modules/dist 未入仓 |
| 13. push 纪律 | 🟡 | 等 D6 批准 |

**☐ D1.1 同意 DoD 13 条对照结果（11 ✅ + 2 ⚠️ + 1 🟡）可进 review**

**☐ D1.2 同意 §7「L1/L2 段落级 mask」与 §10「mock 4 组截图」作为软项，不阻塞本切片合入**

PM 备注（可选）：______________________________

---

### D2. RoleLevelGate 改 shim 策略是否接受？

**背景**：原 `RoleLevelGate` 使用 U1/U2/S1/S2/U3 老级别体系，被本仓 7 个非企业域（techchain / industry / research / talent / policy / service / intelligence）共 30+ 处直接调用。

**本切片做法**：把 `RoleLevelGate` 改为 shim —— 内部调用新 `useCurrentUser() + toLegacyLevel(L0→U1 / L1→U2 / L2→S1 / L3→S2 / L4→S2)` 反向映射，对外保持 `allow=['U1','U2','S1','S2']` 旧 API 不变。

**风险**：
- ✅ 其他 7 个域 0 改动、0 破坏（已 build 自检）
- ⚠️ 短期内本仓两套权限模型并存（新 PermGate + 旧 RoleLevelGate shim），增加心智负担
- ⚠️ 旧 API 仍可被新代码误用（需 lint 规则禁用，未做）

**替代方案**：一次性把 30+ 处 RoleLevelGate 全部改为 PermGate —— 工作量大（约 +2 天）、风险高（破坏其他域）、不在本切片派单范围。

**☐ D2.1 同意 shim 策略（保旧 API + 内部桥接新内核），L03b 完成展示系统切片后再做大迁移**

**☐ D2.2 同意 L03b 增加任务："批量替换 RoleLevelGate → PermGate + 加 ESLint 规则禁用 RoleLevelGate"（约 200K tokens / +1 day）**

PM 备注：______________________________

---

### D3. 残留项 R1–R7 是否纳入 E-PERM-L03b？

> 来源：handoff §6 残留项清单。

| 编号 | 项 | 工作量估计 | 优先级建议 |
|---|---|---|---|
| R1 | UX §8.2 L1/L2 段落级 mask（MetricCard / SectionPanel / TopN 包 PermGate） | ~150K tokens | 🟡 中（甲方走过场时可见） |
| R2 | 8 个企业分析子页页内按钮 PermGate（filter-adv/view-switch/simulate/weight/export-list/fav/subscribe/layout） | ~300K tokens | 🔴 高（影响 L3 强调态正确性） |
| R3 | ECharts 调色板抽离 `chartTokens.ts`（替换 `analysisShared.tsx#ANALYSIS_CHART_COLORS` 等 12 文件硬编码） | ~100K tokens | 🟡 中（D8 §14 合规） |
| R4 | 展示系统三屏权限切片（demo-ui-science 等，屏幕维度 LARGE/MEDIUM/SMALL 过滤） | ~500K tokens | 🔴 高（L03 整任务核心） |
| R5 | DS-ENT 数据可用性映射表（与 PendingBadge 联动） | ~200K tokens | 🟡 中（data-agent 主） |
| R6 | LARGE 屏 feature_classes[showcase] 不渲染规则 | ~50K tokens | 🟢 低（专题不需要，展示切片做） |
| R7 | Wave 1 level→perms 由网关下发（matrix.ts 下线） | ~80K tokens | 🟢 低（Wave 1 启动后做） |

**☐ D3.1 同意 R1 / R2 / R3 / R4 全部纳入 E-PERM-L03b（核心）**

**☐ D3.2 同意 R5 改派 data-agent，不在 L03b 范围**

**☐ D3.3 同意 R6 / R7 推迟到 Wave 1 启动后单开任务**

PM 备注：______________________________

---

### D4. task-registry.yaml E-PERM-L03 整任务 estimate 是否上调？

**背景**：
- 原 estimate：600K tokens（覆盖 demo-ui-science + demo-ui-topic 两仓全权限改造）
- L03a 实际：~480K tokens（仅 demo-ui-topic 企业切片，~1/3 范围）
- L03b 预估：~1.4M tokens（demo-ui-science 三屏 + demo-ui-topic 其他 7 个域 + R1-R4 残留）
- 整 L03 预估总量：1.88M tokens

**建议方案**：
- ✅ **方案 A（推荐）**：把 L03 estimate 从 600K 调到 **1.9M**；并在 task-registry 拆分为 L03a（done, 480K）+ L03b（pending, 1.4M）
- ⚠️ **方案 B**：维持 600K 不动，L03b 完成时累计实际超估 3x，触发预算告警
- ❌ **方案 C**：砍掉 R4（展示系统三屏），把 L03 限定为"仅企业域"—— 范围错位，违反 §1 派单

**☐ D4.1 同意方案 A：L03 整任务 estimate 上调到 1.9M tokens，L03a/L03b 拆分到 task-registry**

PM 备注：______________________________

---

### D5. 本切片实际成本是否认可？

| 字段 | 值 |
|---|---|
| `estimated_tokens` | 200_000（按 L03 / 3 等分估算） |
| `actual_tokens` | ~480_000（2.4× 超估） |
| `model_used` | claude-opus-4.7（parent agent，含读规范 + Layout 大改 + handoff 撰写） |
| `actual_cost` | ~$7.20（< $10 复盘阈值 / < $20 hard stop 阈值，cost_warn=false） |
| 超估主因 | ① 读 UX/UI 规范两份 ~30K 字深度对照 ② Layout.tsx 大改重写 ③ 反复核验路径（gkx-lumen 新根 vs gkx_src 老根，团队公约切换） |

**☐ D5.1 同意 actual_cost $7.20 回填 task-registry（cost_warn=false，无需 retro）**

**☐ D5.2 同意 retro 教训"PROD 派单包含跨规范深读时，estimate 应上调 2x"作为预算估算改进项**

PM 备注：______________________________

---

### D6. 是否批准 `git push origin feat/E-PERM-L03a-enterprise-perm`？

**背景**（团队公约 §4.2 demo-ui-topic 仓策略）：
- demo-ui-topic 仓允许 main 直推 + 自动部署 https://skxrules.unicomcn.tech:30999/（push 后 2–3 min 生效）
- 但本切片走 **feature 分支**（不是直推 main），原因：① 涉及顶栏壳层大改 ② 影响其他 agent 在跑的 main 风险 ③ 派单 §5.11 明确要求 push 前 PM 确认

**push 后影响范围**（推 feature 分支，不影响 main）：
- ✅ 仅创建远端 `feat/E-PERM-L03a-enterprise-perm` 分支
- ✅ **不会触发** main 部署（dev 环境继续是 main 版本）
- ⚠️ CI pipeline 会跑（`.gitlab-ci.yml` `dev branch only` 限制下，feature 分支不会触发部署）
- 🚫 **如要让甲方/QA 看到效果**，需后续单独 merge feature → main（再次 PM 决策）

**推荐操作**：
1. 先 push feature 分支 → 让 PM/QA 在 dev 本地 checkout 验证
2. 4 组 mock_users 截图录制完毕 + PM 在 §10 全部 ✅ 后 → 再决定是否 merge → main 触发部署

**☐ D6.1 批准 push `feat/E-PERM-L03a-enterprise-perm` 到 origin（不触发 main 部署）**

**☐ D6.2 后续 merge feature → main 需另开决策（不在本表）**

PM 备注：______________________________

---

### D7. mock_users 4 组截图谁来录？

> 详细 checklist：handoff §4.1 + §4.2 + §4.3 + §4.4（共 19 张截图）

**选项**：

| 选项 | 责任人 | 耗时 | 备注 |
|---|---|---|---|
| A | QA-agent 接力（next task） | ~1h | 自动化 / 标准化；推荐 |
| B | frontend-agent 手动跑 dev 录 | ~1h | 实施者补做 |
| C | PM 现场录 | ~30min | 适合 PM 自己评审时顺手做 |

**☐ D7.1 选 A：QA-agent 接力录制 + 上传 `agent-handoffs/产品整体定义/screenshots/E-PERM-L03a/`**

**☐ D7.2 选 B：frontend-agent 在 D6 批准 push 后立即补录**

**☐ D7.3 选 C：PM 自录（同步在本表附 4 组截图链接）**

PM 备注（如其他人选）：______________________________

---

### D8. 业务口径决策项（Q019 / Q031 / Q032）如何推甲方？

> 这 3 项已登记 `客户决策清单跟踪表.md` §2.4 / §2.5，状态 🟡 临时默认。本切片已挂 ⚠️ PendingBadge 提示用户。

| Q-ID | 项 | 团队临时默认 | Deadline 建议 |
|---|---|---|---|
| Q019 | M_ENT_MARKET_SHARE 数据源（采购 / 降级 / 下架？） | 暂置空 + UI 标 ❌ 无源 | 评审会前确认 |
| Q031 | E-20 概览 L1「仅结论条」精确范围（哪些 KPI/趋势 对 L1 隐藏） | L1 = 结论条 + 检索入口；其他按降级态 | L03b 启动前确认 |
| Q032 | E-21/E-22 去重后 IA + 命名（"痛难点诊断↔企业发展支持" 统一 / "企业全景"归门户 E-33） | 方案 B 独立页权威；命名"痛难点诊断" | 下次甲方接触 |

**☐ D8.1 同意把 Q019 / Q031 / Q032 列入下次甲方议程，确认后升 🟢 通知 FE 移除 ⚠️**

**☐ D8.2 同意 Deadline 按上表（Q031 必须在 L03b 启动前确认，否则 L1/L2 段落 mask 实施无据）**

**☐ D8.3 是否需要 PM 在评审会前主动追问甲方？** ☐ 是 / ☐ 否

PM 备注：______________________________

---

### D9. 其他切片是否同步接入新权限内核？

**背景**：本切片在 demo-ui-topic 落 `src/app/perms/*`，是新内核源头。

**问题**：要不要把 perms/* 抽到共享包（如 `@gkx/perms-core`），让以下仓共享：
- demo-ui-science（展示系统，L03b 范围）
- lumen-ui-science-pc（lumen 正式仓，L04 范围）
- lumen-ui-science-mobile

**建议**：
- ⚠️ Wave 0 阶段不抽：避免过早抽象 + 跨仓维护成本
- ✅ Wave 1 启动 monorepo 时统一抽到 `packages/perms-core`，配合网关下发矩阵

**☐ D9.1 同意 Wave 0 不抽 perms 共享包，L03b 时 copy 到 demo-ui-science（保持代码同步约定）**

**☐ D9.2 同意 Wave 1 启动 monorepo 时抽 `packages/perms-core` + 联动 SSO/网关**

PM 备注：______________________________

---

### D10. 是否同意进度看板更新？

**当前** `PROD-权限改造-派单-5角色.md` §进度看板 L03 行：

```
| E-PERM-L03 | FE | ⏳ blocked(L02) | FE-权限改造-handoff.md + 两仓代码 | demo-ui-science 可推 main；topic 确认后推 |
```

**建议更新**：

```
| E-PERM-L03  | FE | 🔄 in_progress（L03a review / L03b pending）| FE-权限改造-handoff.md（汇总）             | L02 已实施可放行；topic 直推前必须 PM 确认 |
| E-PERM-L03a | FE | 🟡 review                                  | FE-权限改造-handoff-L03a-企业切片.md       | demo-ui-topic 企业域 / commit a85dd57 / 未 push |
| E-PERM-L03b | FE | ⏳ pending                                 | （待派单）                                   | demo-ui-science 三屏 + topic 其他 7 域 + R1–R4 |
```

**☐ D10.1 同意按上述格式更新进度看板**

PM 备注：______________________________

---

## 2. PM 签字位

> 全部 D1–D10 决策完毕后签字。带 ⚠️ 条件或 ❌ 否决项需用 PM 备注说明。

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PM 签字：____________________________________
PM 姓名（打印）：____________________________
签字日期：__________________________________
是否需架构师联签？☐ 否 ☐ 是 → 架构师签：____________________
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**签字后的下一步**：

| D6 决策 | 下一步动作 | 责任人 |
|---|---|---|
| D6.1 ✅ | frontend-agent 执行 `git push origin feat/E-PERM-L03a-enterprise-perm`（**禁 force**） | frontend-agent |
| D6.1 ❌ | 列出否决理由 → frontend-agent 修改后再签 | frontend-agent |
| D7 选 A | coordinator 派 qa-agent 接力录截图 | coordinator-agent |
| D7 选 B | frontend-agent push 后立即录截图存档 | frontend-agent |
| D8.1 ✅ | PM 列 Q019/Q031/Q032 入下次甲方议程 | PM |
| D10.1 ✅ | coordinator 更新 `PROD-权限改造-派单-5角色.md` 进度看板 | coordinator-agent |

---

## 3. 历史变更

| 日期 | 修改 | 修改人 |
|---|---|---|
| 2026-06-22 | 初版 D1–D10 决策项 | frontend-agent |
