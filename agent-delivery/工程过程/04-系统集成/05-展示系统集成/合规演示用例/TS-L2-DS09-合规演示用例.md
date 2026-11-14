# TS-L2-DS09 科技发展规划 · 合规演示用例

| 项 | 内容 |
|---|---|
| 页面 | 科技发展规划(前端 `lumen-ui-science-pc/src/views/situation/tech-development-plan`,三页签:综合发展规划/重点领域规划/研究领域分析;路由 `/trend/tech-development-plan`,权限码 `menu:display:trend:plan`) |
| WBS | WBS-05-22 |
| 需规来源 | `agent-delivery/bid-reference/srs/02-科技信息展示系统/科技发展态势/科技发展规划.md`,序号 178–196(19 叶,excel 行 181–199) |
| 契约 | `agent-handoffs/科技发展态势-TS/sdd/l2/TS-L2-DS09-{OV,KEY,RES}-API.md`(API-TS-M9,11 端点 + 复用 export/jobs) |
| 版本 | **R2(2026-11-11 重制)**。R1(2026-11-08,M3)判定「dataset 404 整叶 blocked」已过时——11-09 起 PlanningController 11 端点上线、`gkxlumenx_ads.ts_plan_*` 30 表实灌、前端 real 轨道接线完成。R1 的 LOOP 对照与缺口建单段落按规程保持原文,以 git 历史为准(本文件末节存档判定摘要) |
| 任务ID | TS-L2-DS09-DEMO-PREP-L01 |

**主路径一句话(三页面)**:综合发展规划——进入页面默认 12 个月,看 8 项热点技术 → 切规划区域看研判演进 → 生成预警报告;重点领域规划——选「人工智能集群」看载体地图联动 → 方案卡三视图;研究领域分析——比对主体选华为看重叠度 → 生成情报报告 → 行级战略建议。

**当前轨道**:dev/prod 均 real(`VITE_APP_USE_MOCK=false` 双环境显式关闭);mock 仅残留一个种子注册,不影响演示。

## 覆盖表(19 叶 20 行)

> 「输入或选择/请求/期望输出」的值均来自 2026-11-11 实查:`gkxlumenx_ads` 库 + 网关 `http://10.50.69.111:30895` 匿名实测(底稿见 `TS-DS09-数据调研-20261111.md`)。接口均为 GET,base=`/display/v1/situation/planning`,信封 `R<T>`,匿名实测 code=0。

