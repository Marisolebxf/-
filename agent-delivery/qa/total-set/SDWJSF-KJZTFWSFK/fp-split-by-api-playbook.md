# 算法库 · by-api 功能点拆分编排（F0～F4）

- **系统**：`SDWJSF/KJZTFWSFK` 科技专题服务算法库  
- **原则**：[`科技专题服务算法库-功能点拆分原则-by-api.md`](科技专题服务算法库-功能点拆分原则-by-api.md) **v0.2.1**（功能点列名保留；**算法环节** + **具体描述**；无数据源对接；入参一行一环节）  
- **总索引**：[`qa/algo-lib-playbook-index.md`](../../../algo-lib-playbook-index.md)  
- **任务（拟）**：`QA-KJZTFWALGO-FP-BY-API-L01`  
- **工作单元**：**60 条六级需规 = 60 个子 agent**（L01–L60），中间稿目录 `fp-split-by-api-run/`

---

## 角色分工

| 角色 | 做什么 | 不做什么 |
|------|--------|----------|
| **人** | 金样 L01、L13 签收；F4 合表交付签字 | — |
| **父 agent（主对话）** | 读索引/本 playbook/队列；派子 agent；验收 review；更新 `01-task-list.md`、`00-control.md`；归纳条数；F4 触发校验与合表 | 不写 `work/Lxx.md` 功能点表；不一条脚本改 60 份 work |
| **子 agent** | 只读 `prompts/Lxx.md` + 原则；产出本六级 `work` + `review`；5b 登记 orphan | 不拆其它六级；不合表；不读算法实现仓 |

---

## F0 · 准备

1. 确认原则 **0.2.1**、归档 `fp-split-by-api-run-v0-202609/` 存在。  
2. 刷新 catalog 快照：

   ```bash
   python3 agent-delivery/scripts/_dump_algo_apiview_catalog.py
   ```

3. 生成 60 份提示词（不写 work）：

   ```bash
   python3 agent-delivery/scripts/_gen_kjztfwalgo_fp_by_api_prompts.py
   ```

4. 核对 `01-task-list.md`：60 行均为 `pending`（金样 L01/L13 标注 `gold`）。  
5. 更新 `00-control.md` 阶段 = **F0 完成，待 F1**。

**产物**：`prompts/L01.md` … `L60.md`、`_catalog-snapshot.md`、队列与控制面。

---

## F1 · 金样 L01（产业链基础指标 · `chain.basic`）

| 项 | 内容 |
|----|------|
| 提示词 | `fp-split-by-api-run/prompts/L01.md` |
| 子 agent 数 | **1** |
| 验收 | `review/L01.md` 结论通过；表头条数=表行；扩展列齐全；本文件内 `endpoint_id`+`field_key` 无重复 |
| 人闸门 | 人确认拆法可推广 → `01-task-list` L01=`done`，进入 F2 |

子 agent 必读：原则 2b/8a/12a；按 catalog `params` + `responseFields` 字段级拆行；`catalog_status` 按 7b。

---

## F2 · 金样 L13（产业全要素图谱 API · 4A）

| 项 | 内容 |
|----|------|
| 提示词 | `prompts/L13.md` |
| 子 agent 数 | **1** |
| 额外产物 | 建议 `fp-split-by-api-run/memo/L13-graph-endpoint-closure.md`：**图谱类 `endpoint.id` 封闭清单**（供 L05–L12 与全库 4A 对照） |
| 验收 | 图谱 endpoint 主挂 L13；review 说明与 `chain.panorama` / `*.graph` 等边界 |
| 人闸门 | 人确认封闭清单 → L13=`done`，**允许 F3** |

**L05–L12**：子 agent 按提示词 **4A** — 接口扩展列留空，review 写「契约见 L13」，仅按需规写语义行（`req_only` 等）。

---

## F3 · 并行 58 路（L02–L12、L14–L60）

1. 父读 `01-task-list.md`，只对 `pending` 且非闸门阻塞的 ID 派单。  
2. **每条六级 = 一个新子会话**，Kickoff 用总索引 §4，`Lxx` 替换为当前 ID。  
3. 建议分批（如 T01 四条 → 图谱段 → T03…），每批父验收后再开下一批。  
4. 子完成后父检查：
   - `work/Lxx.md` 存在且仅含本六级；
   - `review/Lxx.md` 含「误用实现仓」= 否；
   - L05–L12 符合 4A。  
5. 更新队列 `done`；全 60 `done` 后进入 F4。

**禁止**：父对话代写多份 work；单脚本生成 60 份功能点表冒充子 agent。

---

## F4 · 全库校验与合表

| 步 | 说明 |
|----|------|
| 校验 3c | 全库 `endpoint_id` + `field_key` 唯一（脚本 `_validate_*` 待建） |
| 校验 7b | `catalog_status` 仅 `live`/`unavailable`/`mock`/`req_only` |
| 5b | `catalog-orphan-registry.yaml` 条目未进主表 |
| 合表 | `6.国际科技信息中心项目_科技专题服务算法库_功能点拆分-by-api_v1.xlsx` + 12a 扩展列 |
| 禁止 | 覆盖 `…功能点拆分_v2.xlsx`；merge v0 归档稿 |

父控：校验绿后执行合表（可派独立子任务专做 Excel，仍不算「60 路拆分」）。

---

## 子 agent 细则（执行真源）

1. 以 **`prompts/Lxx.md` 全文** 为准（含需规原文 + 绑定 endpoint 块）。  
2. 原则 **0.2**：字段级；`metricIds` 不单独拆行。  
3. 输出路径仅：
   - `fp-split-by-api-run/work/Lxx.md`
   - `fp-split-by-api-run/review/Lxx.md`  
4. work 表须含扩展列（Markdown 表头即可，合表脚本后映射 Excel）。  
5. catalog 有、需规无 → 登记 `catalog-orphan-registry.yaml`，不写进 work 主表。

---

## 与需规口径任务关系

| 任务 | 关系 |
|------|------|
| `QA-KJZTFWALGO-FUNCLIST-SPLIT-L01` | 需规 v2 / `fp-split-run/` — **内部对照**，不替代 by-api 交付 |
| `QA-KJZTFWALGO-FP-BY-API-L01` | 本 playbook 覆盖范围（待 registry 正式建单） |

---

## 维护

- 改拆法：先改原则 0.2 → 改 `_template.md` → 重跑 `_gen_kjztfwalgo_fp_by_api_prompts.py` → 已 `done` 的 Lxx 由人决定是否重跑。  
- catalog SHA 变更：重跑 dump + 评估是否重拆受影响六级。
