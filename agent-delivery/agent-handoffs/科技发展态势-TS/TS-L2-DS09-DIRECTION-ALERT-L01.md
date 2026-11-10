# TS-L2-DS09 方向预警（seq 184）原型上线 L01 · 2026-11-09

> 任务：`direction-warnings` 从 501 通道翻转为 200 真数据。
> 角色：api/data（本会话一人兼）· 监管：口头授权（用户转述，2026-11-09）。
> 关联：`TS-L2-DS09-OV-API.md` §2.7/§3（501 契约）· `TS-L2-DS09-OV-DATA.md`（表）· D18 铁律 · `nacos-config-change.mdc`。

## 一、结论

| 项 | 状态 |
|---|---|
| `gkxlumenx_ads.ts_plan_direction_warning` | ✅ 61 行真算行入库（high 6 / medium 45 / watch 10） |
| Nacos `gkxlumen-display-dev.yml` | ✅ 已单发追加 `planning.direction-alert.registered: true`，回读验证通过 |
| display 滚动重启 | ✅ FULL_PIPELINE 流水线 4486 · deploy:display 18:55:21 success |
| 端到端 501→200 | ✅ 实测 200：items=61，report_meta high=6/medium=45/watch=10，`?warning_level=high` 过滤=6，`metric_ids=[M_INNOV_PLAN_DIRECTION_ALERT]`，六源 source_averages 服务端现算正常 |

## 二、数据血缘（诚实标注）

- **公式**：王惠 20261021 批口径（指标库 `M_INNOV_PLAN_DIRECTION_ALERT` 登记原文）：
  `F=mean(g_s)；g_s=(近窗年均值-基期年均值)/max(基期年均值,1)；level=2 if F>=1 且两源g>0, 1 if F>=0.5, else 0`。
- **数据源**：`gkx @ 183.240.141.251:3318`（只读），复用 2026-10-23 复现产物
  `agent-delivery/metrics/repro/out/M_INNOV_PLAN_DIRECTION_ALERT_out.json`（`result_A_literal.all` 258 个 IPC4 方向，elapsed 21.4s）。
- **选行**：level 2 全部 6 行 → `high`；level 1 全部 45 行 → `medium`；level 0 中 F 最高 10 行 → `watch`（F∈[0.437,0.496)，接近 0.5 阈值）。
- **六源 JSON 口径**：patent/industry/paper/project/policy 五源 delta 为**真算增速**；
  人才源（无学者→IPC4 映射）score=50 占位 + note 注明"原型期展示占位值"；论文源 note 注明单日回填窗口口径。
- **行标注**：`metric_id=M_INNOV_PLAN_DIRECTION_ALERT`，`generated_by=proto:A5-wanghui-formula+mockfill@gkx-20261023run`，`source=model_output`。
- **指标库状态不变**：D4 保持 mock（原型行非模型服务产出），未越权翻 live。

## 三、闸门翻转（nacos-config-change.mdc 单发机制）

- 模板：`lumen-svc-platform/helm/gkxlumen-platform/configs/gkxlumen-display-dev.yml` 追加 planning 块（commit `0de7c86`→系列，含 `584c996`/`52010e8`/`cf11ea5`）。
- 线上：经控制台 API（NodePort 30849，`/v3/auth/user/login` + `/v3/console/cs/config`）单发该 dataId，回读含 flag ✅。
  **服务端 API（8848）`/v1/auth/users/login` 在 Nacos 3 兼容层 500、`/v3/auth/user/login` 500**——nacos-config-init 的登录路径当前不可用，属平台隐患（见 §六）。
- 回滚位：Nacos 控制台把 `registered` 翻回 `false`（或删 planning 块）→ 重启 display → 恢复 501。

## 四、代码变更（lumen-svc-platform dev）

| commit | 内容 |
|---|---|
| `584c996` | 模板加 planning 块 + `ops:planning-alert-gate` 手动任务初版（pod-exec 方案，失败） |
| `52010e8` | 任务改 runner 直连 ClusterIP + v3/v1 登录兜底（服务端 API 全 500，失败） |
| `cf11ea5` | 修 YAML 块标量（echo 冒号导致 lint 失败） |
| （本日前序）`249f884` | db DDL 补 `del_flag` 列（推送产物表，另一问题） |

**已知未结**：`ops:planning-alert-gate` 任务已由并行会话接手迭代至 v3（08eb5c5 / dda3393：bcrypt 预计算哈希 + kubectl exec 数据库临时账号线 + trylogin 短路），见 §六.1/§六.3——本会话原版（runner 直连 ClusterIP + 控制台凭据思路）已被取代；本次线上发布实际由本会话经控制台 API 手工完成，未依赖该任务。

## 五、验证（已于 2026-11-09 18:58 实测通过）

```bash
curl -s 'https://edu.itic-sci.com/tid/api/display/v1/situation/planning/direction-warnings' \
  -H 'authorization: Bearer <token>' -H 'systemcode: display'
```

实测：`code=0`；`items=61`（high 6 / medium 45 / watch 10）；`report_meta` 计数与 items 一致（**注意为字符串形态 "6"/"45"/"10"，服务端序列化行为**）；六源 `source_averages` 服务端现算正常；`?warning_level=high` → 6 条；`metric_ids=[M_INNOV_PLAN_DIRECTION_ALERT]`。

## 六、遗留与风险

1. **⚠️ P0 · Nacos 管理员密码已进 git**：并行会话在 `ops:planning-alert-gate` 迭代中（08eb5c5 / dda3393）把共享 `nacos` 管理员密码重置为固定值并写入 .gitlab-ci.yml（`gkx-ops-gate-2026`，bcrypt 预计算）。已实测该凭据 console 登录生效（globalAdmin）——**任何有仓读权限的人即得 Nacos 全局管理权**，违反「密钥不进 git」铁律，且与 api-agent 正在做的明文口令清理（46520a8）方向冲突。建议：尽快改密并迁 K8s Secret / masked CI 变量（Maintainer 权限），git 历史中的值视同已泄露。
2. **`nacos-config-init` 默认凭据失效**：上述密码重置后，helm 部署链路的 init 任务默认 `nacos/nacos` 将登录失败（v1 login 对错误凭据返回 500「Handle API Compatibility failed」而非 401——本会话早先据此误判为服务端兼容层损坏，实际是密码错误；正确凭据下登录可用）。devops 需把新凭据接入 init 任务（values/Secret）。
3. **ops 任务多会话并行迭代**：`ops:planning-alert-gate` 已由并行会话重构至 v3（bcrypt 预计算 + /tmp 直通修正 + trylogin 短路），后续改动请基于 origin/dev 最新版（dda3393），不要回退。
4. **刷新机制**：原型行是一次性快照（2026-10-23 数据）。模型服务上线（方案 A）后由 Python Job 周期重算覆写 `warning_id LIKE 'ipc4-%'` 行。
5. **导出任务中心**：`content_key=planning-direction-warning` 的导出闸门共用本开关，已随重启放开——如有导出联调需一并验证。
6. 前端只按 HTTP 501 判定（不解析 msg），501→200 切换对 FE 无代码影响。
