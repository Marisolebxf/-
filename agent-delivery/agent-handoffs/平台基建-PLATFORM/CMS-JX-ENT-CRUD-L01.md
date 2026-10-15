# CMS-JX-ENT-CRUD-L01 · 企业实体写侧：overlay CRUD + gkxlumen-cms 模块骨架

> **任务**：`CMS-JX-ENT-CRUD-L01`（feature / P1 / implementation）
> **依据**：《CMS-JX接口规格书.md》v1.3 §1.1 + A5 冻结 + DDL 单产物
> **代码**：lumen-svc-platform `gkxlumen-cms/`（11 文件 714 行，commit `5527d33b`，origin/dev）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | pull（2026-10-15 18:17，8h 锁窗） |

## Ponytail

ponytail: `full`（GKX 护栏全遵守：鉴权/审计/错误信封/双数据源均为 A5 冻结项，无 yagni 裁剪；未加任何未被要求的抽象——DAO/Service/Controller 三层直译规格）

## 交付内容

### 1. `gkxlumen-cms` 模块骨架（后续 18 张单复用）

| 组件 | 实现 | 规格依据 |
|---|---|---|
| 启动类 | `GkxlumenCmsApplication`（**不启用** ResourceServer——API Key 鉴权，非 OAuth） | 老设计单 A3 |
| 鉴权 Filter | `CmsApiKeyFilterConfig`：`/cms/v1/*` 校验 `X-CMS-Api-Key`；**未配置=拒绝全部（fail-closed）**；401 `CMS_AUTH_FAILED` | §0.1 |
| 双数据源 | 默认=业务库 `gkxlumenx_cms`（读写，视图也在此）；`SourceDataSourceConfig`=demo_dwd 只读 Hikari（read-only 池） | A5-1/A5-8 |
| 错误信封 | `CmsEnvelope`（@RestControllerAdvice）：40001/40401/40901/50001 → R 信封 + 对应 HTTP 码 | §0.2 |

### 2. 企业实体 CRUD（§1.1 全字段）

- `POST /cms/v1/enterprise/list`：查视图 `v_cms_ent`（keyword/isKey/flag/priority 筛选 + 分页，name 升序）
- `POST /cms/v1/enterprise/detail`：视图详情（含只读回显列）
- `POST /cms/v1/enterprise/create`：虚拟实体，ID=`cms:ENT-{uuid8}` 服务端生成，uk 撞重试一次（A5 §5）；name 必填校验
- `POST /cms/v1/enterprise/update`：**11 字段白名单**（name/regInfo/founded/capital/type/industry/scale/isKey/flag/priority/reason → overlay snake 键）；`JSON_MERGE_PATCH` 字段级原子合并（只叠 body 带的键）；真源实体无覆盖行时自动 INSERT 首覆盖
- `POST /cms/v1/enterprise/delete`：reason 必填 → **引用检查**（ent_news.company_ids / ent_sz.org_id / kg_relation.from/to / expert.entity 四路计数，命中返回 40901 + `data.reasons`）→ 软删 + 审计快照

全部写操作同事务写 `cms_op_audit`（CREATE/UPDATE/DELETE + operator + snapshot_before）。

### 3. 验证

- **CI 编译绿**：pipeline [6475](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/6475) `backend:build` success（mvn clean verify 含 gkxlumen-cms，commit 5527d33b）；11 个镜像打包 job 全绿
- 本机 maven 配置指向旧公司 nexus 不可用（用户确认）——编译验证走 CI runner（内网 harbor maven 镜像），已验证此通道可靠
- 运行时验证：待建库执行 + 部署后 curl 联调（见遗留）

## 遗留与移交（联调闸门）

> **2026-10-15 22:55 联调闸门已全部清零**（api-agent / human:徐滕强 授权连跑）：

| # | 项 | 状态 | 证据 |
|---|----|------|------|
| 1 | **建库执行** `db/9x_gkxlumenx_cms.sql` | ✅ 完成 | K8s 临时 pod（mysql:8.0 root@192.168.88.43）执行 `DDL_OK`；11 表 + 4 视图落库；`GRANT ALL ON gkxlumenx_cms.* TO 'gkxlumenx'@'%'` 已授权；四态自检通过（真源透传 189,115 / pol 20,000 / svc 43,296 / prod 0（源空）/ 种子 16+22；**软删后视图 0 行**——bugbot 修复实测生效） |
| 2 | Nacos 配置 `gkxlumen-cms-dev.yml` | ✅ 完成 | v3 admin API 发布（yaml，md5 `269616f2`）：port 7098 + `cms.api-key` + source.db。⚠️ 第一次发布 `\n` 未转义导致 SnakeYAML 报错，已用文件上传方式重发修复 |
| 3 | CI image/deploy + helm cms 段 | ✅ 完成 | pipeline [6483](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/6483)+`backend:image:cms` 绿（commit aebbf77，bugbot 4+1 修复一并合入：视图软删剔除 / org_ids 列名 / 双源 @Primary / Dockerfile / 端口 7098 / Actuator 收敛）；helm values cms 条目 + values-lumen `cms.enabled=true`（commit 6667dbb） |
| 4 | K8s 部署 + Service | ✅ 完成 | `gkxlumen-platform-cms` Deployment/Service（ClusterIP :7098）Running，镜像 `gkxlumen-cms:c55af8ce`；**中途修掉 Spring Security 默认 formLogin 302 拦截**（common-security 传递依赖引入 starter-security，加 `CmsSecurityPermitAllConfig` permit-all 链，鉴权归 Api-Key Filter，commit c55af8c） |
| 5 | 冒烟联调 | ✅ 通过 | 无 key 401 / 坏 key 401 / 正 key `list` 200（total=189115 与视图一致）/ `detail` 200（真实企业"深圳市大族视觉技术有限公司"）/ actuator health 200 / env 已收敛不可达 |
| 6 | **基础加固上线** | ✅ 通过 | commit `0b4d35e` / pipeline [6498](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/6498) `backend:build`+`image:cms` 绿，`deploy:cms` 手动触发绿；Pod 镜像 `gkxlumen-cms:0b4d35e4`。修复：delete 空表 SUM→NULL NPE、幽灵 ID 孤儿 overlay、`SourceDao` 缺 `@Qualifier`、`is_deleted` Boolean 强转、`v_cms_ent` 列契约 `isKey`/`regInfo`/`reason`。冒烟：ghost update/delete→40401 且库无幽灵行；虚拟 create+delete 无 NPE、软删后 detail 404；list total=189115 |

**API Key**：仅 Nacos `gkxlumen-cms-dev.yml` / 分发渠道持有，**禁止写入 git**（本 handoff 不存明文）。

## 架构合规自检

| # | 铁律 | 结论 |
|---|------|------|
| 1-3 | 算法/调用链/图谱 | ✅ 纯 CRUD 无算法；真源只读；不碰 Nebula |
| 4 | 可观测 | ✅ actuator+tracing 配置就绪（OTEL_ENABLED）；写操作审计落库 |
| 5 | CI/CD | ✅ push → pipeline 6475 build 绿（公约铁律 5 履行） |
| 8 | 数据策略 | ✅ overlay 只写业务库 gkxlumenx_cms；真源 demo_dwd 只读 Hikari |
| 12 | demo/lumen 隔离 | ✅ lumen-svc-platform 正式仓，零 demo-* 依赖 |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | ~90000 |
| model_used | glm-5.3 |
| actual_cost | ~$0.9 |
| cost_warn | green |
