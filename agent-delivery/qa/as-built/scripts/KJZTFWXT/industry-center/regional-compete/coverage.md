# 区域产业竞争力评价 脚本→用例 覆盖表（2026-10-14 BATCH32 · chain-regional-compete）

蓝本 = `qa/test-cases/KJZTFWXT/industry-center-产业链分析/REGCOMP-区域产业竞争力评价/FUNC-区域产业竞争力评价-用例.md` v2.0（01100~01124，25 条）。
脚本 **25** 条（金样 6 + 其余 19，includes 展开），与用例 **1:1**，无未脚本化声明。

金样锁定（R3 闸门 overall=pass 收敛）：P0-01=01100 · P0-02=01101 · P0-03=01105 · P0-05=01110 · P0-06=01111（A 档 5；**P0-04=01106 降 B**，与门控重叠）。
脚本 id ↔ func_id ↔ 用例册「自动化用例ID」回填列三方一致。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 |
|---------|----------|---------------|---|----------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01100 | 入口·路由与双 Tab | P0 | goto competitiveness |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01101 | 评价模式·互斥联动 | P0 | 切多产业/单产业 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01105 | 对象·产业/区域占位 | P0 | 展开产业/区域下拉 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01106 | 三维·构成与权重 | P0 | 默认态核对 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01110 | 操作区·门控状态机 | P0 | 空态→选产业 |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01111 | 操作区·显式开始分析 | P0 | 选产业→开始分析 |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01102 | 单产业·产业限选 | P0 | 选产业+提示 |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01103 | 单产业·区域 1–5 | P0 | 区域多选上限 |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01104 | 多产业·对象约束 | P0 | 切多产业选对象 |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01107 | 权重·编辑联动 | P0 | 改 spin / 非法值 |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01108 | 权重·合计 100% | P0 | 偏离→均分恢复 |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01109 | 权重·一键均分 | P0 | 一键均分 |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01112 | 结果·快照 KPI | P0 | B · allow_skip · ticket=GAP-CHAIN-REG-METRICS（结果壳诚实降级无第1名/权重快照；深链 CHAIN-20260911-010） |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01113 | 结果·柱状热力 | P0 | B · allow_skip · ticket=GAP-CHAIN-REG-METRICS（结果壳诚实降级无柱状/矩阵热力；深链 CHAIN-20260911-010） |
| P0-15 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01114 | 结果·GIS 条件 | P0 | B · allow_skip · ticket=GAP-CHAIN-REG-METRICS（结果壳诚实降级无 GIS/待补、模式不可辨；深链 CHAIN-20260911-010；探针 scout-p015-gis.json） |
| P0-16 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01115 | 结果·同源联动 | P0 | B · allow_skip · ticket=GAP-CHAIN-REG-METRICS（结果壳诚实降级无柱/矩阵/表行可点联动；深链 CHAIN-20260911-010） |
| P0-17 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01116 | 结果·生成报告 | P0 | B · allow_skip · ticket=GAP-CHAIN-REG-METRICS（结果降级无排名 KPI/生成报告主路径；共享链路 view=report 待 GAP 闭合；深链 CHAIN-20260911-010） |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01117 | 操作区·重置 | P1 | 重置参数 |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01118 | 异步·单飞 | P1 | B · allow_skip · ticket=OBS-CHAIN-REG-COMPETE-SINGLEFLIGHT（过程窗/当天复用致双发不可测；POST 计数+入口守势；GAP 仅 P0-13~17；口径 Q-ANALYSIS-01） |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01119 | 异步·复用重跑 | P1 | B · allow_skip · ticket=D3-CHAIN-REG-COMPETE-SAME-DAY-REUSE-MISSING（Q-ANALYSIS-01 三判据；着陆 wait+二次 goto 闸；产业叶匹配 /集成电路/；复用/重跑；GAP 仅 P0-13~17） |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01120 | 分析记录·切换构成 | P1 | B · allow_skip · ticket=OBS-CHAIN-REG-COMPETE-RECORDS-COMPOSITION（Tab 往返+g5 五列表/行操作；词面时间/报告份数 observed；无行 ENV-CHAIN-REGIONAL-COMPETE-NO-RECORDS；GAP 仅 P0-13~17） |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01121 | 工作区壳·指数隔离 | P1 | goto index↔compete |
| P1-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01122 | 评审·增量可见 | P1 | 开内部评审模式 |
| P1-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01123 | 评审·关闭零泄漏 | P1 | 关评审→刷新 |
| P1-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01124 | 异常·禁用触发 | P0 | 禁用态 click/Enter |

> 金样 = P0-01~06（id 锁定禁改）；脚本 id 前缀与用例优先级列独立（主表 P 列写用例优先级）。

## 覆盖说明

- **25/25 全脚本化**：用例册 01100~01124 每行恰一脚本；无未脚本化。
- **expect**：双层 `{note, assert}`；禁止裸字符串。
- **allow_skip 预置**：P0-13~17（结果态细项）、P1-02/03（单飞/复用）、P1-04（记录列细项）。
- **禁止**：区域产业指数评价兄弟正向（仅 P1-05 隔离反向）。

## as-built 偏差（相对用例期望）

| 脚本 | 用例 | 偏差 |
|------|------|------|
| P0-04 / P0-10 | 01106 / 01107 | 三维为**固定计入**（勾选 disabled），默认权重 **40/35/25**，非「空态待选+权重空值」；无「模板名称 / 已计入 0 项 · 权重合计 0%」汇总文案 |
| P0-03 | 01105 | 区域默认「深圳市」，占位「请选择区域」仅清空后可见 |
| P0-05 | 01110 | 「维度未配齐」中间态不存在（三维固定+默认合计 100%）；门控主因=未选产业 |
| P1-05 | 01121 | 指数页亦有「一键均分」；隔离以三维选择器/官方模板/四力分组为准，不按「无均分按钮」硬判 |
| P0-13~17 | 01112~01116 | 勘察未见成功结果细项 → allow_skip；构造路径=选集成电路→开始分析 |

## 未脚本化

无。
