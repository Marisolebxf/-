# ENT-COMPARE Demo v1.5 验证报告

> 验证日期：2026-07-16
> Demo：`repos/demo-ui-topic`（`dev`）
> 页面：`http://127.0.0.1:4177/enterprise-center/basket`

## 自动校验

- `node tests/enterprise-compare-basket-definition.test.mjs`：通过。
- `node --experimental-strip-types tests/enterprise-compare-return-context.test.mjs`：通过。
- `node --experimental-strip-types tests/enterprise-compare-target-context.test.mjs`：通过。
- `node tests/enterprise-profile-compare-basket.test.mjs`：通过。
- `npm run design:check`：通过。
- `npm run build`：通过；保留既有 chunk size 警告，无构建错误。
- `git diff --check`：Demo 与四件套仓库均通过。
- `ruby -e 'require "yaml"; ... YAML.load_file(...)'`：TRACE 与交付覆盖 YAML 均可解析。

## 浏览器双模式与往返校验

真实页面 DOM 断言结果见 [dom-assertions.json](evidence/dom-assertions.json)。

- 业务模式：不存在 `aria-label="对比篮说明"`；页面不存在“全部来源”筛选；卡片不包含统一社会信用代码或“企业查询”来源标签；筛选恢复动作显示“重置”，不显示“清空筛选”。
- 评审模式：存在 `aria-label="对比篮说明"`。
- 业务与评审模式均显示“发起分析 / 取消选择”，不显示旧“清空选择”；业务模式不泄露评审说明。
- 选择 2 家企业后打开“选择分析任务”：未选任务时“下一步：前往配置”禁用；选择“技术力评估”只更新单选态，不立即跳转。
- 取消任务浮层后仍保留“已选 2 家”；重新打开时不预选旧任务；确认“下一步：前往配置”后携带 2 家企业和 `analysis_type=technology` 进入目标页。
- L1 权限态保留 5 个分析任务并全部置灰，Tooltip 显示升级至 L2 的原因，“下一步：前往配置”保持禁用。
- 1 家短列表时操作栏与工作区底部间距为 0，列表无需滚动；30 家长列表时列表可视高度 489px、内容高度 1430px，滚动前后操作栏 Y 坐标均为 781.5。
- 选择 1 家企业并进入“综合竞争力评估”：目标页显示“来自对比篮”“已选择 1 家企业”和“返回对比篮”。
- 点击返回：关键词“深芯”和“已选 1 家”恢复；会话快照被消费清理。
- “查看引育名单”可选择招引或培育，培育入口直达 `recommendation_tab=cultivation` 并显示已加入候选企业。
- 3 种企业评估与 2 种风险洞察统一展示自动带入的企业名称，并始终保留“从对比篮带入”：从对比篮跳转时可直接配置分析，直接进入页面时可打开选择器导入篮内对象。

## 截图证据

- `evidence/basket-business-mode.png`
- `evidence/basket-filter-reset.png`
- `evidence/basket-review-mode.png`
- `evidence/analysis-task-picker.png`
- `evidence/analysis-task-picker-locked.png`
- `evidence/basket-pinned-action-short.png`
- `evidence/basket-pinned-action-long.png`
- `evidence/evaluation-handoff.png`
- `evidence/basket-restored.png`
- `evidence/candidate-cultivation.png`
- `evidence/capability-locked-object.png`
- `evidence/capability-auto-import-with-control.png`
- `evidence/competitiveness-locked-objects.png`
- `evidence/supply-chain-locked-object.png`
- `evidence/pain-points-direct-import.png`

## 剩余边界

- 本报告只验证 Demo v1.5；lumen 正式实现和服务端单用户持久化契约不在本次修改范围内。
- 未修改任何任务状态、认领关系或任务登记。
