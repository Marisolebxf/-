ponytail: off（多仓实现总方案；按公约 ponytail §4 不以缩代码为目标）

# TS-L2-M10-DEMO-FULL-L01 · M10 维护管理：除 34–40 外全部需规补到可演示

> **日期**：2026-11-11　|　**执行**：coordinator-agent（拆 4 路并行实现 + 本地联调 + 本地 LOOP）　|　**监管**：human:刘剑锋
> **授权原文（2026-11-11）**：「除了【覆盖不到（设计不实现）：同序 34】先不管，其他需规的最终交付都要求覆盖可演示，一切按照你的推荐方案来执行。所有前后端修改，先只在本地验证，跑完 loop，人工确认可演示达标之后，才能提交代码部署更新。」
> **输入**：`合规演示用例/TS-L2-M10-合规演示用例.md`（11-10 版：可演 1 / 部分 10 / 覆盖不到 9）、`agent-handoffs/展示系统-合规演示用例/TS-M10-CASE-FILL-L01.md` 遗留 11 条。
> **纪律**：四仓改动一律**只留本地工作区，不 commit、不 push、不动共享库**，直到监管人人工确认可演示；本地验证全部打本机 MySQL 隔离库（见 §4）。

## 1. 目标：13 行由「部分 / 覆盖不到」转「可演」

范围 = 序 5、6、7、8、9、41、42、43、44、45、46、47 + WBS-05-24 权限降级。序 34–40 维持「覆盖不到（设计不实现）」，不动。

| 行 | 现状缺口（11-10 实测） | 推荐方案（本次实现） | 落点 |
|---|---|---|---|
| 5 多对象图层管理 | 维护页无图层开关；全域态势不读 `enabled` | 维护页新增「多对象图层管理」表（9 图层 × 显示开关 + 所属组）；全域态势读图层配置：停用图层不出点位、不进筛选，图例置灰标「已停用」 | FE 维护页 + FE 全域态势 |
| 6 实时数据监控 | 探测不落库，「连通」「最近同步」刷新即丢 | 探测结果落库（状态 / 时延 / 时间 / 说明）；数据库表型探测实做（表存在性 + 行数 + 最新数据时间）；「最近同步」= 数据库表型的最新数据时间 / API 型最近一次连通成功时间；API 型 DNS 失败按契约返回 200 + `result=失败` | cms DDL + cms + FE |
| 7 图层分组与组织 | 图层不能分组；分组名 / 色不影响地图 | `cfg_tech_layer` 加 `group_code`，图层可挂组；全域态势图例按组分段（组名 + 组色），图层重命名 / 颜色走序 9 的要素显示配置 | cms DDL + cms + FE |
| 8 数据源灵活配置 | 名称空值前端不拦；数据更新无从体现 | 前端必填校验；三型数据源增删改启停 + 探测（数据库表型给出行数与最新数据时间，体现「及时更新」）；契约里的凭据字段不在需规原文，不做 | FE + cms |
| 9 基础信息查看（配置面） | 全域态势不自己拉 factor-display | 全域态势进页即 `syncFromServer()` + 图层配置；读侧浏览 / 详情 / 筛选 / 收藏 / 标签仍归 TS-L2-DS01（用例注明） | FE 全域态势 |
| 41 推荐列表 | 无排序控件、无分页（Top50 截断）、搜索只在前端、服务端忽略类型 | R1 服务端检索：`keyword`（不区分大小写）+ `entityType` + `yearFrom/yearTo` + `sortBy` + `page/size`，返回 `total`；前端加排序下拉、年份范围、服务端搜索、分页 | PY + Java 透传 + FE |
| 42 添加到全景图 | 可演；全景图只是列表 | 维护页右栏加「全景图」画布（G6）：技术点居中、已挂实体为节点、人工边为连线；新加节点高亮反馈 | FE |
| 43 实体删除 | 只有批量按钮 | 画布与列表都支持单选 / 多选；右键菜单「删除实体」；Delete 键；确认框写明「将同时删除该实体的所有关系，实体回到推荐列表」 | FE |
| 44 关系删除 | 删关系连带实体移出全景图 | **挂接状态与边解耦**：新增 ADS `graph_entity_member`（技术点 × 实体），R2 实体 = 成员；删边只删边，两端实体保留；画布点连线高亮 + 右键「删除关系」 | PY DDL + PY + FE |
| 45 实体属性编辑 | 改类型不生效；技术点描述 / 分类无入口 | overlay `type` 列作类型覆盖，R1/R2 读 `COALESCE(type, entity_type)`；前端 patch 带类型；R2 技术点输出 `description`；编辑框补「分类」；双击 / 右键「编辑属性」 | PY + FE |
| 46 关系编辑 | 强度 / 时间界面只读 | 关系编辑框：类型 + 强度（人工值，标「人工」）+ 时间范围（年）；画布点连线 / 右键「编辑关系」 | FE（PY 已支持，加校验） |
| 47 批量管理 | 无关系多选 / 批量改属性 / 框选 / 预览 / 统计 | 实体与关系都可多选（画布框选 = G6 brush-select，列表 Shift 连选 + 全选）；批量删除 / 批量改属性 / 批量改关系；执行前调 `changes:validate` 弹预览（摘要 + 明细，结构错误 422 列出）；执行后弹结果统计（成功 N / 失败 M + 失败明细） | PY + FE |
| 权限降级 | 写接口匿名可调；无降级提示 | **写接口要求登录**（display 层判 `SecurityUtils.getUser()`，未登录 401 信封 40101；读接口按 2026-10-31 孔东裁定继续匿名）；前端无 token 或写接口 401/403 → 页面切只读并给提示条，不白屏；路由无菜单权限落回页加全局提示条（读 `upgrade/reason` query） | Java + FE |

