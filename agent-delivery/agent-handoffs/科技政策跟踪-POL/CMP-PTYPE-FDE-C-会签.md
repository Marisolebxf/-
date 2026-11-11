# CMP-PTYPE-FDE-C-会签 · 中档会签单（216 政策类型列）

- 波次：CMP-PTYPE-FDE · C
- 日期：2026-11-11
- 监管：`human:淮政玮`（口径已当次会话拍板：文种临时默认 🟡，QPOL-01 增补）
- 定档：中档（数据源/读口变化；视觉零改动，不升高保真）

## 会签对象

| 稿 | 位置 | 状态 |
|---|---|---|
| 产品定义 | 说明书 `#### 216`（功能点 216-PT-1~4、状态清单、已定 4 条） | A 波次 AV-1 过 |
| 架构读法 | `POL-L2-DS10-CMP-ARCH.md` §5.4/§5.6/§8 增补 | B 波次 AV-1 过 |
| API 修订 | `POL-L2-DS10-CMP-API.md` §6.1 `policy_types` 块 | B 波次随稿 |
| DATA 修订 | `POL-L2-DS10-CMP-DATA.md` §6 读法段 | B 波次随稿 |

## 会签结论

| 角色 | 结论 | 依据 |
|---|---|---|
| 产品 | ✅ 签 | 216-PT-1~4 与需规「勾选对标字段（如政策类型…）」逐句对齐；缺文种省空态、🟡 角标、218 交界均已定义 |
| 架构 | ✅ 签 | stats 同步读扩展块（不进 Job）与已签收 216 力度同构；DWD 直读有 `INGEST_SQL` 先例；D1/D9/D16/D18 逐条过 |
| 数据 | ✅ 知会（随签生效） | 只读 `dwd.policy_base_info` 既有三列，不建表不灌行不进 GAPFILL 单；`M_POLICY_TYPE_DIST` 口径不被顶替 |
| API | ✅ 知会（随签生效） | display 透传 `policy_types` 块，无新资源、无契约新增枚举；DTO 细节仍归 `BE-POL-CONTRACT-01` |

## 异议

无异议记录（2026-11-11 会话内 product/arch 双签，data/api 知会无反对）。

## 执行委托

- D 波次 `POL-L2-DS10-CMP-PTYPE-API-L01`：按 API §6.1 实现（element `policy_types` 块 + display 透传）。本地不编译，验证交 CI。
- D 波次 `POL-L2-DS10-CMP-PTYPE-FE-L01`：`BenchmarkCompareModal` 政策类型列/图接线 + 🟡 角标（QPOL-01）。推送按 fe-manual-confirm-push 规则等当次确认。
- E 波次 `POL-L2-DS10-CMP-PTYPE-QA-L01`：演示用例 216/218 行按临时默认重冻结。

## 会签后约束

- 🟡「待甲方确认」角标与 QPOL-01 同开同关；甲方书面确认前不得撤。
- 甲方归一后若切 ODS 主题分类，只改 `policy_types` 块 SELECT 与 UI 文案，链路不动。
