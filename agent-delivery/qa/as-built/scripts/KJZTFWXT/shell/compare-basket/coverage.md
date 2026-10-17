# 系统对比篮 脚本→用例 覆盖表（2026-10-14；entry `shell-compare-basket`）

蓝本 = `qa/test-cases/KJZTFWXT/enterprise-企业分析/COMPARE-对比篮/FUNC-对比篮-用例.md` v2.0（00481~00510，30 条）。
脚本 **30** 条（金样 5 + 其余 25，includes 展开）；未脚本化 **0**。

编号真源：用例册「自动化用例ID」列（既填）+ 本目录 `func_id`。  
金样 yaml 锁定 P0-01~05 = 00481~00485。用例元信息另列「金样」00482/83/86/92/95——其中 00486/92/95 落在 P0-06/P0-12/P0-15，仍在全量；差异记本表，不以元信息改写已填自动化列。  
P0-07 槽位补 00491（原自动化列空缺）。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 |
|---------|----------|---------------|---|----------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00481 | 入口·浮层结构 | P0 | 点对比篮入口展开 |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00482 | 收集·多源去重 | P0 | 两次加入同企业 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00483 | 恢复·近时倒序 | P0 | 移除再加入后刷新 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00484 | 轻筛·名称搜索 | P0 | 填名称搜索/清空 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00485 | 轻筛·类型筛选 | P0 | 选类型+重置 |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00486 | 选择·全选三态 | P0 | 全选/改筛/取消选择 |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00491 | 分发·风险洞察 | P0 | 供应链→下一步 |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00487 | 操作栏·布局 | P0 | 浏览底部栏+滚动 |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00488 | 发起·前置 | P0 | 未选/勾选开任务浮层 |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00489 | 任务·1+3+2 分组 | P0 | 浏览任务浮层 |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00490 | 分发·评估 | P0 | 评估→下一步 |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00492 | 分发·领域分布 | P0 | 领域分布→下一步 |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00493 | Tab·往返 | P0 | 切非企业 Tab 再回 |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00494 | 移除·单个 | P0 | 点卡片移除 |
| P0-15 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00495 | 空态·引导 | P0 | 空篮打开 |
| P0-16 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00496 | 数量·上限矩阵 | P0 | 勾 3/2 家看供应链 |
| P0-17 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00510 | 权限·评估任务保留说明 | P2 | B档·切 VISIT→开任务浮层验评估项保留+权限说明；skip ticket=`ENV-SHELL-COMPARE-NO-RESTRICTED-EVAL-ACCT`（实勘篮空/无差异化账号；企业 picker 无 perm UX→日后可达必红 D3） |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00497 | 互斥·任务窗 | P1 | 篮↔任务往返 |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00498 | 兼容·旧 basket | P1 | 打开旧链 |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00499 | 候选·加入招引 | P1 | 加入招引候选 |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00500 | 清空·二次确认 | P1 | 清空确认 |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00501 | 名单·查看引育 | P1 | 查看引育名单 |
| P1-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00502 | 返回·现场恢复 | P1 | 分发后回篮 |
| P1-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00503 | 边界·篮内无结论 | P1 | 浏览浮层/任务层 |
| P1-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00504 | 异常·满员 50 | P1 | 第 51 家加入 |
| P1-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00505 | 异常·空结果禁用全选 | P1 | 无匹配搜索 |
| P1-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00506 | 宿主·查询无聚合 | P1 | 打开企业查询 |
| P1-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00507 | 宿主·Drawer 接力 | P1 | Drawer 内查看对比篮 |
| P1-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00508 | 异常·恢复失败 | P1 | 断网开篮+重试 |
| P1-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00509 | 边界·取消不收起 | P1 | 任务浮层取消 |

> 金样 = P0-01~P0-05（id 锁定）。P0-17 用例优先级 P2，脚本 id 前缀独立勿混读。

## 未脚本化

| 用例编号 | 原因 |
|----------|------|
| — | 本轮 00481～00510 均已脚本化（00510→P0-17，2026-10-15 GAP 补齐） |

## 覆盖说明

- **30/30 已脚本化**；00510→P0-17（B / allow_skip+ticket）。
- **allow_skip 预置**：P0-02/03/05/14/16/17、P1-01/02/04/08/11/12（数据/环境不足时 Pass-N/A）。
- **as_built 偏差（写期望已吸收，不升 Fail）**：
  1. Tab：用例五 Tab（含政策）；实勘仅企业/产业/服务机构/区域·开发中，**政策 Tab 缺失**。
  2. 任务名：实勘「企业发展痛点分析」≠ 用例「发展痛难点」。
  3. 入口 dual：页头 button「对比篮」+ 右下 dock `aria-label=打开对比篮，共 N 项`。
  4. 搜索 placeholder：`按企业名称搜索`；类型：`全部企业类型`。
  5. 任务浮层：`.arco-modal.analysis-picker-modal`，标题「选择分析任务」。
- **范围**：只测对比篮本身；目标页（评估/领域/风险/引育）仅验「来自对比篮」到达徽记。
- **破坏性**：P0-15 / P1-04 清空会改会话篮数据；全量顺序见 `full.md`。