| 序 | 界面 | 输入或选择 | 触发 | 接口 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 178 | 综合发展规划 · 全球热点技术捕捉 | 不选(默认 12 个月);趋势对比技术默认 Top3(人工智能大模型/量子计算/合成生物学) | 进入页面即取数 | GET hot-technologies | `?range=12m`(3m/6m 已三窗并发预取) | items 8 行:人工智能大模型 heat=98、growth=45.2%、patents=12580;量子计算/合成生物学/固态电池/脑机接口/6G通信/人形机器人/可控核聚变 8 项齐;caliber_note=「热度=论文40%/专利30%/项目20%/资讯10%(口径待M0定稿,U5)」;趋势卡按 8 技术×季度序列切图 | 可演(demo_seed 口径注记) |
| 179 | 综合发展规划 · 多维度指标体系展示 | 指标分类「技术发展」;自定义布局勾选隐藏 1 卡 | 切分类按钮;布局勾选 | GET metric-system | 无参 | categories 7 类 30 条;技术发展类 6 条含「热度指数 98(+12.3%)」;布局勾选后卡片隐藏并存 localStorage(`tzp-overview-layout-hidden`),刷新保持 | 可演(无 metric_id 属 N/A 大屏运营壳) |
| 180 | 综合发展规划 · 技术与产业热点动态跟踪 | 规划区域「深圳」(默认) | 切区域下拉 | GET tracking | `?space_mode=shenzhen&time_mode=year` | timeline 2020–2026 共 7 事件(region 含深圳/湾区/上海/北京/杭州);spatial.points 5 点=深圳 1 城×5 图层(hotspot/space/talent/report/warning,score=94);extra 显示区域口径 | 可演(深圳档仅 1 城点位属种子现状,注记不派单) |
| 181 | 综合发展规划 · 本地特色与优势分析 | 维度 tab「优势领域」(默认) | 切维度 tab | GET local-advantage | 无参 | base_region=深圳,compare_to=全球;3 维度 18 指标双向条形:合成生物学 local=72/global_avg=45、人工智能大模型 92/68;reference_stats 带 `source=contract_draft_sample` | 可演(示例抽样口径需演示话术声明) |
| 182 | 综合发展规划 · 科技人才流动监控 | 时间维度三档依次演示(12 个月默认→6 个月→3 个月);人才流动「学术→产业」 | 切时间下拉(重取,range 过滤已于 2026-11-13 上线);切流动类型(前端过滤) | GET talent-flow | `?range=12m` / `?range=6m` / `?range=3m`(流动类型不进 URL) | **records/stats 三数随窗口变化、net_inflow/institution_flows/od_nodes 全窗口不变(契约 §218)**:12m→records 5 行(stats 预警 2/学→产 29/产→学 10);6m→4 行(预警 1/学→产 20/产→学 10);3m→2 行(清华→华为 2026-11-08、MIT→字节 2026-11-10;学→产 20/产→学 0,预警 0);OD 桑基按机构类型聚合随窗口联动;TOPS 两窗一致(华为 +1248…,全窗口口径,卡上无时间标签与之自洽) | 可演(种子日期分布已按三窗重排,TS-L2-DS09-TALENT-SEED-DATA-L01;talent_fill_demo 标注;U6 仅机构级聚合) |
| 183a | 综合发展规划 · 科创资源整合与推送(订阅配置) | 推送设置:关注领域 tags「人工智能,量子计算,合成生物」;频率「每日」;四类资源全选 | 打开推送设置 Modal → 保存 | GET+POST resource-push/subscriptions | GET 无参;POST body `{"resource_types":["report","project","policy","carrier"],"fields":["人工智能","量子计算","合成生物"],"frequency":"daily"}`(集合项目只许 GET/POST,原 PUT 已改 POST) | GET 未设置时返回默认 `{四类全选,[],daily}`;POST 200 返回更新后同形对象;失败回滚快照+报错提示。**需登录 token(401 即个人块空态,不伪造)** | 可演(需登录;唯一写面) |
| 183b | 综合发展规划 · 科创资源整合与推送(产物清单) | 登录后进入页面 | 进入页面即取数 | GET resource-push | 无参(可带 resource_type/field/is_read/page/size) | records 为当前用户推送产物行(类型/标题/领域/理由/时间),点击「资源详情」开证据 Modal(match/evidenceSource 为空串不造数) | **可演(2026-11-13 转正)**:调度链路已通——`sys_user_planning_push_record` 实有 16+ 行(user 302/3012/3009 各命中 policy/project/report 三行;3012 另有 carrier 行,系其订阅领域为空全命中);整点稳定产出 |
| 184 | 综合发展规划 · 潜在科技发展方向预警 | 产业分类级联「新一代信息技术」(预警随产业分类联动,2026-11-10 裁定 B) | 进入页面即取数;点「生成报告」再刷 | GET direction-warnings | 无参(level/field 过滤为前端行为) | **dev 实测 200**:items 61 条(high 6/medium 45/watch 10),source=model_output、generated_by=`proto:A5-wanghui-formula+mockfill@gkx-20261023run`、metric_id=M_INNOV_PLAN_DIRECTION_ALERT、generated_at=2026-11-09 16:00;六源均分卡+行级六源分条;点行开详情 Modal;报告 Modal 概况/预警/建议三节,Word 走任务中心 | 可演(注记:契约设计态为模型未注册 501+导出禁用,dev 当前注册开且 V1 表 61 行;region 仅「全球」;论文源 +650% 系单日回填窗口口径,summary 已自注) |
| 185 | 重点领域规划 · 区域科技创新空间布局分析 | 集群「人工智能集群」;图层「科技载体」(默认) | 点集群卡 | GET key-areas | `?cluster=ai`(region/carrier_type 留全量) | clusters 3(人工智能 ai/生物医药 bio/新能源 energy,各带 industry_category 与 default_map_layer);carriers 22 行真实坐标(如鹏城实验室 113.932,22.535),marker 按类型着色、集群命中金色描边;carrier_total=22 | 可演 |
| 186 | 重点领域规划 · 竞争力水平与潜力评估 | 无输入(三块平铺不随筛选变化) | 进入页面即取数 | GET key-areas | 无参(competitiveness_metrics/dimension_scores/benchmark_rows) | 指标 5 条(综合指数 78.5…);五维:创新资源 92/科研产出 88/产业竞争力 85/人才支撑 78/开放协同 72;对标 5 行:南山区/深圳湾合作区/广州天河区/香港科技园/珠海横琴新区(带 rank_no) | 可演(不随区域筛选变化为 V1 现状,注记) |
| 187 | 重点领域规划 · 土地用途与效益分析 | 无输入 | 进入页面即取数 | GET key-areas | 无参(land_use 块) | land_use 6 行:研发/产业用地 × 状态 good/medium/poor,柱状按 status 着色;carriers.land_benefit V1 恒 null(正式态回填) | 可演(期望只写表行级效益,载体级效益为空属设计) |
| 188 | 重点领域规划 · 科技载体分布展示 | 载体类型「重点实验室」;三视图切「载体清单」 | 切载体类型下拉(重取);切视图 | GET key-areas | `?carrier_type=lab` | carrier_types 6 行图例(全部 2856/重点实验室 128/工程中心 256/科技园区 68/孵化器 420/加速器 186);类型统计/区县分布(6 区基线)/载体清单(≤7 行,能级 tag+服务能力·资源聚焦文案);筛选后清单收敛 | 可演(carrier_count 全市口径与 carrier_total=22 演示清单双口径,注记) |
| 189 | 重点领域规划 · 产业与领域筛选联动 | 集群卡「人工智能集群」 | 点集群卡 | GET key-areas | `?cluster=ai`(region/carrier_type 同 watch 联动) | 地图 marker 金色描边命中集群载体;联动展示该集群 technologyField 与载体数;「清除集群筛选」恢复全量;时间维度下拉在本页无下游消费(装饰,注记) | 可演(交互壳 n/a_ops 裁定,消费同端点全量) |
| 190 | 重点领域规划 · 资源配置优化建议 | 方案卡「方案A 提升创新策源能力」;模拟目标年 2028(默认) | 点「查看建议」开 Modal(自动全量刷新+模拟) | GET key-areas/simulate | plans 块随 `?cluster=ai`;模拟 `GET key-areas/simulate?plan_id=a&target_year=2028` | plans 3 行:方案A(+18.6%/-23.2%)、方案B(+22.9%/-19.8%)、方案C(+15.2%/-16.7%),含行动建议与三按钮文案;方案对比 Modal 三方案表格;**simulate 2026-11-12 实测 200**:`{plan_id:"a",base_year:2026,target_year:2028,years:2,benefit_cumulative_pct:37.2,gap_relief_cumulative_pct:46.4,…}`(plan_id 大小写归一;线性年化累计口径,metric_id 恒 null 属 N/A) | 可演(G2 已闭合:端点已上线,2026-11-12 实测) |
| 191 | 研究领域分析 · 研究领域重叠度分析 | 比对主体「华为技术有限公司」(默认);时间范围「近3年」(系数 1.00) | 切比对主体(客户端复算) | GET research-analysis | 无参(主体/时间窗为前端状态) | companies 7 家(target=深圳先进技术研究院(锁定禁用),compare=华为/腾讯/阿里巴巴/字节/百度/小米);overlap_matrix 6 真值对:华为×腾讯 68(high)…;gauge=所选比对主体真值对复算均值;条形列表逐对;15 对中 9 对无行显「—(暂无重叠数据)」不造值 | 可演 |
| 192 | 研究领域分析 · 研究领域等级划分 | 重叠规则「balanced」(默认 70/55);切「自定义」阈值 75/60 | 切规则/调阈值(客户端判定) | GET research-analysis | 无参(level_cards+overlap_rules+time_scopes) | 等级卡 4 档:领先级 ≥80/优势级 ≥65/追赶级 ≥45/潜力级(is_draft=1);规则 3 档 strict 75/60/59、balanced 70/55/54、wide 65/50/49;调阈值后分档即时变化 | 可演(阈值 draft 待 M0 终拍,注记) |
| 193 | 研究领域分析 · 多企业竞争情报比对 | 无选择 UI(响应序前两家 compare 自动入象限) | 进入页面即取数 | GET research-analysis | 无参(competing_enterprises 块) | 四象限散点:华为/腾讯自动入象限;avg_overlap=有值对均值(Java 现算);pairs 带 source_tag=overlap/empty,无真值对显 empty_reason=no_seed_pair | 可演 |
| 194 | 研究领域分析 · 研究领域知识图谱展示 | 无输入(图谱全量;缩放控件为装饰) | 进入页面即取数 | GET research-analysis(兜底 research-graph) | 无参(graph 块) | graph 14 节点/13 边、5 类目(enterprise/institution/tech_field/literature/patent),未触发 U9 截断(node≤100/edge≤300);图例文案取响应 categories | 可演 |
| 195 | 研究领域分析 · 竞争情报分析报告 | 情报行任选一行(4 行,plan_id 关联 KEY 方案) | 点「生成报告」;行级「下载报告」 | GET research-analysis + POST /display/v1/situation/export/jobs | 行级 POST body `{"format":"doc","content_keys":["planning-research-intelligence"],"filter":{"title":…,"row_id":…,"field":…,"vars":{…}}}`(带登录 token) | intelligence_rows 4 行(领域/竞争态势/关键证据/区域规划启示/建议动作/优先级);报告 Modal;Word 任务 job_id 回填行内「任务 N」徽标并轮询 | 可演(需登录;G3 已闭合:端点 2026-11-12 实测存在,匿名 POST → 401「访问令牌不存在」即鉴权墙非 404;带 token 的 200 留 LOOP R1 首笔核验) |
| 196 | 研究领域分析 · 企业发展战略建议 | 情报行点「生成战略建议」;Modal 内「方案模拟」 | 点按钮开 Modal | GET research-analysis(strategy_advice 派生块) | 无参(templates 渲染) | 战略 Modal 三节 tech_route/resource_config/cooperation,按 report_export templates 占位符渲染(缺省回落 demo 冻结文案);方案三元组按优先级映射 KEY plans(优先级高→方案A/含追赶→方案B/其余→方案C);「方案模拟」Modal 为静态方案行展示 | 可演(派生口径 mode=derived 注记;无目标年模拟接口) |

