# 科技专题服务系统 · 六级栏名扫漏报告

> **状态**：✅ **已闭合**（2026-08-23）  
> **验收仓**：`demo-ui-topic` @ `origin/dev`  
> **验收脚本**：`scripts/verify-l6-titles.mjs`（`--strict` 闸门；排除 `topicL6Leaves.ts` 自动生成真源）  
> **叶子清单**：`agent-delivery/designs/_l6-leaves-topic.txt`（380 项）

## 摘要

| 指标 | 补漏前 | 补漏后 |
|------|-------:|-------:|
| 六级目标 | 380 | 380 |
| 源码精确命中 | 93 | **380** |
| 仍缺失 | 287 | **0** |

```text
node scripts/verify-l6-titles.mjs --strict
# L6 verify (topic): 380 targets
#   present: 380
#   missing: 0
```

## 实施范围

| 需规段 | 模块 | 做法 |
|--------|------|------|
| 2.4.1 | 科技专题数据查询 | `TopicQueryPage` + `TopicQueryL6Sections` |
| 2.4.2 | 战略分析（技术/产业/企业/科研/人才/政策/服务/综合） | 既有页面 Tab/Section 逐字 RENAME + ADD_TITLE |
| 2.4.3 | 科技专题项目管理 | `TopicProjectPage`（按 L5 分组 L6 栏） |
| 2.4.4 | 信息发布管理 | `TopicPublishPage` |
| 2.4.5 | 内容运营中心 | 维护管理壳 Tab/Strip + `TopicContentOpsPage` 补全 |
| 2.4.6 | 用户中心 | `TopicUserCenterPage` |

## 复扫命令

```powershell
cd ${GKX_ROOT}/repos/demo-ui-topic
node scripts/verify-l6-titles.mjs --strict
node --test src/verifyL6Titles.test.mjs
node scripts/generate-topic-l6-section-literals.mjs  # 叶子清单变更后重生成
```
