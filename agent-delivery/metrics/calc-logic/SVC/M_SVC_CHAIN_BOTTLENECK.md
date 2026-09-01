# 瓶颈堵点判定（M_SVC_CHAIN_BOTTLENECK）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SVC-seed.yaml。

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_SVC_CHAIN_BOTTLENECK |
| 指标名称 | 瓶颈堵点判定 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 产业服务链分析 |
| 三级模块 | 服务链短板分析 |
| 更新频率 | 周 |
| 对齐状态判定 | 二级已按需求7.4+原型六环节收口；正式分档阈值待Q-SVCCHAIN-03 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q-SVCCHAIN-03 |

## 口径定义

选定产业在统计窗口内，按全周期六环节（研发与科研合作、知识产权与标准、技术转移与孵化、中试熟化、检测认证、市场化服务）分别给出短板判定，输出服务空白、薄弱环节、资源瓶颈或正常。六环节并列，不合成单一分数。

## 计算逻辑说明

入集：服务机构认定读 demo_gkxlumenx_ads.svc_org_card

选定产业用 dwd_org_industry_tags.credit_code = dwd_org_base_info.external_id，且 industry_code 须先在 dwd_industry_chain_info 定链。

第一步：按专家知识库六环节归集机构。正式映射待建 svc_chain_stage_map；代理为 main_activities 命中该环节服务类型词。未映射不计入任何环节。产业链节点 industry_link_code 不是本指标六环节。

第二步：各环节计 COUNT(DISTINCT org_id)；平均服务深度读 M_SVC_ORG_COVERAGE_DEPTH，无深度不伪造 0。

第三步：分档（演示规则，正式阈值待 Q-SVCCHAIN-03）：机构数 = 0 → 服务空白；机构数 ≤ 1 → 薄弱环节；平均深度非空且 < 55 → 资源瓶颈；否则正常。三类档位互斥，优先空白、再薄弱、再瓶颈。  WHERE main_activities 命中「委托研发|联合攻关|大设施开放|算力服务

第四步：各环节服务类型仅用于全链路可视化，不作为本指标三级，不单独改写分档。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 瓶颈堵点判定 | 研发与科研合作 |  | 从该环节入集服务机构覆盖规模与平均服务深度，判定研发与科研合作是否为服务空白、薄弱环节或资源瓶颈。 | COUNT(DISTINCT org_id) 归属本环节；AVG(服务深度)；0→服务空白；≤1→薄弱环节；深度<55→资源瓶颈 | dwd_org_org_product_info(org_id, main_activities)main_activities命中委托研发\|联合攻关\|大设施开放\|算力服务 — 本环节归集代理；见 M_SVC_ORG_COVERAGE_DEPTH — 平均服务深度 | svc_chain_stage_map-研发与科研合作映射 |
| 瓶颈堵点判定 | 知识产权与标准 |  | 从该环节入集服务机构覆盖规模与平均服务深度，判定知识产权与标准是否为服务空白、薄弱环节或资源瓶颈。 | COUNT(DISTINCT org_id) 归属本环节；AVG(服务深度)；0→服务空白；≤1→薄弱环节；深度<55→资源瓶颈 | dwd_org_org_product_info(org_id, main_activities)命中专利预审\|IP保护\|标准制定\|合规咨询 — 本环节归集代理；见 M_SVC_ORG_COVERAGE_DEPTH — 平均服务深度 | svc_chain_stage_map-知识产权与标准映射 |
| 瓶颈堵点判定 | 技术转移与孵化 |  | 从该环节入集服务机构覆盖规模与平均服务深度，判定技术转移与孵化是否为服务空白、薄弱环节或资源瓶颈。 | COUNT(DISTINCT org_id) 归属本环节；AVG(服务深度)；0→服务空白；≤1→薄弱环节；深度<55→资源瓶颈 | dwd_org_org_product_info(org_id, main_activities) 命中技术转移\|成功孵化\|产学研对接— 本环节归集代理；见 M_SVC_ORG_COVERAGE_DEPTH — 平均服务深度 | svc_chain_stage_map-技术转移与孵化映射 |
| 瓶颈堵点判定 | 中试熟化 |  | 从该环节入集服务机构覆盖规模与平均服务深度，判定中试熟化是否为服务空白、薄弱环节或资源瓶颈。 | COUNT(DISTINCT org_id) 归属本环节；AVG(服务深度)；0→服务空白；≤1→薄弱环节；深度<55→资源瓶颈 | dwd_org_org_product_info(org_id, main_activities) 命中中试\|中试放大\|工艺验证\|试产代工— 本环节归集代理；见 M_SVC_ORG_COVERAGE_DEPTH — 平均服务深度 | svc_chain_stage_map-中试熟化映射 |
| 瓶颈堵点判定 | 检测认证 |  | 从该环节入集服务机构覆盖规模与平均服务深度，判定检测认证是否为服务空白、薄弱环节或资源瓶颈。 | COUNT(DISTINCT org_id) 归属本环节；AVG(服务深度)；0→服务空白；≤1→薄弱环节；深度<55→资源瓶颈 | dwd_org_org_product_info(org_id, main_activities)命中检验检测\|计量校准\|认证认可 — 本环节归集代理；见 M_SVC_ORG_COVERAGE_DEPTH — 平均服务深度 | svc_chain_stage_map-检测认证映射 |
| 瓶颈堵点判定 | 市场化服务 |  | 从该环节入集服务机构覆盖规模与平均服务深度，判定市场化服务是否为服务空白、薄弱环节或资源瓶颈。 | COUNT(DISTINCT org_id) 归属本环节；AVG(服务深度)；0→服务空白；≤1→薄弱环节；深度<55→资源瓶颈 | dwd_org_org_product_info(org_id, main_activities) 命中投融资\|人才服务\|人才配置\|数字化转型— 本环节归集代理；见 M_SVC_ORG_COVERAGE_DEPTH — 平均服务深度 | svc_chain_stage_map-市场化服务映射 |

