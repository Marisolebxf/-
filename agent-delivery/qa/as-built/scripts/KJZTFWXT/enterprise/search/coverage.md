# 企业查询 脚本→用例 覆盖表（2026-10-13 v2.0 重写）

蓝本 = `qa/test-cases/KJZTFWXT/enterprise-企业分析/SEARCH-企业查询/FUNC-企业查询-用例.md` v2.0（00438~00480，43 条）。
脚本 43 条（金样 5 + 其余 38），未脚本化声明 0 条（00473→P0-19；00480→P0-20）。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 |
|---------|----------|---------------|---|----------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00438 | 初始态·四层主视觉 | P0 | 侧栏进入企业查询 |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00439 | 初始态·示例回填 | P0 | 点示例查询 chip（A 档·零 allow_skip·机跑绿） |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00440 | 结果态·智能搜索 | P0 | 搜索「人工智能」（A·零 skip·N≥1+main 查看画像；拒命中0假绿） |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00443 | 抽屉·名称打开 | P0 | 点企业名称开抽屉（A；assert 自含检索点名） |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00456 | 结果态·指标说明卡 | P0 | 开评审→hover 竞争力 ⓘ 开说明卡→关评审查泄漏（A·零 skip·父验绿） |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00444 | 高筛·热门场景立即检索 | P0 | 点热门场景 chip |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00441 | 结果态·查企业 | P0 | 查企业搜「科技」 |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00449 | 初始态·最近检索恢复 | P0 | 点最近检索记录 |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00445 | 高筛·字段库与 Footer | P0 | 切高级筛选浏览 |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00446 | 高筛·条件叠加 | P0 | 地区+经营状态+应用 |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00447 | 高筛·地区级联 | P0 | 展开地区选择器 |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00448 | 高筛·查询方案 | P0 | 保存/清空/使用方案 |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00450 | 结果态·四类排序 | P0 | 切换四种排序 |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00458 | 结果态·再筛 | P0 | 经营状态再筛+清除 |
| P0-15 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00462 | 结果态·翻页清选择 | P0 | 勾 2 家+翻第 2 页 |
| P0-16 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00457 | 结果态·批量对比 | P0 | 勾 2 家+加入对比 |
| P0-17 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00455 | 全局·数据路径 | P0 | 网络面板核请求 |
| P0-18 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00442 | 初始态·三模式切换 | P0 | 三 tab 轮切 |
| P0-19 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00473 | 异常·非名称字段召回边界（信用代码） | P1 | B档·结构机检（查企业仅填 USCC→出「查企业结果」标题+observed）；预期①②「不因代码命中/空态或名称无关」manual+ticket **D3-ENTSEARCH-CREDIT-CODE-RECALL**（REWORK：对照 org-field P0-12/P0-13，不硬红挡交卷、不假绿抹设计红；零 allow_skip；不进 gold） |
| P0-20 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00480 | 权限·访客最近检索不落库 | P2 | B档·结构机检（评审开态切 VISIT→唯一 marker 检索→刷新→再切访客+「最近检索」区可见+observed）；预期「不出现可归因该访客的记录」manual+ticket **D3-ENTSEARCH-GUEST-RECENT-PERSIST**（REWORK：对照同入口 P0-19，不硬红挡交卷、不假绿抹设计红；零 allow_skip；不进 gold；D1 访客=VISIT 非匿名） |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00453 | 初始态·推荐企业分区 | P1 | 浏览初始推荐区 |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00467 | 初始态·推荐理由分层 | P1 | 评审模式开/关 |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00476 | 空态·主查询零命中 | P1 | 搜必无命中词 |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00451 | 抽屉·查看画像按钮 | P1 | 点查看画像 |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00469 | 结果态·单企加篮 | P1 | 加入对比+开对比篮 |
| P1-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00471 | 查企业·热门场景 | P1 | 查企业下点热门场景 |
| P1-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00468 | 评审模式·标题溯源 | P1 | 评审模式开/关 |
| P1-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00472 | 空态·再筛局部空 | P1 | 构造再筛零命中 |
| P1-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00459 | 结果态·选择区域 | P1 | 点选择区域控件 |
| P1-10 ← 补充 | —（同上条控件顺带核对，非独立脚本） | — | — | — |
| P1-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00478 | 导出·当前结果 | P1 | 导出完整链+文件核对 |
| P1-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00477 | 初始态·无大模型承诺 | P1 | 扫描可见文本 |
| P1-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00463 | 查企业·热门企业 chip | P1 | 点热门企业 chip |
| P1-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00452 | 高筛·深链 | P1 | 直达 ?mode=advanced |
| P1-15 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00454 | 结果态·匹配反馈 | P1 | 浏览摘要卡 |
| P1-17 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00464 | 高筛·收起展开 | P1 | 收起/展开字段库 |
| P1-18 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00465 | 高筛·编辑回库 | P1 | 结果态点编辑高级筛选 |
| P1-19 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00466 | 结果态·引育候选 | P1 | 引育候选→招引候选 |
| P1-20 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00460 | 结果态·仅长卡形态 | P1 | 浏览形态+查切换控件 |
| P1-21 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00474 | 初始态·清空最近检索 | P1 | 点最近检索清空 |
| P1-22 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00479 | 导出·单企 | P1 | 单企导出完整链 |
| P1-23 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00461 | 结果态·排序方向 | P1 | 切排序方向往返 |
| P1-24 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00475 | 初始态·清词回引导 | P1 | 清空搜索框 |
| P1-26 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00470 | 评审模式·不变选择 | P1 | 勾选+评审开关往返 |

> P1-06 / P1-25 / P1-16 母表未使用（编号空洞，保留不用，避免与历史脚本混淆）。

## 未脚本化声明（0 条）

（无）

## 按需暂缓（本册备注已声明，非本轮脚本范围）

- 00478 水印与导出额度细验（Q035 余量）——需额度/水印专项数据，暂缓。
- 00469 跨模块带参链路（原 00042 口径）——对比篮为系统级功能，跨模块链路归对比篮模块，暂缓。
- 00456 说明卡内部字段深度（评审态字段）——归 P0-05 备注口径，评审字样只进 P1-02/P1-08。
- 00473 / 00480 已分别落 P0-19 / P0-20（D3 票见主表）。