**测试残留清理**（监管人已授权按推荐执行；**本地库先执行，共享库在部署时执行**，SQL 见 §5.3）：分组「网关图层」「QA测试分组」删除；分组 1 颜色恢复 `#165DFF`；数据源 2 改回文献组；数据源「百度」保留为 API 连通成功样例，改名「公网 API 连通样例」；技术点 3 名称恢复「神经性厌食症治疗的临床视角」、重要性恢复「中」；9 图层按语义挂组（知识产权：专利、成果；文献：论文、期刊；主体：专家学者、组织机构；新增「科研活动图层组」：会议、课题、项目）。

## 2. 接口增量（契约真源以本节为准，实现完再回写 LAYER-API / ENT-API 册）

前缀：display 对外 `/display/v1/situation/maintain*`；topic `/topic/v1/tech/graph/**`；Python `/internal/v1/sci/tech/graph/**`。三层路径后缀一致，Java 纯透传。

### 2.1 ENT（Python 实现，Java 透传）

1. **R1** `GET /nodes/{technologyId}/recommend-entities`
   - 查询参数：`keyword`（显示名子串，不区分大小写，服务端过滤）、`sortBy=strength|time|name`、`entityType=all|person|institution|paper|patent`（兼容中文 全部/人/机构/论文/专利；person ⇐ person/scholar/expert，institution ⇐ institution/org/organization/enterprise）、`yearFrom` / `yearTo`（闭区间，作用于 `year`；设了就排除无年份项）、`page`（≥1，默认 1）、`size`（1–100，默认 20）。非法值 400/40001。
   - 排除：该技术点的成员实体（`graph_entity_member`）。
   - 响应 `data`：`{items:[...原字段，entity_type 为生效类型], total, page, size}`。
2. **R2** `GET /current`：`nodes[]` 增加 `description`（取 `technology_master.description`）；`nodes[].entities` = 成员表（兼容：人工边存在但无成员行的实体也算成员）；`nodes[].edges` = `source='manual'` 边。实体 `entity_type` 为生效类型。
3. **挂接语义**（ADS 新表 `graph_entity_member(technology_id, entity_id, entity_type, version_id, created_at, PK(technology_id, entity_id))`）
   - `hang_entities`：写成员 + 人工边（同现状）。
   - `unhang_entities`：删成员 + 边按现状回退 / 删除。
   - `delete_entity_edge`：只删边；该边有 `strength_auto` 时以 `('关联',0, strength_auto, time_to, source='auto')` 回写快照边（`INSERT IGNORE`），**成员不动**，实体仍在全景图、不回推荐。
   - `update_entity_overlay`：`patch.type`（person/institution/paper/patent）写 overlay `type` 列；枚举外 422。
   - `update_entity_edge`：`strength_manual` 0–10；`time_range.from ≤ to`，年份 1900–2100；违例 422。
