# 系统能力接入登记卡（模板）

> **用途**：业务模块复用 `SYS-ANALYSIS-JOBS` / `ENT-COMPARE` / `ENT-EXPORT`（及后续系统壳）时的**硬闸门**输入。  
> **原则**：企业金样例已完整 ≠ 新域自动可用；必须登记适配契约 + 跑金样例场景。  
> **权威边界**：系统壳行为以系统包四件套为准；本卡只登记本域适配，禁止在业务包重写壳层故事。  
> **用法**：复制到 `{模块包}/SYS-CAPABILITY-ADAPTER-{MODULE}.md` 后实填；门 1 / Demo 开工前至少填完 §1–§4。

---

## 0. 元数据

| 字段 | 值 |
|---|---|
| module_key | `{MODULE}` |
| 业务包路径 | `agent-delivery/agent-handoffs/产品整体定义/{path}/` |
| 金样例域 | `enterprise`（默认）/ 其它已验收域 |
| 填写人 | |
| 日期 | |
| 系统壳 Owner 会签 | 高颖（体验）· 架构（徐滕强/李伟，涉契约时） |
| 状态 | `draft` / `ready_for_demo` / `demo_verified` |

---

## 1. 接入范围（勾选）

| 系统能力 | 本域是否接入 | 系统包权威 | 本域只负责 |
|---|---|---|---|
| SYS-ANALYSIS-JOBS 任务浮层 | ☐ 是 ☐ 否 | `SYS-ANALYSIS-JOBS/` | task_type、过程页/结果页路由、快照 |
| ENT-COMPARE 对比篮 | ☐ 是 ☐ 否 | `ENT-COMPARE/` | object_type、入篮宿主、分发分析清单 |
| ENT-EXPORT 报告复用 | ☐ 是 ☐ 否 | `ENT-EXPORT/` | ReportContentModel、template_id、fingerprint 输入 |
| 其它（检索壳 / 维护壳…） | ☐ | 对应包 | 配置与字段，不改壳 |

未勾选「是」的能力：业务包 **禁止** 自建第二套浮层 / 篮 / Reader。

---

## 2. 对象与键（必填）

| 项 | 本域取值 | 禁止 |
|---|---|---|
| 主对象类型 | 例：`policy` | 混用企业 `enterprise_code` 当主键 |
| 稳定对象键 | 例：`policy_id` | 用展示名当去重键 |
| 对比篮 tab_key | 例：`policy` | 占位 Tab 假装已启用 |
| 每类型容量 | 50（默认对齐系统包） | 私自改系统总额 |
| 存储 / localStorage 命名空间 | 例：`policy:*` | 读写企业 key |
| 权限点前缀 | 例：`MENU_POLICY_*` | 复用企业菜单码当本域授权 |

---

## 3. SYS-JOBS 适配（接入时必填）

### 3.1 task_type 登记表

| 分析/报告 | task_class | task_type（稳定，不含对象/参数） | 过程页路由 | 结果页路由 | 完成后行为 |
|---|---|---|---|---|---|
| 例：深圳对比 | analysis_generation | `policy:shenzhen:compare` | `.../processing?task_id=` | `.../result?task_id=` | 停进度页 / 手动查看结果 |
| 例：报告 | report_generation | `policy:report:{template}` | 来源页+弹层 | — | 进个人资产投影 |

规则（对齐 `SYS-ANALYSIS-JOBS`）：

- 互斥键 = `user_id + task_type`；参数只进 route / 快照，不拼进 task_type。  
- 同步查询 / 确定性映射 **不** 接入 analysis_generation。  
- 创建报告文件的入口 **必须** 走 report_generation。

### 3.2 金样例对照场景（相对企业已验收路径）

| # | 场景 | 企业金样例期望 | 本域实测 | 差异/as-built |
|---|---|---|---|---|
| G1 | 提交后离页，浮层可见非终态任务 | 可见且可跳回过程页 | ☐ | |
| G2 | 同 task_type 再进配置 | 恢复原任务，不并行第二条 | ☐ | |
| G3 | 不同 task_type 可并行 | 浮层同时列出 | ☐ | |
| G4 | 完成后行为 | 与系统包/本域 UX-SPEC 一致 | ☐ | |
| G5 | 失败可基于原配置重试 | 新 task_id + retry_from | ☐ | |
| G6 | 与对比篮浮层互斥展开 | 只开一个面板 | ☐ | |
| G7 | 不读写企业 storage / task 模型 | 隔离 | ☐ | |

**闸门**：G1–G7 未全过，不得标本域「任务浮层复用完成」。

---

## 4. ENT-COMPARE 适配（接入时必填）

| 项 | 本域取值 |
|---|---|
| 入篮宿主页 | 例：查询结果、门户展示页 |
| 是否页内聚合篮入口 | **禁止**（统一系统 Shell） |
| 分发分析清单 | 列出 analysisKey → 目标路由 |
| 返回上下文 | `return_context_id` 是否恢复筛选/勾选 |
| 跨域混选 | 禁止 |

金样例：加入→角标+1→系统篮 Tab 可见→发起分析→目标页「来自对比篮」→返回恢复。

---

## 5. ENT-EXPORT 适配（接入时必填）

| 项 | 本域取值 |
|---|---|
| report_template_id | |
| 固定核心章节 | 引用 REPORT-CONTRACT，不改 Reader |
| fingerprint 输入 | 结果快照字段列表 |
| 第二消费者一致性 | ☐ 已对照企业评估/风险洞察无企业专属必填字段 |

禁止：业务页自建 PDF 引擎、跳过 HTML 直出 PDF、独立下载中心。

---

## 6. 样式与交互走查挂载

| 检查 | 证据链接/截图 | ☐ |
|---|---|---|
| Design.md §14 | | |
| UX-UE §19 | | |
| 对照企业同构区（过程页/浮层/操作栏）视觉 diff | | |

---

## 7. 签字

| 角色 | 姓名 | 结论 | 日期 |
|---|---|---|---|
| 业务模块体验 | | ☐ 适配完整 | |
| 系统壳体验（高颖） | | ☐ 未改壳 / 壳变更已 ASC | |
| 前端 Lead（孔东） | | ☐ 可实现 / 已隔离企业键 | |
