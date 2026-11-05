# Handoff — LUMEN-INTEL-VIT-BAKE-L01（entan-api 烘焙活力复现盘）

- **执行**：agent:devops-agent　**监管**：human:徐滕强
- **仓**：`repos/lumen-algo-py`（origin/dev，commit `4cfdec8`，**未 push**，等人工确认）
- **强度**：ponytail full
- **状态**：in_progress → 自检绿，待验收

## 1. 根因与修法

**根因**（与派单 E1 复测结论一致）：`vendor/entan-py/entan/synth_vitality/pack.py` 的 `_DEFAULT_REPRO` 硬编码为开发者本机路径 `/Users/samuel_tang/my_project/gkx-lumen/gkx-orchestration/agent-delivery/metrics/repro/out`；镜像里无此路径也无该数据 → `_load_json("M_SYNTH_186_1_out.json")` 失败 → 四维盘 None → `result.vitalityIndex=null`、`dimScores.score=null`。

**方案选型（二选一取入库）**：数据仅 **7.7KB**、内容为深圳/广州/东莞/惠州四城脱敏聚合分数（敏感字段扫描 CLEAN），且仓内已有 `data/precompute/` 随镜像烘焙的既有惯例（`package_precompute.py` + `.gitignore` 白名单 `!data/precompute/` + Dockerfile 现成 COPY 行）→ **数据入仓复用现有 COPY**，Dockerfile 仅加 1 行 ENV。不取 CI 拉取方案（为 7.7KB 文件加构建期拉取逻辑违反最小 diff）。

## 2. 改动清单（commit `4cfdec8`，2 files +301）

| 文件 | 改动 |
|---|---|
| `vendor/entan-py/data/precompute/M_SYNTH_186_1_out.json` | 新增：真源 `gkx-orchestration/agent-delivery/metrics/repro/out/M_SYNTH_186_1_out.json`（2026-10-28 14:38 版，与 handoff 产物区 md_code 副本 diff IDENTICAL），平铺沿用 precompute 惯例，`_out` 后缀不与既有 envelope `M_SYNTH_186_1.json` 冲突 |
| `docker/Dockerfile.entan-api` | +1 行 `ENV SYNTH_VIT_REPRO_DIR=/entan-py/data/precompute`（放 COPY 之后），注释注明根因 |

**零改动**：业务代码（pack.py 只读 ENV 逻辑原本就正确，`os.environ.get(_REPRO_ENV) or _DEFAULT_REPRO`）、CI（标准 `.image` 模板从仓根 build，现有 COPY 行覆盖）、`.gitignore`、entan-worker（vitality 仅 api 侧消费）。

## 3. 验证证据（本地 docker build 不可行 → 镜像内路径语义静态核对 + 实跑）

1. **ENV 生效语义实跑**：`SYNTH_VIT_REPRO_DIR=<仓内 precompute>` 下 `build_vitality_result('深圳','全国重点城市','最近3年')` → `vitalityIndex=74.9981`，dimScores tech/industry/talent/policy = 73.7/77.7925/56.2/92.3，ranks 深1/广2/莞3/惠4 —— 与复现盘逐值一致（复现盘 `index_0_100.深圳市=74.9981`）。gapfill 表缺失告警为预期诚实态（D16 未灌数，不属本修单）。
2. **契约回归**：`python3 vendor/entan-py/scripts/check_synth_vitality.py`（既有自检）→ `{"ok": true, "passes": "all"}`，四条断言（路由挂载/默认三元组/400 拒绝/显式批号不回落）无回归。
3. **静态核对**：COPY 路径存在（git 已跟踪）；`.dockerignore` 不排除 data；`precompute_list`/`_verify_baked` 按 `M_*.json` 遍历/`{mid}.json` 精确匹配，`_out.json` 新条目不破坏两者（前者多一条真实产物条目，后者不受影响）。
4. 遗留：CI/K8s dev 实镜像验证待 push 后由 image:entan-api 流水线确认（本修单不 push）。

## 4. 架构合规自检

- 调用链/算法只在 Python：✅ 未触碰；Java 零改动
- D12 demo↔lumen 隔离：✅ 仅动 lumen-algo-py
- D16/D18 诚实态：✅ 未伪造数值，复现盘为既有已评审产物原样入仓；gapfill 缺行仍返回 null
- git 安全：✅ dev 分支 commit、无 force、未 push；他人 WIP（`scripts/mock_stage_health_scores.py`、`scripts/seed_supply_chain_relations.py` 两个 untracked）未触碰

## 5. 成本

```
ponytail: full（最小 diff：1 数据文件平铺 + Dockerfile 1 行 ENV；零新依赖零抽象）
actual_tokens: ~85000
model_used: glm-5.3-Flash
actual_cost: ~$0.09
cost_warn: false
```
