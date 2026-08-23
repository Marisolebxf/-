# 4.1/4.2 六级栏名扫漏报告

> **状态**：✅ **已闭合**（2026-08-23）  
> **验收仓**：`demo-ui-science` @ `origin/dev` `596b01d`  
> **验收脚本**：`repos/demo-ui-science/scripts/verify-l6-titles.mjs`（`--strict` 闸门）  
> **方案真源**：`tech-dev-trend-and-policy-l6-rename-plan.md`

## 摘要

| 指标 | 补漏前（初扫） | 补漏后（复扫） |
|------|---------------:|---------------:|
| 需改项（非 OK） | 247 | 247 |
| 源码已精确命中 | 182 | **247** |
| 仍缺失 | 64 | **0** |
| 空格/写法变体 | 1 | **0** |

```text
node scripts/verify-l6-titles.mjs --strict
# L6 verify (4.1/4.2 non-OK): 247 targets
#   present: 247
#   missing: 0
```

## 闭合提交（demo-ui-science）

| Commit | 说明 |
|--------|------|
| `0c0f200` | 态势·全景·政策·全球创新/湾区/深圳 六级栏名补漏 |
| `596b01d` | 科技指数逐字修正 + `verify-l6-titles.mjs` / `verifyL6Titles.test.mjs` |

此前批次：`3b044f2` · `577e31b` · `3dea055` · `9b3b78a`（同 Epic 前置改名）。

## 原 64 项缺口 — 已全部闭合

初扫缺失项（地图操作、科学技术全景、全球创新、湾区、深圳、科技指数、政策检索等）均已通过可见标题（`pp-l6-section-title` / `panel-title` / `aria-label` / Tab 文案）写入源码。完整清单见 git 历史与本文件初版（`git show` 旧版）或方案 §2–§3。

代表性闭合项：

- `1.1.1.1.4.1.1.1.1` **放大/缩小** · `1.1.1.1.4.1.1.1.2` **拖动平移** · `1.1.1.1.4.1.1.2.3` **图层分组与组织**
- `1.1.1.1.4.1.2.*` 科学技术全景 / 图谱维护全链路
- `1.1.1.1.4.1.4.*`–`1.1.1.1.4.1.6.*` 全球创新 / 湾区 / 深圳
- `1.1.1.1.4.1.8.2.1` **专家H指数排行可视化**（无空格变体）
- `1.1.1.1.4.2.1.1.2`–`1.1.1.1.4.2.1.1.6` 政策高级检索与结果处理

## 关于「旧近义名仍残留」（初扫 171 项）

初扫用**子串匹配**标出「详情」「筛选」「创新」等通用词共存页面，**不等于六级栏名未改**。闭合判定以 `verify-l6-titles.mjs` 对 247 个目标字符串的**全文精确命中**为准。

人工走查建议（非闸门）：

- 确认 L6 标题节点未被更短近义词**替代**（应并存于 `aria-label` / `pp-l6-section-title`，而非仅保留近义按钮文案）
- 五级容器名（如科技指数 Tab **排行榜**）与六级名（**科技成果综合排名**）分层正确，勿混为同一 Tab

## 已知非闸门项

| 项 | 说明 |
|----|------|
| `techIndexRankingLayout.test.mjs` 部分断言 | mockData 字段结构等**既有**失败，与 L6 精确命中无关 |
| `PolicyPanorama.test.mjs` import 断言 | 改前已存在 |
| 方案 §3 核增 `4.2.4` 17 项 | 本闸门仅覆盖主文 4.1 + 4.2（247 项）；核增另单 |

## 复扫命令

```powershell
cd ${GKX_ROOT}/repos/demo-ui-science
node scripts/verify-l6-titles.mjs --strict
node --test src/verifyL6Titles.test.mjs
```
