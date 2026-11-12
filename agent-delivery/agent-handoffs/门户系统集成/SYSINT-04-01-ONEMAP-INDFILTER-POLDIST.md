# SYSINT-04-01 · 专题一张图产业切换整改 handoff（API-INDFILTER + DATA-POLDIST 合并交付）

> **task-id**：SYSINT-04-01-API-INDFILTER-L01（bugfix→流程裁定 tech_task 化）+ SYSINT-04-01-DATA-POLDIST-L01（feature）
> **执行/监管**：human:徐滕强（两单本人认领本人执行，锁 2026-11-12 16:24 起 4h）
> **来源**：智谱反馈切换产业数据不变/无数据。排查汇总：`工程过程/04-系统集成/04-门户系统集成/对接文档/我方/2026-11-12-专题一张图-切换产业问题排查汇总.md`（§6 为本会话复核附录）
> **强度**：ponytail full

## 1. API-INDFILTER-L01 · 交付内容

### 1.1 交付物（三仓联动）

| 仓 | commit | 内容 |
|---|---|---|
| lumen-topic-py | `8a8325f` | `type-scale-stats` / `district-heat` 加可选 `industry_chain_code`：过滤分支现算（`enterprise_base.org_size` 官方划型四档 / `district` 区县 GROUP BY），INNER JOIN `enterprise_industry_chain`；空参走原聚合口径零影响 |
| lumen-topic-py | 同上 | 自检 `tests/test_one_map_indfilter.py`（对 dev 库断言过滤生效+九区固定输出+空参兼容） |
| lumen-svc-platform | `4679a162` | `OneMapFacadeService` 三处透传 `industry_code`：enterpriseStats 的 typeScaleStats、districtStats 与 thematicMap(enterprise) 的 districtHeat |

### 1.2 方案修正（相对原 DoD，依据排查汇总 §6.2 复核）

原 DoD 的「EXISTS 过滤」不可行——`enterprise_type_scale_stats` / `enterprise_region_summary` 均无
`chain_code` 列（实测），`enterprise_industry_distribution` 0 行；`enterprise_base` 无
`company_type/enterprise_scale` 列但有 `org_size` 官方划型列，四档现算可行。**已按 §6.2 落地，
Java 派生 helper（scaleDist/mediumLargeRatio）零改动**（过滤分支返回同构 `company_type="全部"`+四档 scales）。

### 1.3 验证证据

- Java：`mvn compile` BUILD SUCCESS（JDK17）；`OneMapFacadeServiceTest` **10/10 绿**
- Python：py_compile + AST ✅；自检输出 `OK: 产业过滤分支随产业变（南山区 15929 vs 全市 345）；九区固定输出；空参路径完好`
- ⚠️ **口径提示给联调方**：改造后 scale_dist/enterprise_count 从「窄口径全市聚合表」切到「挂链底表现算」，
  数字量级会变（南山区 345→15,929 家），这是「随产业变」的预期效果；旧调用（不传产业码）不受影响。

## 2. DATA-POLDIST-L01 · 交付内容

### 2.1 盘点报告（DoD 第 1 条）

`demo_gkxlumenx_dwd.policy_base_info` 深圳行（province/city 含深圳）**987 条**，`district` 空 **951（96.4%）**；
`region` 字段全空不可用；`publish_organization` 含明确区级信号（龙岗区 46/龙华区 30/大鹏新区 26/前海 16/盐田 6/南山 3/光明 3/坪山 1）。

### 2.2 补数方案（DoD 第 2 条，D16 合规）

- 新表 `gkxlumenx_gapfill.gapfill_policy_district_map`（policy_id 主键，district_map/source_org/fill_method/gapfill_batch_id）
- 灌数脚本 `scripts/seed_gapfill_policy_district_map.py`（预览/--apply，发文机关保守推导：区名前缀须完整出现，
  市级机关不挂防误配；深汕合作区排除；已有 district 不覆盖；同 policy_id 去重）
- 实写 **131 行**（其余 816 行市级机关诚实归「市本级」，不冒充分布）
- **不改写 DWD 正式表，不写 ODS/ADS/供应方库** ✅

### 2.3 消费端叠加（`policy_routes.py`）

`_scoped_policy_sql` 改 LEFT JOIN 映射表，`COALESCE(gm.district_map, p.district)` 只补空值；
映射表缺失时 schema error → `_qualified_count` 回退原口径（诚实降级）。
`_portal_scope_where` 别名化（p.policy_id），headline COUNT 同步别名。

### 2.4 复验证据（DoD 第 3 条 DB 层）

| 切片 | 复验结果 |
|---|---|
| 全深圳（不限产业） | 全市 951 → 龙岗 48 / 龙华 32 / 大鹏 29 / 前海 16 / 盐田 10 / 罗湖 8 / 坪山 7 / 南山 6 / 光明 3 / 宝安 3 / 福田 3 / 市本级 816 |
| INB1309 产业切片 | 26 条 → 市本级 25 + **龙华区 1**（真实数据形态：市级机关发布的产业政策占绝对多数，诚实呈现） |
| INB1303 对照 | 13 条 → 市本级 12 + **光明区 1** |

- 测试回归：`test_policy_shenzhen_board.py` / `test_policy_portal_gaps.py` 全绿
- ⚠️ 公网 API-3/4/6 复验（DoD 第 4 条）待两服务 CI 部署滚动后执行（见 §4 开放项 1）

## 3. 架构合规自检

| 铁律 | 自检 |
|---|---|
| 调用链 FE→Java→Python | ✅ 未动层次；Java 只加透传参数 |
| 算法只在 Python | ✅ Java 无算法逻辑，仅参数下发 |
| D16 gapfill | ✅ gapfill_ 前缀表、独立库、不改 DWD/ADS |
| 调用链不越层 | ✅ Python 读 demo_gkxlumenx_dwd + gkxlumenx_gapfill（同实例 demo 面） |
| 空参兼容 | ✅ 两端点空参走原口径，企业发展概况页零影响（单测回归） |
| commit 标注 | ✅ `[agent:coordinator]` |

## 4. 开放项 / 风险

| # | 项 | 处置 |
|---|---|---|
| 1 | 公网网关 INB1309 vs INB1323 复验（DoD 第 4/5 条）：需 CI deploy 绿 + K8s 滚动两服务后 curl | CI 完成后复验；Java 部署需 TOPIC 模块（deploy:topic） |
| 2 | `policy_sz_dist` ADS 预聚合表仍是旧口径（全市 951 + 区级小值）——非切片路径 `kind=sz` 读它 | 属 B 轨 ETL（polan/job.py run()），建议另派单让 ETL 读映射表重算；本单消费端全走切片路径不受影响 |
| 3 | 「市本级」816 行占 82.6%：色斑图九区外仍有大值 | 口径诚实，建议前端 legend 加「市本级」说明；若甲方要求市级政策拆区需业务口径拍板（登记客户决策清单候选） |
| 4 | INB17xx 旧码仍无数据 | 不在本单范围（原 note 已声明），需 PM 与智谱确认码系后另立灌数/映射任务 |

## 5. cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | ~85,000（两单合计） |
| model_used | glm-5.3-Flash |
| actual_cost | ~$0.8 |
| cost_warn | green |
