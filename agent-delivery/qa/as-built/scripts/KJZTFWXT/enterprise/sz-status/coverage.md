# 深圳企业现状分析 脚本→用例 覆盖表（2026-10-14）

蓝本 = `qa/test-cases/KJZTFWXT/enterprise-企业分析/SZSTATUS-深圳企业现状分析/FUNC-深圳企业现状分析-用例.md` v2.0（00960~00978，19 条）。
脚本 19 条（金样 5 + 其余 14，includes 展开），与用例 **1:1**，无未脚本化声明。

编号依据：用例册金样清单 P0-01=00960 · P0-02=00964 · P0-03=00966 · P0-04=00967 · P0-05=00969；其余按用例顺序顺延 P0-06~P0-14 / P1-01~P1-05。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 |
|---------|----------|---------------|---|----------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00960 | 入口·路由默认 Tab | P0 | 进入深圳现状页 |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00964 | 筛选·选链生效 | P0 | 下拉选人工智能 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00966 | 结果·六区块 | P0 | 选链后核对六区块 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00967 | 清单·表格列 | P0 | 核对列与记录数 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00969 | 对标·城市池 | P0 | 切对标 Tab |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00961 | 筛选·区域锁定 | P0 | 核对区域 disabled |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00962 | 筛选·链选项构成 | P0 | 开下拉核 8 项 |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00963 | 空态·未选链引导 | P0 | 默认态核对 |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00965 | 过程态·提取中 | P0 | 选链立即看 loading |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00968 | 清单·空态提示 | P0 | 空数据清单 |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00970 | 对标·三项指标 | P0 | 对标指标区核对 |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00971 | 对标·缺口径 | P0 | 暂不可用/无数据 |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00972 | 对标·优势短板 | P0 | 相对优势/短板 |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00973 | 对标·计算中 | P0 | 切 Tab 看过程态 |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00974 | Tab·往返保留 | P1 | 对标↔定位往返 |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00975 | 筛选·切链刷新 | P1 | 改选生物医药 |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00976 | 批量栏·全选计数 | P1 | 全选当前结果 |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00977 | 报告·打开返回 | P1 | 查看 HTML 报告 |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00978 | 评审·追溯显隐 | P1 | 评审开/关往返 |

> 金样 = P0-01/02/03/04/05（id 锁定禁改）。

## 覆盖说明

- **19/19 全脚本化**：00960~00978 每行恰一脚本；无未脚本化。
- **expect**：双层 `{note, assert}`；00978 结构性 4 点；其余 1~3 点。
- **allow_skip**：P1-04（报告浮层文案不可识别时 Pass-N/A）。
- **as-built 偏差**（不升 Fail，见各条 as_built_note）：
  1. 页内无可见快捷 chip，8 链仅在下拉 option（P0-02/P0-07 用下拉验收选链/构成）
  2. 清单表多「选择」「产业链环节」列（P0-04 仍验用例四列存在）
  3. 对标同时有雷达 + 城市表，表含产业链完整度列
  4. 空数据结果态数值多为 0 / 暂不可用 / 无数据
  5. 系统对比篮浮层非本册对象；执行前建议关闭以免挡主区
