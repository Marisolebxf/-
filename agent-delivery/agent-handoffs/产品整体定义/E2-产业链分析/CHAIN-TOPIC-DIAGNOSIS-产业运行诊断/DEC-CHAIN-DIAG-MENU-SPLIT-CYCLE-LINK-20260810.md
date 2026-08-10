# DEC · 诊断侧栏拆分：产业周期分析 / 产业链环节诊断

| 字段 | 值 |
|---|---|
| ID | `DEC-CHAIN-DIAG-MENU-SPLIT-CYCLE-LINK-20260810` |
| 日期 | 2026-08-10 |
| 状态 | **已拍板（产品）** |
| 范围 | `demo-ui-topic` 侧栏 L2 + 诊断工作台 Tab 范围；不改 lumen 正式仓 |
| 关联 | 原 `IA-CHAIN-TOPIC-DIAGNOSIS` 三分析 Tab 工作台；`PLAN-招标五级别名导览与Demo边界-20260810` 原则 1（「不拆成四个平行 L2」）由本 DEC **部分修订** |

---

## 1. 决策

将原侧栏单一 L2「产业运行诊断」拆为三个 L2（2026-08-10 再修订：原「产业链环节诊断」拆为关键环节 / 瓶颈堵点）：

| 侧栏 L2 | `workspace` | 页内 Tab |
|---|---|---|
| **产业周期分析** | `cycle` | 产业周期分析 · 诊断记录 |
| **产业关键环节识别** | `key_link` | 产业关键环节识别 · 诊断记录 |
| **产业瓶颈堵点识别** | `bottleneck` | 产业瓶颈堵点识别 · 诊断记录 |

路由仍共用 `/industry-center/diagnosis`，以查询参数 `workspace=cycle|key_link|bottleneck` 区分工作台；权限码继续复用 `MENU_CHAIN_DIAGNOSIS`。旧链 `workspace=link` 按 tab 映射到 `key_link` / `bottleneck`。

---

## 2. 理由（摘要）

1. **分析对象不同**：周期面向「产业」；关键环节 / 瓶颈堵点面向「产业链」——合在同一 L2 增加对象与文案歧义。
2. **招标发现路径**：评审按五级名找入口时，「产业链环节诊断」比笼统「产业运行诊断」更不易假阴性。
3. **不做四个平行 L2**：六级叶子仍只在页内 Tab / 导览表出现（不推翻导览 PLAN 的六级原则）。

---

## 3. 兼容

- 旧链 `?tab=cycle|key-link|bottleneck|records`（无 `workspace`）：按 Tab 推断 workspace；`records` 单独出现时默认 `cycle`。
- 对比篮分组标题与侧栏对齐；`buildIndustryAnalysisUrl` 写入对应 `workspace`。
- 诊断记录按当前 workspace 过滤任务类型（周期只看 cycle；环节诊断看 key_link + bottleneck）。

---

## 4. 非目标

- 不拆权限码、不拆路由 path、不拆任务 `taskType` 前缀。
- 不把区域产业指数评价并入本拆分。
- 产品包总称「产业运行诊断」可保留在 TRACE/IA 文档层；侧栏不再使用该四字作为唯一 L2 名。
