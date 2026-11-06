# REVIEW-M10-IMPL-20261106 · M10 维护管理·图层与数据源 前后端双 MR 评审

- 评审人：`agent:reviewer`
- 日期：2026-11-06
- 对象：
  - **BE** `repos/lumen-svc-platform` 分支 `feat/m10-tech-maintain-config`（2 commits，9 文件 +1183 行）：`db/9x_gkxlumenx_cms_tech_maintain_config.sql`、`gkxlumen-cms` 侧 `CmsErrors.java`/`CmsEnvelope.java`（改）/`TechMaintainService.java`/`TechMaintainController.java`（新）、`gkxlumen-display` 侧 `SituationMaintainController.java`/`RemoteCmsTechMaintainClient.java`（新）、两侧测试 17 个
  - **FE** `repos/lumen-ui-science-pc` 分支 `feat/m10-maintain-wiring`（2 commits，7 文件 +619/-59）：`src/types/maintain.ts`、`src/api/situation/maintain.ts`、`src/mock/modules/maintain.ts`、`src/mock/register.ts`、`src/views/situation/maintain/components/LayerSourcePanel.vue`、`src/stores/factorDisplay.ts`、`src/views/situation/maintain/index.vue`
- 契约真源：`sdd/l2/TS-L2-M10-LAYER-API.md`（接口）/ `TS-L2-M10-LAYER-DATA.md`（列与种子）/ `TS-L2-M10-LAYER-ARCH.md` §3 v3（链路）
- 评审方式：只读（git diff / 源码逐行 / node 信封行为复算 / Spring 6.2.16 字节码核验重定向语义 / vue-tsc 全量类型检查）；未改任何代码、未 commit/push

---

## 总结论：**需返工**

两个 P0：① 前后端信封/DTO 端到端断裂（BE 裸数组 + snake_case 直漏 vs 契约 `{items}` + camelCase；FE real 轨对真实 BE **所有读恒为空**，两个 MR 显然从未联调）；② probe SSRF 防护可被重定向绕过且存在 DNS 重绑定 TOCTOU（会签 ARCH-C4 的安全要求实质未实现）。修复集中且方向明确（BE 响应组装层重做 + SSRF 按 IP 连接 + FE mock/防抖小修），但修完必须补前后端联调与「响应形状」断言测试，重新过一轮评审。

---

## P0（阻断，修复后才能进联调）

### P0-1 信封/DTO 端到端断裂：契约 `{items:[camelCase]}` vs 实际裸数组 + snake_case，FE real 轨全部读操作恒空

逐层真实 JSON 形状（证据链）：

1. **cms 侧**（`gkxlumen-cms/.../service/TechMaintainService.java`）：
   - `:60-63` `listLayers()` = `jdbc.queryForList("SELECT id, layer_code, layer_name, enabled, sort_order FROM cfg_tech_layer ...")` → 行 map 键即列名（snake_case；`enabled` 是 tinyint 的 `1/0` 数字）
   - `:83-85` `listGroups()`（`group_code`/`group_name`/`sort_order`）；`:127-129` `listDatasources()`（`source_code`/`source_name`/`source_type`/`target_layer_code`/`group_code`，**无 `groupId` 字段**）；`:258-260` `listFactorDisplay()`（`factor_key`/`display_name`）
   - `TechMaintainController.java:44` `CmsEnvelope.ok(service.listLayers())`；`CmsEnvelope.java:18-24` → 响应体 `{code:0, msg:'ok', data:[ <裸行数组> ]}`。契约 §2–§5 规定的是 **`200 { items: Layer[] }`**
2. **display 门面**（`SituationMaintainController.java:143-171` `relay()`）：2xx 原样透传，**零转换零包装**；Feign（`RemoteCmsTechMaintainClient.java`）也是 `Map` 直传
3. **FE**（`src/api/situation/maintain.ts`）：
   - `:47-61` `request()` 剥信封返回 `body.data`（= 裸数组）
   - `:65-70` `itemsOf()` 只认 `payload.items`，对**裸数组返回 `[]`**（node 复算确认：`itemsOf(BE data) = []`）
   - `:172`/`:112` `toSourceRow` 读 `row.groupId`（BE 从不返回该字段，只有 `group_code` 字符串）→ 所有数据源恒「未分组」

