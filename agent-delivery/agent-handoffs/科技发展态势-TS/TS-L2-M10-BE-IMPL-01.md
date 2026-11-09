# TS-L2-M10-BE-IMPL-01 · handoff

- 任务：`TS-L2-M10-BE-IMPL-01`（implementation · 维护管理图层与数据源 Java 实现）
- 日期：2026-11-06 · 监管：`human:刘剑锋` · 认领：`agent:api-agent`
- 状态：代码已推 feat 分支 + MR !2 待合入 dev；模块测试全绿。**未部署未联调**，不标 done
- 分支：`lumen-svc-platform` `feat/m10-tech-maintain-config`（e7bcc69+15d06cc）· MR：`/-/merge_requests/2`

## 实现落点（相对定义稿的一个实现级裁定）

定义稿 ARCH §3 写「领域服务承载候选 gkxlumen-topic 侧 element 模块」。实现时经代码勘察改落 **`gkxlumen-cms`**（:7098，业务库 gkxlumenx_cms）：

- element 是只读定位（hikari `read-only: true` + 架构注释「展示侧 L3 只读」），不能承载写
- cms 是全仓**唯一现成的配置 CRUD 机制**（JdbcTemplate + CmsErrors/CmsEnvelope 400/404/409 信封 + `/cms/v1/**` 内部整合轨——2026-10-26 徐滕强四区模型），与 M10「跨专题运营配置」同族；未来 ENT 二级（41–47 图谱维护）也有 KgAttr/KgRelation 现成邻居
- 对外契约不变：display BFF `/v1/situation/maintain/**`（网关 `/display/v1/situation/maintain/**`）照 API 分册逐资源实现；D15（display 不直连 Python/DB）保持

## 产物清单（9 文件，+1183 行）

| 层 | 文件 | 说明 |
|---|---|---|
| DDL | `db/9x_gkxlumenx_cms_tech_maintain_config.sql` | 四表 + 种子 26 行（3/3/9/11；11 色值逐字对齐 `entityColorByKey`，曾写错已核正） |
| cms 错误 | `CmsErrors.java` + `CmsEnvelope.java` | 增 `NotImplemented`（50101→HTTP 501），DB 型 probe 契约 501 |
| cms 业务 | `TechMaintainService.java`（407 行） | JdbcTemplate CRUD；枚举三套冻结校验；`groupId↔group_code` 翻译层（会签备注落点）；删组 409 GROUP_IN_USE；code 生成 `src-/grp-+序`；probe HEAD→405 回退 GET、5s、不读体、**SSRF 黑名单**（环回/私网/链路本地/任播/组播 + DNS 重绑定 IP 复核） |
| cms 入口 | `TechMaintainController.java` | `/cms/v1/tech-maintain/**` 内部轨，12 端点与契约一一对应 |
| display Feign | `RemoteCmsTechMaintainClient.java` | `@NoToken`（cms 无 @Inner，与 element 配对不同——注释已写明勿混淆） |
| display 门面 | `SituationMaintainController.java` | 纯转发不改语义；FeignException → HTTP 状态 + 信封体原样透传（Jackson 解析失败降级 fallback 信封，HashMap 容 null） |
| 测试 | `TechMaintainServiceTest`（12）+ `SituationMaintainControllerTest`（5） | 纯 JUnit+Mockito；display 侧验证 200/400/409/501/503 五态透传 |

## 测试与验证

- `mvn -pl gkxlumen-cms test`：**104/104 绿**（含新增 12）
- `mvn -pl gkxlumen-display test`：**55/55 绿**（含新增 5）
- 测试抓出并修复 1 个真 bug：`nextCode` 字符串拼接优先级（`src-01`→`src-4`）

## 环境备注（给后来者）

- 本机 Maven 跑在 Homebrew **JDK 27**，javac 默认 `-proc:none` 导致 lombok 不生效（common-swagger「找不到符号」假象）。修法：`export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-21.jdk/Contents/Home`
- build-cache 扩展会跳过 jar 产生坏构件，install common 链时需 `-Dmaven.build.cache.skipCache=true`

## 偏离与遗留

- 实现级偏离 1 处（落点 cms 而非 topic 侧，见上，语义与契约不变）——**建议随 MR 评审确认**
- 未做：部署、网关路由核验（`/display/**` 已有路由，无需新增）、与 FE-TS-10B 联调、执行 DDL（需库口令，DBA/部署流程走）
- FE-TS-10B 接线依赖本 MR 合入 + DDL 执行后方可联调

## 架构合规自检

| 铁律 | 状态 |
|---|---|
| 调用链 前端→display→Feign→cms→业务库 | ✅ v3 终版链路 |
| D15 display 不直连 Python/DB | ✅ 经 Feign |
| D12 无 demo 依赖 | ✅ 种子值仅作冻结事实源 |
| 契约=API 分册（路径/DTO/枚举/错误码/空态） | ✅ 12 端点逐一对应；空=200 空数组 |
| SSRF（ARCH-C4） | ✅ 黑名单+IP 复核进代码 |
| 不碰 BE-TS-CONTRACT-02 / 无 Python 组件 | ✅ |

## cost

- actual_tokens: ~90k（含编译排障）
- model_used: glm-5.3（ZCode agent）
- actual_cost: <$1
- cost_warn: green
