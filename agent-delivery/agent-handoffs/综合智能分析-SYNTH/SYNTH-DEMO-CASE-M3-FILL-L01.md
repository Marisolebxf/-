# SYNTH-DEMO-CASE-M3-FILL-L01 Handoff — M3 逐条条件填充矩阵（47 条零缺格）

- **任务**：`SYNTH-DEMO-CASE-M3-FILL-L01`（长任务 M3 叶，总控：`../SYNTH-合规演示用例-长任务总控.md`）
- **执行**：agent:data-agent（子智能体，本会话 coordinator 收口）
- **监管**：`supervised_by=human:徐滕强`；`claim_type=coordinator_dispatch`
- **仓**：`gkx-orchestration`（origin/dev）
- **强度**：ponytail: full（单文件 YAML；schema 照总控，判定口径写头注释）
- **日期**：2026-11-07

## 1. 范围与实现

产出 `合规演示用例/condition-fill-matrix.yaml`（555 行）：47 条 CASE 逐条判定 `supported | gap | partial`，零缺格、零重复、零新造缺口编号。

| 叶 | 条数 | supported | gap | partial |
|---|---:|---:|---:|---:|
| vitality | 16 | 12 | 4 | 0 |
| element | 14 | 10 | 1 | 3 |
| collab | 17 | 14 | 0 | 3 |
| **合计** | **47** | **36** | **5** | **6** |

## 2. 判定要点

- **gap 全部引 G-01**（活力 1y/5y 空窗 4 条：VIT-04/05/09/15；要素无历史年行趋势 1 条：ELEM-12）
- **partial 6 条**：要素非默认窗 3 条（G-01，但 137 四维过渡表三窗全齐可出）+ 协同东莞/惠州/广州子区块降级 3 条（G-05/G-06）
- **拦截即期望**：VIT-10（legacy_unknown）/ VIT-11（WEIGHT_PROFILE_INVALID）/ COLLAB-17（batch_meta_missing）判 supported
- **协同 ADS 六表 0 行 = 合规诚实态**（G-04），按实时计算 + gapfill 输入路径判 supported
- **D-01~D-03 数据缺陷**不进 verdict，仅在 `m2_annotation` 注记，M4 登记修复项

## 3. 验收证据（双重校验）

1. 子智能体内联 5 行校验：PASS（yaml 可解析/47 条/叶计数/无缺 verdict/引用必带）
2. coordinator 独立 python3 复核：`counts {supported:36, gap:5, partial:6}` 与 `meta.summary` 一致、47 id 零重复、gap/partial 零缺 `gap_refs`、supported/partial 零缺 `tables` → **全过**

## 4. 给下游的交接

- M4：gap 5 条 + partial 6 条 → `gap-summary.md` 归并（既有引用 vs 新登记——本叶零新造，全部既有编号）；另列 D-01~D-03 修复建议+责任方
- M5：LOOP 轮次以 36 条 supported 为主演轮，6 条 partial 按降级脚本排程，5 条 gap 归入验证轮（期望=诚实空态/拦截）

## 5. 架构合规自检

- ✅ 证据只读引用 data-survey（未重查库、未写库）
- ✅ 零 git/registry/业务仓改动；cicd: skip
- ✅ 缺口编号白名单校验过（G-01~G-08 / Q-SYNTH-*），零新造

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | ~100000 |
| model_used | glm-5.3-flash |
| actual_cost | 0.13 |
| cost_warn | green |

## 7. ponytail

ponytail: full——单文件交付；schema 6 字段复用总控 §4 CASE 字段；自检内联跑完即弃不落盘。
