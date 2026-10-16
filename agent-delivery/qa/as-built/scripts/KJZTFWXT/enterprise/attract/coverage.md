# 招引企业推荐分析 脚本→用例 覆盖表（2026-10-14 BATCH32 · ent-attract）

蓝本 = `qa/test-cases/KJZTFWXT/enterprise-企业分析/ATTRACT-招引企业推荐分析/FUNC-招引企业推荐分析-用例.md` v2.0（00979~01003，25 条）。
脚本 25 条（金样 5 + 其余 20，includes 展开），与用例 **1:1**。
金样锁定：P0-01=00979 · P0-02=00983 · P0-03=00986 · P0-04=00987 · P0-05=00993。
locator 基准 = `fixtures/scout/`（2026-10-14 无头；先 `/login` 再深链；`scout-deep.md` / `page-result` 为二次探针）。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 |
|---------|----------|---------------|---|----------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00979 | 入口·路由与默认 Tab | P0 | 深链进入招引页 |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00983 | 门控·无条件置灰 | P0 | 空条件看开始分析 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00986 | 异步·发起到成功 | P0 | 选标签→开始分析 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00987 | 结果·列表构成 | P0 | 浏览列头与家数 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00993 | 候选·加入招引 | P0 | 勾选→加入招引候选 |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00980 | 条件·三选择器占位 | P0 | 浏览占位 |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00981 | 条件·8 产业链项 | P0 | 开行业领域下拉 |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00982 | 条件·选择回显 | P0 | 选标签/领域 |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00984 | 门控·条件恢复可用 | P0 | 设条件看启用 |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00985 | 评审·8 态图例 | P0 | 开评审→状态下拉 |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00988 | 详情·价值三字段 | P0 | 点详情 |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00989 | 结果·指数降序 | P0 | 比前两行指数 |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00990 | 指标·ⓘ 口径卡 | P0 | 点指标说明 |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00991 | 治理·阈值角标 | P0 | 点阈值角标 |
| P0-15 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00992 | Tab·候选工作台 | P0 | 切候选工作台 |
| P0-16 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00994 | Tab·最近分析 | P0 | 切最近分析 |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00995 | Tab·三 Tab 往返 | P1 | 三 Tab 循环 |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00996 | 异步·分析中防重 | P1 | 过程态再点开始 |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00997 | 空结果态 | P1 | 冷僻条件发起 |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00998 | 详情·缺失降级 | P1 | 详情找暂无/— |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00999 | 条件变更重分析 | P1 | 改条件→提示→发起 |
| P1-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01000 | 对比篮·招引/培育隔离 | P1 | 浮层两加入按钮 |
| P1-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01001 | 历史·不覆盖当前条件 | P1 | 最近分析再回条件 |
| P1-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01002 | 同条件复用 | P1 | 同条件再开始分析 |
| P1-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01003 | 评审·追溯显隐零泄漏 | P1 | 评审开/关+三 Tab |

## 覆盖说明

- **25/25 已脚本化**：无未脚本化空洞。
- **allow_skip 预置**：
  - P0-05：结果工具栏无「加入招引候选」（实勘仅「加入对比篮」；浮层另有该按钮）
  - P0-14：业务态无阈值角标
  - P1-03：冷僻组合仍非空
  - P1-04：无缺失字段可观察
  - P1-06：对比篮无企业/按钮禁用
- **as-built 偏差**（写期望已吸收）：
  1. 8 产业链项在「行业领域」下拉，页内无独立快捷 chip（P0-07）
  2. 区域标签文案实勘「地域来源」，占位仍「全国 / 全部」（P0-06）
  3. 价值三字段主落点在「详情」抽屉（P0-11）
  4. 8 态图例挂评审态「内部评审状态」下拉（P0-10）
  5. 对比篮关闭钮可能 DOM 存在但 `isVisible=false`——脚本只在可见时点
  6. 同路由培育页（`workspace=cultivation`）不写正向
- **禁止**：培育兄弟页、报告 Reader 专册、对比篮研判闭环 L2/L3 正向展开

## 自检

- [x] 每条用例 ≥1 脚本；func_id 尾号与用例一致
- [x] expect 双层 `{note, assert}`，无裸字符串
- [x] 业务态路径含关评审 / 对比篮仅可见时关闭（P3/P8）
- [x] 未把培育推荐分析正向写进本套
