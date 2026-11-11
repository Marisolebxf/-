# POL-L2-DS12-SIM-242-COVER-FDE · B 波次 · arch

- 总单：`POL-L2-DS12-SIM-242-COVER-FDE-L01`
- 日期：2026-11-12
- 身份：arch
- 输入：A 波 `2026-11-12-SIM-242-COVER-FDE-A-product.md`；卡1=**B**（监管人 human:淮政玮）
- 对照：`POL-L2-DS10-CMP-ARCH` §5.5 / `POL-L2-DS10-CMP-API` §7（217）；`interpretExport.ts` + `policyReportExport.ts`；`SituationReportServiceImpl`（`reportType` 自由字符串、无白名单）

## 1. 定档

**中档**（成立）：复用已有态势报告链；不退定义规程；不新表；不扩 237–241；不接核增 `report/jobs`；**默认不改 Java**；D4 仍 mock。

## 2. 废止句（与卡1=B 冲突，C 波必须删/改）

下列句子**整句废止**（不得保留「导出服务存在前」前提）：

| 位置 | 废止原文（摘） |
|---|---|
| ARCH §4 流程步5 | 「页面呈现正文，不做文件生成；『自定义报告内容和格式』在导出服务存在前不实现，不灌假配置」 |
| ARCH §5.5 | 「『下载』在导出服务存在前不实现，不灌假 PDF / Word；『自定义报告内容和格式』不灌假配置」 |
| API §8 | 「下载在导出服务存在前不实现。自定义报告内容和格式不灌假配置」 |
| API §10 / 空态表 242 行（冲突部分） | 「不产生 PDF，不产生 Word」若被读成「本叶永不导出」则废止该读法；**保留**「jobs 响应不内嵌文件 / 不灌假文件进 gapfill」 |
| 说明书 §242 / 差表 | 「章节自定义和导出格式没有列，接口不返回文件」中「导出不实现 / 无导出」表述 |

**仍成立（勿误删）**：

- jobs 解读报告仍**只读段落、不返文件**；不写对象存储业务新目录；前端不直连 RustFS
- 不灌假 PDF/Word 进 `gapfill_policy_sim_result`；不接 `report/jobs` / `gapfill_policy_report_body`
- 「自定义内容」≠ 持久化配置表：= 页内章节勾选（不灌假配置列）——废止的是「因此不做下载/格式」，不是「因此不做勾选」

## 3. 技术钉死

| 项 | 裁定 |
|---|---|
| 读面 | 仍 `POST /display/v1/policy/simulation/jobs`，种类=解读报告；同步读 `gapfill_policy_sim_result` 解读段落行；**不返文件** |
| 下载 | **另轨**：`POST /display/v1/situation/report/generate`（及同族 download），对标 217 |
| `reportType` | 固定字符串 `policy-interpret-report`（FE `interpretExport.ts` 已用） |
| 后端注册 | `SituationReportServiceImpl`：`reportType` 为自由字符串、**无白名单** → **本波不改 Java**；跑通失败再最小排查（非默认范围） |
| 内容 | FE 用当次勾选段的 `section_name` + `body_text` 拼完整 HTML；标题=政策名或「推演解读报告」 |
| PDF | `format=pdf` → topic-async **OpenHTMLtoPDF** → 真 `.pdf` 字节；禁 text/plain、禁打印另存 |
| Word | **与 217 同构**：请求 `format=html`，下载后以 **`.doc`（HTML Word）** 落盘；域服务闭集仅 `html\|pdf`，不新开 docx 引擎（见 `policyReportExport.ts` `downloadHtmlAsWord`） |
| 复用 | 同 `reportType` + `conditionKey` + `format` 可复用已有成功产物（态势既有行为） |
| 空态 | 无行 / 无勾选章节 → 不发 generate、不产空文件 |
| 明确不做 | 不扩 237–241；不新表；不接核增研报；不改 FE（D 波）；不改合规用例正文（E 波） |

## 4. 要改的文件清单（C 会签改文稿；本 B 波只落简报）

