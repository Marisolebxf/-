# 企业技术力评估对比分析 脚本→用例 覆盖表（BATCH32 回炉 r4 2026-10-14）

蓝本 = `qa/test-cases/KJZTFWXT/enterprise-企业分析/EVALTECH-企业技术力评估对比分析/FUNC-企业技术力评估对比分析-用例.md` v2.0（00900~00929，30 条）。
**本轮自动化 30 条**（A 金样 5 + B 其余 25）；**本轮不自动化 0 条**（00916 已回填 P0-15、00917 已回填 P0-16、00923 已回填 P0-19、00924 已回填 P0-20、00925 已回填 P0-21、00926 已回填 P0-22）。
env-gate：`fixtures/scout/env-gate.json` → **overall=fail**（ticket=`ENV-EVAL-TECH-PRECHECK-001`）。
金样锁定 id：P0-01~05；语义随 A 档可绿路径重绑（P0-05 现绑 00902 空态门控，原 00913 过程态本轮不自动化）。
**r4**：关闭对比篮须 `visible+enabled` 才点（DOM 常驻 hidden 硬点会卡 30s）；类型筛 as-built=`placeholder=全部企业类型`。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 | 档(A/B) | skip ticket |
|---------|----------|---------------|---|----------|---------|-------------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00900 | 入口·路由标题 | P0 | 进入技术力评估页 | A | — |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00903 | 浮层·选择分析企业 | P0 | 点前往对比篮选择企业 | A | — |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00907 | 模板·三态分组 | P0 | 打开模板下拉 | A | — |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00908 | 指标·默认五维权重 | P0 | 浏览指标与权重区 | A | — |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00902 | 对象·空态门控 | P0 | 空态+开始分析禁用 | A | — |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00901 | 同壳·mode 隔离 | P0 | 切 business/competitiveness | B | — |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00906 | 数据覆盖·五档可信度筛选 | P0 | 回填后浏览覆盖区+展开筛选 | B | —（as-built 下拉非 Tab，见 as_built_note） |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00904 | 浮层·确定回填+预检门控 | P0 | 勾选 2 家确定 | B | —（断言 as-built 门控，非 skip） |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00913 | 过程态·开始分析双分支 | P0 | 开始分析→过程态/结果态 | B | —（business 壳 P0-05 双分支模板移植；2026-10-15 实勘甲分支可达） |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00909 | 指标·勾选移除 | P0 | 取消/恢复勾选 | B | — |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00910 | 权重·调节非法值 | P0 | 上下调+非法输入 | B | — |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00911 | 权重·一键均分 | P0 | 一键平均分配 | B | — |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00914 | 结果态·完成迁移与得分呈现 | P0 | 开始分析→轮询 view=result | B | —（双分支移植 P0-09；catalog 备注金样，gold 提升待父裁） |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00915 | 结果态·雷达对比 | P0 | 结果态后浏览雷达区块（X3 代理断言） | B | —（复用 P0-13 三分支前置；2026-10-15 实勘回填） |
| P0-15 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00916 | 结果态·技术力加权排名 | P0 | 结果态后浏览排名区块（默认降序） | B | —（REWORK C6：body 90s 轮询 + 保 fp reload / 最近评估「恢复结果」；禁冷深链；ticket=ENV-EVAL-TECH-RESULT-SHELL-001 仅真空壳） |
| P0-16 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00917 | 结果态·差距分析报告 | P0 | 点「查看 HTML 报告」→ view=report | B | —（复用 P0-15 三分支；2026-10-15 实勘回填；入口文案 D1） |
| P0-17 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00928 | 异常·仅 1 家拦截 | P0 | 勾 1 家 | B | — |
| P0-18 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00929 | 异常·权重/指标校验门控 | P0 | 偏权重/清空指标 | B | —（第三点 as-built 预检门控） |
| P0-19 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00923 | 结果态·调整配置返回 | P1 | 点「调整配置」→配置态 | B | —（主路径最近评估→恢复结果；用例册回填列曾写 P1-08，本波 GAP 落 P0-19；零 allow_skip） |
| P0-20 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00924 | 结果态·重新分析 | P1 | 点「重新分析」→过程态+新 task_id | B | —（主路径最近评估→恢复结果；用例册回填列曾写 P1-09，本波 GAP 落 P0-20；零 allow_skip） |
| P0-21 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00925 | 过程态·取消任务 | P1 | 点「取消任务」→离开过程态+配置保留 | B | ENV-EVAL-TECH-PROCESS-WINDOW-001（用例册回填列曾写 P1-10，本波 GAP 落 P0-21；allow_skip） |
| P0-22 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00926 | 过程态·稍后查看 | P1 | 点「稍后查看」→离开过程态+我的任务计数不减 | B | ENV-EVAL-TECH-PROCESS-WINDOW-001（用例册回填列曾写 P1-11，本波 GAP 落 P0-22；allow_skip） |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00905 | 浮层·按钮门控 | P1 | 未勾选禁用/取消选择 | B | — |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00912 | 抽屉·指标明细 | P1 | 点查看 | B | — |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00918 | Tab·当前/最近 | P1 | Tab 往返 | B | — |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00919 | 模板·加载恢复 | P1 | 系统/个人模板 | B | — |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00920 | 模板·保存 30 字 | P1 | 保存为个人模板 | B | — |
| P1-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00921 | 浮层·搜索筛选重置 | P1 | 搜索/类型/重置 | B | — |
| P1-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00922 | 对象·移除 | P1 | 点移除 | B | — |
| P1-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00927 | 评审·显隐零泄漏 | P1 | 内部评审开关往返 | B | — |

## 本轮不自动化（env-gate fail · 过程链残留）

