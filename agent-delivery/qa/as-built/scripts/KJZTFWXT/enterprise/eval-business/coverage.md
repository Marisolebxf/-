# 企业商业力评估对比分析 脚本→用例 覆盖表（2026-10-14 BATCH32 · ent-eval-business）

蓝本 = `qa/test-cases/KJZTFWXT/enterprise-企业分析/EVALBIZ-企业商业力评估对比分析/FUNC-企业商业力评估对比分析-用例.md` v2.0（00930~00959，30 条）。
脚本 30 条（金样 6 + 其余 24，includes 展开），与用例 **1:1**，无未脚本化声明。

金样锁定（用例册元信息）：P0-01=00930 · P0-02=00933 · P0-03=00937 · P0-04=00938 · P0-05=00943 · P0-06=00944（本册金样 6 条，不强制 5）。
脚本 id ↔ func_id ↔ 用例册「自动化用例ID」回填列三方一致。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 |
|---------|----------|---------------|---|----------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00930 | 入口·侧栏进入 | P0 | 进入商业力页核路由/标题 |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00933 | 浮层·选择分析企业 | P0 | 点前往对比篮选择企业 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00937 | 模板·三态分组 | P0 | 打开选择模板下拉 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00938 | 指标·6 项默认权重 | P0 | 默认态核对 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00943 | 过程态·进入 | P0 | B 档 · 过程态/结果态双分支实跑（demo 任务瞬时过窗按附录 E 直达结果） |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00944 | 结果态·进入 | P0 | B 档 · 结果态实跑，最近评估→恢复结果直达 view=result（2026-10-15 A_SKIP 回炉，无 allow_skip） |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00931 | 同壳·mode 隔离 | P0 | 切 tech/compete 再回 business |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00932 | 对象·空态门控 | P0 | 浏览空态+开始分析禁用 |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00934 | 浮层·确定回填 | P0 | B 档 · 勾选 2 家确定（allow_skip；ticket=ENV-EVAL-BUSINESS-PRECHECK-001） |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00936 | 覆盖·五档 Tab | P0 | B 档 · 回填后看可信度 Tab（allow_skip；ticket=ENV-EVAL-BUSINESS-PRECHECK-001） |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00939 | 指标·勾选移除 | P0 | 取消/恢复市场 |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00940 | 权重·调节与非法值 | P0 | 上调/下调/填 -1·1.5 |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00941 | 权重·一键均分 | P0 | 均分→去 2 项再均分 |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00945 | 结果·排名 | P0 | B 档 · 最近评估→恢复结果后核「商业力加权排名」+ 综合得分降序（2026-10-15 SKIP_FIELD 去 allow_skip；发起链预检债见 ENV-EVAL-BUSINESS-PRECHECK-001） |
| P0-15 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00946 | 结果·可视化对比 | P0 | B 档 · 最近评估→恢复结果后核「关键经营指标对比」+ 维度/对标企业（2026-10-15 SKIP_FIELD 去 allow_skip；发起链预检债见 ENV-EVAL-BUSINESS-PRECHECK-001） |
| P0-16 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00947 | 结果·诊断明细 | P0 | B 档 · 最近评估→恢复结果后核「商业诊断与明细」+ 按企业诊断结论（2026-10-15 SKIP_FIELD 去 allow_skip；发起链预检债见 ENV-EVAL-BUSINESS-PRECHECK-001） |
| P0-17 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00958 | 异常·单家拦截 | P0 | 仅勾 1 家点开始 |
| P0-18 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00959 | 异常·权重和校验 | P0 | B 档 · 偏离/清空/修复（2026-10-15 SKIP_FIELD 去 allow_skip；第三点发起链预检债见 ENV-EVAL-BUSINESS-PRECHECK-001，仅验配置修复不假绿） |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00935 | 浮层·按钮门控 | P1 | 未勾选/取消选择 |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00942 | 指标·明细抽屉 | P1 | 市场行查看 |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00948 | Tab·当前/最近 | P1 | 往返 Tab |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00949 | 模板·加载恢复 | P1 | B 档 · 系统/个人模板切换恢复权重且不恢复对象（2026-10-15 SKIP_FIELD 去 allow_skip；不依赖预检/env-gate 发起链） |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00950 | 模板·保存个人 | P1 | 超长名+合法保存 |
| P1-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00951 | 浮层·搜索筛选重置 | P1 | B 档 · 浮层名称搜索+类型筛选+重置实跑（2026-10-15 SKIP_FIELD 去 allow_skip；不依赖预检/env-gate 发起链） |
| P1-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00952 | 对象·移除条目 | P1 | 回填后移除 |
| P1-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00953 | 结果·调整配置 | P1 | B 档 · 最近评估→恢复结果后点调整配置回配置态（2026-10-15 SKIP_FIELD 去 allow_skip；发起链预检债见 ENV-EVAL-BUSINESS-PRECHECK-001） |
| P1-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00954 | 结果·重新分析 | P1 | B 档 · 最近评估→恢复结果后点重新分析进过程态+新 task_id≠旧（2026-10-15 SKIP_FIELD 去 allow_skip；发起链预检债见 ENV-EVAL-BUSINESS-PRECHECK-001） |
| P1-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00955 | 过程·取消任务 | P1 | B 档 · allow_skip · ticket=ENV-EVAL-BUSINESS-PROCESS-WINDOW-001 · target=最近评估（§5.2 回炉：抢窗失败诚实 n/a；预检债 ENV-EVAL-BUSINESS-PRECHECK-001） |
| P1-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00956 | 过程·稍后查看 | P1 | B 档 · allow_skip · ticket=ENV-EVAL-BUSINESS-PROCESS-WINDOW-001 · target=最近评估（§5.2 回炉：抢「稍后查看」窗失败诚实 n/a；预检债 ENV-EVAL-BUSINESS-PRECHECK-001） |
| P1-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00957 | 评审·追溯显隐 | P1 | 开/关内部评审模式 |

