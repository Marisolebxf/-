# POL-L2-DS12-SIM-242-ASYNC · E 波次 · 用例 / 冒烟

- 总单：`POL-L2-DS12-SIM-242-ASYNC-L01`
- 日期：2026-11-13
- 身份：qa-agent
- 依据：D 三切片（algo `bf0a440` + Java `3fbbd267` + FE 本地 `2243b99` 待推）+ A/B/C 已齐
- 未改 FE / Java / algo

## 用例改了哪些句

| 文件 | 位置 | 改动 |
|---|---|---|
| `合规演示用例/POL-L2-DS12-SIM-合规演示用例.md` | 文头日期 | 增补「2026-11-13 242 ASYNC 补 `policy_sim_interpret` 真算路径」 |
| 同上 | 覆盖表 242 · 触发 | 无行→「生成解读报告」走 `evaluation/jobs` `policy_sim_interpret`（可 force）；有行进签只读 `simulation/jobs`；「重新生成」须 force；下载仍 situation/report（COVER） |
| 同上 | 覆盖表 242 · 接口/请求 | 对齐 237/238：`evaluation/jobs` → `simulation/jobs`；导出轨不变 |
| 同上 | 覆盖表 242 · 期望输出 | **保留**四段字段期望 + COVER 形态期望；**补真算期望（ASYNC）**：Job 键、LLM/密钥依赖、无密钥 `generated=0` 不造假 |
| 同上 | 主路径第 6 步 | 同步无行 create / 有行直读 / force 重算 / 密钥诚实 / COVER 导出 |

## 与 D 对齐

| D 落点 | E 用例是否钉住 |
|---|---|
| `sub_type=policy_sim_interpret`（evaluation/jobs） | ✅ |
| 有行进签直读 `simulation/jobs` kind=解读报告 | ✅ |
| 「重新生成」须 `force=true` | ✅ |
| 无密钥 `generated=0` 不造假行 | ✅ |
| 下载仍 `situation/report/generate`（COVER） | ✅ 形态期望保留 |
| FE 本地 `2243b99` 待推 | 记入总单 note；冒烟须 FE 已部署或本机带该 commit |

对标：同文件 237（`policy_text_parse_run`）/ 238（`policy_sim_focus`）真算路径写法。

## 建议冒烟（§6.5）

1. 展示 PC 进「政策效果推演 · 科技政策推演」，政策编号 `18363390`，解读报告签。
2. **无行**：点「生成解读报告」→ Network 见 `POST .../evaluation/jobs`，body 含 `sub_type=policy_sim_interpret`；进度「正在生成解读报告…」；成功后读面四段非空（有密钥）或诚实空/既有行（无密钥不造假）。
3. **有行**：换政策再进签 → 只打 `simulation/jobs` kind=解读报告，**不**自动 create。
4. 点「重新生成」→ 须带 `force=true`（可再验 evaluation/jobs）。
5. 见「章节自定义」；导出 Word/PDF 各一次 → `POST .../situation/report/generate`，`reportType=policy-interpret-report`；PDF 真字节、Word 同源 `.doc`。
6. 无行/无勾选时导出不产文件。

前置：FE `2243b99` 已合入运行面（本机或推送后 CI）；algo/Java 白名单已含 `policy_sim_interpret`；真算绿需 LLM 密钥。

## 总单下一状态

| 项 | 结论 |
|---|---|
| E 用例 | ✅ 已改；真算路径 + COVER 下载 + 密钥诚实已钉 |
| AV-0 → `integration` | **暂不改状态**：尚无总单 handoff + cost；evidence 可指本 E 简报 |
| 建议 | 保持 `in_progress`；note「D三切片齐；FE本地2243b99待推；E用例已改」。FE 推送 + 冒烟绿 + 总 handoff/cost 后走 AV-0。**勿**改 `done` |
