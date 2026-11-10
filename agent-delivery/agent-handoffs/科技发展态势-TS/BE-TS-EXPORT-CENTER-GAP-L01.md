# BE-TS-EXPORT-CENTER-GAP-L01 · M1 §3.8 导出任务中心补建（184/195 报告导出后端承接）

> 执行：zcode 会话（2026-11-10 上午），菜单监管 human:王梓真 当面指令实施（原单注建议转李伟，改由王梓真监管）。
> 交付：`gkxlumen-display` 内实现 M1 §3.8 契约五端点，DS-09 的 184（方向预警报告）/195（竞争情报报告）导出自此有后端承接（此前 FE 已按契约实现客户端并对 404 诚实降级）。

## 1. 先查后建（DoD 第 1 条）

全仓核查：`lumen-svc-platform` 无任何 `export/jobs` 实现（仅 DS-09 注释引用本缺口）；`lumen_analysis_task`/`analysis_task` 属 topic-async-service 专有任务体系（跨服务 DB 耦合不采纳）；topic-policy 的导出走 MinIO 桶 + 自有任务流，形态不匹配 M1 §3.8 契约。**判定：查无，按契约新建。**

## 2. 实现清单（单 commit）

| 文件 | 职责 |
|---|---|
| `controller/SituationExportController.java` | M1 §3.8 五端点：GET /config（角色配置）、POST /jobs（建任务）、GET /jobs/{id}（轮询）、POST /jobs/{id}/cancel、GET /jobs/{id}/download（签名下载，免登录） |
| `service/ExportJobService.java` | 任务注册与编排：白名单（planning-direction-warning / planning-research-intelligence）400；184 同闸 501（复用 `PlanningDirectionAlertGate`）；同步确定性渲染（五阶段全 done，禁假进度不返百分比）；审计走结构化日志（替代 demo localStorage） |
| `service/ExportReportRenderer.java` | Word(.doc) 渲染：**demo `downloadHtmlAsWord` 同款 Word-HTML**（零新依赖，不引 POI）；195 正文全部来自 `ts_plan_research_report_template.template_text` 表行占位符替换（缺值落「—」不造数）；184 数据行来自 direction-warnings 块（六源均分现算） |
| `service/ExportSigner.java` | 下载短时签名 HMAC-SHA256（jobId\|userId\|exp）；URL 即凭证，过期 410、签名不符 400 |
| 测试 `ExportJobServiceTest` | 7 用例：195/184 主路径、白名单 400 ×3、184 未注册 501（195 不受闸）、用户隔离 403/404、cancel 409、签名真伪+有效期 |

## 3. 关键取舍（V1，已注记）

1. **任务存储 = 内存注册表 + 确定性重渲染**：报告产物由 ADS 表行确定性生成（同请求同产物），进程内持有元数据与字节；**不写任何库**（保持「display 不直连主库」红线）。代价：重启丢任务列表——FE 流为建任务→2s 轮询→30s 内下载，不受影响；持久化任务列表待 M0 拍板复用中心时升级。
2. **Word = Word-HTML**：demo 的「.doc」本就是 HTML 存 .doc（L1817），服务端同款（MIME application/msword），Word/WPS 均可打开。
3. **角色**：GkxlumenUser 只有 roleIds 无角色码——V1 缺省 analyst（max_rows 50）；统一用户中心角色映射待 M0（config 端点 javadoc 已标）。
4. **行数闸**：M1 的角色行数硬闸属 CSV 行导出语义；M9 报告为叙述型产物，row_count 入审计不硬闸（handoff 登记，待 M0 复核）。
5. **下载 URL 前缀**：`gkxlumen.display.export.url-prefix`（默认 `/tid/api/display`，FE 直挂 a.href 同源可达；换网关前缀时 Nacos 覆写）。`/v1/situation/**` 已在 ignore-urls 匿名放行 → 签名即鉴权。

## 4. 验收证据

- `mvn -pl gkxlumen-display -am test`：**BUILD SUCCESS**（新 8 用例全绿 + 既有 134+ 用例无回归）。
- 契约对齐：API-TS-M1 §3.8 五端点/禁假进度/用户隔离/审计落服务端；API-TS-M9 §1/§2.7 两通道白名单与 501 同闸；FE 客户端（`techDevelopmentPlanModel.ts` createPlanningExportJob/pollPlanningExportJob）零改动直通（file.url|download_url 双键兼容、status=success 触发下载）。

## 4a. 推送前 review 修复（2026-11-10，菜单监管人要求，六项）

1. **诚实性 bug**：渲染器曾用 `level_cards[0]`（等级 A 定义行）冒充靶标企业成绩——改为按靶标自身 `level_tag` 匹配等级卡，无等级三占位符落「—」（G-B4）。
2. **内存泄漏**：任务注册表无界增长——加 `max-jobs` 容量上限（默认 500，Nacos 可覆写）+ 插入序淘汰最旧（同实例防御 `map.remove(key, value)`），新增淘汰用例。
3. **防御性转换**：POST body 的 `content_keys`/`filter` 先 instanceof 校验再强转（防 ClassCastException → 500）。
4. **常量时间比较**：HMAC 签名校验改 `MessageDigest.isEqual`（防时序侧信道）。
5. **时区一致性**：exp 计算与下载端过期比较统一 `OffsetDateTime.now().getOffset()`（容器可能 UTC，原硬编码 +8 会错 8 小时）。
6. **清洁**：删未用 helper；benchmark 分数取整。

## 5. 遗留与后续

1. 部署后真机验收（登录态建任务→轮询→浏览器下载 .doc）——归 `TS-L2-DS09-TEST-L01` 复测 184/195 导出链路（其验收矩阵当时按 404 降级通过，需复测）。
2. 下载 URL 前缀与 `sign-secret`：prod 必须 Nacos 覆写（dev 默认值已注记）。
3. `subscriptionPushJob` 调度缺失（XXL-Job admin 任务表全空）仍未配置——推送链路端到端的最后一环，见 `TS-L2-DS09-BATCH4-OPS-L01.md` §5。
4. 跨菜单复用：M1 的 factor/event CSV 导出、POL 报告导出可复用本中心——扩展 content_keys 白名单 + 新渲染器即可（本单 DoD「跨菜单登记」以 WBS-05-22 行注记承载）。
