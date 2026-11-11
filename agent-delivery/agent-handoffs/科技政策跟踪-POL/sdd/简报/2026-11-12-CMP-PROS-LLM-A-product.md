# POL-L2-DS10-CMP-PROS-LLM · A 波次 · product

- 总单：`POL-L2-DS10-CMP-PROS-LLM-L01`
- 日期：2026-11-12
- 身份：product（本会话代写）
- 裁定：监管人锁定方案 A（开始对比后空优缺点起 LLM；界面用政策名称）
- 档位：中档（不退定义规程）

## 1. 功能点 · 界面必见

| 功能点 | 界面必见 | 空态 / 失败 |
|---|---|---|
| 214-6 优缺点 LLM | 点「开始对比」后：若所选政策优缺点皆空，自动起 Job 生成并回读；每策见「优点 / 缺点」条目 | 无密钥 / 失败 / 仍空 → 该策「暂无优缺点说明」；不造假文；已有非空不覆盖 |
| 214 政策名称 | 对比表列头、差异柱图图例、差异分析总结标题均为政策名称 | 候选未命中时用 detail 正文标题；仍无 →「—」；**禁止**「政策 #id」 |

不扩 213/215–218；不改六维勾选与力度 Job 语义。

## 2. 状态清单

| 状态 | 表现 |
|---|---|
| 未选够 / 未点开始 | 空态引导；不自动起 Job |
| 读详情中 | loading；不清已返回块 |
| 优缺点生成中 | 二次 loading（业务文案「正在分析优缺点」）；禁「演示/gapfill」 |
| 有优缺点 | 每策优点绿 Tag + 列表、缺点红 Tag + 列表 |
| 生成失败 / 无密钥 | Alert 或空态一句；保留已读正文与条件材料 |
| 名称 | 全程政策名或「—」 |

## 3. 影响清单

| 层 | 影响 |
|---|---|
| 说明书 / 四单 | ARCH §5.2、API §4.x、DATA §4：增 `policy_detail_pros_cons` |
| gapfill | 仍用 `gapfill_policy_detail_compare`；LLM 写 `pros_text`/`cons_text`，`fill_method=llm-synth` |
| Python | `polan.job` 新子类型 + LLM 写表 |
| display / async | JOB 白名单增 `policy_detail_pros_cons` |
| FE | `ComparisonModal` + `compareLive` |
| 合规用例 | 补空优缺点路径 + 名称形态期望 |

## 4. 回写要点（交 C）

- 空才 LLM；非空只读。
- 展示名禁止编号回退。
