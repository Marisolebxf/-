# 企业综合竞争力评估 脚本→用例 覆盖表（2026-10-14）

蓝本 = `qa/test-cases/KJZTFWXT/enterprise-企业分析/EVALCOMP-企业综合竞争力评估/FUNC-企业综合竞争力评估-用例.md` v2.0（00403~00437，35 条）。
脚本 35 条（金样 5 + 其余 30，includes 展开），与用例 **1:1**，无未脚本化空洞。

金样（用例册元信息锁定）：P0-01=00403 · P0-02=00405 · P0-03=00409 · P0-04=00414 · P0-05=00419。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 |
|---------|----------|---------------|---|----------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00403 | 入口·侧栏进入 | P0 | 进入综合竞争力评估页 |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00405 | 浮层·选择分析企业构成 | P0 | 点前往对比篮选择企业 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00409 | 模板·三态分组 | P0 | 打开模板下拉 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00414 | 结果·进入结果态 | P0 | 开始分析→等待结果（allow_skip） |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00419 | 结果·差距诊断 | P0 | 浏览差距诊断（allow_skip） |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00404 | 隔离·mode | P0 | 打开技术力/商业力路由核 mode |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00406 | 浮层·确定回填 | P0 | 勾选确定回填 |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00408 | 覆盖·可信度 Tab | P0 | 回填后看五档（allow_skip） |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00410 | 指标·三维默认权重 | P0 | 默认态核对 |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00411 | 权重·上下调节 | P0 | 上调/下调 |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00412 | 权重·一键平均 | P0 | 点一键平均分配 |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00413 | 过程·开始分析 | P0 | 点开始分析进过程态 |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00415 | 结果·综合得分 | P0 | 浏览得分区（allow_skip） |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00416 | 结果·雷达单企 | P0 | 浏览雷达（allow_skip） |
| P0-15 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00417 | 结果·雷达双企 | P0 | 切双企对比（allow_skip） |
| P0-16 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00418 | 结果·排名 | P0 | 浏览排名（allow_skip） |
| P0-17 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00420 | 结果·评估报告 | P0 | 打开报告（allow_skip） |
| P0-18 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00421 | 结果·我的任务 | P0 | 看任务入口（allow_skip） |
| P0-19 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00422 | 明细·查看抽屉 | P0 | 点创新能力「查看」 |
| P0-20 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00436 | 异常·空态门控 | P0 | 空态核开始分析禁用 |
| P0-21 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00437 | 异常·权重和校验 | P0 | 调偏离→拦截→一键平均 |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00407 | 浮层·未勾选门控 | P1 | 核确定/取消选择禁用 |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00423 | 浮层·重置 | P1 | 勾选后点重置 |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00424 | 浮层·搜索与类型筛选 | P1 | 搜索/清空/类型筛选 |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00425 | 权重·非法输入 | P1 | 试负数/超界/小数 |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00426 | 浮层·取消选择 | P1 | 勾选后点取消选择 |
| P1-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00427 | 模板·保存个人模板 | P1 | 保存为个人模板 |
| P1-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00428 | 模板·重载系统模板 | P1 | 重选综合竞争力标准模板 |
| P1-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00429 | 对象·移除条目 | P1 | 点对象移除 |
| P1-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00430 | Tab·当前/最近往返 | P1 | 两 Tab 往返 |
| P1-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00431 | 评审·显隐零泄漏 | P1 | 开关内部评审模式 |
| P1-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00432 | 结果·调整配置 | P1 | 点调整配置（allow_skip） |
| P1-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00433 | 结果·重新分析 | P1 | 点重新分析（allow_skip） |
| P1-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00434 | 过程·取消任务 | P1 | 点取消任务（allow_skip） |
| P1-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00435 | 过程·稍后查看 | P1 | 点稍后查看（allow_skip） |

> 金样 = P0-01/02/03/04/05（id 锁定禁改）。脚本 id 前缀与用例优先级列独立。

## 覆盖说明

- **35/35 全脚本化**：无「未脚本化」空洞；结果态依赖链（P0-04/05/13~18、P1-11/12）与五档可信度（P0-08）预置 `allow_skip`。
- **未脚本化清单**：无。
- **expect**：全部双层 `{note, assert}`；译自用例预期列；结构性例外 00405/00409/00413/00431（4 点）。
- **as-built 偏差（2026-10-14 headless）**：
  - 系统模板名 =「综合竞争力标准模板」（非旧册 v1.0 文案）。
  - 三维权重默认 40/40/20；分组「综合竞争力三域」；spin `readonly=false`。
  - 浮层企业 Tab 实勘 7/50；回填后可信度区可能仅「全部可信度」+「未找到匹配企业」（五档不全 → P0-08 allow_skip）。
  - 过程态可达（`view=processing` + `analysis_type=competitiveness` + `EVAL-YYYYMMDD-NNN`），但任务曾「评估失败/生成失败」→ 结果态链 allow_skip。
  - 同壳兄弟（技术力/商业力）仅隔离反向（P0-06），不写兄弟正向。
- **同路由隔离**：本套 `entry_id=ent-eval-compete` only；禁止技术力/商业力正向断言。