4. **validate** `POST /changes:validate`（dry-run，不落库）：逐 op 结构与存在性校验（技术点在主表且 active；hang 的实体存在于候选或 overlay；unhang / overlay 更新的实体是成员；边操作的 `edge_key` 存在；patch 字段枚举与范围）。有错：HTTP 422 `{code:42201, msg, data:{errors:[{index, client_op_id, op, msg}]}}`。无错：`{dry_run:true, op_count, summary:{hang_entities, unhang_entities, delete_entity_edge, update_entity_edge, update_entity_overlay, update_node}, preview:[{index, op, client_op_id, target, desc}]}`；`summary` 计的是对象数，`desc` 是中文一句话，如「将实体「X」添加到技术点「Y」」。
   - `POST /changes` 提交前跑同一套校验，422 同上。
5. **publish** 响应 `data`：`{version_id, status, stats, results:{succeeded, failed, failed_items:[{index, client_op_id, op, reason}]}}`；按 op 影响行数判定，0 行算失败（如「关系不存在」），其余照常发布。
6. **impact**：技术点不在主表返回 404/40401（对齐契约）。

### 2.2 LAYER（cms 实现，display 透传）

1. `cfg_tech_layer` 加 `group_code varchar(32) NULL`。`GET /layers` 每行加 `groupId`（同数据源的 id 翻译层，未挂为 `null`）。`POST /layers/save` 的 `items[]` 支持 `{layerCode, enabled?, groupId?}`，`groupId: null` 表示取消挂组，不存在的组返回 404/40401。
2. 删组：组下仍有图层或数据源时返回 409 `GROUP_IN_USE`，文案「组下仍有 N 个图层、M 个数据源，请先改挂」。
3. `cfg_tech_datasource` 加 `last_probe_status varchar(8)`（通过/失败）、`last_probe_at datetime`、`last_probe_latency_ms int`、`last_probe_message varchar(256)`、`last_data_at datetime`、`last_row_count bigint`。`GET /datasources` 每行加 `probeStatus / probeAt / probeLatencyMs / probeMessage / dataUpdatedAt / rowCount`（无值为 `null`）。
4. probe：
   - API 型：DNS 失败、超时、非 2xx/3xx 一律 HTTP 200 + `result=失败` + `message`；SSRF 黑名单维持 400。
   - 数据库表型（新增，不再 501）：`endpoint` 须匹配 `^[A-Za-z0-9_]+\.[A-Za-z0-9_]+$`。逻辑库前缀经配置 `gkxlumen.maintain.probe.schema-alias`（默认 `dwd→demo_gkxlumenx_dwd`、`ads→demo_gkxlumenx_ads`、`ods→demo_gkxlumenx_ods`）翻成实际库名，再查 `information_schema`：表在 → `COUNT(*)`（5s 超时，超时退 `TABLE_ROWS` 估算），取 `updated_at|update_time|gmt_modified|created_at|create_time` 首个存在的列的 `MAX` 作为最新数据时间；表不在 → `失败：表不存在`。只读，参数化，库名不在白名单就拒绝。
   - 用户填报型：维持 400 无探测语义。
   - 每次探测结果都写回该行，响应体与契约一致，另加 `rowCount / dataUpdatedAt`。
5. 写接口鉴权（display 两个 maintain 控制器）：`POST` 写接口与 probe 由 `gkxlumen.maintain.write-require-login`（默认 `true`；`application-local.yml` 置 `false` 便于本地联调，另起一次 `true` 验 401）控制，未登录返回 HTTP 401 `{code:40101, msg:"未登录或登录已失效，维护操作需登录后进行", data:null}`。GET 读接口不变。

## 3. 拆分（4 路并行，本地改不提交）

