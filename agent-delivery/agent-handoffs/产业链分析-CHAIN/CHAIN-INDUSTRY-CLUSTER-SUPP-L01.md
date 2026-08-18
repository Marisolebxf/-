# CHAIN-INDUSTRY-CLUSTER-SUPP-L01 · 产业集群功能设计和实现的补充任务

> 波次 A+B+C 已齐 · 选择器 DEC 已签 · 2026-08-18 · 系统和算法（联调台）已开；波次 D lumen 未开

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:李伟` |
| supervised_by | `human:李伟` |
| claim_type | `pull` |
| 说明 | 2026-08-17 17:24 认领；17:25 转 `in_progress`。不管看板。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | 文档 `off`；Java / 前端 / 算法 `full` |
| 说明 | 波次 A 不缩 DEC / 契约 / Q068。波次 B 复用 `gkx-innov` JdbcTemplate。波次 C 三端各写一份 seed，不新加 npm。系统和算法同契约。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载。 |

## 问题清单

- 选择器 DEC **高颖已补签**（2026-08-17；李伟指示按已完成、以高颖身份签）。选择器叶可开。
- Q068 仍 🟡（甲方对外说法），UI 须标 ⚠️。
- 淮政玮尚未书面点实施方案 §6。团队默认已按 P1–P7 改文档。
- `lumen-ui-science-mobile` 本轮不做。国标 NIC 不换。
- 政策算法库 `polan` mock 关键词仍含旧产业名（非联调台选择器）；下轮可对齐 15。

## 修改内容

波次 A～C 见前稿（至第 20 条）。

21. 2026-08-18：GKX 系统和算法（`demo-ui-system-test` + 算法）接同一套 15 集群
   - 联调台：`lib/industryCluster` 补齐 resolve / resolveScope；`ChainSelect` 改级联（集群 → L0）；切集群不偷第一项；无映射 Empty「无相关产业数据」
   - 产业链算法库 8 子页（基础指标 / 全景 / 周期 / 关键环节 / 瓶颈 / 区域 / 深圳 / 热点）出数跟叶子；只选集群则展开全部已映射 L0
   - `demo-algo-science`：`chainan/mockgen` 改为 12 条 INB L0；API `_require_l0_chain_id` 拒绝 `CL-*`（400）
   - `demo-algo-ent-analysis`：企业 mock `DOMAINS` / `DOMAIN_CHAIN_CODE` 改为 12 条已映射 L0（去掉量子信息等未挂名）
   - 维护页 `/ops/cluster-map` 此前已齐；契约检查 `cluster-catalog.check.mjs` 绿
   - 不换：国标 NIC / 服务 `field-*`；波次 D lumen 仍未开

22. 2026-08-18：展示系统人才 + 政策漏网一刀切 → 现行 15 集群 `IndustrySelect`
   - 人才态势：分布洞察 / 动态 / 关注地区 / 画像 / 推荐评估 / 相似学者筛选 → IndustrySelect；过滤走 `legacyDomainInScope` / `fieldScopeShare`；空选=全部；无映射空态
   - 人才预览：顶栏「当前产业」IndustrySelect；无映射「无相关产业数据」；mock 数据集按叶子映射（生物医药/机器人等）
   - 政策：`industryFields` 改为集群 + L0；高筛选项同源；mock 旧 slug 仍可经 `LEGACY_POLICY_INDUSTRY_LABEL` 出中文名再 scope
   - 评估 NewPage「技术领域」+ 旧评估 4 Tab「产业领域」→ IndustrySelect
   - 不换：人才「行业类别=机构类型」；国标 NIC；lumen

23. 2026-08-18：菜单/路由可达漏网清扫（三系统）
   - 专题：技术链 6 + 科研 5 + 人才 4（侧栏 hidden 但路由可达）旧八大 Select → `ClusterIndustryTypeSelect`（15 集群+L0）；侧栏可见主域此前已齐
   - 展示：科技交流 / 创新生态 / ReportTab / 推演空间模拟 等主筛或明显漏网 → IndustrySelect；软科学/时空主题 label 对齐集群名
   - 死代码（无路由的 `pages/research/*`、根目录旧 Cycle/Bottleneck 等）未改，可后续归档
   - 检查：topic `route-industry-leftovers.check.mjs`；science scope check 扩展

回链：`dim-industry-cluster.md` · 说明书 · 实施方案 · `API-CHAIN-INDUSTRY-CLUSTER.md` · Q068。

## 验收证据

- 库：`demo_gkxlumenx_dim.industry_cluster` 15 行；`industry_cluster_map` 12 行。
- DEC 状态 = 已批准（`human:高颖`）。
- 三前端 + 联调台已换 15 集群目录；展示人才/政策漏网已切；未动 lumen UI / 正式 dim。
- catalog check：topic + science + **system-test** `cluster-catalog.check.mjs`；science `science-industry-scope.check.mjs`（含人才/政策）。
- 2026-08-18 夜回归：见前稿。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 / 算法只在 Python / Nebula | Java 只读写 dim；Python 拒 CL-* ✅ |
| D8 / D10 | 选择器 DEC 已签；联调台级联已换源 ✅ |
| D9 | 覆盖数分母仍 5；Q068 ⚠️ ✅ |
| D12 | 只动 demo 库 + demo-svc-platform + demo-algo-*；未写正式 dim ✅ |
| 不替甲方拍板 | Q068 仍 🟡 ✅ |

## 终核（横向 / 纵向 / 清单外）

| 轴 | 结论 |
|---|---|
| 横向选择器 | 专题主域 + **路由可达 hidden 域** / 展示主筛+服务漏网 / 联调台 同源 15 |
| 纵向查询 | 前端展开 L0 再打 `/innov/v1/industry/**`；Python 拒 CL-* |
| 空集群 | 新能源等 `l0=[]`：联调台 Empty，不装有数 |
| 仍不做 | 波次 D lumen；国标 NIC / 服务 `field-*`；无路由死代码归档；政策算法 mock 关键词全量对齐 |

## 下一步

波次 C + 系统和算法选择器已齐。波次 D lumen 仍禁止先于 demo。Q068 仍 🟡。
