# SYSINT-DICT-02-L01 · 专题字典下拉：只读久新 ADS 字典并做成内部 API

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-10-27 用户确认认领并执行。协作 api-agent、frontend-agent，同一 task-id。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 topic-svc 已有 Feign 与 `/internal/gkx-svc` 挂载，不新造连接层以外的框架。未跳过调用链、OTel 中间件与 QPOL-tech 角标。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SYSINT-DICT-02-SEQ` |
| 图 diff | 在字典下拉接口.md 增加时序：lumen-ui-topic → 网关 → lumen-svc-platform → lumen-topic-py → 久新 Doris。不另画全局拓扑。 |
| 会签态 | 过程文档，无 frontmatter 会签态。 |
| 说明 | 图在 `agent-delivery/工程过程/04-系统集成/02-对接三要素/字典下拉接口.md`。 |

## 问题清单

- 部署到 K8s 前必须注入 `JX_ADS_PASSWORD`。密码不进 git。
- 业务仓改动停在本地，未 commit、未 push。
- 政策页产业下拉未改。`QPOL-tech` 仍待确认。

## 修改内容

- `lumen-topic-py`：`POST /internal/gkx-svc/dict/query`，只读久新库 `gkx_technology_analysis_dev`。学科、人才类型、机构类型、地理位置、产业分类都走这一处。中文名空则留空。`company` 作为类型代码原样返回。
- `lumen-svc-platform` 的 `gkxlumen-topic-svc`：`GET /topic/v1/dict/**` 只转发，网关路径 `/svc/topic/v1/dict/**`。Java 不连久新。
- `lumen-ui-topic`：政策时序、区域对比、深圳现状共用的技术领域多选改读 `GET /svc/topic/v1/dict/subfield/list`。不再从政策 indicators 抽 `tech_field`。
- 深圳市在久新表里的中文名是「深圳」。仅深圳按「深圳 / 深圳市」匹配，实测树根下有 9 个区。

## 测试结果

- `python -m pytest tests/test_jx_dict.py`：7 passed。
- 本机用环境变量连久新：子学科 252 条，版本 `202610080150`，中文名空行 0。机构类型含 `company`。人才类型当前 PUBLISHED 有节点。仅深圳返回城市节点和 9 个区。产业树根 20 个。
- Java `TopicDictFacadeServiceTest` 未执行：本机 Maven 3.6.0，编译插件要求 3.6.3 以上。
- 浏览器未走通已部署环境：新接口还在本地，网关上的旧包不会出现这批选项。

## 遗留风险

- 未把密码写入 Deployment。集群里的 search-py 在注入 `JX_ADS_PASSWORD` 之前，字典接口返回失败，页面保持空选项。
- 地理位置中国全量树行数多于深圳。本叶没有新页面去拉这棵树。
- 未改 iticsci 仓，未建技术链、人才、科研机构深度页。

## CI/CD（必填）

- 分支：三个业务仓均为本地 `dev` 工作区改动，未提交。
- commit：无。
- pipeline URL / ID：无。
- 部署 namespace / 镜像 tag：未发布。
- K8s rollout：未做。
- dev 测试 URL / 命令与结果：Python 单测与久新只读冒烟见上。页面 URL 仍是现网 `http://10.50.69.111:30892` 的政策三页，要等发布后才读到新接口。

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用 lumen-topic-py 已有日志与 Trace 中间件，路由 `gkx-svc-jx-dict`。
- traceId（dev 抽样）：未部署，无。
- Tempo / Loki：未抽样。

## 涉及文件

- `repos/lumen-topic-py/gkx_svc_service/jx_dict.py`
- `repos/lumen-topic-py/gkx_svc_service/views/jx_dict.py`
- `repos/lumen-topic-py/tests/test_jx_dict.py`
- `repos/lumen-svc-platform/gkxlumen-topic-svc/gkxlumen-topic-svc-biz/src/main/java/com/topcomm/gkxlumen/topic/svc/controller/TopicDictController.java`
- `repos/lumen-svc-platform/gkxlumen-topic-svc/gkxlumen-topic-svc-biz/src/main/java/com/topcomm/gkxlumen/topic/svc/service/impl/TopicDictFacadeServiceImpl.java`
- `repos/lumen-ui-topic/src/views/policy/PolicyAnalysisConfigPage.vue`
- `repos/lumen-ui-topic/src/api/dict/index.ts`
- `agent-delivery/工程过程/04-系统集成/02-对接三要素/字典下拉接口.md`