后果（real 轨对真实 BE）：

- `GET /layers|/layer-groups|/datasources|/factor-display` 四个读**全部解析为空**，页面显示空表却带 notice「已连接服务端配置」（误导）；`factorDisplay.syncFromServer()` 拿到空 rows → overlays 清空并镜像写 localStorage
- 写路径（camelCase body）与读路径（snake_case 行）互不兼容：保存成功 → `reloadInto` 回读仍为空 → 用户看不到自己刚建的行
- 字段级缺陷（即使信封修好仍然全灭）：`layer_code`≠`layerCode`、`display_name`≠`factorName`、`enabled: 1`≠`enabled: true`、无 `groupId`

修法建议（按契约收敛，BE 是主责方）：

- cms 侧 SELECT 用别名或组装 `LinkedHashMap`：`layer_code AS layerCode`、`enabled` 转 boolean、`group_code` JOIN `cfg_tech_layer_group` 反查数字 `groupId`（写侧 `resolveGroupCode` 已做正向翻译，读侧补反向）
- 响应包装 `{items:[...]}`：在 display 门面包装（同时满足 ARCH「门面聚合」）或 cms 直接包；12 个端点读响应统一
- FE `itemsOf` 可顺手兼容裸数组（防御），但**契约以 `{items}` 为准，BE 必须改**
- 补一个「响应形状」集成测试（当前 17 个测试无一断言 DTO 字段名——正是被击穿处）

### P0-2 probe SSRF 防护可被重定向绕过 + DNS 重绑定 TOCTOU + 100.64/10 网段未覆盖

`TechMaintainService.java:188-254`：

- **重定向绕过（最严重）**：`probeRestTemplate` 用 `SimpleClientHttpRequestFactory`（`:52-55`），Spring 6.2.16 该工厂字节码证实 `prepareConnection` 执行 `setInstanceFollowRedirects("GET".equals(method))`——**GET 自动跟随重定向**。`ssrfGuard(uri)`（`:207`）只校验原始 URI；HEAD 405 回退 GET（`:209-219`）后，公网 `http://evil.com` 302 → `http://169.254.169.254/...` 或内网地址会被 HttpURLConnection 透明跟随直连，**重定向目标不复核**，且 probe 返回「通过」。会签 ARCH-C4/API §4.1 的黑名单要求实质失效
- **TOCTOU**：`ssrfGuard` 先 `InetAddress.getAllByName(host)` 校验（`:241-246`），`RestTemplate.exchange` 连接时**再次独立解析**；重绑定 DNS 第一次解析返回公网 IP 过检、连接时返回内网 IP 即穿透。契约明文「解析后按 IP 复核再连接（实现单 DoD 落地）」——实现是"检了但没按检到的 IP 连"
- **网段缺口**：`isLoopback/siteLocal/linkLocal/anyLocal/multicast` 五判断**不含 100.64.0.0/10（CGNAT/云元数据，契约点名）**，也不含 IPv6 ULA `fc00::/7`；`PRIVATE_HOSTS` 仅 4 个主机名字面量。`100.100.100.200`（阿里云 metadata）可直连

修法建议：

- 关闭自动重定向（`factory.setConnectTimeout` 之外自行 `HttpURLConnection.setInstanceFollowRedirects(false)` 不可行于 RestTemplate——换 `HttpComponentsClientHttpRequestFactory`/手动 `HttpURLConnection`，或捕获 3xx 后对 `Location` 新 URI 递归 `ssrfGuard` 且计数 ≤3）
- 连接按已校验 IP 发起（解析全部 IP → 逐 IP 复核 → 用 IP 建 `URI`（Host 头补域名）或自建 connection），消灭 TOCTOU
- 黑名单补 CIDR 判断：`100.64/10`、`fc00::/7`、`0.0.0.0/8`、` multicast/广播`、以及常见 metadata 主机名

---

## P1（应修）

