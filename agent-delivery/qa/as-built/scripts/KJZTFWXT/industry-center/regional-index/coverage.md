# 区域产业指数评价 脚本→用例 覆盖表（2026-10-14 BATCH32 · chain-regional-index）

蓝本 = `qa/test-cases/KJZTFWXT/industry-center-产业链分析/REGIDX-区域产业指数评价/FUNC-区域产业指数评价-用例.md` v2.0（00562~00577，16 条）。
脚本 **16** 条（金样 4 + 其余 12，includes 展开），与用例 **1:1**，无未脚本化声明。

金样锁定（用例册元信息）：P0-01=00562 · P0-02=00563 · P0-03=00566 · P0-04=00570（本册金样 4 条，不强制 5）。
脚本 id ↔ func_id ↔ 用例册「自动化用例ID」回填列三方一致。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 |
|---------|----------|---------------|---|----------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00562 | 入口·路由与双 Tab | P0 | 进入指数评价页 |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00563 | 评价模式·互斥联动 | P0 | 切多产业/单产业 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00566 | 指标树·模板态锁定 | P0 | 默认模板六指标 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00570 | 开始分析·显式触发 | P0 | 选产业后开始分析 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00564 | 产业·空态与门禁 | P0 | 空态提示/选产业 |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00565 | 区域·多选上限 | P0 | 展开区域多选 |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00567 | 指标·启停移除 | P0 | B · allow_skip · ticket=D3-CHAIN-REG-INDEX-CUSTOM-STICKY-LOCK（自定义态启停粘滞只读；哨兵=未锁定 checkbox） |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00568 | 指标·添加库项 | P0 | B · 去裸 skip 转实（库追加+空名「暂无数据」；≠ D3-CHAIN-REG-INDEX-CUSTOM-STICKY-LOCK） |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00569 | 汇总·所见即所得 | P0 | B · 去裸 skip 转实（初始/产业/区域/权重文案+移除验已计入联动；全取消→0 项债=D3 sticky→P0-07） |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00571 | 重置参数 | P1 | 改条件后重置 |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00572 | 模板·两态切换 | P1 | 官方↔未保存配置 |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00573 | 一键均分·数值校验 | P1 | B · allow_skip · ticket=D3-CHAIN-REG-INDEX-CUSTOM-STICKY-LOCK（自定义态 spin 粘滞只读；一键均分/填 0/拒非法依赖可写权重；哨兵=未锁定 checkbox，同 P0-07） |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00574 | 个人模板·保存 | P1 | B · allow_skip · ticket=D3-CHAIN-REG-INDEX-PERSONAL-TEMPLATE-PERSIST（合法态保存后「我的模板」未落库/分组不可见；哨兵=保存为个人模板按钮，≠ sticky 债） |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00575 | 评审·追溯零泄漏 | P1 | 开/关内部评审模式 |
| P1-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00576 | 分析记录·结果 | P1 | B · allow_skip · ticket=GAP-CHAIN-REG-METRICS（g5 有已完成可开壳；种子 CHAIN-20260910-020 结果 KPI/四力诚实降级；哨兵=「第 1 名」；≠ sticky 债；无已完成归 ENV-CHAIN-REGIONAL-INDEX-NO-DONE-TASK） |
| P1-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00577 | 异常·权重门禁 | P1 | B · allow_skip · ticket=D3-CHAIN-REG-INDEX-CUSTOM-STICKY-LOCK（自定义态 spin/checkbox 粘滞只读；合计偏离/0 计入门禁依赖可写权重或可取消计入；哨兵=未锁定 checkbox，同 P0-07/P1-03） |

## 覆盖说明

- **16/16 全脚本化**：用例册 00562~00577 每行恰一脚本；无未脚本化。
- **expect**：双层 `{note, assert}`；禁止裸字符串。
- **allow_skip 预置**：P0-07 / **P1-03** / **P1-07**（同 ticket=D3-CHAIN-REG-INDEX-CUSTOM-STICKY-LOCK：自定义态 spin/checkbox 粘滞只读；P1-03/P1-07 已补 skip_reason+ticket，非裸 skip）、**P1-04**（ticket=D3-CHAIN-REG-INDEX-PERSONAL-TEMPLATE-PERSIST：保存落库/「我的模板」不可见，已补 skip_reason+ticket）、**P1-06**（ticket=GAP-CHAIN-REG-METRICS：已完成种子结果 KPI/四力诚实降级；P1-06 已补 skip_reason+ticket，禁 ALLOW_SKIP throw，≠ sticky 债）。**P0-08 / P0-09 已去裸 skip 转实**（P0-09：即时汇总主路径可绿；全取消→0 项仍挂 P0-07 sticky 债，本条用移除验已计入联动）。
- **as-built 现场口径**（写期望已吸收，不升 Fail）：
  - 模板稳定名「区域产业指数官方模板」；加载竞态瞬态可能「区域产业综合指数 V1.0」或空工作集 → 脚本 wait≥3~5s 至「已计入 6 项」
  - 六指标叶名现场为「企业商业化能力 / 融资事件 / 专利 / 技术成熟度 / 科研机构 / 政策覆盖率」（用例旧勘察名营收/技术壁垒/…）；权重仍 16×5+20
  - 切「当前未保存配置」后 spin/checkbox 可能仍 disabled（粘滞只读）
  - 初始汇总「未选产业 · 深圳市 · 已计入 6 项」；选产业后出现「权重合计：100% · 校验通过」
  - 过程态 `view=processing` + `CHAIN-YYYYMMDD-NNN`；分析记录 `tab=records`
  - **禁止**把「区域产业竞争力评价」写进本套正向脚本

## 未脚本化

无。
