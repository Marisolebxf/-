# 审阅结论 — ARCH-ANALYSIS-TASK 设计方案 v3.0

> 审阅人：algorithm-agent（唐绍祖）
> 日期：2026-07-24
> 范围：异步任务编排设计方案（企业评估/风险洞察/引育推荐）

---

## 整体评价

文档质量很高（1867行），架构清晰、决策记录完整（D-1~D-29）、遗留问题全部闭合（Q-1~Q-9）。**总体可行，无设计层面的错误。**

设计方案中 §15（算法侧改造清单）、§17（关键决策）、§19（实现任务映射）已充分覆盖算法侧的 2 个任务。

---

## 需确认的 2 个问题

### 问题 1：算法侧 MySQL 连接

> 设计 §2 决策 C-16 + §6.1 说算法侧持久化统一使用 MySQL，不再用 PostgreSQL。
> 之前 entan 连接的是 `gkx_szc_ods`（PostgreSQL）。

**请问**：
- 算法侧 MySQL 连接哪个实例/库？连接串怎么配置？（.env / settings.yaml / Nacos）
- 算法侧 MySQL 的表结构是与 Java 侧共用 `analysis_task` 表，还是算法侧自己建表（如 `algo_task`）？

> 如果已有 MySQL 实例和连接信息，请直接给配参。若无特殊要求，我按如下方案实现：
> - entan 新建 `settings_mysql.py` 读取 `MYSQL_HOST/PORT/USER/PASSWORD/DB` 环境变量
> - 算法侧独立建表 `algo_task` / `algo_task_node`（不与 Java 侧共表，通过 API 交互而非直连）

### 问题 2：entan 现有 Webhook 回调是否带 analysisType

> 设计 §8.2 要求回调 payload **必须带 `analysisType`**，否则 Python 无法路由到 `/callback/eval|risk|recommend`。

**请问**：entan 现有的 `/gdf/tasks` 回调 Webhook payload 中是否已包含 `analysisType` 字段？

> 若已包含 → 无需改回调格式，算法侧只需确保透传正确。
> 若未包含 → 需要确认两种方案：
>   - **方案 A**：算法侧在回调体中追加 `analysisType` 字段
>   - **方案 B**：Python 侧在创建任务时缓存 `taskId → analysisType` 映射，收到回调后查表路由

---

以上 2 个问题确认后即可开始实现。

其余细节（如 science 框架结构、联调 mock 方式等）我可以在实施过程中自行解决。
