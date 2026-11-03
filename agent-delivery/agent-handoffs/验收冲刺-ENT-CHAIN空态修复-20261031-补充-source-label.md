# HANDOFF 补充：识别依据来源标注中文化 + svc 测试闸门收口（2026-11-02）

> 归属：`验收冲刺-ENT-CHAIN空态修复-20261031.md` 的追加单。

## 变更

1. **来源位置去英文字段名**（`a41506e`）：「产业链挂接」卡 `source_label` 由「产业链挂接模型结果 / industry_chains」改为「**专题产业链挂接数据**」（测试要求 UI 不得出现英文字段名；风格对齐另外两卡「企业登记信息 / 经营范围摘要」「专利与技术标签摘要」）。前端 mock fixture 本就中文，无前端改动。
2. **svc 契约测试对齐**（`db765e9`）：pipeline 3493 `py:smoke` 红为同日 `2cc3d4e`（org_coverage/tech_power 不再下推 industry）漏改测试，非本会话引入；断言改为 URL 不带 `industry=`，闸门收口。

## 验证

- key_analysis / svc_task 相关 21 tests 绿；pipeline **3498 全绿**（py:smoke + 四镜像 + deploy:search-py/ai-py/ai-worker/show-py 全部 success）
- 存量说明：本机 `test_meta_dimension_endpoints` / `test_query_tree_dsl` 3 例失败经 stash 对照确认与本改动无关（其他会话遗留），未在本单处理

## 生效

刷新页面重新打开识别依据弹框即可（接口实时返回，无任务重跑）。
