# ENT-MOD-OPS-PACK-L01 派单包 · 企业·维护管理（全量 15 项）

> **性质**：coordinator / product 派单容器  
> **日期**：2026-07-24 · **升版** v0.2（纠正旧「三分菜单 / 不做 OPS 六分区」）  
> **监管人**：`human:淮政玮`  
> **PACK / UX / V1-HIFI 状态**：均 `done`（重跑收口）  
> **作者**：`[agent:product-agent]` / 父会话同步

---

## 0. 背景结论（给所有下游）

企业中心「维护管理」按《企业维护管理-能力全清单》**全量 15 项**：

| 分组 | 项数 | 说明 |
| --- | --- | --- |
| 内容运营（CMS） | 5 | 门户 / 主体 / 动态与区域 / 专家知识 / 可视化配置 |
| 图谱运营 | 4 | 实体生命周期 / 关系链生命周期 / 实体属性 / 图谱绘制 |
| 分析配置（APP OPS） | 6 | 字段指标 / 模型规则 / 数据批次 / 报告模板 / 权限脱敏 / 审计 |

完整样例叶子仍为 **E-37 门户内容**；分析配置六分区**必须列入菜单**（不得再误剔）。E-36 与 A5 边界见开放项 Q-OPS-04。

四件套 + UX + 全清单路径：

```text
agent-handoffs/产品整体定义/ENT-OPS-维护管理/
├── 企业维护管理-能力全清单.md
├── USM-ENT-OPS-维护管理.md
├── TRACE-ENTOPS-维护管理.yaml
├── IA-ENTOPS-维护管理.md
├── Wireframe-ENTOPS-维护管理.md
└── UX-SPEC-ENT-OPS.md
```

任务链：

| Task | Agent | 状态 | 依赖 |
| --- | --- | --- | --- |
| ENT-MOD-OPS-PACK-L01 | product-agent | **done** | — |
| ENT-MOD-OPS-UX-L01 | ux-agent | **done** | PACK |
| ENT-MOD-OPS-V1-HIFI | ui-agent | **done** | PACK |
| ENT-MOD-OPS-PDR-G1 | product-agent | blocked | 门1正式会签 |

原型：`/enterprise-center/maintenance?tab=<id>`（需 L4 / `MENU_ENT_MAINTENANCE`）；冻结版 **HIFI-ENT-OPS-medium-v0.2**。

---

## 1. 派单话术 A · 体验 Owner 人评审 PACK（粘贴）

```markdown
/goal human-review
收件：高颖（体验 Owner）+ 郭万迎（合规 Owner）
任务：ENT-MOD-OPS-PACK-L01 人评审（不改代码）
目标：确认企业·维护管理全量 15 项四件套可支撑门1
必读：
  - agent-handoffs/产品整体定义/ENT-OPS-维护管理/企业维护管理-能力全清单.md
  - USM / TRACE / IA / Wireframe 同目录（v0.2）
核对要点：
  1. 角色是否均可回指 bid 源章节
  2. 15 项是否齐全；分析配置六分区未误剔
  3. E-37 完整样例 + 其余占位成熟度是否清晰
  4. Q-OPS-01~04 是否已挂决策清单
产出：评审意见（通过 / 修订项）
```

---

## 2. 派单话术 B · UX-L01（已完成，归档参考）

```markdown
/goal ux-agent
任务 ID：ENT-MOD-OPS-UX-L01（重跑已 done）
范围：全量 15 项导航 / 空态 / 权限态；不得再写「排除 OPS 六分区」
产物：UX-SPEC-ENT-OPS.md v0.2 + ENT-MOD-OPS-UX-L01.md
```

---

## 3. 派单话术 C · V1-HIFI（已完成，归档参考）

```markdown
/goal ui-agent
任务 ID：ENT-MOD-OPS-V1-HIFI（重跑已 done）
目标：左侧 15 项 + ?tab= 同步；portal/entity/entity_dynamics/lifecycle 可演示；其余占位不可删
产物：会签单 v0.2（HIFI-ENT-OPS-medium-v0.2）；H-04/H-08 🟡 待高颖+孔东补签
仓库：repos/demo-ui-topic（本轮未 commit/push）
```

---

## 4. 派单话术 D · 门 1 PDR（下一闸）

```markdown
/goal product-agent
任务 ID：ENT-MOD-OPS-PDR-G1
依赖：PACK + UX-L01 + V1-HIFI 均 done；待正式会签
主持：human:郭万迎；必到：高颖、何老师/唐绍祖、徐滕强/李伟
产出：PM-PDR-ENT-OPS-评审纪要.md；PDR-01~PDR-14
范围卫生：全量 15 项验收；开放项 Q-OPS-01~04 + Q020/Q029/Q041/Q048–Q050
```

---

## 5. 开放项（已同步决策清单）

| ID | 摘要 |
| --- | --- |
| Q-OPS-01 | §5.1.3 / §5.3.1.3 等 LF 能力 catalog 编目 |
| Q-OPS-02 | 企业主体写侧：久新独占 vs 本系统可写运营层（关联 Q050） |
| Q-OPS-03 | C1–C6 验收叶子与源岗位名（待业务确认） |
| Q-OPS-04 | A5 可视化配置 vs E-36 边界 |
