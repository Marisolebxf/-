# SYSINT-03-VIZ-API-L01 · 可视化四菜单 Java 只读接口（复用不改契约，新增 4 条聚合）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent`（supervised_by `human:徐滕强`） |
| claim_type | `pull`（2026-11-03 用户当面确认监管人） |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 每条路由=DTO+Controller+Service 三件套最小实现；复用既有 Python 端点编排，未新增依赖、未造抽象（review 后删掉 VizBlock marker）；D9 空态纪律未跳过 |

## 背景与范围

《可视化四菜单-Java接口清单.md》：4 个可视化页面复用 7 条旧接口（R-1~R-7b 路径字段不变）+ 新增 4 条按页聚合接口（清单改版后原 N-1~N-8 八条并入这 4 条的块结构）。Java 只读 ADS、计算块只走 Python `/internal/*`、块级空态 `{empty,reason}`、数值缺省 null 不补 0。

## 实现清单（lumen-svc-platform dev，4+2 commit）

| 路由 | commit | 模块 | 块与数据来源 |
|---|---|---|---|
| V-E `POST /enterprise/topic/v1/profile/viz` | 98ee6ed | topic-enterprise | card（Python card+competitiveness 编排五列）、finance（trend 三条线+rd 取 card.finance_latest 按 rdYear 行对齐、basis 动态跟随 fallback）；scatter/timeline/swot/peers Python 无端点诚实空块 |
| V-I `GET /chain/topic/v1/industry/viz` | 1bf931b | topic-chain | scale（SYNC series MARKET_SIZE 优先+增长率）、heat（regionPoints 无经纬度剔除）、structure（snapshot 节点，share 口径未定 null 不造数）；mix 结构给齐待口径、forecast 空块+growthPct clamp[0,20]/years∈{3,4,5} |
| V-S `POST /svc/topic/v1/service-portal/viz` | 3d7cc82 | topic-svc | orgs（portal/region-map china 省级聚合行：id/type 置 null 不冒充机构语义、weight 不用条数充当、band_rule 临时规则）；demand/match/effect/cases 诚实空块 |
| V-P `GET /policy/topic/v1/policy/viz` | 74db750 | topic-policy | events/terms/clusters/depth 全为 Python 计算块，四块诚实空态（不拿政策条数/指标数冒充 value） |

Review 修复 commit `13211f3`（双轴 code review：Standards 5 项 + Spec 2 项，详见下节）+ `1c66528`（清误入 pyc）。

## 双轴 Code Review（大变更门禁，2026-11-04 用户要求）

Standards 轴 + Spec 轴并行子代理审查，修复：
1. **P0 测试断言矛盾**：forecast 测试期望 99→8 与实现 clamp 99→20 冲突（测试从未跑过）→ 按清单"滑块 0-20"定 clamp 语义，改断言为 20
2. **P0 Spec 违规**：`FinancialYearItem` 加 rd_expense 违反清单 §2 R-2"不往这条序列加字段"→ 回退字段，rd 改取 card.finance_latest
3. **真 bug（实跑抓出）**：全空年剔除条件误用全局 latestRd，rd 有值时空年份误留 → 按行 rowRd 判定
4. basis 标签动态跟随 fallback 口径（主营/营收、净利/总额）
5. V-S orgs id/type 不用省名冒充
6. 卫生项：unused import×2、多余 @SuppressWarnings×2 收敛局部、VizBlock 删、regionText 内联、ScaleEvent 补 ponytail 注释、测试类 *ControllerTest→*ServiceImplTest 挪 service/impl 包

## 测试（真跑，非声称）

本机 nexus 不可达 + 默认 javac 1.8 读不了 Mockito 5 字节码 → 用 JDK21（/Library/Java/JavaVirtualMachines/jdk-21.jdk）javac + 自写 JUnit launcher + 手动 classpath（~940 jar）逐模块编译运行：
- **V-E 3/3、V-I 4/4、V-S 3/3、V-P 1/1 = 11/11 全绿**（正是实跑抓出修复项 3 的真 bug）

## CI/CD 与线上验证（清单 §5 两种形态）

- pipeline 3689：backend:build 绿、四模块镜像绿、deploy:topic-{enterprise,chain,svc,policy} 全 success（本批自动跑）
- 线上实测：
  - V-E 空参=六块空态「未选择企业」；有行=红阳电池 card（名称/小型/72.5）+ finance 5 年序列（basis 主营/净利）+ 计算块空 ✅
  - V-I structure 4 节点（INB1303）、forecast 缺省 8/5 ✅；scale/heat 该链无数据空块 ✅
  - V-S orgs 3 省级行 + 四计算块空 ✅
  - V-P 四块空态 ✅
