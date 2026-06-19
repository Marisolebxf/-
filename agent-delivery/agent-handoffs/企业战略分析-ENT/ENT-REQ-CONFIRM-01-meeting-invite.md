# ENT-REQ-CONFIRM-01 · 会议邀请（草稿）

> coordinator-agent 起草 · 2026-06-19  
> task-registry：`ENT-REQ-CONFIRM-01` · Epic `E-ENT-PROTOTYPE`  
> 陪审包：`DATA-ENT-prototype-jury-pack.md` @ commit `7c9ac7a`

---

## 会议基本信息（PM 填写后发出）

| 字段 | 内容 |
|------|------|
| **主题** | ENT 企业分析原型需求确认 · E-20~E-30 + Q010~Q019 |
| **时长** | 90 分钟 |
| **形式** | 线下 / 腾讯会议（PM 定） |
| **建议时间** | _PM 填写，如 2026-06-24（周二）14:00–15:30_ |
| **task-id** | ENT-REQ-CONFIRM-01 |

---

## 参会人

| 角色 | 姓名 | 职责 |
|------|------|------|
| **PM（主持）** | _填写_ | 排期、记决策、会后更新决策清单 |
| **UE lead** | _填写_ | topic_demo 逐页演示（9 页 /enterprise/*） |
| **数据 lead** | _填写_ | 讲 ODS/ADS 可行性、⚠️/❌ 指标 |
| **算法 lead** | _填写_ | 讲 🔧 算法方案、权重/阈值待确认项 |
| **coordinator** | _填写_ | 对照陪审包、收签收表、更新 task-registry |
| **甲方**（可选） | _PM 定_ | Q010~Q019 现场拍板或书面确认 |
| **架构师**（可选） | _按需_ | 范围 ±10%、合并 Tab 等架构边界 |

---

## 会前必读（30 min）

1. `agent-handoffs/企业战略分析-ENT/DATA-ENT-prototype-jury-pack.md`（陪审包全文）
2. `agent-handoffs/企业战略分析-ENT/ENT-delivery-summary.md` §2.2 路由表
3. `客户决策清单跟踪表.md` §2.4（Q010~Q019）
4. （UE）本地或 demo2 打开 topic_demo `feat/ent-elements-build`

---

## 议程（90 min · 对齐陪审包 §6）

| 时段 | 内容 | 主讲 |
|------|------|------|
| 0–10 min | 目标与范围：E-20~E-30、Wave 0 Mock 标注、本轮不含 E-31~E-35 | PM |
| 10–25 min | P0/P1/P2 演示 + Q010/Q011/Q012/Q013 | UE + 数据 |
| 25–40 min | P3/P5 演示 + Q014/Q016/**Q019（必拍板）** | UE + 算法 |
| 40–55 min | P6/P8 演示 + Q015/Q017 | UE + 算法 |
| 55–70 min | P9/P10 演示 + Q018/Q014 | UE + 算法 |
| 70–85 min | 决策项逐条确认（陪审包 §4 表格） | PM |
| 85–90 min | 页面三态签收（§7）+ 后续 task 计划 | PM |

---

## 演示路径清单（UE 会前自检）

| E-XX | 路由 | 页面 |
|------|------|------|
| E-20 | `/enterprise/overview` | 战略驾驶舱 |
| E-21 | `/enterprise/type-distribution` | 类型分布 |
| E-22 | `/enterprise/domain-distribution` | 领域分布 |
| E-23/24 | `/enterprise/capability` | 技术力/商业力 Tab |
| E-25 | `/enterprise/status-analysis` | 深圳现状 + 城市对标 |
| E-26/27 | `/enterprise/recommendation` | 招引/培育 Tab |
| E-28 | `/enterprise/supply-chain` | 供应链 |
| E-29 | `/enterprise/pain-points` | 痛难点 |
| E-30 | `/enterprise/competitiveness` | 竞争力 |

> ⚠️ `topic_demo` 分支 `feat/ent-elements-build` 若未 push，请 UE 会前确认本地可演示或 push 至 demo2。

---

## 会后产出（DoD）

- [ ] `客户决策清单跟踪表.md` §2.4 更新（Q010~Q019 状态 + 甲方决策证据链接）
- [ ] `ENT-REQ-CONFIRM-01-signoff.md`（纪要 + §7 签收表 + 待跟进 task）
- [ ] task-registry `ENT-REQ-CONFIRM-01` → `done`
- [ ] 🟢 确认项 → 数据/算法更新 cfg_metric + formula（另开 follow-up task）

---

## 微信/邮件正文（复制即用）

**主题**：【ENT-REQ-CONFIRM-01】企业分析原型需求确认会 · E-20~E-30

各位好，

数据/算法侧已提交「原型陪审包」，请安排 **90 分钟** 企业分析原型需求确认会。

**目标**：
1. 确认分析层 9 页（E-20~E-30）功能范围与 bid 一致
2. 对 Q010~Q019 共 10 项业务口径确认或书面认可临时默认
3. 每页给出「确认 / 待改 / 暂缓」三态

**会前材料**（GitLab / 本地）：
- `agent-delivery/agent-handoffs/企业战略分析-ENT/DATA-ENT-prototype-jury-pack.md`
- `agent-delivery/agent-handoffs/企业战略分析-ENT/ENT-delivery-summary.md`

**会中分工**：UE 演示 · PM 记决策 · 数据/算法讲指标可行性

**建议时间**：_PM 填写_

请确认参会并会前阅读陪审包 §3–§4。谢谢。

---

**维护**：会议结束后由 PM 归档；coordinator 验收 handoff 并关闭 task。
