# TOPIC-SYNTH-R3 修正 · E8 三叶子 Pack1 派单总包

> **性质**：coordinator / product 派单容器（定义轨重开）  
> **日期**：2026-08-10  
> **触发**：修正 `TOPIC-SYNTH-R3` 单叶 `SYNTH-REGION` 收口；按系统方案二级功能 + 算法库「产业综合分析模型构建」拆为三叶子 Pack1  
> **作者**：`[agent:coordinator]`  
> **监管拍板**：`human:淮政玮`（三叶子 Pack1 监管人；R3 状态不回写）

---

## 0. 修正结论（给所有下游）

| 项 | 旧（R3） | 新（本总包） |
| --- | --- | --- |
| 叶子数 | 1：`SYNTH-REGION`（8.1+8.2+8.3 捆死） | **3**：活力 / 要素 / 协同 |
| 产品定义权威 | `SYNTH-REGION-区域创新分析/` 五件套 | 三叶子各自交互五件套；**旧目录降级为历史参照，不再是执行契约** |
| 算法真源 | 系统方案为主，算法口径偏演示态 | **强制对齐** `科技专题服务算法库.md` §`1.1.1.1.1.1.1.10`「产业综合分析模型构建」对应模型小节 |
| 任务形态 | `TOPIC-SYNTH-R3`（feature：五件套+实现捆单） | 三条 **`definition` / Pack1**：只出 IA·TRACE·USM·UX-SPEC·Wireframe；**不含** demo 重实现 / V1-HIFI |

### 0.1 对 `TOPIC-SYNTH-R3` 的处置

**按监管确认：不回写 R3 状态。** 产品定义权威以三叶子 Pack1 为准；R3 实现产物仍可作历史/UX 参照。

### 0.2 双源对齐铁律

| 层级 | 真源文件 | 用法 |
| --- | --- | --- |
| 产品模块 / 业务任务 / 服务对象 | `bid-reference/科技信息展示系统和科技专题服务系统.md` §`1.1.1.2.4.2.8`（及 `.8.1` / `.8.2` / `.8.3`） | USM 角色、故事、验收单元 |
| 算法 / 指标 / 模型 I/O | `bid-reference/科技专题服务算法库.md` §`1.1.1.1.1.1.1.10` 及对应子节 | TRACE `implementation`、metric 公式占位、开放项算法卡 |

禁止只用系统方案拍算法口径；禁止用旧 `SYNTH-REGION` 演示权重复制为「已对齐算法库」。

---

## 1. 三叶子划分

| # | 叶子代号 | 中文名 | 系统方案 | 算法库锚点 | Pack1 任务 ID | 目录 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `SYNTH-VITALITY` | 区域创新活力分析 | §8.1（.1.1–.1.3） | §10.5 区域创新活力综合分析模型；维度输入参照 §10.1–10.4 | `SYNTH-MOD-VITALITY-PACK-L01` | `SYNTH-VITALITY-区域创新活力分析/` |
| 2 | `SYNTH-ELEMENT` | 区域创新要素分析 | §8.2（.2.1–.2.3） | §10.6 类型 · §10.7 层次 · §10.8 领域 · §10.9 综合 | `SYNTH-MOD-ELEMENT-PACK-L01` | `SYNTH-ELEMENT-区域创新要素分析/` |
| 3 | `SYNTH-COLLAB` | 区域创新协同分析 | §8.3（.3.1–.3.3） | §10.10 区域创新协同分析模型（完整度/中心度/密度） | `SYNTH-MOD-COLLAB-PACK-L01` | `SYNTH-COLLAB-区域创新协同分析/` |

共享上下文（区域 / 对比范围 / 时间窗）写在父 README 与各 TRACE `cross_leaf_contracts`，**不得**再合并回单叶以免切断算法专章边界。

### 1.1 Pack1 交付物（本用户口径 = 交互五件套）

每个叶子目录必须产出并可独立审阅：