| 路 | 仓 / 目录 | 内容 | 自检 |
|---|---|---|---|
| A 算法（PY） | `lumen-algo-py/vendor/entan-py/api/tech_graph_maintain_routes.py` + `scripts/mysql/`（DDL 追加 + 迁移脚本 `tech_graph_maintain_v2_member.sql`） | §2.1 全部 | `pytest vendor/entan-py/test_graph_maintain.py` 绿 + 新增用例 |
| B 接口（Java） | `lumen-svc-platform`：cms `TechMaintainService/Controller` + `db/` 迁移 SQL；display 两控制器 + Feign；topic 控制器 + client；display/cms/topic 的 local profile | §2.2 全部 + §2.1 的参数透传 | `mvn -pl gkxlumen-cms,gkxlumen-display,gkxlumen-topic -am test` 相关用例绿 |
| C 前端·图层 | `lumen-ui-science-pc`：`LayerSourcePanel.vue`、`FactorIdentityPanel.vue`、`api/situation/maintain.ts`、新 `stores/layerConfig.ts`、`views/situation/overview/**`（图例 / 停用 / 分组）、维护页 `index.vue` 只读模式 + 全局降级提示条 | 序 5–9 + 权限降级 | `pnpm type-check` + 自检 + build |
| D 前端·实体 | `lumen-ui-science-pc`：`EntityRelationPanel.vue`、`api/situation/maintain-ent.ts`、新 `components/EntityPanoramaGraph.vue` 等、mock 轨同步 | 序 41–47 | 同上 |

C / D 同仓不同文件：`types/maintain.ts` 只追加各自区段；`maintainModel.ts` 由 D 只改实体段；`index.vue` 归 C；只读开关 C 提供 `readonly` prop，D 消费。

## 4. 本地验证环境（隔离，不写共享库）

| 组件 | 端口 | 说明 |
|---|---|---|
| 本机 MySQL 8.4（brew） | 3306 | `gkxlumenx_cms`、`demo_gkxlumenx_dwd`、`demo_gkxlumenx_ads`。DDL 用仓内真源，数据来自 2026-11-11 线上**只读 GET 快照**（`/tmp/m10-full/snap`），种子脚本 `/tmp/m10-full/seed_local.py`；不连远端库，不需要远端口令 |
| entan-py API | 8000 | `/tmp/m10-full/venv`（py3.12），`ENTAN_MYSQL_HOST=127.0.0.1`，未配 `GKX_NEBULA_MAINTAIN_SPACE`（不写 Nebula） |
| topic | 7092 | local profile，`TOPIC_ALGO_BASE_URL=http://127.0.0.1:8000` |
| cms | 7098 | local profile，`MYSQL_HOST=127.0.0.1` |
| display | 7099 | local profile，`feign.cms.url` / `feign.techgraph.url` 直连 |
| FE dev | 3000 | vite proxy：`/api/display/v1/situation/maintain*` → 7099，其余 → 远端网关（全域态势读底图数据） |

## 5. 验收

### 5.1 本地 LOOP（产品实现规程 §6.5 的本地变体）

- 与 §6.5.3 的差异：打本地 display 7099，不是线上网关；本地鉴权关（`write-require-login=false`），所以不需要 token 文件；另起一轮 `true` 验证 401。线上 LOOP 留到部署后，由监管人放 token 再跑。
- 对照物：重写后的《合规演示用例》里每行「按界面值填好的请求 → 期望输出」；库侧只读核对本机库。
- 判定、缺口分类、报告格式照 §6.5.4 / §6.5.5。报告写到 `agent-handoffs/科技发展态势-TS/TS-M10-DEMO-ACCEPT-LOOP.md` 的「运行 2026-11-11（本地）」。

### 5.2 人工确认

LOOP 全过后交监管人在 `localhost:3000/trend/tech-situation-maintain` 走查主路径。确认后再按仓提交（前端遵守 fe-manual-confirm-push）→ CI 部署 → 共享库执行 §5.3 → 线上 LOOP。

### 5.3 部署时共享库变更（只在人工确认后执行）

1. `gkxlumenx_cms`：`db/9x_gkxlumenx_cms_tech_maintain_config_v2.sql`（加列 + 图层挂组种子 + 残留清理）。
2. `demo_gkxlumenx_ads`：`scripts/mysql/tech_graph_maintain_v2_member.sql`（建成员表 + 从人工边回填）。
3. 技术点 3 名称和重要性恢复：通过页面的编辑功能执行（会走变更集，留审计），不直接改库。
