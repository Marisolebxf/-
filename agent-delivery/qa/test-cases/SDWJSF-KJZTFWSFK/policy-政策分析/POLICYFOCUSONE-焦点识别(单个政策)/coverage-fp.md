# 焦点识别(单个政策) · 功能点覆盖（policy.focus-one / L35 单政策变体）

> catalog `policy.focus-one` · 50897 · path `/policy/focus-one`  
> 用例 `API-焦点识别(单个政策)-用例.md`  
> **A 线范围**：**L35** 同能力单政策变体（主挂页 `policy.focus`；本 catalog 页按 `fp-split-by-api-run/_l6-to-catalog-map.yaml` catalog_skip「挂 L35 时按 path 去重」；功能点语义见 `fp-split-by-api-run-v0-202609/work/L35.md` POST 段，非当前 `work/L35.md` GET-only 稿）  
> 功能点键：`L35 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| policy.focus-one.main | POST | /policy/v1/policy/analysis/focus-one | API-000454～API-000458 | catalog `status=unavailable` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L35 \| policy.focus-one.main \| mode \| 算法输入-mode识别模式 | catalog mode | API-000457 | 已覆盖 | 非法枚举外取值；合法 rule/llm 主路径待 endpoint available 后补 |
| L35 \| policy.focus-one.main \| title \| 算法输入-title政策标题 | catalog title | API-000454 | 部分覆盖 | FOC-01 随样例携带；单独校验待 live |
| L35 \| policy.focus-one.main \| text \| 算法输入-text政策文本 | catalog text（必填） | API-000454、000456、000458 | 已覆盖 | 缺键与空串失败；与空态验收区分 |
| L35 \| policy.focus-one.main \| execution \| 算法输入-execution执行数据 | catalog execution | API-000454 | 部分覆盖 | FOC-01 随样例携带 |
| L35 \| policy.focus-one.main \| aux \| 算法输入-aux辅助数据 | catalog aux | API-000454 | 部分覆盖 | FOC-01 随样例携带 |
| L35 \| policy.focus-one.main \| focus_list \| 算法输出-focus_list焦点列表 | catalog focus_list | API-000454 | 契约占位 | unavailable，禁止 sample 词条作通过条件 |
| L35 \| policy.focus-one.main \| bottleneck_list \| 算法输出-bottleneck_list堵点清单 | catalog bottleneck_list | API-000454 | 契约占位 | 同上 |
| L35 \| policy.focus-one.main \| suggestions \| 算法输出-suggestions优化建议 | catalog suggestions | API-000454 | 契约占位 | 同上 |
| L35 \| policy.focus-one.main \| _empty \| 焦点识别无清单空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable，无稳定「合法 text 必空三清单」试调证据 |
| L35 \| policy.focus-one.main \| _fail \| 焦点识别调用失败 | 契约错误态 | API-000454、000456、000457、000458 | 已覆盖 | 含 catalog 不可用与入参失败语义 |
| L35 \| POST focus-one \| 标准化与指标权重算法 | 需规（v0 L35 算法行） | — | 未覆盖 | req_only / 无独立 endpoint |
| L35 \| POST focus-one \| 趋势特征与动态更新 | 需规（v0 L35 状态行） | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 3（`text`、`mode`、`_fail`） |
| 部分覆盖 | 3（`title`、`execution`、`aux`） |
| 契约占位 | 3（`focus_list`、`bottleneck_list`、`suggestions`） |
| 未覆盖 | 3（`_empty` 1 + req_only 2） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000454～API-000458 |
| `_empty` 未覆盖 | 1 |
| FUNC 条数 | 0 |
| 试调 | **未试调**（§0） |
| registry / run-log | 本子任务 **不修改**（父控维护） |
