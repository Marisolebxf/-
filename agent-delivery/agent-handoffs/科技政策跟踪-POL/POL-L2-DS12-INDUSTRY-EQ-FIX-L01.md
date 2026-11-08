# handoff — POL-L2-DS12-INDUSTRY-EQ-FIX-L01 未出台仿真目标产业等值过滤

- 任务：`POL-L2-DS12-INDUSTRY-EQ-FIX-L01`（bugfix，M，跨 lumen-svc-platform / lumen-algo-py / lumen-ui-science-pc）
- 监管人：human:淮政玮；执行：agent:api-agent（Java + 库）；前端半场见下「遗留」。
- 强度：ponytail full

## 范围与实现

| 层 | 改动 | commit |
|---|---|---|
| lumen-svc-platform | Feign `policySimulation` 增 `target_industry` 参数；`PolicySimulationService.jobs` 透传 body 字段；`PolicyEvaluationService` 文本解析调用补 null；element `forecast()` 未出台仿真加 `addEq(target_industry)`（空值不加谓词）；`FORECAST_COLUMNS` 补列 | `80cfe8a` + 测试签名修正 `678cf55` |
| lumen-algo-py | 主种子：建表加 `target_industry varchar(256)`、`uk_forecast_params` 五列(128) 前缀唯一键、ALTER 迁移（1060/1061/1091 幂等跳过）；研发补助行=新一代信息技术、人才引进行=生物产业；extras 恢复脚本七行未出台仿真全部补 industry 值 | `f1bf5eb` + 前缀修正 `8e327f6` |
| gkxlumenx_gapfill | 已 `--apply` 实测：列落库、uk 五列前缀就位、主种子 6 行 + extras 25 行（forecast 21 = 6 + 15） | — |

未动区域/新出台/多维/利益攸关方过滤，235–236 不读该列（DoD 第 5 条 ✅）。不新增 metric_id，D4 仍 mock。

## 单测（DoD 第 4 条对照）

`PolicySimulationReadControllerTest`：带产业命中 `target_industry = ?`；对不上产业同样生成等值谓词（HTTP 200 records 空）；空串不加谓词；区域空间带产业参数仍只按 `region_name` 过滤（隔离）。`PolicySimulationServiceTest.unpublishedForwardsTargetIndustryToElement`：display 透传断言。

## CI / 部署证据

- svc-platform 管线 4285（首推）`backend:build` 红：element 测试两处 7 参直调漏改 → `678cf55` 修正。
- svc-platform 管线 4286：`backend:build` ✅、`backend:image:element/display` ✅、`deploy:element/display` ✅（rollout 成功）；manual 项为 Nacos/helm 人工档，未触碰（遵守 nacos-config-change.mdc）。
- algo-py 管线 4284 / 4287：`py:test` + 全部 image/deploy 自动档 ✅（manual 完成态）。

## 线上行为复核（部分被 ENV 挡）

- 直连库核对 ✅（列、唯一键、7 行未出台仿真 industry 分布：新一代信息技术/生物产业/海洋产业/高端装备/新材料/新能源/绿色环保）。
- HTTP 复核：本机 `display-loop-token` 已过期（401）。按《产品实现规程》§6.5.3 归 **ENV**：不自动重登、不据此改代码；待 human:淮政玮 换 token 后按 LOOP 计划 §5 重入（验收轮只读，不做 `--apply`）。
- 兜底安全：Java 对不存在的列查询会落 Feign warn + 空records（不 501），列现已落库，无线上风险敞口。

## 遗留（前端半场，不属本 handoff 关闭范围）

lumen-ui-science-pc 工作区已有另一会话的未提交改动（`EstimateWorkbench.vue` 级联字段常显 + 保存标签带产业 + 样式，`.env.development` 本地联调开关）——按多会话保护铁律未触碰、未提交。DoD 第 3 条（前端把级联回显全文作为 `target_industry` 提交、空选择不提交）由该会话完成后随其提交；`simulationLive.mjs` 尚无 target_industry 提交逻辑，前端完成前线上接口对新字段的行为已就绪（提交即过滤）。

## 架构合规自检

- 调用链 ✅ 前端→display→element，未越层；✅ 未调 Python、未直连库（Java 侧）。
- D4 仍 mock ✅；未动锁定算法 ✅；Nacos 零改动 ✅。
- ponytail：复用既有 `addEq`/`text`/种子框架，未加新依赖；迁移幂等逻辑为最小实现。

## cost

actual_tokens: ~60000（估）· model_used: glm · actual_cost: ~$0.6 · cost_warn: false
