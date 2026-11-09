# E-E7-POLICY-M1-L10-FIX01 · 科创政策全景 · 导出不出文件

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 缺陷来源：用户 2026-11-07 截图，点「导出」提示 OssTemplate 未启用，响应没有文件字节 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用仓内 `OssTemplate`、`policy_share_export`、展示侧已有字节代理写法（态势报告下载）。未加新依赖。 |

## 问题清单

1. `gkxlumen-topic-policy` 的 Nacos 私有配置没有 `file.oss.*`，Deployment 也没有 RustFS 凭证变量。`OssTemplate` 不装配，`share` 走诚实空态，不写桶。
2. L10 只写桶、只回对象键，没有任何下载入口。前端拿不到文件字节，只能提示「未在本页下载」。

## 修改内容

| 层 | 改动 |
|---|---|
| 配置 | `helm/.../configs/gkxlumen-topic-policy-biz-dev.yml` 追加 `file.oss` 段（端点同 topic-async-service）。`values.yaml`、`values-lumen.yaml` 的 topic-policy env 加 `GKX_MINIO_ACCESS_KEY/SECRET_KEY`，取自 Secret `gkxlumen-platform-rustfs` |
| 门面 | `GET /topic/v1/policy/share/download?object_key=`：只认 `policy_share_export` 中 `download_permission=当前用户` 的对象，`OssTemplate.getObject` 回传字节；匿名、无记录、无对象都 404 |
| 门面 | `PolicyShareRecordStore.allowed(...)` + JDBC 实现 |
| 展示 | `GET /display/v1/policy/panorama/share/download`：Feign 取字节原样回，不组装文件、不连对象存储 |
| 前端（未推） | `presentShare` 透出 `objectKey`；导出拿到对象键后 `downloadPanoramaShareFile` 经展示代理下载 blob |

## 线上操作（zhipu-tts，已做）

- Nacos `gkxlumen-topic-policy-biz-dev.yml`（namespace `public`）在跳板机上就地只追加 `file:` 段后发布：md5 已变化，53 行，原两处密码行仍在。临时文件已删。
- `kubectl set env deploy/gkxlumen-platform-topic-policy --from=secret/gkxlumen-platform-rustfs --prefix=GKX_`。只引用 Secret，值不出现在任何输出。

## 测试结果

- 前端：`displayPanoramaQuery.selfcheck.mjs` ok；`displayPanoramaQuery.compliance.test.mjs` 全绿；`vite build` 成功。
- 前端 `pnpm type-check` 红 6 处，全部在 `displayPanoramaQuery.ts` 114–214 行排序代码，来自已推提交 `c52ba15`，不是本单改动（本单只改 495 行以后）。
- 后端：本机无 JDK/Maven，单测未在本地跑；新增 `shareDownload` 断言写在 `PolicyFacadeServiceImplTest.shareWritesExcelThroughOssTemplateAndKeepsDisplayUrl`。CI 只 `package -DskipTests`，编译通过（新镜像已部署）。
- 线上门面 Pod：`GKX_MINIO_*` 2 个变量在；`/actuator/beans` 有 `ossTemplate`；`/share/download` 无令牌 401（入口已挂且需鉴权）；health UP。
- **未做**：带登录令牌的端到端下载。前端未推，页面仍是旧逻辑。

## 遗留风险

- 2026-11-07 查实线上库 `gkxlumenx_topic_policy` 原本没有 `policy_share_export`（1146）。已按 `db/9x_gkxlumenx_topic_policy.sql` 中该表的 `CREATE TABLE IF NOT EXISTS` 补建，其余表未动。
- helm `runOnUpgrade=false`：本单线上 Nacos 与 env 是手工补的，仓内模板已同步，下次全量 helm 不会丢。
- 前端改动停在本地，等用户确认推送。

## CI/CD（必填）

- 分支：`origin/dev`
- commit：lumen-svc-platform `8da89da`；前端未提交
- 部署 namespace / 镜像：zhipu-tts；topic-policy `sha256:af72cc25…`，display `sha256:8e5f604e…`
- K8s rollout：成功
- dev 测试：见上「测试结果」

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkxlumen-topic-policy-biz`、`gkxlumen-display`
- traceId：未抽样（未做带令牌实测）

## 架构合规自检

- ✅ 调用链：浏览器 → 展示 `/display/v1/policy/panorama/share/download` → 门面；浏览器不打 `/topic/v1/policy`
- ✅ D14：只读写桶 `gkx-lumen` 的 `gkx-others/`、`gkx-user-reports/`；前端不直连 RustFS；凭证只在 Secret
- ✅ D12：不调 demo-*
- ✅ 展示侧只代理字节，不组装文件
- ✅ 下载权限只认当前登录用户，库里不存文件字节

## 涉及文件

- `gkxlumen-topic-policy/.../controller/PolicyFacadeController.java`
- `gkxlumen-topic-policy/.../service/PolicyFacadeService.java`、`PolicyShareRecordStore.java`
- `gkxlumen-topic-policy/.../service/impl/PolicyFacadeServiceImpl.java`、`JdbcPolicyShareRecordStore.java`
- `gkxlumen-topic-policy/.../PolicyFacadeServiceImplTest.java`
- `gkxlumen-display/.../controller/PolicyPanoramaQueryController.java`、`feign/RemotePolicyQueryClient.java`
- `helm/gkxlumen-platform/configs/gkxlumen-topic-policy-biz-dev.yml`、`values.yaml`、`values-lumen.yaml`
- 前端（本地）：`lumen-ui-science-pc/src/api/policy.ts`、`src/views/policy/panorama/index.vue`、`search/displayPanoramaQuery.ts`、`search/displayPanoramaQuery.selfcheck.mjs`

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 30000 |
| model_used | claude-opus |
| actual_cost | 0.16 |
| cost_warn | green |