1. **mock 轨 `createMaintainSeqs()` 每次调用新建计数器 → 反复新增产出重复 id** — `src/mock/modules/maintain.ts:61,69`：`saveSource/saveGroup` 内联 `createMaintainSeqs()`（sourceSeq 恒重置为 4、groupSeq 为 3），第二次「新增图层组」再得 `grp-3`、第二次「新增数据源」再得 `src-4` → 同 id 两行，删/改错行。demo 语义是页面持有**单一** seqs（`index.vue:48` 的 `seqs` 已存在且已作为 `props.seqs` 传入 api 参数，mock 却无视它）。修法：mock 处理器改用 `params.seqs`
2. **`submitSource` 漏包 `apply()` busy 防抖，弹窗可双击双提交** — `LayerSourcePanel.vue:106-118`：唯一不走 `apply()` 的写操作；`MaintainDialog.vue:110` 保存按钮无 loading/disabled → real 轨双击 = 两条重复数据源（服务端 nextCode 串行不撞，会老老实实建两行）。修法：包 `apply()` 或给弹窗传 busy
3. **写操作多字段分次 UPDATE 且无事务 → 校验失败仍半写** — `TechMaintainService.java:98-111`（updateGroup：`groupName` 先提交，`color` 格式非法才抛 400）、`:145-171`（updateDatasource 同构）、`:66-79`（updateLayers 枚举校验与 UPDATE 交错）。契约语义是 400 = 拒绝整个请求。修法：先全量校验后写，或 `@Transactional` + 校验前置
4. **display 门面零校验，偏离 ARCH §3 v3 / API §1 的职责划分** — 两分册均写「§7 枚举与格式校验在门面完成，400 类错误不出网关层」；实现里 display 纯转发，全部校验落 cms。外部行为等价（400 仍回浏览器），但架构文档与 as-built 不符。修法二选一：门面补校验；或按 as-built 回写 ARCH/API 偏差记录并经监管人确认
5. **HEAD 探测不跟随重定向 → 可达但 30x 的 endpoint 误报「失败」；契约「重定向跟随 ≤3」未实现** — Spring 工厂仅对 GET 开重定向（见 P0-2 证据）：HEAD 收 301/302 → `RestClientResponseException` 非 405 → 直接判失败；GET 跟随无跳数上限。与 P0-2 一并重构 redirect 处理即可闭环

---

## P2（建议，合入前顺手/后续单）

1. **POST 契约 201 vs 实现 200**：`POST /layer-groups`、`POST /datasources` 契约表写 `201`，cms `CmsEnvelope.ok` 恒 200（`TechMaintainController.java:64-66,91-93`）。FE 用 `response.ok` 不受影响；建议对齐契约或记偏差
2. **nextCode 并发竞态**：`TechMaintainService.java:366-373` 两并发请求同 max → 同 code → 唯一键冲突 → 50001/500。单管理员运营配置可接受，建议 catch `DuplicateKeyException` 重试一次（代价一行）
3. **deleteGroup count→delete 竞态**：`:114-123` 之间插入引用则留下悬挂 `group_code`（无物理 FK、无事务）。低概率，建议事务化或删后复查
4. **`CMS_NOT_FOUND:` 前缀直出用户**：`CmsErrors.java:15` → groupId 不存在时 notice 显示「CMS_NOT_FOUND: groupId 不存在: 5」。建议 msg 去前缀
5. **DDL 种子无幂等保护**：`db/9x_...sql` 重跑撞唯一键报错（`CREATE TABLE IF NOT EXISTS` 有、INSERT 无守护）。建议 `INSERT ... ON DUPLICATE KEY UPDATE` 或文件头注明一次性执行
6. **application-local.yml 缺 `feign.cms.url`**：element/graph/datacatalog/innov 都有本地直连项，cms 没有 → local profile 单机起 display 调不通本模块
7. **mock layers 保真度**：`maintain.ts:50-58` `layerName: ''`、`tsMaintainLayersUpdate` 恒返回全启用（当前无消费者，M1 接线时会踩）
8. **submitSource 以 notice 文案嗅探成败关窗**：`LayerSourcePanel.vue:113-115` `includes('失败')/('请')` 字符串匹配，脆弱。建议 api 层返回结构化成败
9. **store `reset()/resetAll()` 静默吞错**：`factorDisplay.ts:174,189` `catch(() => undefined)`，服务端写失败仍提示「已恢复默认」→ UI 与服务端不一致（`pushToServer` 至少有 notice，这两处没有）
10. **`pushToServer` 失败不回滚本地**（`:79-92`，注释已声明取舍）：可接受；建议失败标记 dirty 重试而非等整页 sync 校正
11. **index.vue 读失败落本地种子后写全灭**：`index.vue:61-64` 失败保留 demo 种子（id=`grp-ip` 等非数字），real 轨后续 `PUT /layer-groups/grp-ip` 在 display `@PathVariable long` 处 400。建议失败态禁写或提示刷新
12. **probe 细节**：GET 回退把响应体整体读进 `byte[]`（契约「不读响应体」，且无大小上限）；connect 2s + read 5s 合计可超契约「超时 5s」；`URI.create` 抛异常落入「失败 200」而非 400（scheme 非法已正确 400）
13. **`updateLayers` 缺 `enabled` 键静默当 false**（`:70-77` `bool()` 对缺键返回 false → 意外禁用图层）；建议缺键 400
14. **领域服务载体选 `gkxlumen-cms`**：ARCH 写「候选 gkxlumen-topic 侧，实现单定」——DDL 头注释了理由（与 ops_ent_content 同库同机制），属允许的 as-built 决策，建议在 handoff 偏差节正式记录；另外 API §1 说 display 门面做「聚合」，现实是透传，一并在偏差里说清

