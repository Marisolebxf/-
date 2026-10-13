# QA handoff：QA-WORKSPACE-RESTRUCT-L01

- 时间：2026-10-13
- 范围：QA 工作区系统码统一 + 目录结构调整（对齐总集测试模板-v2 交付形态）
- 监管人：human:淮政玮（用户聊天授权 2026-10-13 11:22）

## 一、范围与实现

### 1. 系统码统一（问题 H1）

| 项 | 旧 | 新 |
|----|----|----|
| total-set 目录 | `qa/total-set/KJZTFWALGO/` | `qa/total-set/SDWJSF-KJZTFWSFK/` |
| as-built catalog | `catalog/KJZTFWALGO.yaml` | `catalog/SDWJSF-KJZTFWSFK.yaml`（内部 `system:` 同步） |
| 用例编号前缀 | `ZNFWJQ-KJZTFWALGO-v1.0-FUNC-` / `ZNFWJQ-KJZTFWALGO-byapi-v1.0-FUNC-` | `ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-`（含 by-api 合表 numbering） |
| 引用同步 | 148 个文件（376+ 行）：prompts L01–L60 ×2 套、原则文档、00-control、_inventory.json ×2、schema.md、as-built README/catalog index、5 个 `scripts/_*kjztfwalgo*` 脚本、QA-ASBUILT-METHOD handoff | 全部替换；**grep 零残留**（除受保护项） |

**受保护不改**（历史主键）：任务 ID `QA-KJZTFWALGO-FUNCLIST-SPLIT-L01`（registry/handoff 文件名与正文引用）；脚本**文件名**含 `kjztfwalgo`（保历史关联，docstring 注明「旧记 KJZTFWALGO」）；`task-registry.yaml` 历史 note 中的旧路径（规约禁改 registry 文件本体，MCP 无历史改写能力——8 处仅为审计记录，不影响工具链）。

编号内 `/` 与目录名 `-` 的差异已写入 spec §4 约定 6。

### 2. 目录结构调整

| 变更 | 说明 |
|------|------|
| `test-records/KJZTFWXT/{SEARCH,KEYENT,ANALYSIS,SZSTATUS}/` → `R0/` | 5 份记录 git mv（spec §4 轮次结构；旧目录已清） |
| `evidence/KJZTFWXT/{SEARCH,KEYENT,ANALYSIS,SZSTATUS,EVAL}/` → `R0/` | 6 份 JSON 证据 git mv |
| `delivery/` 根 xlsx → `delivery/KJZTFWXT/` | 交付版入系统子目录；新增 `KJXXZSXT/`、`SDWJSF-KJZTFWSFK/` 占位 |
| 🆕 `coverage/{三系统}/` | 三张评估表 MD 工作稿落点（README 含模板列结构） |
| 🆕 `reports/{三系统}/ + _security/` | 5 类报告 MD 源稿落点（README 含模板章节骨架；安全在 `_security/`，待决策 S3） |
| 🆕 `tools/{jmeter,postman}/` | 测试工具产物（服务报告交付；与 as-built/tools 分工已注明） |
| 🆕 `bug-registry.yaml` | BUG 按日取号台账（问题 H5） |
| 🆕 `templates/test-retest-template.md` | 复测记录模板（问题 H7；对齐记录簿「复测记录」sheet） |
| 🆕 `delivery/README.md` | 交付映射表 + **交付前 sheet 级清检单 6 条**（含样例脏数据风险登记） |

### 3. 文件间引用同步（问题：引用断链）

- 4 份 INT 记录内 evidence 路径 → R0 路径
- SEARCH 用例册、`qa/README.md` 内记录路径
- 6 份 ENT handoff（RISK/RECOMMEND/EVAL/CALLBACK/ARCH/SZSTATUS/KEYENT）内记录与证据路径
- B 线返工 handoff 内交付版路径 → `delivery/KJZTFWXT/`
- spec §4 目录树整体重绘 + 约定 6/7 新增 + 修订记录 v1.1

### 4. 治理文件更新

`qa/README.md`（全面重写：目录表、A/B 线索引、待决策清单 H3/H4/S3）· `code-registry.yaml`（v2，变更注记）· `qa-test-case-spec.md`（v1.1）。

## 二、验证证据

- `grep -rn KJZTFWALGO`（排除任务 ID/脚本名/「旧记」注记）→ **零残留**
- `python3 agent-delivery/scripts/_check_kjztfwalgo_fp_work.py` → OK L01–L05（改名后脚本定位新目录正常）
- `git status`：R 263 + RM 133（重命名含修改，历史保留）、M 25、?? 8（全部新增占位文件）；无删除条目
- git mv 全程使用，无 cp/rm，成果零丢失

## 三、脏数据 / 待用户决策清单（未删除，仅登记）

| # | 项 | 位置 | 建议 |
|---|----|------|------|
| D1 | 交付版 xlsx 三个非功能 sheet 仍为总集样例脏数据（智慧服务门户「科技人才评选」，自带通过+序列日期 46174） | `delivery/KJZTFWXT/6.国际科技信息中心项目_科技专题服务系统_测试用例.xlsx` 兼容/集成/性能 sheet | 用户已确认现阶段不管；**放行交付前必须清空**（清检单第 1 条已登记） |
| D2 | 旧自造码的历史痕迹 | `task-registry.yaml` 8 处 note（禁改）；任务 ID `QA-KJZTFWALGO-*`；脚本文件名 | 保留（历史审计需要）；如要彻底清理需 PM 批准批量改 registry |
| D3 | `evidence/KJZTFWXT/R0/` 内 JSON 为旧模块结构时期产物，轮次语义是追溯拟合 | R0 目录 | 保留；后续轮次自然分化 |
| D4 | 算法库 fp-split-by-api 续跑任务未建单 | 原则文档标注「登记表待 PM 补建」 | PM 补建 `QA-KJZTFWALGO-FP-BY-API-L01`（或按新码命名） |

待决策（本次未处理，已在 `qa/README.md` 登记）：H3 三屏范围 · H4 评估表责任矩阵 · S3 安全执行主体。

## 四、产物清单

- 重命名/引用同步：396 文件（git R/RM）
- 新增：`bug-registry.yaml` · `templates/test-retest-template.md` · `delivery|coverage|reports|tools` README ×4 · 系统占位目录 ×9（gitkeep）
- 更新：`qa/README.md` · `code-registry.yaml` · `qa-test-case-spec.md`（v1.1）

## 五、架构合规自检

铁律逐条：1 算法Python ✅未涉及 · 2 调用链 ✅ · 3 Nebula ✅ · 4 可观测 ✅ · 5 CI/CD ✅（编排仓无业务 CI）· 6 demo2 只读 ✅ · 7 共享聚合 ✅ · 8 数据策略 ✅ · 9 D8 ✅ · 10 D9 ✅（未动指标）· 11 D10 ✅ · 12 D12 ✅。本次为文档/目录重组，未触碰业务仓。

## 六、cost

- actual_tokens: ~120k（含前序探讨轮上下文）
- model_used: glm-5.3
- actual_cost: ~$1.2
- cost_warn: green

ponytail: full（目录重组未写多余代码；脚本仅批量替换用后即弃 /tmp）
