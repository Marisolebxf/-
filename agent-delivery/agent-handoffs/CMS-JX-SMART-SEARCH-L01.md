# CMS-JX-SMART-SEARCH-L01 handoff

- **任务**: CMS 智能搜索四模块接口（转发专题 Java 门面）
- **执行**: agent:api-agent · 监管 human:徐滕强 · 强度 ponytail full
- **仓**: lumen-svc-platform · commits 98a0ea3 / 11dbc69 · push origin/dev

## 范围与实现

- 新增 `SmartSearchController`（4 个 POST `/api/open/cms/v1/smart-search/{enterprise|industry|policy|service}`）+ `SmartSearchService`（薄转发+归一化）
- 下游 = 四个专题 Java 门面（@Inner(false) 匿名）：enterprise `/topic/v1/search/smart`、chain `/topic/v1/industry/search?mode=smart`、policy `/topic/v1/policy/search`、svc `/topic/v1/service/search/orgs`；Python 零改动、专题模块零改动
- 传输：复用 cmsAlgoRestTemplate 先例，baseUrl 进 application.yml（nacos cms-dev.yml 可覆盖）；零新依赖；D12 合规仅调 gkxlumen-*
- 归一化信封 `{total,page,size,records[]}`，行内字段原样透传；keyword 必填（40001）；page≤1 归 1、size 1..100
- 文档 live-1.5 + OpenAPI 112 paths 已推（gkx-orchestration 4a9914dd）

## 验收证据（2026-11-02 集群冒烟，镜像 11dbc694，走久新同款网关 30895 + /cms + X-CMS-Api-Key）

| 接口 | keyword | code | total | records | 首条 |
|---|---|---|---|---|---|
| enterprise | 深圳 | 0 | 10000 | 3 | 深圳市红阳电池有限公司 |
| industry | 集成电路 | 0 | 9 | 9 | 集成电路 |
| policy | 人才 | 0 | 1020 | 3 | 国家广电总局…人才扶持… |
| service | 检验 | 0 | 95 | 3 | 东莞兰卫医学检验实验室 |
| policy p2 | 人才/页2 | 0 | 1020 | 翻页生效 | 中小企业领军人才培训 |
| 守卫 | 空 keyword | 40001 keyword 必填 | — | — | — |

自检：SmartSearchServiceTest 4/4 绿（nexus 断连期手工 javac + JUnit Platform launcher 直跑）。

## 偏离说明

- 首轮默认 Service 名误写 `-biz:9000/8500/8600/8700`，冒烟 DNS 不解析；按集群 svc 实名改 `gkxlumen-platform-topic-{enterprise:7093,chain:7095,policy:7097,svc:7096}`（commit 11dbc69）

## 架构合规自检

- D1 调用链：前端 → CMS → 专题 Java → Python ✅（CMS 未直调 Python）
- 全 POST + JSON、X-CMS-Api-Key、信封一致 ✅；无路径业务参数 ✅
- D12：仅调 gkxlumen-* ✅；可观测走既有 OTel agent ✅

ponytail: full；cost 随后回填 registry。