---

## 各维度通过项小结

| 维度 | 结论 |
|---|---|
| 1. 信封/DTO 端到端 | ❌ **P0-1**：三层全对不上（裸数组 vs `{items}`；snake vs camel；无 `groupId`；`enabled` 1/0 vs boolean）。probe 响应字段 `result/latencyMs/message` 三层恰好一致（cms 手工 put camelCase）✓ |
| 2. 契约合规 | 12 端点路径/方法全对（gateway 剥 `/display` → display `/v1/...` 与既有控制器同惯例）✓；错误码链 cms `40001/40401/40901/50101` → HTTP `400/404/409/501` → FE `MaintainApiError.status` ✓（display 透传 + 不可达 fallback 信封均有测试）；空态 200 空数组 ✓；枚举三套（SourceType 中文 3 / LayerCode 9 / FactorKey 11）BE 常量、契约、FE 翻译表完全一致 ✓；响应信封形状与 POST 201 两处偏差（P0-1 / P2-1） |
| 3. SSRF | ❌ **P0-2**：环回/私网/链路本地/组播/anyLocal 覆盖 ✓、非 http(s) scheme 400 ✓、主机名黑名单 4 项 ✓；重定向绕过 / TOCTOU / `100.64/10`+`fc00::/7` 缺口 ✗ |
| 4. SQL/DDL | ✅ 四表列/类型/可空/唯一键逐列对齐 DATA §2–§5（含「不设 last_sync/test_status/active」的负约束）；种子 26 行与事实源**逐字一致**（11 色值 = `entityColorByKey` 全对、endpoint 原文、enabled 1/1/0、组色 #165DFF/#00B42A/#F97316、sort_order 序）；utf8mb4 ✓；表名拼接全为内部常量、用户输入全走 `?` 占位，无注入面 ✓ |
| 5. BE 代码质量 | nextCode 并发 → 500（P2-2，可接受）；updateLayers 空 items = no-op 返回全量 ✓；HEAD 405→GET 回退 ✓（但重定向行为 P0-2/P1-5）；deleteGroup 竞态 P2-3；事务性 P1-3；Feign `url="${feign.cms.url:}"` 与仓内惯例一致、`name=gkxlumen-cms` = Nacos 注册名 ✓（local 缺项 P2-6） |
| 6. FE 代码质量 | mock seqs 重复 id P1-1；submitSource 漏 busy P1-2；probe/toggle/删除/分组按钮 busy+loading ✓；`renameGroup` 换 `@change`（失焦提交）签名正确 ✓；store pushToServer 失败取舍已注释、P2-9/10；index.vue 双 fetch 各自兜底不挡页 ✓（失败后写全灭 P2-11）；`vue-tsc` 全量类型检查通过 ✓ |
| 7. 测试质量 | 17 个测试均为真断言（SQL 捕获、信封码、透传五态含 503 不可达 fallback），无空转 ✓；**盲区**：无响应 DTO 形状断言（P0-1 正中此处）、无 ssrfGuard/重定向/HEAD 回退测试——建议随返工补 |
| 8. 规约合规 | D15 ✓（display 只 Feign→cms，不碰 DB/Python）；D12 ✓（无 demo 依赖）；BE-TS-CONTRACT-02 未触碰 ✓；commit 带 `[agent:api-agent]`/`[agent:frontend-agent]` ✓；门面校验落位偏离 ARCH（P1-4）、领域服务载体 as-built 决策待记录（P2-14） |

