# KJZTFWXT B∪A 切点投影交付对账

> 生成脚本：`scripts/_gen_zt_delivery_func_ab_merge.py`
> 交付文件：`qa/delivery/KJZTFWXT/6.国际科技信息中心项目_科技专题服务系统_测试用例.xlsx`
> 口径：`as-built/prompts/_submit.md`；未覆盖不投影；政策/综合智能本波不纳入

## 汇总

| 项 | 值 |
|----|----|
| 投影行（交付功能 sheet） | **886** |
| 已覆盖 | 507 |
| 部分覆盖 | 379 |
| 缺源场景跳过 | 7 |
| 编号来自 A 线 v8 | 885 |
| 新号（无 A 匹配/冲突） | 1 |
| A 线 v8 总功能点 | 1298（含政策/综合等未做 B 册） |

## 按册

| 册 | 投影行 |
|----|--------|
| `SVCCAP-服务机构技术力评估分析` | 44 |
| `REGIDX-区域产业指数评价` | 41 |
| `EVALTECH-企业技术力评估对比分析` | 41 |
| `ATTRACT-招引企业推荐分析` | 41 |
| `SVCSZ-深圳服务链现状分析` | 40 |
| `EVALBIZ-企业商业力评估对比分析` | 39 |
| `BOTTLENECK-产业瓶颈堵点识别` | 39 |
| `SVCGRAPH-服务链图谱分析` | 39 |
| `SVCTREND-服务机构新增趋势分析` | 38 |
| `CYCLE-产业周期分析` | 37 |
| `SZSTATUS-深圳企业现状分析` | 37 |
| `PANORAMA-产业链全景图谱` | 36 |
| `KEYLINK-产业关键环节识别` | 36 |
| `PAIN-企业发展痛难点分析` | 36 |
| `SVCFIELD-服务机构产业领域分析` | 36 |
| `SVCSHORT-服务链短板分析` | 35 |
| `REGCOMP-区域产业竞争力评价` | 33 |
| `CULTIVATE-培育企业推荐分析` | 33 |
| `SUPPLY-企业供应链关系分析` | 33 |
| `SVCCULT-培育服务机构推荐分析` | 32 |
| `EVALCOMP-企业综合竞争力评估` | 30 |
| `SVCATTR-引入服务机构推荐分析` | 26 |
| `KEYENT-重点企业类型分析` | 24 |
| `SZCMP-深圳产业情况分析对比` | 23 |
| `SZDEV-深圳产业发展分析` | 20 |
| `KEYDOM-重点企业领域分析` | 17 |

## 抽样对账（前 30 行）

| 交付编号 | 功能点 | 状态 | 源场景 | 编号来源 |
|----------|--------|------|--------|----------|
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00001` | 指定图谱所展示的产业 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00531` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00002` | 构建产业链节点－连线结构 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00535` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00003` | 以节点－连线图谱展示产业链结构 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00535` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00004` | 在图谱中展示各个环节节点 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00535` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00005` | 在图谱中以连线展示环节关联 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00535` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00006` | 在图谱中展示企业关联 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00536` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00007` | 在图谱中展示技术关联 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00537` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00008` | 展示环节节点名称 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00535` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00009` | 识别产业链完整性 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00534` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00014` | 校验未指定产业时不可展示图谱 | 部分覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00545` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00016` | 校验图谱含环节节点及企业或技术关联 | 部分覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00535` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00017` | 默认以节点－连线形式展示产业链 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00535` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00018` | 展示产业链图谱为空提示 | 部分覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00545` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00019` | 展示产业链图谱生成中状态 | 部分覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00533` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00023` | 点击环节节点发起下钻 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00536` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00024` | 对任一环节节点均可下钻 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00536` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00025` | 下钻提取关联企业 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00536` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00026` | 下钻提取主流技术路线 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00537` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00027` | 下钻提取市场规模 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00537` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00028` | 在下钻详情中展示关联企业 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00536` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00029` | 在下钻详情中展示主流技术路线 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00537` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00030` | 在下钻详情中展示市场规模 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00537` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00031` | 校验下钻详情含关联企业、主流技术路线与市场规模 | 部分覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00536` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00032` | 未点击环节节点时不展示下钻详情 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00536` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00033` | 按周期更新产业链图谱 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00538` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00034` | 识别新企业加入 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00543` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00035` | 识别技术替代 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00543` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00036` | 识别环节退出 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00543` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00037` | 在图谱中反映新企业加入 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00543` | A线v8 |
| `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00038` | 在图谱中反映技术替代 | 已覆盖 | `ZNFWJQ-KJZTFWXT-v1.0-FUNC-00543` | A线v8 |

## 已知限制（本波）

1. 步骤/预期为**规则化最小切片**（对准功能点、不加严）；若验收要求人工精炼切片，可按册回炉改投影。
2. 未覆盖功能点未进表；政策 T19–T21、综合智能 T30–T32 无 B 线册，未纳入。
3. 门户/查询/维护/对比篮等 A 线 N/A 册不进本表（无 v8 点可挂）。
4. 非功能 sheet（兼容/集成/性能）仍为模板样例，放行前须清检。
