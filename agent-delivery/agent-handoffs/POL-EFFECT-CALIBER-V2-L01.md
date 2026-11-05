# POL-EFFECT-CALIBER-V2-L01 · 政策效果双指标口径 v2（去随机确定性）

> **强度**：ponytail full ｜ **类型**：bugfix（口径治理） ｜ **仓**：lumen-algo-py（主）+ demo-algo-ent-analysis + gkx-orchestration + lumen-ui-science-pc
> **监管人**：human:淮政玮（2026-11-05 口头拍板方案 A，chat 内决策；甲方书面待补）

## 范围与实现

背景：展示系统「政策实施效果跟踪」（SRS 209）区域效果板 v1 公式含三处 `rng.gauss` 随机代理（socio/env/impl 噪声），含随机分量的分数不可复现、不可归因，永远翻不了 D4=live。用户质疑「接了真接口为何还标演示数据」→ 追溯发现根因在公式随机性，监管人拍板**方案 A（双指标拆分，全确定性）**：

| 指标 | v1（随机） | v2（确定性） |
|---|---|---|
| 效果评分 `M_POLICY_EFFECT_SCORE` | execution×0.4 + gauss(60,15)×0.35 + gauss(58,12)×0.25 | **有效率×0.5 + 力度均值×50** |
| 落地实效 `M_POLICY_IMPLEMENTATION_EFFECT` | execution×0.6 + 条数×0.3 + gauss(0,5)，封顶 100 | **= 有效政策占比（百分数值）** |

改动清单：
1. `lumen-algo-py/vendor/entan-py/polan/eval/effect.py`：公式抽纯函数 `effect_score_of` / `impl_effect_of`；三处 gauss 删除；`run()` 签名不变（job/脚本/registry 调用面零改动）；ext 增 `caliber: v2-deterministic`
2. `demo-algo-ent-analysis/polan/eval/effect.py`：fc 逐字节同文同步（vendor 真源纪律）
3. `vendor/entan-py/conf/cfg_model_registry.yaml`：POLICY_EFFECT baseline → `rule_stat_deterministic_v2`，version v0.2
4. seed（`cfg_metric-POLICY-seed.yaml`）两指标 definition 追加 v2 记录 + `caliber_note`，updated 2026-11-05；判档 / is_mock 不动
5. 矩阵 `metric-readiness-matrix-POLICY.yaml` 两指标 d4_note 追加 v2 记录（D4 仍 mock）
6. calc-logic 两份正本顶部 v2 addendum（正本章节零改动）
7. `客户决策清单跟踪表.md` QPOL-02 临时默认列增补拍板记录（仍 🟡）
8. `lumen-ui-science-pc` `policyMetricsMirror.gen.ts` 外科手术式同步两 entries + MIRROR_VERSION 2026-11-05

## 偏离说明

- **is_mock / D4=mock / 🧪 角标本次不翻转**（非偏离，是设计）：v2 只解决「公式可复现」，输入仍是政策代理；D4 翻转路径 = QPOL-02 甲方归一 → 正式灌数批次 → QA 四段链路核验（policy §7.6）
- **口径治理边界**：v2 为 QPOL-02 范围内团队临时基线，**不覆盖王惠三维正本**（calc-logic §3.7 单维代理不继承综合名分的口径漂移警告已在 seed definition 引用）；🟡 不升 🟢
- **镜像未全量重生成**：gen 脚本硬编码他机路径（`D:\web\...`），本机不可跑；两条目由本轮真源写入者自同步（零漂移），全量重生成随 FE-POL-S01 系补跑

## 产物清单

| 仓 | commit |
|---|---|
| lumen-algo-py | `a3862be` + merge `c31474c`（dev） |
| demo-algo-ent-analysis | `f643655` + merge `5d565f4`（dev） |
| gkx-orchestration | `f233c473`（dev） |
| lumen-ui-science-pc | `898d7ac`（dev） |

## 验收证据

- `python tests/test_effect_v2.py` 全绿（确定性 / 边界值 / 代码行禁随机源三组断言）
- `pytest tests/test_policy_job.py tests/test_effect_v2.py` → **36 passed**（存量零回归）
- `fc /b` 双仓 effect.py 逐字节一致（merge 后复核）
- 前端 `policy.test.mjs` 全绿（D9 镜像 35+QPOL13）+ `pnpm type-check` 绿
- 中间过程自纠两处：公式量纲错（`valid_rate×50` 爆表 4035 → 修 `×0.5`）、`calc_batch_id` 笔误（`"batch"` → `batch`），均被自检/测试当场抓出

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| D1 调用链 | ✅ 只改 Python 算法层，Java/前端调用面零改动 |
| D9 数据血缘 | ✅ seed/矩阵/calc-logic/镜像/决策清单五处同步；D4 诚实保持 mock；判档不动 |
| D12 demo/lumen 隔离 | ✅ 双仓同文同步（vendor 真源纪律），无 merge 越界 |
| 算法只在 Python | ✅ |
| §3.3 commit 标注 | ✅ 全部 `[agent:data-agent]` |

## ponytail

> ponytail: 公式抽纯函数 + 单文件自检（无框架），升级路径 = QPOL-02 归一后改两纯函数 + 权重配置即可回切正本三维公式。

## 开放项

- QPOL-02 甲方归一时：复核 v2 临时基线 → 定正式权重 → 灌执行监测/宏观/社会数据 → D4 走 mock→ingesting→live（QA 四段核验）
- `gen-policy-metrics-mirror.ps1` gap-catalog 路径参数化（FE-POL-S01 系）
- 本任务为 chat 内口头拍板，上线前与 QPOL-02 一并补甲方书面

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | ~85k |
| model_used | glm-5.3-flash |
| actual_cost | $0.35 |
| cost_warn | false |