1. `IA-{LEAF}.md`  
2. `TRACE-{LEAF}.yaml`  
3. `USM-{LEAF}.md`  
4. `UX-SPEC-{LEAF}.md`  
5. `Wireframe-{LEAF}.md`  

> 规程消歧：门 1 正式「五件套」编号仍以 `产品定义评审规程.md` 为准（USM/TRACE/IA+wireframe/指标卡/开放项）。本批 Pack1 **先交交互五件套**；④指标语义卡 / ⑤开放项 catalog 另开 `METRIC-OPEN-L01`（可并行规划，不阻塞本 Pack 开工）。

---

## 2. 任务链（建议 registry）

| Task | task_type | agent | 监管建议 | depends_on | effort / difficulty |
| --- | --- | --- | --- | --- | --- |
| `SYNTH-MOD-VITALITY-PACK-L01` | definition | product-agent | human:淮政玮 | —（可与另两叶并行） | 5 / M |
| `SYNTH-MOD-ELEMENT-PACK-L01` | definition | product-agent | human:淮政玮 | — | 8 / L |
| `SYNTH-MOD-COLLAB-PACK-L01` | definition | product-agent | human:淮政玮 | — | 5 / M |
| （后续）`SYNTH-MOD-*-UX-L01` | definition | ux-agent | human:淮政玮 | 若 Pack 已含 UX-SPEC 则 **跳过或改为审阅修订** | — |
| （后续）`SYNTH-MOD-*-METRIC-OPEN-L01` | definition | algorithm + data | human:唐绍祖 | PACK done | — |
| （后续）`SYNTH-MOD-*-V1-HIFI` | feature | ui/frontend | human:淮政玮 | PACK +（建议）METRIC-OPEN 启动 | — |
| （后续）`SYNTH-MOD-*-PDR-G1` | definition | product-agent | human:郭万迎 | PACK + METRIC-OPEN + UX 可评 | — |

三叶 **允许并行**；共享区域上下文契约须在三份 TRACE 互相引用同一 `CT-SYN-CTX`（新建），避免三套互斥状态机。

---

## 3. 分派单包索引

| 叶子 | 派单包 |
| --- | --- |
| 活力 | `SYNTH-MOD-VITALITY-PACK-L01-派单包.md` |
| 要素 | `SYNTH-MOD-ELEMENT-PACK-L01-派单包.md` |
| 协同 | `SYNTH-MOD-COLLAB-PACK-L01-派单包.md` |
| registry 粘贴草案 | `SYNTH-三叶子-PACK-L01-registry-提案.md` |

---

## 4. 开放项前缀（预分配，写入决策清单时落表）

| 前缀 | 叶子 | 预留主题 |
| --- | --- | --- |
| `Q-SYNTH-V-*` | 活力 | 四维权重、归一化基准、活力指数合成（承接并细化原 Q-SYNTH-01） |
| `Q-SYNTH-E-*` | 要素 | 类型/层次/领域权重、要素指数合成、贡献路径算法（承接 Q-SYNTH-02） |
| `Q-SYNTH-C-*` | 协同 | 完整度/中心度/密度定义与合成、协同-产出相关（承接 Q-SYNTH-03） |

原 `Q-SYNTH-01/02/03` **保留编号**，在新 TRACE 中 `supersedes` / `refines` 映射，禁止静默改号导致决策清单断链。

---

## 5. 协调动作清单

- [x] PM/淮政玮确认拆叶方案（监管人=淮政玮；不回写 R3；三单 ready）  
- [x] MCP CLI `task-create` ×3 + `supervised_by=human:淮政玮`  
- [x] 更新本目录 `README.md`  
- [x] 旧 `SYNTH-REGION-*` 顶栏加废止说明  
- [ ] 三叶 Pack 派 `product-agent` 认领开工  
- [x] 活力叶 Pack done 后已建并认领 METRIC-OPEN（王惠）+ V1-HIFI（淮政玮）；PDR-G1 仍待排  
- [ ] 要素/协同叶 Pack done 后排各自 METRIC-OPEN / V1-HIFI / PDR-G1  
