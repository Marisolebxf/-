# Handoff — POL-REGIONDIFF-PY-L01

> 需求：区域政策差异性分析（FE-POL-01B · Bid §4.2.1.3.2）打通后台分析链路 · Python 算法叶
> 强度：ponytail full
> 认领：`agent:algorithm-agent` / 监管：`human:淮政玮` / `claim_type: pull`

## 范围与实现

| 项 | 内容 |
|---|---|
| 新增 | `vendor/entan-py/polan/region_diff.py`：`build_region_diff` 纯函数核心 + `build_region_diff_board` 板组装器 |
| 修改 | `vendor/entan-py/polan/job.py`：注册 `sub_type=policy_region_diff`（`JOB_SUB_TYPES` 全名、入 `_NO_INDUSTRY_XOR`、`execute_policy_job` 结果板分支） |
| 新增 | `tests/test_policy_region_diff.py`：7 用例 |

### 计算口径（实算，非写死）

- **覆盖范围 coverage**：`ads.policy_industry_rel` 产业频次 Top4（∪ `{theme}` 主题），无产业映射时降级为主题信号、再无则诚实 None
- **支持力度 support**：命中 `FACTOR_GRADE` 扶持要素 → `主要方式：{Top3 要素}` + 力度指数（均值×100）
- **实施条件 condition**：区域内政策 `policy_support.申报条件` 首条非空原文摘录（60 字截断）
- **差异点 points**：三块（覆盖/力度/条件），每块取领先区域或如实「未提取到信号」
- **区域匹配**：`province/city/district/region/publish_organization` 子串包含；未匹配行计入 `honesty.unmatched`，不摊进区域

## 关键决策与对照

- **D18 合规**：不建 ADS 表，结果板进 `result.result_payload` 前端直渲——与已签收 `policy_regional` / `policy_timeseries` 板完全同构
- **诚实性**：底层 `dwd.policy_base_info` 为 mock 种子 → 板内每行 `is_mock: true` 透传，UI MockBadge 不撤（D4 仍 mock）
- **无 LLM 依赖**：纯规则/词表口径；正式权重口径挂 `QPOL-02`（客户决策既有项）
- `regions` 白名单：字符串清洗去重、20 字截断、封顶 8 个；缺省 `深圳/北京/上海/广州/杭州`

## 验证证据

```
tests/test_policy_region_diff.py        7 passed
tests -k "policy"（存量回归）          112 passed, 594 deselected
```

- push：`lumen-algo-py` origin/dev `6ec91f2`（CI 由仓库管线触发）
- 仓内无 ruff 配置（CI 仅 pytest），格式随既有文件风格

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 全部在 polan，Java 叶只放行白名单 |
| 调用链 FE→Java→Python `/internal` | ✅ 复用既有 jobs 转发链，无越层 |
| NebulaGraph | ✅ 未触图谱 |
| 可观测 | ✅ 走既有 job 链路埋点，无新增旁路 |
| D9 | ✅ is_mock 透传，不伪闭合；D4 仍 mock |
| D12 | ✅ 只在 lumen-algo-py 正式仓改动 |

## 开放项

- 力度要素词表沿用 `FACTOR_GRADE` 经验档（QPOL-02 待甲方确认后统一调）
- `region` 匹配为子串包含（如「深圳市」「广东深圳」均命中「深圳」）；更精确的行政区划归一见 `客户决策清单跟踪表` 既有行政区划精度项

## ponytail

> ponytail: 力度指数为要素均值相对口径（无正式权重），升级路径 = 换 QPOL-02 权重，字段不变。
> ponytail: 区域匹配用子串包含（O(n·m) 扫描，政策量级 ≤ 千条），升级路径 = 行政区划码归一。

## cost

- `actual_tokens`: ~120k
- `model_used`: glm-5.3-flash
- `actual_cost`: ~$0.12
- `cost_warn`: false
