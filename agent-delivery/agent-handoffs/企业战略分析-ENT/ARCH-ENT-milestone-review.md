# ARCH-ENT 里程碑合规评审（architect-agent 只读建议稿）

- 评审时间：2026-06-18
- 评审者：architect-agent（只读建议，需人类架构师 lead 会签）
- 评审范围：企业分析（战略分析）Wave 0 流水线产物
  - ux：`topic_demo/docs/ia/enterprise/*.md`（5 份，commit `6686cf1`）
  - ui handoff：`UI-ENT-strategic-analysis-p0.md`（commit `bc16e5a`，未 push）
  - data 种子：`agent-delivery/metrics/cfg_metric-ENT-seed.yaml`（commit `b4bf381`，未 push）
  - 决策跟踪：Q009 / Q010~Q018
- 落盘说明：architect-agent 以只读模式运行，本文件由 coordinator 代为落盘，内容为其原始评审建议。

---

## 结论：GO（带阻塞）

可进入 algorithm-agent 实现 formula 阶段，但须先解 P0 阻塞（Q009 命名拍板）。

---

## 一、Q009 命名冲突拍板建议（ENT vs E1）

- **冲突**：`data-lineage-policy §3.2` 规定企业要素代号为 `E1`（→`M_E1_*`）；ux 派单 + wireframe + data 49 条种子统一用 `M_ENT_*`，已规范登记 K-O1 / Q009（未擅自拍板，符合公约 §3.8）。
- **关键发现**：§3.2 现行要素表**已非纯数字制**——软科学 `SS`、创新生态 `IC`、创新监测 `INNOV`、通用 `COMMON` 已是字母助记码，`ENT` 与之同风格（先例已存在）。
- **推荐：方案 B —— 保留 `M_ENT_*` + 修订 §3.2 注册"助记代号表"**
  - 理由：①迁移成本/影响面最低（种子/wireframe/UI 零改动，仅 1 处文档补丁）；②与既有 SS/IC/INNOV/COMMON 助记先例统一；③可读性与评审追溯性更高。
  - 方案 A（改回 `M_E1_*`）成本高：需改 49 条种子 + wireframe 大量引用 + registry + 已交付 UI（ⓘ tooltip 内嵌 metric_id）重提交 + 未来 cfg_metric/api catalog。
  - **强制附带条件**：签字时**一次性确定全 7 要素助记表**（建议 `E1=ENT / E2=CHAIN / E3=ORG / E4=TECH / E5=TALENT / E6=SVC / E7=POLICY`，`E1~E7` 保留为废弃别名），bump policy 版本，避免后续每要素重复触发同类冲突。
  - ⚠️ 需人类架构师 lead 签字 + 落 `data-lineage-changelog.md`。

## 二、§2 铁律 1–10 合规自检

✅ 6 项（1 算法只在 Python / 2 调用链 / 3 NebulaGraph / 6 demo2 只读 / 7 共享聚合核心 / 8 数据策略）
⚠️ 4 项（4 可观测性 observability.ts 延后 lumen / 5 CI-CD 未 push 待评审 / 9 D8 前端规范 topic_demo 兼容豁免 / 10 D9 完整组件延后 lumen）
❌ 0 项。4 个 ⚠️ 均为原型期合理豁免或延后待办，无硬性违规。

> D8（铁律 9）建议：架构师**显式确认 topic_demo 新页（Type/Domain）用旧栈的豁免边界**（原型可，lumen 复刻必须 Arco/ECharts/Leaflet/G6）。

## 三、scope ±10% 核验

- 10 子功能（.3.1~.3.10）+ 概述 = 11 页面 ↔ E-20~E-30，覆盖 10/10，无遗漏。
- 无越界：明确排除科研机构分析 §1.1.1.2.4.2.4、E-31~E-37 企业发展快速入口。
- 页面拆/并不改叶子数（P3 承载 .3.3+.3.4），符合 policy §8。
- 结论：scope 合规，在 ±10% 内。

## 四、8 件套抽查（49 条种子）

- 整体齐全、占位标注清晰、D9 合规。
- 轻微问题（非阻塞，建议 Wave 1 整改）：
  1. `source_tables` 把 ADS/DWD 混写字符串、缺 DWS 层、ADS 直接复用 `dwd.enterprise` 而非独立 `ads_*` 表名 → 补齐 ODS→DWD→DWS→ADS 四段链 + 正式 ADS 表名。
  2. 评分类 metric 的 source 与 handoff 的 `gkx_ads.ads_enterprise_score` 对齐。
  3. `M_ENT_INNOVATIVE_COUNT` 等 definition 偏短，上线前数据 lead 须补足 ≥50 字。
  4. `M_ENT_MARKET_SHARE` 空血缘 + `no_source` 标注合理，但**未在跟踪表登记为采购/决策项，建议补登**（K-O7）。

## 五、go/no-go 与开工前阻塞项排序

**GO（带阻塞）**，按序解阻塞：

1. **🔴 P0 — Q009 命名拍板（人类架构师签字）**：必须在 algorithm-agent 大规模落 formula **之前**完成，否则改名返工翻倍。推荐方案 B。
2. **🟠 P1 — Q014 评分指标库与默认权重**：不阻塞编码，algorithm-agent 把权重/阈值做成**可参数化 config 占位**先实现模型骨架，数值待甲方确认注入。
3. **🟡 P2 — Q010~Q013/Q015~Q018 业务口径**：临时默认值先跑，阻塞上线移除 ⚠️，PM 并行推甲方。
4. **🟡 P3 — `M_ENT_MARKET_SHARE` 无来源（K-O7）**：采购/降级/下架，仅影响 1 条；补登跟踪表。

**可立即并行（不等阻塞）**：14 条 ✅ → api-agent 接 ADS/DWD 联调；30 条 🔧 → Q009 签字后 algorithm-agent 参数化实现。

## 六、待办小结（非阻塞，Wave 1 前）

①observability.ts；②完整 D9 三件套（lumen 复刻）；③血缘补 DWS 层 + 正式 ADS 表名；④MARKET_SHARE 采购/下架登记；⑤架构师显式确认 topic_demo 新页 D8 豁免边界。
