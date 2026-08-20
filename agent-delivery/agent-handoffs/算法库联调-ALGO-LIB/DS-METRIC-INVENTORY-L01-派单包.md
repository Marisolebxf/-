# 派单包 · DS-METRIC-INVENTORY-L01

> **状态**：backlog（专题 `TOPIC-METRIC-INVENTORY-L01` + `TOPIC-METRIC-CLASSIFY-L01` 过审后 unlock）  
> **Agent**：`algorithm-agent` · **supervised_by**：`human:唐绍祖`  
> **依赖**：专题两叶

## 1. 目标

从 `srs/02-科技信息展示系统/` 抽出展示系统指标/能力清单；每条标注 `impl_owner`：

`我方前端展示` | `久新API` | `燕大API` | `专题算法复用`

我们负责整体前端与协调；人才/科研机构/技术相关指标定义与实现、知识图谱 API 不归我方算法展开。

## 2. 产出

`ds-inventory.yaml`（每条 `level`+`parent_id`+`impl_owner`）· `ds-hierarchy.md`（按 DS 模块展开一/二/三级）· `ds-README.md` · `ds-gaps.md`  
招标未写下级 → `level_absent: true`，**禁止**为凑三级而发明指标。  
handoff：`DS-METRIC-INVENTORY-L01.md`

## 3. `/goal`（unlock 后粘贴）

```text
/goal
task: DS-METRIC-INVENTORY-L01
agent: algorithm-agent
supervised_by: human:唐绍祖
强度：definition/spike；不写代码。

先读：给人说明-指标盘点-2026-08-20.md、本派单包、srs/02-科技信息展示系统/、专题侧 inventory 对照。
认领后抽出 ds-inventory（含 impl_owner、level、parent_id）+ ds-hierarchy.md → handoff → review
```
