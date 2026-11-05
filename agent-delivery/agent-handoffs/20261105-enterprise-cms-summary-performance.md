# 企业内容管理列表性能优化

交付标识：20261105-enterprise-cms-summary-performance。
ponytail: full；只调整已有SQL查询组织，不新增索引、表、缓存或依赖。

## 问题与范围

`GET /cms/cms-ops/v1/enterprise/content/enterprise-summary?future_industry_code=INB1303&profile_status=all&page=1&size=10`
线上曾实测7.73秒。旧SQL COUNT复用完整投影，分页前对189293家企业重复执行6个相关子查询并物化，再排序取10条。

## 需求保持

- 企业集合仍来自`v_cms_ent`，包含DWD只读底稿与CMS覆盖/新增实体；软删语义保持，CMS修改后的名称参与关键词筛选和排序。
- 产业只限定运营内容范围，不擅自改为按产业过滤企业主数据。
- 档案状态仍是有已发布优先published，否则有记录draft，否则empty；已删除记录排除。
- 排序保持`(profile_status<>'empty') DESC,name,enterprise_code`，draft与published不额外区分优先级；分页前应用全部筛选条件。
- 明星存在性含草稿，入选标签仍按sort_order/id第一条取；重点及深圳名单保持原JSON_CONTAINS语义，包括字符串大小写和历史异常JSON值。
- CMS修改只落CMS，DWD和ES零写入；不改变接口字段。

## 实现

产业参数一次绑定，档案状态按企业预聚合、明星记录按企业排序编号取首条。COUNT只关联筛选必需的状态。分页阶段保留档案状态及必要筛选，分页后只对当前页补明星标签、重点和深圳重点标记。

JSON名单没有强行改为普通字符串关联：边界SELECT测试发现历史数组值与JSON_CONTAINS也会匹配，最终保留原函数，正常默认查询只在当前页执行。

## 验证

- 待提交索引快照隔离编译，OpsContentServiceTest 37项通过。工作区另有其他会话政策/服务CMS改动，仅暂存本次enterpriseWorkspace及对应测试。
- 真实库旧/新SQL首轮默认页：COUNT3.425→0.881秒，分页3.612→1.213秒，合计7.037→2.094秒；总数189293、全部结果字段及顺序一致。查询仍有宽视图物化成本，未承诺固定延迟。
- 11组真实数据对照全部通过：第一页、第二页、draft/empty/published、明星yes、明星no+重点no、重点yes、地区+状态、无产业的CMS新增实体、跨产业完整编码。对照COUNT及每行全部字段/顺序，不只比数量。
- 13组纯SELECT边界数据对照全部通过（不建临时表、不写业务数据）：同企业重复draft+published、已删除档案/名单、同企业多条明星记录首条选择、重复名单、大小写编码、JSON数值/null/数组/缺失编码、CMS修改后的名称搜索、CMS新增、无产业、跨产业、size=1分页。
- 最终真实库对照：默认页COUNT3.425→0.881秒、分页3.612→1.213秒；第二页合计6.855→2.009秒；draft合计7.238→1.725秒；重点no+明星no合计7.610→3.291秒（筛选仍需保留原JSON判断）；关键词限定查询约0.8–1秒，未将不同筛选场景混称统一耗时。
- 代码32be90d已推送origin/dev，流水线3917 backend:build（BUILD SUCCESS）、helm:lint、backend:image:cms成功；deploy:cms排队时，通过项目SSH跳板发布同一CI镜像`gkxlumen-cms:32be90df`，rollout成功。
- 线上同一入口默认页连续3次5.545/2.421/2.457秒（第一轮在新实例刚启动后）；total=189293及前10家顺序与发布前一致。发布前本次记录12.254秒，早前基线7.73秒，避免把单次网络波动当成SQL固定提速比例。
- 线上筛选全部回归通过：draft=3（2.099秒）、published=0（1.941秒）、draft+star=yes=1（2.645秒）、draft+key=yes=2（2.551秒）、draft+坪山区=1（0.738秒）。无业务数据写入。
- 先前两个不可见试验索引收益不显著，已删除；本次无DDL。

## 状态

不虚构task-registry登记、成本或视觉验收；当前会话未提供对应registry MCP。用户明确要求保持需求语义，按结果等价性通过后发布。
