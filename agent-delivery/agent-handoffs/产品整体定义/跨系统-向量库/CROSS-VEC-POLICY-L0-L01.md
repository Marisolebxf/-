# CROSS-VEC-POLICY-L0-L01 · 政策 ODS→DWD L0 — theme 退出产业槽，仅进 ext5

> 对照 SAD `02-概要设计.md` §1.1 / §3；派单包 `派单/CROSS-VEC-POLICY-L0-L01-派单包.md`。特殊授权抢跑，不等 SAD 双签。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控 Wave 1；lock 24h；已 claimed + in_progress 后本叶落地 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只改共享映射（`ods_to_dwd` + `enrich_related_industry_vids` + hang 读槽），未新依赖、未另起灌数入口。未用 YAGNI 跳过单测 / 架构铁律 / handoff。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 编码叶，本机未走 Headroom 压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `02-概要设计.md` §1.1 业务灌数（L0 结构映射 → L1 字面对码） |
| 图 diff | L0：`theme` → 仅 `ext5`，不再进入 `related_entities.industry`；L1 边仍走标题/摘要/关键词/要点 + `match_industry_anchors`；未加向量/LLM 边 |
| 会签态 | `v0.3-draft`（源文件 frontmatter；禁止自填绿） |

## 范围与实现

根因：`ods_to_dwd` 把 ODS `theme`（监督管理 / 产业发展等主题标签，可为 JSON 数组）写入 `related_entities.industry`，并拼进 L1 匹配文本；`iter_related_slots` / `_hang_slots` 再用 `ext5` 回灌产业槽。时序板 `LIKE chain:INB*` 因此命中 0。

本叶：

1. L0：`normalize_policy_theme` 后 **只写 `ext5`**；产业槽默认空，不再用 theme / `目标产业` 种子。
2. L1：`l1_industry_match_text` 只用标题/摘要/关键词/要点 + policy_support 要素（不含 theme/ext5）；`enrich_related_industry_vids` 剥离主题标签，锚点命中才写 `industry_link_code`。
3. 上图读槽不再把 `ext5` 当产业名。
4. 重灌路径仍走已有 `ingest_pending` / `reload_from_ods` → 共享 `ods_to_dwd`；**不调 Milvus / LLM / rebuild**。

## 偏离

无。未写正式 `gkxlumenx_*`，未碰 `amcpdp-*`，未造 `chain:INB1303`。

## 产物清单

- `lumen-algo-py` `vendor/entan-py/polan/graph/entity.py`
- `lumen-algo-py` `vendor/entan-py/polan/mockgen/incr.py`
- `lumen-algo-py` `vendor/entan-py/polan/graph/ops.py`
- `lumen-algo-py` `tests/test_industry_vid_enrich.py`
- 本 handoff

## 验收证据

```text
python -m pytest tests/test_industry_vid_enrich.py -q --tb=short
.........                                                                [100%]
9 passed in 0.10s
```

相关子集：`python -m pytest tests -q -k "policy or industry or ods or vid or incr or theme"` → **37 passed**。

DoD：

- 纯 `theme=监督管理` 且标题无链名 → 产业槽无 `chain:INB*`，`ext5=监督管理`
- 标题含集成电路且锚点存在 → 仍对 `chain:INB1303`（L1 未破坏）
- `theme=["监督管理"]` JSON 数组 → `ext5=监督管理`

## 问题清单 / 开放项

- SAD / ARCH-SIGN 正式双签仍 🟡 后补，不挡本叶。
- Demo 库存量 DWD 需 **政策重灌/reload** 才会清掉旧产业槽里的 theme；本叶未连库实灌。
- Mock `generate.py` replace 仍把造数用的产业名写入 `ext5`（不是 ODS theme 路径）；reload 走 `ods_to_dwd` 后按新 L0。
- 主题标签枚举未获供应方书面码表（POLICY-P0-2）；`POLICY_THEME_LABELS` 按入站样例 + 本行 theme 剥离。
- 时序板 LIKE `chain:INB*` 覆盖仍取决于标题是否含图上链名；Job A 向量补槽是后叶。

## 修改内容

| 共享函数 | 行为 |
|----------|------|
| `normalize_policy_theme` | 数组/JSON → 逗号文本，写入 ext5 |
| `l1_industry_match_text` | L1 拼文本，禁止 theme/ext5 |
| `enrich_related_industry_vids(..., theme=)` | 主题标签退出产业槽；字面对锚点才写 VID |
| `ods_to_dwd` | L0+L1 唯一映射；append/reload 共用 |
| `iter_related_slots` | 去掉 ext5→industry 回灌 |
| `_hang_slots` | 对码文本改为 title/abstract/keywords/keypoints |

## 测试结果

- `tests/test_industry_vid_enrich.py` **9 passed**
- 未调 Milvus、未调 LLM、未 rebuild

## 遗留风险

- 未重灌的旧 DWD 行仍可能带 theme-in-industry，需 reload。
- 图锚点加载失败时 L1 不写 VID（诚实空槽），禁止假码。

## CI/CD（必填）

- 分支：`lumen-algo-py` `origin/dev`
- commit：`a83df403dd4c0e0738379fa9dd9a76f911b063d3`
- pipeline URL / ID：push 后 GitLab CI（本叶不挡）
- 部署 namespace / 镜像 tag：未发版（算法映射，pytest 闭环）
- K8s rollout：未做（本轮总控段 E 不派专题金路径）
- dev 测试：见上 pytest

## 可观测性（建议）

- OTEL_SERVICE_NAME：未改（无新 HTTP）
- Tempo / Loki：无

## 涉及文件

- `vendor/entan-py/polan/graph/entity.py`
- `vendor/entan-py/polan/mockgen/incr.py`
- `vendor/entan-py/polan/graph/ops.py`
- `tests/test_industry_vid_enrich.py`

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 映射与 L1 在 `polan` |
| 调用链 | ✅ 未越层；未调 Java / 前端 |
| 图谱仅 Nebula | ✅ 只用已有锚点 VID；未造码 |
| 可观测 | N/A（无新接口） |
| CI/CD | ✅ push `origin/dev`，禁 force |
| demo2 不 merge lumen | ✅ |
| Java 不写算法 | ✅ 未改 Java |
| 数据策略 | ✅ 只映射 Demo ODS→DWD；禁写正式 `gkxlumenx_*` |
| D8 / D10 | N/A |
| D9 | N/A（本叶非指标页） |
| D12 | ✅ 未调 `demo-*` 服务；未碰 `amcpdp-*` |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 80000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.48 |
| cost_warn | green |

口径：algorithm 默认 75/25；B 档 `$3/$15` per 1M；`80000×0.75×3/1e6 + 80000×0.25×15/1e6 = 0.48`。