| 用例编号 | 原因 | ticket |
|----------|------|--------|
| — | （无）00926 已由本波 GAP 落盘 P0-22 | — |

> 00925/P0-21、00926/P0-22 均为 B 档 allow_skip+ticket（过程窗实勘不可稳达）；禁止假金样 / 裸 allow_skip。

## 覆盖说明

- **脚本条数**：A=5，B=25（含 P0-07、P0-09、P0-13、P0-14、P0-15、P0-16、P0-19、P0-20、P0-21、P0-22），合计 30；**allow_skip 2/30 ≈ 6.7%**（P0-21、P0-22）。
- **expect**：双层 `{note, assert}`，无裸字符串；金样 **零 allow_skip**。
- **env-gate**：登录✅ 深链✅ 关评审✅ 选 2 家✅ → 开始分析 **disabled** +「预检未返回企业明细」→ overall **fail**。
- **as-built 偏差**：
  1. D1 空态文案 =「请先在对比篮选择企业…」+ CTA「前往对比篮选择企业」
  2. D3 回填后预检失败 → 开始分析仍 disabled（P0-08/P0-18 第三点跟现场门控，不写过程态）
  3. 对比篮层挡点击须先关；评审开关用 `aria-label=内部评审模式`
  4. D2 五档「可信度筛选 Tab」as-built 为下拉筛选（`aria-label=筛选数据可信度`，2026-10-15 实勘；P0-07 跟现场）
  5. P0-09 双分支移植 business 壳 P0-05；2026-10-15 tech 壳实勘过程态真实可达（15~20s 完成迁移，非 business 壳近即时），蓝本 4 点零新增偏差
  6. P0-13（00914 结果态进入）同日按 P0-09 双分支骨架回填；三要素收口（URL view=result+task_id、结果区标题、\d+分 得分呈现，数值不钉死）；迁移证据 fixtures/scout/probe-p009.json；catalog 备注金样，tier 暂 B 待父裁
  7. P0-14（00915 结果态雷达）2026-10-15 复用 P0-13 三分支前置回填；雷达 X3 代理断言（标题同词 + 区块内 canvas 轮询 + 5 项指标名正文 + 对象 A/B + ≥2 企业名）；ECharts canvas 内部归 observed（生产构建未暴露 window.echarts，证据 fixtures/scout/probe-p014.json / probe-p014b2.json / probe-p014v3.json）
  8. P0-14 与 P0-13 差异：2026-10-15 慢态实证（probe-p014v3）——点开始分析后 URL 可不迁移 view=result、结果内容原地渲染（20~40s），P0-13「30s 窗 + URL 三要素统一收口」在慢态会假性超窗；P0-14 expect1 扩为双形态收口（快=URL 三要素 / 慢=body 结果区标题+\d+分，URL 仅核 workspace=technology），建议父单对 P0-13 回炉（本轮禁改兄弟 case）
  9. P0-15（00916 结果态排名）：2026-10-15 无头 probe-p015.json——标题 D1「技术力加权排名」；canvas+紧邻诊断表代理名次/得分；默认降序 scores_desc=true；升序入口缺失 D2（开放项 4）；零 allow_skip。REWORK（验收 C6）：旧无 fp 冷深链假空壳（probe-p015-rework）；改 body 90s + reload 保 fp /「恢复结果」（probe-p015-restore 对 tid-004 可绿）；仍空真红 ENV-EVAL-TECH-RESULT-SHELL-001
  10. P0-16（00917 差距报告）：2026-10-15 无头 probe-p016c/d.json——入口 D1「查看 HTML 报告」（非「差距分析报告」文案）；同页 view=report+report_id；只读报告+技术力评估报告可读；关键发现「领先/差距」同源摘要（无独立「技术优势/技术差距」标题 → D1）；零 allow_skip；冷深链无 fp 落「返回配置」不主路径
  11. P0-19（00923 调整配置）：2026-10-15 无头 probe-p019.json——恢复结果后点「调整配置」→ 离开 view=result；配置态「评估对象」+「开始分析」；CTA D1「返回对比篮」；对象保留 observed；用例册曾写 P1-08→本波落 P0-19；零 allow_skip；不进 gold
  12. P0-20（00924 重新分析）：2026-10-15 无头 probe-p020.json——恢复结果后点「重新分析」→ view=processing +「技术力评估生成中」；task_id 004→005；用例册曾写 P1-09→本波落 P0-20；零 allow_skip；不进 gold；配置态预检闸门不挡本条（历史结果链）
  13. P0-21（00925 取消任务）：2026-10-15 无头 probe-p021*.json——重新分析可进 view=processing 但「任务不存在或已失效」无取消钮（D3/D4）；或当天复用跳过过程窗；B 档 allow_skip+ENV-EVAL-TECH-PROCESS-WINDOW-001；用例册曾写 P1-10→本波落 P0-21；不进 gold
  14. P0-22（00926 稍后查看）：2026-10-15 无头 probe-p022.json——同路径进 view=processing 空壳无「稍后查看」/「打开我的任务」（D3/D4）；B 档 allow_skip+ENV-EVAL-TECH-PROCESS-WINDOW-001；用例册曾写 P1-11→本波落 P0-22；不进 gold

## 自检

- [x] 金样无 `allow_skip`；expect 双层
- [x] B 档 skip 占比 ≤25%（本轮 2/30 ≈ 6.7%）
- [x] coverage 含列：档(A/B)、skip ticket
- [x] `fixtures/scout/env-gate.json` 已落盘
- [x] 未改 catalog；自跑 `run-scripts.mjs --only P0-01,P0-02,P0-03,P0-04,P0-05` 全绿（见 runs/`*-eval-tech-r4-self`）
