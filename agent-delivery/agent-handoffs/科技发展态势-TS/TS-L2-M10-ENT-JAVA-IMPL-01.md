# TS-L2-M10-ENT-JAVA-IMPL-01 · handoff

- 任务：`TS-L2-M10-ENT-JAVA-IMPL-01`（implementation · 关键实体与关系 Java 双门面）
- 日期：2026-11-08（首版）/ 2026-11-09（走查返工）· 监管：`human:刘剑锋` · 认领：`agent:api-agent`
- 状态：integration。待 topic 点名发布（`TOPIC_RELEASE=true`）后 edu 接口联调，不标 done

## 范围与实现

- 首版 8d90869：topic 门面 `/topic/v1/tech/graph/**`（7 op 封闭枚举 / ops≤50 / client_op_id 本地 400 + 信封透传）；display ENT 门面 `/v1/situation/maintain-ent/graph/**`（C1=A display 代理，D15）
- 返工 d8bbea6（edu 实测 `/current` 503「Load balancer does not contain an instance for the service lumen-algo-py」，topic 未发布时为 401）：
  - topic `TechGraphMaintainClient` url 原 `${feign.techgraph.url:}` 未配、entan-py 不注册 Nacos → 改继承 `gkxlumen.topic.algo-base-url`（K8s `TOPIC_ALGO_BASE_URL=http://gkxlumen-platform-entan-py:8000`）
  - topic 门面 `@Inner(false)` → `@Inner`：仅 display Feign（`@NoToken` 带 `from: Y`）可调，网关 `/topic/**` 外部不可达（同 cms 4f708f1）
  - display/topic relay：Feign status=-1（连不上/超时）时 `HttpStatus.valueOf` 抛异常成 500 → 统一 503 信封
  - display Feign `keyword/sortBy` 改可选；local profile topic 端口 7081 → 7092

## 验证

- topic `TechGraphMaintainControllerTest` 8/8（新增不可达透传）；display `SituationMaintainEntControllerTest` 2/2（新增）、`SituationMaintain*Test` 6/6
- 本机：`JAVA_HOME=jdk-21`；display 编译需先 `mvn -o -pl gkxlumen-upms/gkxlumen-upms-api install -DskipTests -Dmaven.build.cache.skipCache=true`

## 部署

- `gkxlumen-topic` 不在日常发布：GitLab Run pipeline（dev）+ 变量 `TOPIC_RELEASE=true`；display 推 dev 自动发

## 架构合规自检

| 铁律 | 状态 |
|---|---|
| 调用链 FE→display→topic→Python /internal | ✅ |
| Java 零写 nGQL / 无算法 | ✅ 纯转发 + 本地参数校验 |
| D15 display 不直连 Python/DB | ✅ 经 topic Feign |
| D12 无 demo 依赖 | ✅ 下游 entan-py（gkxlumen-platform-*） |
| 内部轨不对外 | ✅ topic `@Inner` |

## cost

- actual_tokens: 首版 ZCode ~未记；返工含于 2026-11-09 走查会话 · model_used: claude-opus-5-5 · cost_warn: green
