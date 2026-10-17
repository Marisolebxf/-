# 重点布局产业推荐 · 功能点覆盖（chain.layout / L26）

> catalog `chain.layout` · 50897 · path `/chain/layout`  
> 用例 `API-重点布局产业推荐-用例.md`  
> A 线范围：**L26**（`fp-split-by-api-run/work/L26.md`）  
> 功能点键：`L26 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| chain.hotspot.recommendation | GET | /innov/v1/industry/{chainId}/recommendation | API-000394～API-000398 | catalog `status=unavailable` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L26 \| chain.hotspot.recommendation \| chainId \| 算法输入-chainId产业标识 | catalog chainId | API-000396、API-000397 | 部分覆盖 | 非法 id 与缺 path；live 成功校验待 endpoint available 后补主路径 |
| L26 \| chain.hotspot.recommendation \| recommend_index \| 算法输出-recommend_index产业推荐指数 | catalog recommend_index | API-000398 | 契约占位 | unavailable，禁止 sample 指数作通过条件 |
| L26 \| chain.hotspot.recommendation \| recommend_level \| 算法输出-recommend_level重点布局推荐等级 | catalog recommend_level | API-000398 | 契约占位 | 同上 |
| L26 \| chain.hotspot.recommendation \| _empty \| 布局推荐无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法 chainId 必空」试调证据（附录 LAY-04 仅文档参考） |
| L26 \| chain.hotspot.recommendation \| _fail \| 布局推荐查询失败 | 契约错误态 | API-000394、API-000396、API-000397 | 已覆盖 | 含 catalog 不可用与入参失败语义 |
| L26 \| \| etl_clean_standardize \| 多源产业数据标准化清洗 | 需规（1）采集清洗 | — | 未覆盖 | req_only，无 catalog endpoint |
| L26 \| \| scale_growth_potential_advantage \| 规模增长率潜力与优劣势识别 | 需规分析阶段 | — | 未覆盖 | req_only |
| L26 \| \| advantage_problem_fusion \| 优势与问题识别结果融合 | 需规优势+问题输入 | — | 未覆盖 | req_only |
| L26 \| \| expert_recommend_strategy \| 专家推荐策略参数驱动 | 需规专家策略 | — | 未覆盖 | req_only |
| L26 \| \| index_rank_layout_select \| 指数排名筛选重点布局产业 | 需规排名筛选 | — | 未覆盖 | req_only |
| L26 \| \| dynamic_strategy_refresh \| 策略动态优化与结果刷新 | 需规动态优化 | — | 未覆盖 | req_only |
| L26 \| \| ranking_trend_layout_outputs \| 排名清单趋势图表与布局报告 | 需规（2）四类输出 | — | 未覆盖 | req_only |
| L26 \| \| demand_tag_region_category \| 需求标签区域与产业类别范围 | 需规（3）调用范围 | — | 未覆盖 | req_only |
| L26 \| \| trend_monitor_report_export \| 趋势监测与报告导出 | 需规（3）监测导出 | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 1（`_fail` 行） |
| 部分覆盖 | 1（`chainId`） |
| 契约占位 | 2（`recommend_index`、`recommend_level`） |
| 未覆盖 | 10（含 `_empty` 1 + req_only 9） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000394～API-000398 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
