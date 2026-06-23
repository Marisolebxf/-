# Handoff —— DATA-POLICY-metric-seed

- **任务**: POLICY-PROTO-L01（Epic: E-POLICY-PROTOTYPE）
- **角色**: data-agent ｜ **日期**: 2026-06-23 ｜ **Wave**: 0（Mock 阶段）
- **commit 标记**: `[agent:data]`

## 1. 范围与实现

产出政策域（POLICY，废弃别名 E7）指标种子 **`metrics/cfg_metric-POLICY-seed.yaml`**，
将 19 条 `M_POLICY_*` 指标升级为 D9 数据血缘 8 件套（metric_id / metric_name_zh /
definition / formula / source_tables / source_systems / update_freq / version）+
推荐字段（is_mock / bid_ref / acceptance_unit_id / owner_agent / mapping_status），
严格镜像 `cfg_metric-ENT-seed.yaml` 的头部注释 + 字段结构。

### 指标族（19 条）

| 族 | 指标 | bid_ref | P-XX |
|----|------|---------|------|
| A 基础(5) | M_POLICY_LEVEL_DIST / TYPE_DIST / TIMESERIES / NATIONAL_DIST / SZ_DIST | §1.1.1.1.1.1.1.1.3 | P-03~P-07 |
| B 门户扶持(5) | M_POLICY_TOTAL_COUNT / INTENSITY_INDEX / INDUSTRY_COVERAGE / VALIDITY_RATE / RELATION_DEGREE | §..1.3 / §8.2 / §2.6 | P-17/P-20/P-19/P-66 |
| C 深度模型(6) | M_POLICY_FOCUS_INDEX / INTENSITY_SCORE / EFFECT_SCORE / SHORTBOARD_COUNT / OPPORTUNITY_COUNT / LAYOUT_REC_COUNT | §1.1.1.1.1.1.1.8.1~.8.6 | P-11~P-16 |
| D 三维框架(3) | M_POLICY_SUPPORT_STRENGTH / INDUSTRY_FIT / IMPLEMENTATION_EFFECT | §1.1.1.1.1.1.1.9 | P-72/P-73 |

## 2. 指标统计 / 状态分布

- **总计 19 条**，batch=`mock_20260623`，is_mock=true，seed_version 0.1.0
- **✅ 4**：LEVEL_DIST / NATIONAL_DIST / SZ_DIST / TOTAL_COUNT（直接聚合，口径清晰）
- **🔧 12**：formula 待 algorithm-agent（多数同时含 definition pending_data_lead）
- **⚠️ 3**：口径待甲方——TYPE_DIST(QPOL-01) / INTENSITY_INDEX(QPOL-02) / SUPPORT_STRENGTH(QPOL-02)
- **❌ 0**

## 3. 与 bid / 映射报告对照

- 5 基础指标 1:1 对应 bid §1.1.1.1.1.1.1.1.3 政策基础指标模型（政策级别/类型/时序/全国/深圳分布）。
- 6 深度指标 1:1 对应 bid §1.1.1.1.1.1.1.8 政策深度分析模型 6 子模型（焦点/力度/效果/短板/机遇/布局）。
- source_tables 引用真实血缘：`ads → dwd.policy_base_info ← ods: dwd_zck_policy/dwd_zck_intl_policy`，
  字段名对齐现行 DDL（issueno/pubtime/pubdeptname/policylevel/abs/maelements/ma_keypoints/allfactors/
  docstatus/expiration_date），与映射报告 §4 逻辑字段名差异已在 db 设计 §2 注明。

## 4. 待甲方决策（登记 客户决策清单跟踪表.md）

| 编号 | 决策项 | 影响指标 | 临时默认 |
|------|--------|----------|----------|
| QPOL-01 | 政策"类型"一级分类口径 | TYPE_DIST | 取 topic_type 主题分类归一 |
| QPOL-02 | 力度/效果/焦点/短板/机遇/布局/三维 权重与阈值 | INTENSITY_INDEX/_SCORE/FOCUS/EFFECT/SHORTBOARD/OPPORTUNITY/LAYOUT/SUPPORT_STRENGTH/IMPL_EFFECT | 等权打分 |
| QPOL-03 | 政策关联/产业适配匹配规则 | RELATION_DEGREE / INDUSTRY_FIT | 共现/余弦相似度 |

## 5. 架构合规自检（§2 十条）

- 铁律1 算法只在 Python：✅ 12 条 🔧 formula 交 algorithm-agent，种子不含实现
- 铁律3 图谱 NebulaGraph gkx_policy：✅ RELATION_DEGREE 标注图谱来源
- 铁律8 标准表先行+Mock：✅ is_mock + batch=mock_20260623
- 铁律10 D9 8 件套：✅ 19 条全部齐全
- 不替甲方拍板：✅ 歧义项标 ⚠️ + definition_status: pending_data_lead + pending_ref(QPOL-01~03)

## 6. 阻塞与风险

- **效果/落地数据缺口**：M_POLICY_EFFECT_SCORE / M_POLICY_IMPLEMENTATION_EFFECT 的执行监测/宏观经济/
  社会数据无 ODS 来源，归 🔧 并在 source_tables 标注"待采购"，Wave 0 以 Mock 填充。
- **深度字段格式**：elements/keypoints/factors/pedigree 为 text，是否 JSON 待与供方确认。
- 以上不阻塞本次种子产出；接力 algorithm-agent（formula）+ PM（QPOL-01~03 推甲方）。

## 7. 产物清单

- `agent-delivery/metrics/cfg_metric-POLICY-seed.yaml`（19 指标 8 件套）
- `agent-delivery/data-source-mapping-registry.yaml`（追加政策 DWD/ADS/Nebula 登记，未破坏现有内容）

## 8. 接力

- **algorithm-agent**：实现 12 条 `pending_algorithm` 的 formula（焦点/力度/效果/短板/机遇/布局/三维/关联）。
- **PM**：推动甲方确认 QPOL-01~03。
- **ux/ui-agent**：wireframe 字段表第 6 列引用上述 metric_id，统计数字旁加 ⓘ + 🧪 MockBadge。
