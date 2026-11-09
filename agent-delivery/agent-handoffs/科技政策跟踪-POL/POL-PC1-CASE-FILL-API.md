# POL-PC1-CASE-FILL-API · 治理页政策选择器候选改全库返回

- **任务**：POL-PC1-CASE-FILL-API（`task_type=feature`，监管人 human:淮政玮，`claim_type=coordinator_dispatch`）
- **日期**：2026-11-09
- **仓**：`repos/lumen-svc-platform`（分支 `dev`，**未 commit、未 push**，等 human:淮政玮 确认）
- **ponytail**: full（最小 diff：1 个 SQL 常量 + 1 行 body.put + 降级分支 1 行）

## 1. 范围与实现

human:淮政玮 拍板：治理页政策选择器候选不再只来自 gapfill 两表，改由后端 `GET /display/v1/policy/governance/results` 直接返回全库政策（加尽加），不新开资源。

调用链（已核实）：前端 → `gkxlumen-display` `PolicyGovernanceService.results`（Feign `RemoteElementClient.policyGovernanceResults`）→ `gkxlumen-element` `PolicyGovernanceController.results`（`@Inner`，JdbcTemplate 经 `ElementDao`）。返回体在 element 侧组装，display 只透传 + 降级。

### 改动点（共 2 文件）

| 文件 | 改动 |
|---|---|
| `gkxlumen-element/.../controller/PolicyGovernanceController.java` | 新增常量 `POLICY_OPTION_SQL`；`results()` 返回体插入 `policyOptions`（位于 `totalPolicyCount` 之后、`qualityAgg` 之前） |
| `gkxlumen-display/.../service/PolicyGovernanceService.java` | `emptyResults()` 降级分支补 `policyOptions = []`，与正常结构对齐 |

三资源（results 其余字段 / lineage-index / indicator-library）**一字未动**；`@Inner` 保持；`ElementDao` 现有 `listOrEmpty` 用法（表失败自动空列表，不抛错）；无新依赖、无实体出入参。

### SQL（列名以仓内既有引用与线上实测为准）

```sql
SELECT policy_id AS id, title FROM {dwd}.policy_base_info
WHERE is_deleted = 0 ORDER BY publish_date DESC, policy_id LIMIT 200
```

- 主键列名是 **`policy_id`**（表无自增 `id` 列依赖；任务文中「可能是 policy_id/title」猜对），`SELECT` 别名 `id` 与前端候选契约对齐。
- 排序：`publish_date DESC`，`policy_id` 兜底稳定序；NULL 日期行（如 LLM 合成）MySQL 排序时排最后。
- 上限 200：兜底防 2 万行大表全量下发。

## 2. ⚠️ 偏离/待拍板：任务假设与数据事实矛盾（不自行改口径）

任务假设「gapfill 已有政策 18319069、18363390、18407696 应在列表内」。线上实测（10.50.11.76 `demo_gkxlumenx_dwd.policy_base_info`，只读核对）：

| policy_id | publish_date | 按 `publish_date DESC` 真实排名 | LIMIT 200 内？ |
|---|---|---|---|
| 18407696 | 2022-06-15 | ~135 | ✅ 在 |
| 18363390 | 2022-04-06 | ~6950 | ❌ 不在 |
| 18319069 | 2019-01-08 | ~6950+ | ❌ 不在 |

全库活行 **20,169** 条，按发布日期倒序前 200 名全是 2025-11 之后的新政策；2022-04 以前的行根本进不了窗口。**3 个 ID 只有 1 个成立**。

- 当前代码按任务字面口径实现（`publish_date DESC`），未自行改成「补 gapfill 优先」之类方案——该改动属业务口径，须 human:淮政玮 拍板后另派叶（如 `publish_date DESC, gapfill 优先` 或放宽 LIMIT）。
- 若维持现口径：前端选择器默认搜不到 18319069/18363390，需确认前端候选支持按标题关键字过滤（否则这两个政策在治理页选不到）。

## 3. 验收证据

- **编译**：`mvn -pl gkxlumen-element -am -DskipTests compile` → **EXIT=0 绿**（本机 PATH 默认 Maven 3.6.0 跑不动 compiler-plugin 3.14.0，改用 IDEA 捆绑 Maven 3.9.9 + JBR 21；`-Dmaven.build.cache.enabled=false`）。
- **格式化**：`mvn spring-javaformat:apply -pl gkxlumen-element,gkxlumen-display -am` 已跑，改动文件按仓规约格式落盘。
- **SQL 抽样**（线上库只读执行，与代码同口径）：
  - 总数：`totalPolicyCount` 口径 = 20,169（活行）。
  - policyOptions 前 5 条（2026-11-07 附近发布，`SYN` 前缀为主数据同步 ID）：
    1. `SYN202611097db9d7cb98` 北京市人民政府关于印发《北京市关于加快新型储能产业高质量发展的若干措施》的通知（2026-11-07）
    2. `SYN20261109cae44b12c1` 深圳市福田区人民政府关于印发《福田区支持网络与通信产业科创平台建设实施细则》的通知（2026-11-07）
    3. `SYN20261109cfa6fc3d94` 深圳市南山区人民政府关于印发《南山区促进合成生物科技成果转化应用指南》的通知（2026-11-06）
    4. `SYN20261109a3fa3e4aa6` 苏州市人民政府关于印发《苏州市新材料产业知识产权强基行动方案》的通知（2026-11-04）
    5. `SYN20261109a927ec90c1` 工业和信息化部关于印发《海洋经济领域科创平台建设指南》的通知（2026-11-04）
  - 降级一致性：display 侧 `policyOptions=[]` 与 element `listOrEmpty` 失败返空行为对齐。

## 4. 架构合规自检

| 铁律 | 自检 |
|---|---|
| 调用链（前端→Java→Python/internal） | ✅ 本改动纯 Java 读库只读面，无越层、无新资源 |
| Java 不做算法 | ✅ 纯 SQL 透传 |
| D3/D9（指标血缘） | ✅ 不涉统计数字口径变化；候选列表非统计指标，无 ⓘ 诉求 |
| 只读 ADS 禁扫 DWD 豁免 | ✅ 沿用 element 现有 `{dwd}` 豁免登记（application.yml 技术债条款），未新增豁免面 |
| 密钥/配置 | ✅ 未动 helm / Nacos / Secret |
| 前端 push 闸门 | ✅ 未 commit、未 push（后端仓，仍按任务要求等确认） |

## 5. 遗留

1. §2 矛盾待人拍板（拍板后如需改排序/上限，另派小叶，diff 预计 ≤5 行）。
2. 前端接线（`policyOptions` 消费）不在本叶范围（任务明示不改前端）。