## 三条主路径

### 主路径一 · 综合发展规划(178–184)
1. 进页面(默认 12 个月/深圳/产业分类空):热点榜 8 行,「人工智能大模型 heat=98 / +45.2%」居首(178);
2. 趋势卡技术多选保持 Top3,时间趋势↔空间分布切换,口径三卡显示热度定义(178/180);
3. 切规划区域「粤港澳大湾区」:tracking 重取,时间轴事件按区域过滤、地图视口收敛(180);
4. 指标体系切「技术发展」:6 条指标含热度指数 98;勾自定义布局隐藏一卡并刷新保持(179);
5. 本地优势切三维 tab:深圳 vs 全球 18 指标(181);
6. 人才流动依次切「12 个月→6 个月→3 个月」:records/stats 三数随窗口递变(5→4→2 行;预警 2→1→0)、桑基联动;TOPS 保持全窗口(华为 +1248)(182);
7. 产业分类选「新一代信息技术」:预警行联动收敛;点「生成报告」开 Modal,概况/预警/建议三节(184);
8. 推送设置:领域 tags 三值+每日,保存(登录态);资源表现状空态属 G1 缺口如实展示(183)。

### 主路径二 · 重点领域规划(185–190)
1. 切页签:集群导航 3 卡(人工智能/生物医药/新能源);
2. 点「人工智能集群」:key-areas `?cluster=ai` 重取,marker 金色描边、载体数联动(185/189);
3. 载体类型切「重点实验室」再切「载体清单」视图:清单收敛至 lab 载体,能级/服务能力文案齐(188);
4. 竞争力卡:综合指数 78.5、五维 92/88/85/78/72、对标 5 区(186);
5. 土地效益柱状 6 行按 status 着色(187);
6. 点方案A「查看建议」:开 Modal 并请求 simulate(404 回落公式,注记话术),再开「方案对比」看三方案(190)。

