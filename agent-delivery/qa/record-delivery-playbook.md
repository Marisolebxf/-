# 可交付测试记录编排手册（S5）

> **定位**：把 **正式轮次** 的脚本执行结果 + 交付用例簿，转录为客户模板 **「7.…_测试记录.xlsx」**（记录簿）。  
> **总路由**：[`func-test-playbook-index.md`](func-test-playbook-index.md) 阶段 **S5**。  
> **不替代**：工作区记录稿 [`../templates/test-record-template.md`](../templates/test-record-template.md)；执行真源 [`as-built/script-batch-run-playbook.md`](as-built/script-batch-run-playbook.md)（S3）；用例交付簿编排 [`case-delivery-playbook.md`](case-delivery-playbook.md)（S4）+ [`as-built/prompts/_submit.md`](as-built/prompts/_submit.md)；清检 [`delivery/README.md`](delivery/README.md)。  
> **状态**：骨架版（Kickoff + 列映射 + DoD）。导出脚本 / 复测自动化待补；Bug 提交方式 🟡 待定。

---

## 0. 与上下游边界

| 产物 | 阶段 | 能否当客户交付 |
|------|------|----------------|
| `as-built/runs/{wave}/results.xlsx` + `EXEC-SUMMARY.md` | S3 | **否**（工作清单；`runs/` 默认不入库） |
| `test-records/{系统}/R{n}/` + `evidence/` | S3 正式轮升级 | **否**（工作区；可含阻塞/跳过） |
| `delivery/{系统}/6.…_测试用例.xlsx` | S4 | 用例簿；「是否通过」列应空 |
| `delivery/{系统}/7.…_测试记录.xlsx` | **S5（本手册）** | **是**（记录簿；是否通过仅「通过/不通过」） |

**禁止**：用调通 run、未消化的跳过/阻塞行直接灌进 7.x 交付版。

---

## 1. 新对话 Kickoff（整段复制 · 填【】）

```text
【身份】qa-agent 父控。阶段 S5·可交付测试记录。
【总索引】agent-delivery/qa/func-test-playbook-index.md
【必读】agent-delivery/qa/record-delivery-playbook.md（本手册）
         → templates/test-record-template.md
         → delivery/README.md（清检单）
         → as-built/script-batch-run-playbook.md §6～§7（正式轮次口径）
【工作根】/Users/roy/data/projects/zhipu/gkx/gkx-lumen/gkx-orchestration
【系统】【SYSTEM=KJZTFWXT】
【输入】
  1) 正式轮次：test-records/【SYSTEM】/R【n】/（含 results.xlsx 或等价清单 + EXEC-SUMMARY）
  2) 证据：evidence/【SYSTEM】/R【n】/（不通过须有图）
  3) 交付用例簿：delivery/【SYSTEM】/6.…_测试用例.xlsx（功能 sheet 行作主数据）
【产物】delivery/【SYSTEM】/7.国际科技信息中心项目_{系统中文}_测试记录.xlsx
         + test-records/【SYSTEM】/R【n】/FUNC-…-记录.md（工作区可选）
【做法】
  1) 门禁：确认输入是「正式 R 轮」不是 as-built/runs 调通垃圾
  2) 按手册 §2 列映射拼功能记录行；§3 消化阻塞/跳过/待人工
  3) 不通过行：实际结果 + 截图路径；BUG编号按 §4（可空若提交方式未定）
  4) 过 delivery/README 清检单；交卷路径 + 行数统计
【禁止】改业务仓；改脚本期望充绿；把 n/a/阻塞原样写入交付「是否通过」；臆造 BUG 号
【强度】ponytail full
开干：先核 R【n】目录与 6.x 用例簿存在，再派子任务按模块填功能 sheet。
```

---

## 2. 列映射（骨架）

### 2.1 主路径：用例簿行 × 执行结果 → 记录簿功能 sheet

以 **交付用例簿功能 sheet 的一行**（用例编号）为主键；用正式轮次 `results.xlsx`（或 R{n} 清单）按 `用例编号`/`func_id` 左连接执行结果。

| 记录簿列（模板 7 / 工作区主表） | 来源优先 | 说明 |
|--------------------------------|----------|------|
| 用例编号 | S4 用例簿 | 禁止复测改号 |
| 功能模块～预期结果、优先级等 | S4 用例簿同名列 | 场景/步骤/预期以用例簿为准 |
| 是否通过 | S3 `通过情况` → §3 消化 | 交付仅 `通过` / `不通过` |
| 测试工程师 | 本波填写 / WAVE.md | |
| 测试时间 | R{n} 执行日 | MD=`YYYY-MM-DD`；导出再转 Excel 序列 |
| 审核员 | 本波填写 | 可空至签收 |
| 测试截图 | `evidence/…` 相对路径 | 不通过必填 |
| 实际结果 | S3 `失败原因` / `actual`；通过可写「与预期一致」或摘要 | |
| 用户故事编号～路由等扩展 | S4 用例簿右侧扩展列 | 总集导出是否带扩展列见 delivery 清检单 |
| 关联任务ID | 本波任务 ID | 如执行叶 / S5 叶 |
| BUG编号 | §4 | 不通过建议有；方式待定则可空并在备注说明 |
| traceId | S3 清单 / result.yaml | 无则空 |
| 复测轮次 | `R{n}` | 初测 R0 |
| 阻塞/跳过原因 | **仅工作区 MD** | **禁止入交付「是否通过」**；定稿前须消化 |
| 备注 | C 类、环境债、豁免 | |

