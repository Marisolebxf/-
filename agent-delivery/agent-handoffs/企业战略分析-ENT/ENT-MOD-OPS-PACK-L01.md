# handoff：ENT-MOD-OPS-PACK-L01（重跑 v0.2）

- **时间**：2026-07-24
- **角色**：`[agent:product-agent]` · 监管 `human:淮政玮`
- **状态**：四件套已按全量 15 项重写，待体验/合规人评审（**task-registry 状态由父 agent 收口，本 handoff 不改 registry**）

## 范围与实现

对照真源：

1. `企业维护管理-能力全清单.md` v0.2（15 项 + tab id）
2. bid `科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.5 及企业相关子节
3. 分析配置补充：`企业完整深化规格.md#维护管理`（C1–C6）

| 分组 | 能力 | 章节 / 规格 | 本包处理 |
| --- | --- | --- | --- |
| A1 | 门户内容（企业发展） | §5.6.3 / **E-37** | **完整样例** |
| A2 | 企业主体信息维护 | §5.1.3.1 | LF 登记/占位 |
| A3 | 企业动态与区域 | §5.1.3.2 | LF 登记/占位（独立菜单） |
| A4 | 企业专家知识 | §5.2.3 | LF 登记/占位 |
| A5 | 企业发展可视化配置 | §5.4.3 / E-36 企业侧 | LF 登记/占位（**收回菜单**） |
| B1 | 企业实体生命周期 | §5.3.1.3 | LF 登记/占位 |
| B2 | 企业关系链生命周期 | §5.3.2.3 | LF 登记/占位 |
| B3 | 企业实体属性 | §5.3.3.3 | LF 登记/占位 |
| B4 | 企业相关图谱绘制 | §5.3.4 | LF 登记/占位 |
| C1–C6 | 分析配置六分区 | 深化规格·维护管理 | LF 登记/占位（**收回菜单，不得删除**） |

## 相对旧版（v0.1 三分菜单）的差异

| 维度 | 旧版 v0.1（错误） | 重跑 v0.2 |
| --- | --- | --- |
| 菜单结构 | 门户 / 主体 / 生命周期 三项 | **内容运营 5 + 图谱运营 4 + 分析配置 6** |
| 应用 OPS 六分区 | 明确「移出本包 / 不做」 | **必须列入菜单**；占位成熟度 |
| E-36 / 可视化配置 | 后置不进菜单 | **A5 列入内容运营** |
| 动态与区域 | 并入主体 | **A3 独立** |
| 专家知识 / 关系链 / 属性 / 绘制 | 遗漏 | **A4、B2–B4 列入** |
| TRACE leaves | `ENT-OPS-ENTITY` / `LIFECYCLE` 等临时名 | **`E-37` + `LF-ENT-OPS-A*`/`B*`/`C*`** |
| 完整样例 | E-37 | **仍为 E-37**（未改） |

## 偏离说明

- 非 E-37 能力尚无 catalog 正式叶子号 → TRACE 用 `LF-ENT-OPS-*` + bid/规格章节追溯（Q-OPS-01）。
- C1–C6 招标未给独立岗位名 → 产品角色标「待业务确认」；深化规格 OPS/SYS 仅实现映射（Q-OPS-03）。
- A5 与 E-36 验收边界（配置写侧 vs 前台消费）待确认（Q-OPS-04）。
- Demo 仍偏门户工作台 → as-built：保留 E-37 为样例，IA/Wireframe 要求 UX/HIFI 升全量 15 项导航。

## 产物清单

1. `agent-handoffs/产品整体定义/ENT-OPS-维护管理/USM-ENT-OPS-维护管理.md`（v0.2）
2. `…/TRACE-ENTOPS-维护管理.yaml`（v0.2，leaves=E-37+14×LF）
3. `…/IA-ENTOPS-维护管理.md`（v0.2，15 项树）
4. `…/Wireframe-ENTOPS-维护管理.md`（v0.2，含用户/角色切换与 E-37）
5. 真源清单（既有）：`企业维护管理-能力全清单.md` v0.2
6. 本 handoff：`agent-handoffs/ENT-MOD-OPS-PACK-L01.md`
7. 开放项同步：`客户决策清单跟踪表.md` Q-OPS-01~04

## 验收证据

- 结构检查命令（本地已跑，见下节输出）：
  ```text
  node .codex/skills/gkx-product-definition-review/scripts/check-product-definition-package.mjs \
    --module-id ENT-OPS --module-name 维护管理 \
    --leaf-id E-37 --leaf-name 企业发展内容管理
  ```
- 角色均可回指源章节或显式「待业务确认」（见 USM §3 / TRACE `product_roles`）
- IA / Wireframe 均列出全部 15 项；分析配置六分区未删除
- Wireframe 含「用户 / 角色切换」与内部评审模式说明，并含 E-37 完整样例 Frame

## 架构合规自检（公约 §2）

| # | 项 | 结果 |
| --- | --- | --- |
| 1 | 算法只在 Python | ✅ 本包无算法 |
| 2 | 调用链前端→Java→Python | ✅ 契约层叙述；无越层实现 |
| 3 | NebulaGraph | ✅ 图谱绘制评审态禁止 Neo4j |
| 4 | 可观测性 | N/A 设计包 |
| 5 | CI/CD | ✅ cicd skip_design_only |
| 6 | demo 不 merge lumen | ✅ |
| 7 | 共享聚合核心 | ✅ 前台消费走既有 topic/Facade；本包为写侧 IA |
| 8 | ADS/Mock 策略 | ✅ CMS/APP 分治引用 PARTITION-L01 |
| 9 | Design.md | ✅ Wireframe 指向实现交 HIFI |
| 10 | D9/D10 | ✅ 无统计 KPI；交互走查交 UX-L01 |

## cost（本重跑轮次估算）

- `actual_tokens`: 120000
- `model_used`: cursor-grok-4.5
- `actual_cost`: 0.70
- `cost_warn`: green

## 残留风险 / 开放项

| ID | 风险 | 状态 |
| --- | --- | --- |
| Q-OPS-01 | LF 能力 catalog 编目 | 🟡 |
| Q-OPS-02 | 主体写侧归属（久新 vs 本系统） | 🟡 |
| Q-OPS-03 | C1–C6 验收叶子与源岗位名 | 🟡 |
| Q-OPS-04 | A5 vs E-36 边界 | 🟡 |
| Demo 债 | 原型尚未升至 15 项导航 | 交 UX-L01 / V1-HIFI |
| 派单包债 | `ENT-MOD-OPS-PACK-L01-派单包.md` 仍写「三分菜单 / 不做 OPS」——需父 agent / coordinator 另更，本轮未改以免越权改下游话术 |

## 下一步

1. 高颖 + 郭万迎按 **15 项**评审 PACK  
2. UX-L01 / V1-HIFI 范围改为全量导航（废止三分裁剪话术）  
3. PM 推进 Q-OPS-01~04；父 agent 收口 task-registry  