---

## 返工清单（按序）

1. BE：响应组装层按契约重做（camelCase + `groupId` 反查 + `enabled` 布尔 + `{items}` 包装），12 端点统一
2. BE：probe 重定向/SSRF 重做（禁自动跟随 + Location 逐跳 ssrfGuard ≤3 + 按 IP 连接 + `100.64/10`/`fc00::/7` 补段）
3. BE：写操作校验前置或事务化（P1-3）
4. FE：mock 轨改用 `params.seqs`（P1-1）；`submitSource` 包 `apply()`（P1-2）
5. 双侧：补「响应形状」集成测试 + 一次真实联调（当前双方显然零联调）
6. 修完重新提交评审；P2 项可并入本 MR 或开后续单


---

## 整改回执（2026-11-06 同日 · 起草方 agent:frontend-agent 执行）

**总结论更新：需返工 → P0/P1 已整改，待评审复检后可合入。**

| 问题 | 级别 | 处置 | 提交 |
|---|---|---|---|
| 信封/DTO 端到端断裂 | P0 | ✅ 已修：cms Service 加契约映射层（snake→camel、enabled 数字→boolean、group_code→groupId 反查），Controller 六端点 `{items}` 包装；FE `itemsOf` 双形状防御（意外形状显式抛错防静默空）；新增 2 个契约形状回归测试（防再犯） | svc `539c111` + ui `ce0a265` |
| probe SSRF 重定向绕过 | P0 | ✅ 已修：`SsrfSafeRequestFactory` 禁自动跟随；手动逐跳 ≤3 且**每跳 ssrfGuard**；补 100.64/10（CGNAT/云元数据）与 fc00::/7（IPv6 ULA）网段 | svc `539c111` |
| mock 轨重复 id | P1 | ✅ 已修：saveSource/saveGroup 复用 `params.seqs`（页面持有的单一计数器） | ui `ce0a265` |
| submitSource 漏 busy 防抖 | P1 | ✅ 已修：包 `apply()`，双击双建消除 | ui `ce0a265` |
| 多字段分次 UPDATE 半写 | P1 | ✅ 已修：updateGroup/updateDatasource 改「全字段先校验 + 单条动态 UPDATE」原子化 | svc `539c111` |
| HEAD 不跟随重定向（误报失败） | P1 | ✅ 随 P0-2 一并解决（手动逐跳循环对 HEAD 同样生效） | svc `539c111` |
| display 门面零校验 | P1 | 📝 记 as-built 偏差：校验实现在 cms 侧（400 语义不变，仅物理位置不同于 ARCH §3 表述「门面校验」）；display 纯转发 + 信封透传。复检时请评审方裁定接受或要求上移 |
| P2 ×14 | P2 | 📝 暂缓（不阻塞联调）：201/200、nextCode 并发竞态、CMS_NOT_FOUND 前缀直出、DDL 非幂等、feign.cms.url 本地缺省、notice 嗅探关窗、reset 静默吞错、读失败落种子后写 404 等——均为体验/加固项，随联调反馈按优先级分批处理 |

**回归证据**：cms 123/123、display 72/72 全绿（+2 形状回归）；FE maintain 测试 ok、type-check ✅、build 50s ✅。