### 主路径三 · 研究领域分析(191–196)
1. 切页签:等级卡 4 档+摘要(目标主体锁定深圳先进技术研究院);
2. 比对主体「华为技术有限公司」:gauge=华为真值对复算均值、条形列表逐对,无值对显「—」(191);
3. 重叠规则切「自定义」75/60:分档即时变化(192);四象限看华为/腾讯落位与 avg_overlap(193);
4. 知识图谱 14 节点/13 边,图例五类目(194);
5. 点「生成报告」开 Modal;情报行「下载报告」走任务中心(G3 探测)、「查看证据」开证据 Modal(195);
6. 行级「生成战略建议」:三节建议+方案映射;「方案模拟」静态展示(196)。

## 判定分布(R2.2 · 2026-11-13 终版)

| 分类 | 行数 | 序号 |
|---|---|---|
| ✅ 可演 | **20(全部)** | 178–196 全行(183a 需登录;195 需登录;183b 已于 2026-11-13 转正) |
| ⚠️ 部分/条件可演 | 0 | — |
| ⛔ 覆盖不到 | 0 | — |

口径:183 拆 a/b 两行后 20 行对 19 叶。全部「可演」行均要求演示话术携带口径注记(demo_seed/talent_fill_demo/contract_draft_sample/model_output 四类 source 与 caliber_note),不隐匿演示数据属性。

