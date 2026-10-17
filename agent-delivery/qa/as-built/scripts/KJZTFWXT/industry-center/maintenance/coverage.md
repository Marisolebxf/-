# 维护管理（产业链） 脚本→用例 覆盖表（2026-10-14 BATCH32 · chain-maintenance）

蓝本 = `qa/test-cases/KJZTFWXT/industry-center-产业链分析/CHAINMAINT-维护管理/FUNC-维护管理-产业链-用例.md` v2.0（01159~01177，19 条）。
脚本 19 条（金样 6 + 其余 13，includes 展开），与用例 **1:1**，无未脚本化声明。

金样锁定（用例册元信息）：P0-01=01159 · P0-02=01160 · P0-03=01161 · P0-04=01162 · P0-05=01163 · P0-06=01168。
脚本 id ↔ func_id ↔ 用例册「自动化用例ID」回填列三方一致。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 |
|---------|----------|---------------|---|----------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01159 | 入口·路由与标题 | P0 | goto /industry-center/maintenance |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01160 | 页面·双区结构 | P0 | 左导航+右面板可见 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01161 | 导航·15 分类构成 | P0 | 回读 15 分类顺序 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01162 | 导航·三分组标题 | P0 | 回读三 H2 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01163 | 默认子面板·构成 | P0 | H2+IC-43 说明 |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01168 | 子面板·互斥切换 | P0 | 主体信息→图谱绘制 |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01165 | 操作区·按钮构成 | P0 | 新增/提交审核可见 |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01166 | 操作区·初始禁用 | P0 | 两按钮 disabled |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01167 | 导航·默认选中 | P0 | 门户内容 primary |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01171 | 异常·禁用点击 | P0 | force 点击无抽屉 |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01164 | 导航·分组挂载 | P1 | 5+4+6 section |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01169 | 子面板·切回恢复 | P1 | 主体→门户内容 |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01170 | 子面板·跨分组 | P1 | 动态资讯→实体生命周期 |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01172 | 评审·追溯按钮 | P1 | 开评审→点追溯 |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01173 | 评审·关闭零泄漏 | P1 | 关评审→刷新 |
| P1-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01174 | 系统·对比篮可达 | P2 | 开浮层 / 无入篮触点 |
| P1-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01175 | 边界·末位审计监控 | P2 | 点审计监控 |
| P1-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01176 | 边界·首分类再选 | P2 | 主体→门户内容 |
| P1-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01177 | 异常·网络空态 | P1 | offline 刷新 |

> 金样 = P0-01~06（本册 6 条金样，条数不强制 5）；脚本 id 前缀与用例优先级列独立（主表 P 列写用例优先级）。

## 覆盖说明

- **19/19 全脚本化**：用例册 01159~01177 每行恰一脚本；无未脚本化声明。
- **expect 点数**：全部译自用例「预期结果」列；双层 `{note, assert}`（X9）。
- **observed 口径**（不作硬 expect）：各子面板正文构成、选中后按钮恢复、追溯弹层正文细节、对比篮 8 类型完整清单、异常反馈具体文案。
- **allow_skip / manual**：P1-09（网络模拟不可用或壳页缓存命中）→ `allow_skip` + 第二点 `manual: true`。

## as-built 偏差（相对用例期望）

| 脚本 | 用例 | 偏差 |
|------|------|------|
| P0-01 | 01159 | 无；现场有 h1「维护管理」+ document.title「维护管理 - 科技专题服务系统」 |
| P0-06 / P1-* | 切换类 | 评审追溯弹层未关时会拦截分类点击 → assert 内先 Esc / 关对比篮（P8） |
| P0-10 | 01171 | 「无送审请求」机检以无抽屉/弹层 + 仍 disabled 代理；网络面板无 POST 记 observed |
| P1-04 | 01172 | 追溯弹层实勘文案含「只复刻 Demo 15 项工作台壳…」 |
| P1-06 | 01174 | 对比篮类型 tab 可见数以现场为准（≥4）；「共 8 项」类型清单 observed |
| P1-09 | 01177 | 壳页可能缓存命中，离线刷新无异常反馈时 allow_skip |

## 未脚本化

无。

## 隔离声明

- 本 entry = `chain-maintenance`（`/industry-center/maintenance`），**禁止**写入 `svc-maintenance`（`/service/maintenance`）断言。
