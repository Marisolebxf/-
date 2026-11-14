# TS-L2-M10-STANDALONE-L01 · 维护管理单走线自建表

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api`（跨 PY / Java / 前端 / 文档，一次会话完成） |
| supervised_by | `human:刘剑锋` |
| claim_type | `coordinator_dispatch`（监管人当面派单） |
| 说明 | 注册表条目待补（本会话无 task-registry MCP），ID 拟 `TS-L2-M10-STANDALONE-L01` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 删除优先：全景叠加模块整文件删除、全景读图回退到叠加前版本；表名只改映射与字面量，不加抽象。D9/可观测/调用链未动 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `TS-L2-M10-LAYER-ARCH` / `TS-L2-M10-ENT-ARCH` / `TS-L2-M10-GRAPH-ARCH` 存储流图 |
| 图 diff | ① 存储节点 `gkxlumenx_cms.cfg_*`、`demo_gkxlumenx_dwd.technology_master/graph_*`、`demo_gkxlumenx_ads.graph_*` → 统一 `demo_gkxlumenx_ads.m10_*`；② 删边「M10 → 科技全域态势（图层配置消费）」「M10 → 科学技术全景（overlay 叠加）」「entan → Nebula（impact 只读）」；③ 禁止事项不变（Java 不写 nGQL，前端不直连） |
| 会签态 | 四单未改，仍为 11-13 签收版；**图与实现已不一致，需按本 handoff 补改三份 ARCH/DATA 的存储节点与删边**（未自填绿） |

## 问题清单

- 2026-11-13 线上 edu 科学技术全景 502（燕大图数据库连接问题），维护管理当时与全景关联。
- 孔东裁定（2026-11-13）：全景那个接口是空接口，放弃；**维护管理单走线、自建表，跟所有页面都不关联，数据库走 `demo_gkxlumenx_*`，表都新建，跟真实的不共用**。
- 监管人确认（同日）：科技全域态势联动断开、维护页内置效果预览；新表放现有 demo 库 + `m10_` 前缀；「论文主题库」数据源继续只读探测 `demo_gkxlumenx_ods.dwd_zh_paper`（属 demo 系列）。
- 交付目标不变：合规演示用例 20 行全部可演。

## 修改内容

### 库表（18 张新表，全在 `demo_gkxlumenx_ads`）

| 文件 | 内容 |
|---|---|
| `lumen-svc-platform/db/9x_demo_m10_layer_config.sql` | `m10_layer` / `m10_layer_group` / `m10_datasource`（含 6 个探测列）/ `m10_factor_display`；按原 id 一次性拷 `gkxlumenx_cms.cfg_*`（接口里的 id 不变）；种子兜底；幂等 |
| `lumen-algo-py/vendor/entan-py/scripts/mysql/m10_standalone_graph_v1.sql` | 图谱与实体 14 张，列为旧基线 + v2 + v3 终态；一次性拷当前工作状态（技术点、实体节点/边/成员/覆盖层、墓碑、维表），只用基线列，旧表有没有 v3 列都能跑；版本链不拷，写一个 `kind=seed` 起点版本，版本号接续旧表最大值 |
| 旧 DDL 5 份 | 文件头标注「已停用，勿再执行」 |

旧表全部**只读不改不删**；回退 = DROP 18 张 m10_* 表。

### PY（lumen-algo-py）

- `vendor/entan-py/api/tech_graph_maintain_routes.py`：`_Tx.t` 改指 `m10_*`，单库 `GKX_M10_DB`（默认 `demo_gkxlumenx_ads`；旧变量 `GKX_M10_ENT_*_DB` / `ENTAN_MYSQL_*_DB` 不再生效）；删除 `_panorama_hidden_relation_count` 与 Nebula 依赖，impact 返回三项计数。
- `tech_graph_snapshot.py`：仅补注释（payload 键名沿用旧逻辑名，物理表经 `{key}` 映射）。
- 全景去叠加：`lumen_common/algorithms/tech_graph_read.py`、`lumen_algo_service/views/tech_graph_read.py`、`tests/test_tech_graph_read.py` 回退到 `2f5d6b6~1`；删除 `lumen_common/algorithms/tech_graph_overlay.py`。
- 两个 Nebula 种子脚本文件头标注停用。

### Java（lumen-svc-platform）

- `gkxlumen-cms/.../TechMaintainService.java` + 测试：四表名换成 `demo_gkxlumenx_ads.m10_*`（库名硬编码，带 `ponytail:` 注释，同 `PolicyService` 惯例）。
- **display 未改**：`SituationPanoramaService` 的 overlay 透传在 PY 不再返回 overlay 后为空分支，为免多发一个服务保留，后续顺手删。

### 前端（lumen-ui-science-pc）

- 科技全域态势 `views/situation/overview/index.vue`：不再引用 `layerConfig` / `factorDisplay` 两个 store，图例回到平铺、无停用置灰与名色覆盖（pinia 全局状态也带不过去）。
- 科学技术全景：去掉「维护技术图谱」入口按钮及样式、overlay 不可用提示、学科筛选提示、「人工 / 存量」标注与人工强度；**保留**存量关系码中文字典（与 M10 无关）。涉及 `panorama/index.vue`、`GraphEmbedSection.vue`、`KnowledgeGraphCanvas.vue`、`lib/graph/liveGraph.ts`、`types/panorama.ts`、`styles/demo-panorama.css`。
- 维护页：新增 `maintain/components/LayerEffectPreview.vue`（复用 `overview/models/layerLegend.ts` 的 `buildLegendSegments`），挂在「多对象图层管理」表下；删除确认框去掉第 4 项计数；页头与注释去掉跨页联动口径。

### 文档

- `工程过程/04-系统集成/05-展示系统集成/合规演示用例/TS-L2-M10-合规演示用例.md`：环境 / 状态 / 主路径 / 序 5·7·9·35 期望 / 汇总 / 备注按单走线改写，新增「单走线改造本地回归」表。

## 测试结果（全部本机 127.0.0.1，未连共享库 / Nebula）

| 项 | 结果 |
|---|---|
| 两份 DDL 本机执行 + 重跑幂等 | 通过（9 / 4 / 4 / 11；技术点 4、实体边 59、成员 8、覆盖层 59） |
| entan vendor 单测 | 46 passed |
| PY 根套件 | 906 passed / 7 skipped（较 918 少 12 项 = 随叠加删除的 overlay 测试） |
| cms 单测 | `TechMaintainServiceTest` 20/20；模块 BUILD SUCCESS |
| 前端 | `vue-tsc --build` 通过；maintain 4 + overview 5 个单测通过；`vite build` 通过 |
| 接口冒烟 34–40 | 23/23（脚本口径更新：impact 三项、无快照用 seed 版本） |
| 图层 + 实体 LOOP 5–9、41–47 | 48/48；鉴权段需开鉴权的 display（7299），本机未起，display 代码未改 |
| 浏览器冒烟 | 8/8，截图 `/tmp/m10-standalone/shots/` |
| 旧表零写入 | 14 张旧表冒烟前后 `CHECKSUM TABLE` 完全一致 |

本机数据说明：本机旧表带早期联调残留（8 个挂接、「示范研究机构-19·联调…」），推荐初始为 51 条；经维护接口解挂 6 个 + 本机库改回名称后与线上形态一致（57 条），LOOP 全过。线上旧表无此残留，拷贝后应直接是 57。

## 遗留风险

- **部署前置（须监管人）**：共享库执行两份 DDL；确认 cms 连库账号对 `demo_gkxlumenx_ads` 有 INSERT/UPDATE/DELETE（本机为 root，线上未验）。顺序：DDL → entan → cms → 前端。PY 先于 DDL 发布时读面返回空态、写面 50302，不会写旧表。
- **线上 20 行待复测**：需监管人放 `~/.gkx/display-loop-token` 后跑线上 LOOP，回填用例「可演（线上）」。
- **seed 起点版本无快照**：不能回滚到迁入起点；演示前按用例备注先保存一次得到带快照的基线。
- ARCH/DATA 三份四单的存储节点与删边未同步（见「图即契约」）。
- 各仓改动均未提交；`lumen-ui-science-pc` 另有一个 11-13 本地提交（34–40 前端）尚未推送。

## 2026-11-14 上线与线上复测

| 项 | 结果 |
|---|---|
| 共享库 DDL | 两份脚本已执行（`gkxlumenx@10.50.11.76`），18 张 m10_* 表；seed 起点 v70 |
| 推送 | algo `0590704`、svc `051030a5` → `2e28e137`、ui `481b1ce`、编排 `0c274efce` |
| CI 失败与修复 | 051030a5 `backend:build` 失败：`OpsContentServiceTest` 3 处断言仍查字段 key，`a0680f6b` 已把必填文案改为中文名（该提交流水线被取消未暴露）。`2e28e137` 改断言后 cms / display 部署 |
| 本地测试的坑 | 本机 Maven 构建缓存会让 `mvn test` 不执行测试仍报 BUILD SUCCESS；须 `-Dmaven.build.cache.enabled=false`（CI 同款 `clean verify -pl … -am`）。11-13 报告里「cms 模块 BUILD SUCCESS」不成立，只有 `-Dtest=TechMaintainServiceTest` 的 20 项真实执行过 |
| 操作人 40-4 | display 新增 `SsoOperatorNameResolver`：门户 SSO 用户写图谱时用同一令牌调用户中心 1.4 取 `userInfo.realName`（缺省 nickname），按 userId 缓存，失败回退 username。线上 v95 起显示 `jianfeng` |
| 演示基线复位 | 解挂 11-11 后新增 3 实体（v71）→ 推荐 57 |
| 线上复测 | 图层 LOOP 22/22、实体 LOOP 30/30（含匿名写 401）、图谱接口冒烟 23/23；旧表 13 张（含 cfg_*）CHECKSUM 迁移时与复测后一致 |
| 演示初始图谱 | `vendor/entan-py/scripts/seed_m10_graph_demo.py` 发布 v95（14 点 / 18 关系）；00:20 有会话把图谱回滚到冒烟中间态 v87（带回「维护联调节点甲 / 乙」），已删除得 **v96**（带快照）= 演示基线 |
| 剩余 | LAYER/ENT/GRAPH-ARCH 存储流图同步；线上界面需登录后走查（未登录跳 SSO） |