### 2.2 S3 `results.xlsx` → 中间字段

| S3 列 | → | 记录侧 |
|-------|---|--------|
| 用例编号 | → | 用例编号（join key） |
| 用例描述 | → | 可核对「测试内容」；冲突以用例簿为准 |
| 脚本ID | → | 备注或工作区扩展（交付可不带） |
| 通过情况 | → | §3 映射后再写「是否通过」 |
| 失败原因 | → | 实际结果（不通过/曾阻塞） |
| 失败分类 | → | 备注（C1–C6）；不单独占交付列除非模板有 |
| 严重程度 | → | 工作区 BUG 清单 / 备注 |
| BUG编号 | → | BUG编号 |
| 证据路径 | → | 映射到 evidence 拷贝后的截图路径 |
| traceId | → | traceId |

### 2.3 记录簿 sheet 范围（本骨架默认）

| sheet | 本阶段是否做 |
|-------|----------------|
| 功能 | **要做**（FUNC） |
| 集成 / 性能 | 有正式执行再填；否则清空样例行（见 delivery 清检单） |
| 复测 | 仅 Rn 复测波填写 |
| 规则-0529 | 按模板保留/同步，不手改规则正文 |

兼容性（COMP）若走独立用例集，另表；不从专题 UI 脚本波次自动生成。

---

## 3. 「是否通过」消化规则（交付前）

| S3 / 工作区态 | 能否进交付「是否通过」 | 定稿动作 |
|---------------|------------------------|----------|
| 通过 | ✅ `通过` | 直接 |
| 不通过 | ✅ `不通过` | 实际结果 + 截图；BUG 按 §4 |
| 跳过（n/a） | ❌ | 本轮不纳入交付行，**或**补测后改写；禁止写「跳过」进总集 |
| 阻塞 | ❌ | 解除阻塞后重跑；或降级为不通过+说明（须人拍板） |
| 待人工 | ❌ | 人工判定后改为通过/不通过 |

未脚本化、本轮未执行的用例：**默认不出现在本波记录簿**（或单独「未测清单」附录，不进是否通过列）。

---

## 4. BUG 编号（🟡 待定）

- 格式真源：`BUG-{板块}-{系统}-{YYYYMMDD}-{3位}`（见 `bug-registry.yaml` / qa-test-case-spec）。  
- **提交渠道待定**：未定前交付行允许 BUG 号为空，须在 EXEC-SUMMARY / 记录备注写「待登记」。  
- 禁止臆造编号；占号必须先写 `bug-registry.yaml`。

---

## 5. 角色与子任务（骨架）

| 角色 | 做 |
|------|----|
| 父 | 核输入门禁；派模块子任务；过清检单；交卷 |
| 子·填表 | 按模块把 join 结果写入工作区 MD 或直接生成 xlsx 行（工具待补） |
| 子·清检 | 跑 §6 DoD + delivery README 清检单 |

导出自动化（`scripts/_gen_*_test_record.py` 等）**尚未建**——本骨架允许手工 / 半自动填；工具就绪后改本 § 指向命令。

---

## 6. 收口 DoD

- [ ] 输入已声明为正式 `R{n}`，而非仅 `as-built/runs` 调通目录  
- [ ] 产物路径：`delivery/{系统}/7.…_测试记录.xlsx` 存在  
- [ ] 功能 sheet：用例编号均可在 6.x 用例簿找到；无复测改号  
- [ ] 「是否通过」**仅**含 `通过` / `不通过`（无跳过/阻塞/待人工字样）  
- [ ] 每一「不通过」有实际结果 + 可打开的截图证据（或书面豁免）  
- [ ] 样例脏数据已清（集成/性能等非本波 sheet）  
- [ ] 日期为可导出的 `YYYY-MM-DD` 语义  
- [ ] 工作区 `test-records/…/R{n}/` 留有摘要或 MD 记录稿（可选但推荐）  
- [ ] handoff / 对话交卷含：行数、通过/不通过计数、空 BUG 说明  

---

## 7. 待补（非本骨架范围）

| 项 | 说明 |
|----|------|
| 导出脚本 | 6.x + results.xlsx → 7.x 一键生成 |
| Bug 提交流程 | 渠道 + 与 registry 联动 |
| 复测 sheet 细则 | 与 `templates/test-retest-template.md` 对齐 |
| 展示系统 | env 锁定后再套本手册换系统码 |

---

## 8. 文件索引

| 文件 | 职责 |
|------|------|
| **本手册** | S5 编排 |
| `func-test-playbook-index.md` | 命令路由 S5 |
| `templates/test-record-template.md` | 工作区记录列 |
| `delivery/README.md` | 交付清检 |
| `as-built/script-batch-run-playbook.md` | S3 执行与正式轮升级 |
| `bug-registry.yaml` | BUG 取号 |
