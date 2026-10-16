# 用例交付合并编排手册（S4）

> **定位**：把 B 线场景用例对功能点的覆盖，投影为客户模板 **「6.…_测试用例.xlsx」**（用例簿 · 一功能点一行）。  
> **总路由**：[`func-test-playbook-index.md`](func-test-playbook-index.md) 阶段 **S4**。  
> **不替代**：切点写法真源 [`as-built/prompts/_submit.md`](as-built/prompts/_submit.md)；清检 [`delivery/README.md`](delivery/README.md)。  
> **状态**：骨架版（Kickoff + 输入/列口径 + DoD）。专题已有一键生成脚本；展示系统待 env/catalog 后再套。

---

## 0. 与上下游边界

| 产物 | 阶段 | 说明 |
|------|------|------|
| `test-cases/…/FUNC-*-用例.md` + `coverage-fp.md` | S1 | 场景用例 + 功能点覆盖矩阵 |
| `as-built/scripts/…/coverage.md` | S2 | 脚本 → 场景（投影行填自动化 ID 时用） |
| **`delivery/{系统}/6.…_测试用例.xlsx`** | **S4（本手册）** | 用例簿；「是否通过」列**留空** |
| `delivery/…/ab-merge-manifest.md` | S4 | 投影对账（专题 B∪A 脚本产出） |
| `delivery/{系统}/7.…_测试记录.xlsx` | S5 | 记录簿；见 [`record-delivery-playbook.md`](record-delivery-playbook.md) |

**未覆盖功能点**：不投影、不造行（须先 S1 补场景或 PM 豁免）。

---

## 1. 新对话 Kickoff（整段复制 · 填【】）

```text
【身份】qa-agent 父控。阶段 S4·用例交付合并（B∪A 切点投影）。
【总索引】agent-delivery/qa/func-test-playbook-index.md
【必读】agent-delivery/qa/case-delivery-playbook.md（本手册）
         → as-built/prompts/_submit.md
         → delivery/README.md（清检单）
         → delivery/【SYSTEM】/ab-merge-manifest.md（若已有，先读再决定重跑或增量）
【工作根】/Users/roy/data/projects/zhipu/gkx/gkx-lumen/gkx-orchestration
【系统】【SYSTEM=KJZTFWXT】
【模式】【full-regen | module-patch】
  - full-regen：重跑生成脚本，覆盖功能 sheet + 刷新 manifest（专题默认）
  - module-patch：只补指定册的投影 MD / 矩阵后再纳入下次 full-regen（手工切片时用）
【输入门禁】
  - 各册 coverage-fp.md 存在且含「已覆盖/部分覆盖」行
  - 源场景 FUNC 册可读；A 线 v8 拆分表路径见生成脚本（专题）
【产物】
  - delivery/【SYSTEM】/6.国际科技信息中心项目_{系统中文}_测试用例.xlsx
  - delivery/【SYSTEM】/ab-merge-manifest.md（对账）
  - 可选工作区：test-cases/…/FUNC-*-总集投影.md + coverage-submit.md（按册手工时）
【专题一键重跑】
  python3 agent-delivery/scripts/_gen_zt_delivery_func_ab_merge.py
【做法】
  1) 确认模式与门禁
  2) full-regen：跑脚本 → 读 manifest 行数/缺源场景跳过数
  3) 过 delivery/README 清检单（样例脏数据、编号、是否通过列为空等）
  4) 交卷：xlsx 路径、投影行数、未纳入个数（未覆盖只计数）
【禁止】未覆盖造行；全文复制场景充多行；改场景号当投影号重复；为投影行新写 Playwright；改业务仓
【强度】ponytail full
开干：专题默认 full-regen；若只修一册切片，先 module-patch 再 full-regen。
```

---

## 2. 输入 / 输出与列口径（骨架）

### 2.1 输入

