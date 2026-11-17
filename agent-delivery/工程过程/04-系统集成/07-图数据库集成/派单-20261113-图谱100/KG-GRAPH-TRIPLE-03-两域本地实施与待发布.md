# KG-GRAPH-TRIPLE-03 · 两域本地实施与待发布（2026-11-17）

## 结论

PERSON/RESEARCH两域12操作及Java/UI代码已在本机实现；整单仍in_progress。8操作已经本地Python接真实图库验证；名称检索/全域浏览4操作消费完整图索引，目前缺索引时503。没有部署到正式K8s，没有发布Nacos，没有真实网关鉴权回执，不申请整单integration/done。

## 文件与调用链

- Python：lumen_common/algorithms/entity_graph.py；lumen_algo_service/views/entity_graph.py；main.py注册两域精确路由；scripts/build_entity_graph_index.py仅处理本地已验证图库导出。
- Java：gkxlumen-innov/entitygraph下Controller/Client/FeignOptions/FeignRegistration；只透传Python，不写nGQL。
- UI：src/api/entity-graph/index.ts、src/views/entity-graph/*、src/router/menu.ts；两个认证入口/knowledge-graph/person与/knowledge-graph/research，保留原默认首页。
- 两域均遵循前端→Java网关/topic/v1/{person,research}/graph/ops/{op_id}→Java gkxlumen-innov /v1/...→lumen-algo-py /internal/...。

## 本地验证

1. Python专用测试26项通过：参数/注入/跨空间、无向和类型隔离、属性解码、强度口径、签名分页及数据变化拒绝、缺索引503、200点/500边有界子图、零度与无向邻居去重、快照哈希损坏、只读及并发上限等。
2. Java采用仓库相同的Spring Boot 3.5.11 / Spring Cloud 2025.0.1版本，在独立小工程编译本次实际源码（含真实NoToken注解），5项JUnit通过：原样透传、400/404/501/503/504、操作白名单及trace头白名单。**未运行整个多模块Java仓CI**。
3. 前端type-check、Vite build、4项口径行为测试、既有menu.selfcheck通过。构建有现有大chunk提示，不据此改动无关模块。
4. 真实Python证据：KG-GRAPH-TRIPLE-03-two-domain-python-live.json。人才样本15合作邻居，归属关系另有1条正例；科研机构样本20合作邻居，超大邻域排序返回503，二跳子图最多200点并标截断。科研机构项目操作已验证成功空态，尚未取得非空项目正例，不冒充已全量验收。
5. 浏览器证据：KG-GRAPH-TRIPLE-03-two-domain-local-ui-chain.json。独立本地Vue页面→本地Java门面→本地Python→真实Nebula，无数据拦截/Mock；两域合作关系200，浏览缺索引503，改变条件清空旧结果且不自动取数，无页面运行错误。该独立验证入口不覆盖正式门户登录、权限、K8s网关/Nacos及部署链路。
6. 本地页面截图保存在宋飞扬本次Codex输出目录，包含真实合作关系；截图为本地链路，不是线上发布证据。

## 数据口径和护栏

- 人才strength=props.co_paper_count；原始weight仅保留原值，不用于排序/边宽；专利/项目合作计数标missing。
- 科研机构co_paper_count_total/weight仅称合著篇数；strength_by_year必须指定year，缺年份数据null，禁跨年求和/比较。
- 合作度=唯一合作邻居数，包括0度节点，不能用合著篇数或截断样本替代。
- VID仅稳定ID拼前缀：person: / inst:；关联端点使用真实边VID，科研机构与institution:服务机构严格区分。两端Tag隔离cooperate，排除company。
- 每次单点邻域501候选作完整性探针；>500不提供伪完整排序。子图200点/500边/20查询，单查询3秒/整个操作10秒预算；每进程4个实时读操作并发，无全图聚合。
- dry_run默认true不连接；false仍全只读。无图/源库写入，无schema操作，无实例重启。

## 索引准备（尚未执行真实构建）

运行期KG_ENTITY_GRAPH_INDEX_DIR指向只读索引目录。每域manifest命名{domain}.manifest.json，索引文件名{domain}.{sha256}.sqlite3不可变；核验SHA256、space、origin=nebula、complete/verified、图版本、节点/边摘要与时效，拒绝源表导出、过期/损坏文件。缺失时SEARCH_INDEX_NOT_READY/RANK_INDEX_NOT_READY，超邻域ADJACENCY_INDEX_NOT_READY。

离线构建器不连接数据库、不发网络请求。输入每域{domain}.export.json，必须含format=entity-graph-export-v1、domain、space=demo_gkx_chain、origin=nebula、complete=true、verified=true、graph_version、captured_at、validated_at，以及files.nodes/edges的filename/rows/sha256。nodes JSONL为{tag,vid,name,properties}，edges JSONL为{src,dst,edge_type:cooperate}；导出须包含完整域、零度节点和去重口径所需全部边。构建器复核行数/摘要，计算唯一无向邻居数，原子发布。不得拿T03源表快照改origin冒充图库导出。

```bash
python scripts/build_entity_graph_index.py --snapshot-dir /path/to/verified-graph-export --domain person --output-dir /path/to/readonly-index
# research同理；本轮没有启动全图库导出或构建。
```

## 部署配置

图连接优先KG_ENTITY_GRAPH_HOST/PORT/USER/PASSWORD；兼容现有LUMEN_ALGO_NEBULA_HOSTS/USER/PASSWORD和GKX_NEBULA_HOSTS/PASSWORD。复用既有集群secret/env，不在源码、文档或命令参数中放密码。生产分页多副本应注入相同KG_ENTITY_GRAPH_CURSOR_SECRET；游标5分钟，绑定op/条件/排序/结果快照，数据变化拒绝旧游标。

Java默认下游http://lumen-platform-algo-py:8000（仓库k8s/api.yaml服务名）；可通过gkxlumen.innov.entity-graph.algo-base-url覆盖，禁止指向demo。Feign连接2秒/读12秒、不自动重试；只传X-Trace-Id/traceparent，不复制Authorization。

## 待用户确认后的发布顺序

1. 审查并提交三个业务仓和编排仓变更；前端AGENTS要求当次会话明确确认push。未获该确认前全部停在本地。
2. 跑正式各仓CI、验证Python路由与Java镜像已更新，再部署。确认两域/internal可用后再启用网关路由/UI。
3. Nacos按gkx-nacos-shared-config，仅gkxlumen-gateway-dev.yml单dataId：先读线上原文比对；模板只新增gkxlumen-topic-entity-graph精确person/research ops路由，置catch-all前；无StripPrefix（GlobalFilter已剥topic一次），不重发其他dataId。线上操作须当次会话用户批准。
4. 正式Java网关带实际鉴权逐op留curl/apiview；无完整索引的4操作保留503，不写“有数”；补科研项目非空样本与四态走查。完整索引、TECH与COVER-01回执齐后再申请integration。
5. 回滚：撤回本次网关单条路由、各服务回到前一镜像digest、前端回前版；本任务没有图写入，不涉及图数据回滚。不删除他人路由或空间。

## 发布限制的原文依据

- lumen-ui-topic/AGENTS.md：“改动停在本地工作区，等当前会话用户人工确认（明确说‘推/可以推/提交推送’）后才push”。
- gkx-orchestration/.cursor/skills/gkx-nacos-shared-config/SKILL.md §2：“执行前须当次会话用户批准（线上变更）”。

## 未完成与签收

TECH 9操作等待COVER-01；完整图索引与超大邻域完整排序尚未就绪；科研项目非空样本待补；正式CI/K8s/网关鉴权与线上页面仍待验证。成本工具未提供实际token/费用，不编造。整单仍in_progress，本阶段不触发签收。

## 2026-11-17T19:09:52+08:00 · 用户已批准提交推送

当前会话用户明确授权“提交推送”，本机Git凭据已存macOS钥匙串（无密码落仓）。已提交的业务仓版本如下，均推送目标origin/dev：

- [lumen-algo-py 6fa198ca](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-algo-py/-/commit/6fa198ca1a5878d7fce6d1a6dd17c12d3dc0ca6a)
- [lumen-svc-platform f5ae0e8d](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/commit/f5ae0e8d69dc51f95493ded7ee70257433a31eda)
- [lumen-ui-topic cb6656d2](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-topic/-/commit/cb6656d2cb1c868c1122f7c35bdae4a7b9fe3d5d)

已同步编排仓最新dev并保留团队登记内容；任务仍in_progress，不标整单完成。CI状态另以各提交的流水线结果为准，未声称CI/正式网关联调已通过。本次执行提交推送；Nacos单dataId线上发布尚未执行，相关索引与TECH限制仍按前文。此前“尚未提交推送”描述为该阶段历史状态。

## 2026-11-17T19:20:26+08:00 · 推送与CI核验

四仓origin/dev推送已由GitLab提交refs API复核。Java CI首轮暴露Mockito旧版本不支持verifyNoInteractions，已改为兼容never断言并补推`7107ceee`；新流水线backend:build及deploy:innov通过。

- Python：948 passed、7 skipped；自动镜像/部署/路由smoke通过；deploy:innov与deploy:entan-worker保留手动。流水线：https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-algo-py/-/pipelines/5723
- Java：必需构建、测试与innov自动部署通过；可选sonar:scan（allow_failure=true）在记录时仍运行，不据此宣称整条流水线已成功；其他手动任务未触发。流水线：https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/5726
- 前端：构建、扫描、镜像与自动部署全部成功。流水线：https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-topic/-/pipelines/5725
- 编排仓：文档/任务登记变更按workflow过滤，不触发Feishu服务部署。

Git HTTPS凭据已按用户要求存macOS钥匙串，未写入仓库；网页会话与Git凭据独立。没有触发Nacos手动任务或单dataId发布，正式新增网关路由仍待发布，完整索引/TECH等限制继续保留，任务仍in_progress。