## 覆盖说明

- **30/30 全脚本化**：用例册 00930~00959 每行恰一脚本；无未脚本化。
- **expect**：双层 `{note, assert}`；00943 / 00957 结构性 4 点与用例一致。
- **allow_skip 预置**（预检失败 / 我的模板空 / 类型选项不可用 / 过程窗不可抢）：P0-09/10、P1-10、P1-11。（P0-05 已于 2026-10-15 改过程态/结果态双分支实跑，移出本清单；P0-06 已于 2026-10-15 回炉 B 档结果态实跑，移出本清单；P0-14 已于 2026-10-15 SKIP_FIELD 回炉去 allow_skip，走恢复结果核排名；P0-15 已于 2026-10-15 SKIP_FIELD 回炉去 allow_skip，走恢复结果核「关键经营指标对比」；P0-16 已于 2026-10-15 SKIP_FIELD 回炉去 allow_skip，走恢复结果核「商业诊断与明细」；P0-18 已于 2026-10-15 SKIP_FIELD 回炉去 allow_skip，门控+配置修复实跑、预检债下第三点不假绿发起链；P1-04 已于 2026-10-15 SKIP_FIELD 回炉去 allow_skip，配置区模板切换实跑；P1-06 已于 2026-10-15 SKIP_FIELD 回炉去 allow_skip，浮层搜索/筛选/重置实跑；P1-08 已于 2026-10-15 SKIP_FIELD 回炉去 allow_skip，恢复结果后点调整配置回配置态；P1-09 已于 2026-10-15 SKIP_FIELD 回炉去 allow_skip，恢复结果后点重新分析进过程态+新 task_id；P1-10 已于 2026-10-15 §5.2 回炉补 ticket+skip_reason+allow_skip_target，过程窗债 ENV-EVAL-BUSINESS-PROCESS-WINDOW-001；P1-11 已于 2026-10-15 SKIP_FIELD 回炉补 ticket+skip_reason+allow_skip_target，过程窗债 ENV-EVAL-BUSINESS-PROCESS-WINDOW-001，对齐 P0-22/P1-10）
- **as-built 现场口径**（写期望已吸收）：
  - 系统模板名用例「系统商业力模板 v1.0」→ 现场「商业力标准模板」
  - 模板三组需点开「选择模板」下拉可见
  - 空态文案「请先在对比篮选择企业，再进入企业评估配置。」
  - 2026-10-14 回填 2 家后「预检未返回企业明细…」→ 无五档可信度 Tab、开始分析仍 disabled（过程/结果链本环境不可达）
  - 企业勾选 aria-label 前缀「选择 」（勿点「选择指标：」）
  - 同壳隔离只作反向断言，不把技术力/综合竞争力写成兄弟页主测脚本

## 未脚本化

无。