- **环境发现（非本单缺陷）**：30892 前端 nginx 未配 `/chain/**`、`/policy/**` 前缀转发（R-4/R-5 旧接口同样回 HTML，历来走 30895 网关）。前端联调 chain/policy 页走 30895，或另提 nginx 配置单。

## 架构合规自检

| 铁律 | 结论 |
|---|---|
| 调用链 前端→Java→Python /internal | ✅ 四路由均 Java 编排；计算块等 Python，无越层 |
| 2/7 Java 不写算法只读 | ✅ 无预测/归一化/文本生成落在 Java；空块不写死数 |
| 8 D9 诚实性 | ✅ null 不补 0、share/weight/depth 不用条数冒充、空态带 reason |
| 5 CI/CD | ✅ pipeline 绿 + deploy success + rollout |
| 12 lumen 隔离 | ✅ 仅 lumen-svc-platform dev |

## 遗留 / 移交

1. **Python 计算端点缺口清单**（移交算法侧，接入后对应块自动有数）：V-E scatter/timeline/swot/peers；V-I events/mix 数据/share 口径/forecast；V-S 机构级明细+weight 口径+demand/match/effect/cases；V-P events/terms/clusters/depth 全部
2. **30892 nginx** chain/policy 前缀未配（历史问题，前端联调走 30895 或提配置单）
3. R-2 逐年 rd：待 Python trend 序列官方支持后从 card.finance_latest 过渡方案升级

## 联调阶段补遗（2026-11-04/05 前端接线发现，均已在 dev 修复部署）

| # | 页面 | 问题 | 定性 | 处置 |
|---|---|---|---|---|
| 1 | 企业发展可视化 | 画像导出按钮真实模式无实现 | 前端缺口 | `exportCards` 双源（真实走 V-E card 五列），lumen-ui-topic 1deda3a |
| 2 | 企业发展可视化 | 地区列恒空 | Python card 缺地区 | `/profile/card` 补 region 省-市-区拼接（8b3d371）+ Java CardResponse.region 透传（9b722ff） |
| 3 | 企业发展可视化 | 散点图空 | 原维度（竞争力分×专利）ES 覆盖率 1.6%——**维度拍板更换** | Python enterprise_scatter 改注册资本×企业规模档位（d2e210e），Java/前端轴名同步（c8ea35f/fe68e9f）；原维度待数据补录后可回切 |
| 4 | 产业全景可视化 | 指标卡 10 个全空 | 三因叠加：批次隔离 + Q056/QC07 诚实空黑名单（设计内 4 指标置 None）+ 十指标 fact 缺行 | 批次统一 + INB1204 十指标补齐 → 6 卡亮起 |
| 5 | 产业全景可视化 | 曲线显示"64" | pickScaleSeries 误拿 NEWS_COUNT 冒充规模 | 只认 MARKET_SIZE + MARKET_SIZE series 补 6 年（561c4df）|
| 6 | 产业全景可视化 | 地理热力空 | **表结构缺口**：region_dist 无 lat/lng/weight 列 | ALTER 补 3 列 + 省级坐标/权重回填 119 行 → 线上 9 省点亮 |
| 7 | 产业全景可视化 | 结构 Tab 0 节点 | snapshot 需 chainId（前端传 industryId 时 0 节点，INB1303 chainId 通路 4 节点正常）| 链路确认，前端传参对齐 |

**数据覆盖盘点结论**（ES gkx_enterprise 20.8 万家）：competitiveness_score 仅 1 家、nested patent_total 3,270 家（1.6%）、financials 0 覆盖——散点/部分指标空态为真实数据缺口，非代码缺陷；DWD 侧 rd_investment/rd_staff_ratio/revenue_latest 覆盖 18.9 万家，region_dist 已补省级坐标。

## 涉及文件（联调补遗新增）

- `lumen-topic-py`：enterprise_profile.py（card region + _CARD_SOURCE 补省市区）、enterprise_scatter.py（维度重写）
- `lumen-svc-platform`：EnterpriseVizResponse.java（ScatterBlock xLabel/yLabel）、EnterpriseResponseDTOs.java（CardResponse.region）、EnterpriseVizServiceImpl.java（buildCard/buildScatter 接线）、IndustryVizServiceImpl.java（pickScaleSeries 修正）
- `lumen-ui-topic`：EnterpriseVizPage.vue（exportCards 双源 + 轴名）

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | ≈310000（含双轴 review 两子代理与本地实跑测试搭建） |
| model_used | glm-5.3-Flash |
| actual_cost | ≈$0.7 |
| cost_warn | green |
