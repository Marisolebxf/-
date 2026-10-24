# ALGO-LIB-POL-PORTAL-DENS-NAT-L01 · 全国政策发布密度真算法（最小叠加实现）

> 2026-10-23 晚二次修订：淮政玮团队 17:03 已在 demo 两仓推送十条占位实现（`5427a65` 后端 / `67ccd78`+`dfe18cb` 前端）。
> 本单执行时发现该并行实现，**放弃本方平行版本**（含 ADS 表方案与 gap-* 前端，均未提交即弃），
> 改为在其架构上做最小叠加。因此本单**前端零改动、无新表**，全部增量在算法仓一个函数 + 一处路由。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent`（代 human:唐绍祖 执行） |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 前置 `ALGO-LIB-POL-PORTAL-GAP-L01` 已 done。本单为十条实现单的第一单，验证「登记口径→出数」链路可走通，其余九单照此模板。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过测试与 handoff。未新编口径填数：分母未登记前行为与主干完全一致（空行）；登记后同链路自动出数。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 不适用 |
| 图 diff | 未改架构图。数据仍走既有 `GET /v1/policy/indicators?kind=all` 的 `portal_gaps` 面 |
| 会签态 | 不适用 |
| 说明 | demo 结果不进 lumen；SYSINT-03-04B 对本条仍返回空。 |

## 问题清单

- QPOL-02 仍是 🟡。本单不拍板。
- `portal_gaps.density_denominator` **当前未登记** → 页面诚实显示「缺已登记分母」的空行（这是 DoD 要求的正确行为，不是缺陷）。
- 登记方式：`conf/settings_policy.yaml` 加一段
  `portal_gaps: { density_denominator: natural_month }`，刷新页面即出数，**无需改码、无需重灌**（路由实时现算）。
- 口径本身（密度=条/月是否可作为对外口径）请淮政玮拍板后登记；本单交付的是「登记即可用」的机制。

## 修改内容（全部在 demo-algo-ent-analysis，前端零改动）

### `polan/basic/indicators.py`

- 新增 `_national_monthly_density(pols)`：按 `publish_date` 逐月计数，输出 `[{name: 'YYYY-MM', value: n}]`（键名与前端 `PortalGapPage.vue` 的 `paint()` 序列约定对齐）。日期缺失/非法/**13 月**等一律不进序列（宁缺毋假）。
- `portal_gap_rows()` 签名扩展：新增首个位置参 `pols`（DWD 行集，默认 `None` 向后兼容——老调用 `portal_gap_rows()` 行为不变）。
- 出数逻辑：`density_denominator == "natural_month"` 且传了行集 → 仅 `density_national` 行填 `value`（最后一个有数月份的条数）+ `series`；其余九条与省/市两条兄弟密度行口径不变，仍诚实空，reason 写明「省/市级需区域×期间密度公式，仍 pending」。
- 拒绝改挂加固：黑名单标量撞上出数值时，`value` 与 `series` **一并撤销**（诚实优先，不留半填行）。

### `api/policy_routes.py`（`/v1/policy/indicators` 的 `kind=all` 分支）

- 从 `settings_policy.yaml` 读 `portal_gaps.density_denominator`；
- 仅当登记为 `natural_month` 才查一次 `SELECT publish_date FROM dwd.policy_base_info WHERE is_deleted=0`（未登记零查询开销）；
- 行集与 `key_cities` 一起传入 `portal_gap_rows`，过 `reject_portal_gap_rehang` 后返回。

### 测试 `tests/test_policy_portal_gaps.py`

原 2 个用例不动，追加 4 个：
1. 分母登记但未传行集 → 空 + 「无可用逐月序列」；
2. 登记+传行集 → `value=1`（2026-02），`series=[{2026-01:3},{2026-02:1}]`（深圳计入全国面），其余九条全空；
3. 13 月拒绝：序列月份只有 01/02；
4. 拒绝改挂撞值：`value`+`series` 一并撤销。

## 测试结果

- `pytest tests/test_policy_portal_gaps.py -q` → **6 passed**；
- 全仓 `pytest tests/ -q` → **258 passed，2 failed**（`test_entan_metrics.py` 的 health/catalog 计数断言；已验证 `git stash` 后同样失败，属 entan 域存量问题，与本单无关，建议另开清理单）；
- 手工冒烟 5 场景（未登记/登记+有数/登记+无数/撞黑名单/13月）全过。

## 验收与回滚

- **验收路径**：淮政玮审口径 → 拍板「条/月」→ 在 `conf/settings_policy.yaml` 登记两行 → 页面「政策扶持-全国政策发布密度」出柱状序列。未拍板前什么都不用做，页面保持诚实空行。
- **回滚**：`git revert` 本单单个 commit 即可；或删掉配置里 `portal_gaps` 段（代码保留无害，回到空行行为）。

## 遗留风险

- demo 服务未部署：页面看到效果需本地/测试环境起 demo-algo-ent-analysis。
- entan 域 2 个存量测试失败待另单清理。
- gkx 真库（183.240.141.251）的 `publish_date` 断档（2022-09 后 48/50 个月零记录）会直接反映在序列上——这是数据事实，算法不修饰。

## CI/CD（必填）

- 分支：`demo-algo-ent-analysis` 本地 `dev`，单 commit 推 `origin dev`
- pipeline / K8s：无（demo 仓无 CI）
- 前端仓：零改动，无 commit

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅（前端只画后端给的 series） |
| 前端只经既有网关到 Python | ✅（既有端点，未加路由） |
| 未把 demo 接进 lumen | ✅ |
| 未改种子、矩阵、契约 | ✅（口径登记是配置项，不是种子） |
| 未拍板 QPOL-02 | ✅ |
| demo_* 之外零写入 | ✅（只读 DWD，无新表） |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | ~150000（含与并行实现撞车后的重构） |
| model_used | GLM（价表按 algorithm 75/25 估算） |
| actual_cost | 0.9 |
| cost_warn | green |

ponytail: full
