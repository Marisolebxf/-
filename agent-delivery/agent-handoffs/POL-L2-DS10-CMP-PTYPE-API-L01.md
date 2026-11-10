# POL-L2-DS10-CMP-PTYPE-API-L01 · D 波次 API 端 handoff

- 任务：`POL-L2-DS10-CMP-PTYPE-API-L01`（`POL-L2-DS10-CMP-PTYPE-FDE` D 波次）
- 认领：`agent:api-agent`；监管：`human:淮政玮`
- 强度：ponytail full
- 日期：2026-11-11

## 范围与实现

SRS 216 标杆比对「政策类型」列（QPOL-01 文种临时默认 🟡），按会签 `CMP-PTYPE-FDE-C-会签.md` 与 L2 增补（ARCH §5.4 / API §6.1 / DATA §6）实现：

1. `gkxlumen-element` `PolicyGapfillController`：
   - 新增 `POLICY_TYPE_SQL`：`SELECT province, policy_type, COUNT(DISTINCT policy_id) AS policy_count FROM {dwd}.policy_base_info WHERE is_deleted=0 AND source_plane IN ('domestic','global') AND province IS NOT NULL AND policy_type IS NOT NULL GROUP BY province, policy_type ORDER BY province, policy_count DESC, policy_type`——聚合下推库端，Java 不做内存聚合。
   - `compareStats` 增第 4 块 `policy_types`；`policyTypeRows(...)`：条件门与支持力度一致（`benchmark_scope=国内先进地区` + 对象 ≥2 + `compare_field` 含「政策类型」），对象→省映射沿用 `OBJECT_SQL` 的 `scope_code`/`scope_name`；每对象输出 `{scope_name, province, top_type, top_count, items[]}`（Top 文种=件数多者，同数取字典序首，由 SQL ORDER BY 保证取首行）；某省无行条目缺席，不造 0。
   - `fields(...)` 既有「政策类型」识别复用（增 `FIELD_POLICY_TYPE` 常量替换字面量）。
2. `gkxlumen-display` `PolicyPanoramaService.statsBody`：同步透传 `policy_types` 块（`recordMap(element.get("policy_types"))`），不聚合、不改名。

## 偏离说明

无。与 L2 增补一致。

## 产物清单

- commit `a795cd1`（lumen-svc-platform `origin/dev`，已推送，CI 自动触发）
- `PolicyGapfillController.java` / `PolicyPanoramaService.java` 2 文件 +114 行

## 验收证据

- 本地不编译（用户指令「本地不需要编译前端和java」）；编译与接口验证走 GitLab CI（push `a795cd1` → Pipeline）+ E 波次 LOOP 复测。
- 自检锚点：`FE-POL-CMP-LIVE.test.mjs`（前端仓）对 `policy_types` 契约（`top_type`/`top_count`/`items`）断言全绿。

## 架构合规自检

| 铁律 | 结论 |
|---|---|
| D1 调用链 | ✅ 前端 → display stats → element `/internal`（`@Inner` compare-stats 扩块），不越层；不进 Job、不调用 Python |
| D9 血缘 | ✅ 不新造 metric_id（复用 DWD `policy_base_info.policy_type` 已有列做对照展示）；无行缺席不造 0；UI 🟡 由 FE 承接 |
| D16 gapfill | ✅ 不建表、不写 ODS/DWD/ADS，只读 |
| D18 | ✅ 读 DWD 真列，不造 ADS mock 行，接口不返回写死数据 |
| D19 字符集 | ✅ 单表 GROUP BY 无跨库 JOIN 混排 |

## cost

- `actual_tokens`: ~85k；`model_used`: glm-5.3-flash；`actual_cost`: ~$0.35；`cost_warn`: 无

ponytail: 省级文种行有限整表读再筛（`ponytail:` 注释在 `policyTypeRows`），行数过万再改 `province IN` 下推。