## 缺口清单(2026-11-13 终态:全部闭合)

| 缺口键 | 类 | 终态 |
|---|---|---|
| G1 `sys_user_planning_push_record` 0 行 | DATA(链路修复) | **已闭合(2026-11-13)**:admin 连库恢复(1045 于 11-12 晚间自行消解,首条调度 19:00;期间累计合入的净改进:otel agent/配置段/mysql.enabled 显式/env 去重/druid 硬编码/nodeSelector 支持);调度整点稳定(15+ 次 200/200),display+topic-async 双执行器 30s 心跳注册,16+ 行推送落表(3 用户),聚合一通知 ✓;183b 转可演 |
| G2 `GET key-areas/simulate` | QUERY | **已闭合(2026-11-12)**:实测 200,190 转可演 |
| G3 `POST export/jobs` | QUERY(探测) | **已闭合(2026-11-12)**:端点在,匿名 401 需登录,195 转可演 |

**保持现状不派单**(演示话术如实声明):预警 200/501 双态语义(dev 注册开);预警 region 仅全球;tracking 深圳档 1 城 5 点;186 三块不随区域筛选;carrier_count(全市统计)与 carrier_total(演示清单 22)双口径;local_adv 合同草稿示例抽样;人才流动机构级聚合(U6)且 **TOPS/net_inflow/od_nodes 为全窗口口径(时间维度仅作用于 records/stats 三数/桑基,契约 §218 设计如此)**;192 阈值 draft 待 M0;196 派生建议无模拟接口;Overview「查看全部/查看联动指标」与图谱「图例说明/缩放控件」为 demo 装饰无 handler;Overview 产业分类级联与 KeyArea 集群为两套选项源(前者 `/situation/industry-domains`,后者 key-areas clusters)。

## 调度核对

- 需规 19 叶(178–196)每叶至少一行;183 因读写两面拆 a/b,合计 20 行,无空行。
- 功能点编号(§4.2.3)对照:契约三册(OV/KEY/RES-API v2)全部端点均出现在本表期望输出列,含复用端点 export/jobs(195)与 FE 追加调用 simulate(190,记 G2)。
- 「覆盖不到」0 行;3 行部分/条件可演均挂缺口键,可进入 LOOP 首轮。

## 历史记录(R1 · 2026-11-08,存档)

R1 基于当时实测:核心接口 `POST /display/v1/situation/planning/dataset` 404(单端点契约草案期),判定 19 行整叶 blocked「待开发完成」,未进 LOOP;缺口建单建议排期 DS-09 planning 控制器。完整 R1 文本以 git 历史(`git log --follow` 本文件)为准。11-09 起架构落地为 11 端点(单 dataset 拆分)并实灌 30 表,R2 起以本版为准。