| 文件 | C 波动作 | 本 B 是否改盘 |
|---|---|---|
| `sdd/l2/POL-L2-DS12-SIM-ARCH.md` §4 步5、§5.5 | 按 §5 替换 | 否（交 C） |
| `sdd/l2/POL-L2-DS12-SIM-API.md` §8、§9 表 242、§10 冲突句 | 按 §5 替换；钉「下载≠jobs」 | 否（交 C） |
| `sdd/科技政策跟踪-系统详细设计说明书.md` §242 + 差表 | 删「无导出」；写章节勾选 + Word/PDF + situation/report | 否（交 C） |
| Java / element SELECT / 新 display 资源 | **默认否** | — |
| FE `InterpretWorkbench.vue` live | D 波：格式+下载复用 `exportInterpretReport` | 否 |
| 合规用例 242 | E 波：废止「没有下载」；验真 PDF + 章节勾选 | 否 |
| gapfill | 不重灌 | — |

## 5. 给 C 会签的修订要点草稿（可直接贴）

### 5.1 ARCH §4 流程步5 · 整段替换为

> 5. 用户查看解读报告。前端提交 `jobs`（种类=解读报告）。element 读该政策的解读段落行：政策背景、主要内容、预期效果、实施建议。页面呈现正文即「查看」。用户可在页内勾选章节（内容自定义，不持久化配置、不灌假配置列），并选择 Word / PDF 下载。下载**不走** `simulation/jobs`，走已有 `POST /display/v1/situation/report/generate`（`reportType=policy-interpret-report`）→ topic-async OpenHTMLtoPDF；PDF=`format=pdf` 真字节；Word=`format=html` 同源 HTML 存为 `.doc`（与 217 同构）。无行或不勾选章节则不产文件。不接核增 `report/jobs`，不灌假 PDF/Word 进 gapfill。

### 5.2 ARCH §5.5 · 将「下载在导出服务存在前…」两条改为

> - 页面呈现正文即「查看」。**界面必见**：章节勾选（内容自定义）+ Word/PDF 格式选择 + 下载。下载走 `situation/report`（`reportType=policy-interpret-report`）→ OpenHTMLtoPDF；与 CMP 217 同构（PDF 真字节；Word=html→`.doc`）。jobs 仍只返段落、响应不内嵌文件。内容自定义=页内勾选，不灌假配置列、不持久化导出配置表。无行不产文件。禁 trackingExport 打印另存、禁 text/plain 冒充。

（「不做什么」段保留：不把 `report/jobs` / `gapfill_policy_report_body` 当成本叶；不把 226/224 复制成本叶段落。）

### 5.3 API §8 · 在「不产生 PDF…响应里不内嵌」之后替换下载两句为

> - **jobs 本资源**：不产生 PDF/Word 文件；响应不内嵌写死文件；不写对象存储；前端不直连 RustFS。
> - **下载（另轨，2026-11-12 卡1=B）**：浏览器走已有公开资源 `POST /display/v1/situation/report/generate`（`reportType=policy-interpret-report`），对齐 217 / 态势报告；PDF=`format=pdf`；Word=`format=html`→`.doc`。不新开 simulation 导出 URL，不走 `report/jobs`。自定义内容=章节勾选；自定义格式=Word/PDF（live 验收只认二者）。无解读段落行或不勾选则不发 generate。
> - ~~下载在导出服务存在前不实现。自定义报告内容和格式不灌假配置~~（废止）

### 5.4 API §9 表 242 行 · 空态列改为

> 没有解读段落行则报告区空。**jobs 不产生** PDF/Word、不写对象存储。下载另走 `situation/report`；无行不产文件。不返回 501。

### 5.5 API §10 · 「不产生 PDF，不产生 Word…242 不灌文件…」改为

> jobs 解读报告不产生、不内嵌 PDF/Word；不灌假文件进 gapfill；不灌自定义格式配置列。242 下载复用已有 `situation/report`（见 §8），不新建桶、前端不直连 RustFS。

### 5.6 说明书 §242 / 差表（要点）

- 242 live：生成 → 四段预览 + 章节勾选 + Word/PDF 下载
- 下载 = 态势 `situation/report`（`policy-interpret-report`），非 jobs 内嵌文件
- 差表「章节自定义和导出格式没有列 / 导出不实现」**作废** → 改为：章节勾选在页内；格式 Word/PDF；文件走态势报告链

## 6. B 波收口 + 下一跳

- 本简报即 B 产物；定档 **中**；Word **同构 217（`.doc`）**；**默认不改 Java**
- 下一跳：**C** 会签——按 §5 段落级替换回写 ARCH / API / 说明书差表；不改 FE、不改用例
- C 后：**D** FE live 接线；**E** 用例废止「没有下载」
