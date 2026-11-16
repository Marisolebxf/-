# POL-L2-PC3-PC4-WRITE-L01 · 写入政策对比研报一行

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 开工时已是 in_progress。本叶不重新认领，不改 task-registry。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用检索、`policy_text_parse` 和已有四个拆解 Job。不新注册模型，不新依赖，不把对比结果写入 gapfill。 |

## 修改内容

- 接口：`POST /internal/policy/compare-report`（`vendor/entan-py/api/policy_routes.py`）。
- 写入：`vendor/entan-py/polan/compare_report.py` → `gkxlumenx_ads.ads_policy_compare_report` 一行。Java 不写。
- 写入前执行 `scripts/mysql/ads_policy_compare_report.sql`（`CREATE TABLE IF NOT EXISTS`，可重复）。
- 政策编号只取检索命中。请求带标题时，用稳定片段检索，不用编造编号。
  - `固态电池产业发展行动方案`，标题须同时含「珠海」「固态电池」。
  - `新型储能产业发展规划`，标题须同时含「深圳」「新型储能」。
  - 先按地区、效力级别检索；没有命中再放宽级别，再放宽地区。命中不足两份则失败，不插入完成行。失败文案：`这次对比没有写出来，可稍后重试`。
- 材料：先读 `policy_text_parse.structured_elements`，语义侧面再读已有 `gapfill_policy_semantic`（只读）。缺的维才提交已有 Job：`policy_parse_semantic`、`policy_parse_clause`、`policy_parse_metric`、`policy_parse_entity`。
  - 条款内容 ← 607 条款。
  - 核心指标、扶持力度 ← 608 指标和力度。
  - 适用范围、实施路径 ← 606 语义（适用场景 / 约束或条款分类）。
  - 知识图谱点边 ← 609 实体和关联。
- 某一维拆完仍空：该维正文为「这次对比没有识别出」加该维名字。点或边为空时图注为「这次对比还没有这张图」。
- 研报溯源两条路径：`原文→条款→结论`、`结论→条款→原文`。正文过滤含「演示」或「mock」的摘录。
- D4 仍是 mock。本叶不改指标注册表，不把 D4 改绿。

## 指纹

当天（`created_at` 落在本地自然日）同一指纹已有 `status=已完成` 则直接返回该行，不再插入。

指纹 = SHA-256 十六进制（64 字符）。原文是下面对象的 JSON（`sort_keys`，中文不转义）：

- `policy_ids`：政策编号排序后的列表
- `dims`：请求里的维度；缺省为条款内容、核心指标、扶持力度、适用范围、实施路径
- `weight`：请求里的权重；缺省各维为 1
- `threshold`：阈值字符串，缺省 `0`
- `time_window`：时间窗字符串

地区和效力级别不进指纹。

## 样本

地区广东省，效力级别市级。检索命中：

| 政策 | 编号 |
|------|------|
| 珠海市人民政府办公室关于印发《珠海市推动固态电池产业发展行动方案（2025-2030年）》的通知 | `cn-zh-3840797` |
| 深圳市人民政府办公厅关于印发《深圳市新型储能产业发展规划（2026—2030年）》的通知 | `SYN2026111046a36ecf4c` |

珠海已有条款，没有语义、指标和实体，因此走了已有 semantic / metric / entity 三个 Job。其中 `policy_parse_semantic` 按该 Job 原设计写入了已有表 `gkxlumenx_gapfill.gapfill_policy_semantic`，没有新建 gapfill 表。深圳四块已齐，没有再跑 Job。对比行本身只在 `gkxlumenx_ads.ads_policy_compare_report`。

珠海这侧核心指标、扶持力度分数是 0：已有指标 Job 没有抽出额度。维度正文用了深圳一侧识别出的指标和力度。五个维度都有分数。四类识别、点边、摘要、结论、深度四块、四类洞察、章节、双向溯源都在这一行。正文不含「演示」「mock」。

活行：已插入。`run_id=5ad8bcba9fae419e835ae2f3fed6a662`，`status=已完成`，`created_at=2026-11-17 01:18:06`。

## 测试结果

不连真库：

```
python -m pytest tests/test_policy_compare_report.py -q
...                                                                      [100%]
3 passed in 1.03s
```

假连接里的库返回上面两份标题对应的编号。断言完成行含五个维度分数、四类识别、点边、摘要、结论、深度四块、四类洞察、章节、双向溯源，正文不含「演示」「mock」。同一天再请求一次，返回同一 `run_id`，表内仍是一行。

## 涉及文件

- `repos/lumen-algo-py/vendor/entan-py/polan/compare_report.py`
- `repos/lumen-algo-py/vendor/entan-py/api/policy_routes.py`
- `repos/lumen-algo-py/tests/test_policy_compare_report.py`

## CI/CD

- 分支：`origin/dev`
- lumen-algo-py commit：`9a784b42446960e1c398f3ba24f5754803b942cc`
- 未改 Java、前端、金路径。未改 Nacos。未改 task-registry。