| 输入 | 用途 |
|------|------|
| 各模块 `coverage-fp.md` | 取出状态 ∈ {已覆盖, 部分覆盖} 的功能点行 |
| 源场景 `FUNC-*-用例.md` | 切片步骤/预期；填「源场景用例」 |
| A 线 v8 功能点拆分 xlsx（专题） | 优先复用交付编号；对账 |
| `as-built/.../coverage.md`（可选） | 填「自动化用例ID」 |
| 客户模板 6.x | sheet 结构 |

### 2.2 输出列（功能 sheet · 与模板对齐）

投影行 = **一个功能点一行**。核心列口径（细节以 `_submit.md` 为准）：

| 列（概念） | 规则 |
|------------|------|
| 用例编号 | 投影**新号**或复用 A 线 v8 号（专题脚本策略）；**禁止**用同一场景号填多行 |
| 测试内容 / 步骤 / 预期 | **按该功能点切片**，禁止场景全文复制 |
| 功能点 / 子功能项 | 与覆盖矩阵键一致 |
| 是否通过 | **留空**（记录簿 S5 再填） |
| 源场景用例（扩展） | 完整场景 `FUNC-xxxxx` |
| 自动化用例ID（扩展） | 脚本 `P0-xx`；同源多点可同一脚本 id |
| 备注 | `同源切片`；部分覆盖写清弱于需规之处 |

### 2.3 专题自动化 vs 手工

| 方式 | 何时 |
|------|------|
| `_gen_zt_delivery_func_ab_merge.py` | 专题全量/重跑默认 |
| 按册写 `FUNC-*-总集投影.md` + `coverage-submit.md` | 脚本未覆盖的系统、或单册精修切片 |

展示等系统：无生成脚本前走手工投影；有脚本后把命令补进本 §。

---

## 3. 未覆盖与范围

| 矩阵状态 | S4 动作 |
|----------|---------|
| 已覆盖 / 部分覆盖 | 投影 |
| 未覆盖 | **不投影**；manifest/交卷只计个数 |
| 无 B 册的 A 线段（如政策/综合智能） | 本波可不纳入（专题现状）；纳入前须先 S1 |

「须全覆盖交付」→ 先消未覆盖或拿 PM 豁免表，再宣称 S4 完成。

---

## 4. 角色（骨架）

| 角色 | 做 |
|------|----|
| 父 | 门禁、选模式、跑/派生成、读 manifest、清检、交卷 |
| 子·切片（可选） | 单册手工投影 MD（遵守 `_submit.md`） |
| 子·清检 | delivery README 清检单 |

本步**不跑** 50892、不新建脚本 yaml。

---

## 5. 收口 DoD

- [ ] 产物：`delivery/{系统}/6.…_测试用例.xlsx` 存在  
- [ ] 对账：`ab-merge-manifest.md`（或等价）含投影行数、已覆盖/部分覆盖/跳过统计  
- [ ] 投影行仅来自已覆盖/部分覆盖；未覆盖零行（或豁免表已附）  
- [ ] 无一场景号占用多行「用例编号」；无全文复制充数的明显注水  
- [ ] 功能 sheet「是否通过」为空  
- [ ] 非功能 sheet 样例脏数据：按 delivery 清检单处理或登记「放行前必清」  
- [ ] 交卷含：行数、缺源场景跳过数、未纳入未覆盖个数  

---

## 6. 待补

| 项 | 说明 |
|----|------|
| 展示/算法库生成器 | 对标专题 `_gen_zt_*` |
| 与 S1 未覆盖消缺联动清单 | 自动从矩阵拉「待补场景」 |
| 手工投影与脚本投影差异机检 | 防漏切/过严预期 |

---

## 7. 文件索引

| 文件 | 职责 |
|------|------|
| **本手册** | S4 编排骨架 |
| `as-built/prompts/_submit.md` | 切点写法铁律 |
| `scripts/_gen_zt_delivery_func_ab_merge.py` | 专题一键投影 |
| `delivery/{系统}/ab-merge-manifest.md` | 对账 |
| `delivery/README.md` | 清检 |
| `func-test-playbook-index.md` §4 | B∪A 口径补注 |
| `record-delivery-playbook.md` | S5 记录簿 |