## 源表字段

- demo_gkxlumenx_ads.svc_org_card— 服务机构认定；
- dwd_org_industry_tags(credit_code, industry_code) — 选定产业挂接
- dwd_industry_chain_info(industry_code) — 定链
- 见 M_SVC_ORG_COVERAGE_DEPTH — 环节平均服务深度

## 待建字段

- svc_chain_stage_map-六环节映射

## 参考资料

瓶颈堵点判定｜研发与科研合作 | 国家发展改革委 |[https://www.ndrc.gov.cn/wsdwhfz/202512/t20251203_1402210.html](https://link.wtturl.cn/?target=https%3A%2F%2Fwww.ndrc.gov.cn%2Fwsdwhfz%2F202512%2Ft20251203_1402210.html&scene=im&aid=582478&lang=zh)

瓶颈堵点判定｜知识产权与标准| 国家知识产权局（九部门科技服务业实施意见）|[https://www.cnipa.gov.cn/art/2025/6/20/art_55_200211.html](https://link.wtturl.cn/?target=https%3A%2F%2Fwww.cnipa.gov.cn%2Fart%2F2025%2F6%2F20%2Fart_55_200211.html&scene=im&aid=582478&lang=zh)

瓶颈堵点判定｜技术转移与孵化 | 全国人大（国务院科技成果转化专项报告）|http://www.npc.gov.cn/npc/c2/c30834/202512/t20251229_450858.html

瓶颈堵点判定｜中试熟化 | 国家发展改革委 |[https://www.ndrc.gov.cn/wsdwhfz/202512/t20251203_1402210.html](https://link.wtturl.cn/?target=https%3A%2F%2Fwww.ndrc.gov.cn%2Fwsdwhfz%2F202512%2Ft20251203_1402210.html&scene=im&aid=582478&lang=zh)中华人民共...

瓶颈堵点判定｜检测认证| 中国政府网（质量基础设施助力产业链供应链指导意见）|[https://www.gov.cn/zhengce/zhengceku/202401/content_6926534.htm](https://link.wtturl.cn/?target=https%3A%2F%2Fwww.gov.cn%2Fzhengce%2Fzhengceku%2F202401%2Fcontent_6926534.htm&scene=im&aid=582478&lang=zh)

瓶颈堵点判定｜市场化服务 | 国家发展改革委（四链融合专题）|[https://www.ndrc.gov.cn/xwdt/ztzl/NEW_srxxgcjjpjjsx/yjcg/zw/202512/t20251204_1402237.html](https://link.wtturl.cn/?target=https%3A%2F%2Fwww.ndrc.gov.cn%2Fxwdt%2Fztzl%2FNEW_srxxgcjjpjjsx%2Fyjcg%2Fzw%2F202512%2Ft20251204_1402237.html&scene=im&aid=582478&lang=zh)
