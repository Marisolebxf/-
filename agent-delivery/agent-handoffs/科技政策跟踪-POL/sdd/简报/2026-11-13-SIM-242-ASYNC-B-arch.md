# POL-L2-DS12-SIM-242-ASYNC · B 波次 · arch

- 总单：`POL-L2-DS12-SIM-242-ASYNC-L01`
- 日期：2026-11-13
- 身份：arch-agent
- 方案真源：`2026-11-13-SIM-242-LLM-ASYNC-ARCH方案.md`
- A 简报：`2026-11-13-SIM-242-ASYNC-A-product.md`
- 锁卡：三卡 A；Job 键 `policy_sim_interpret`；表 gapfill `解读段落`；force 有行短路；≥1 段可落库；`is_mock` 暂 1；下载 COVER 保留
- 范围：只回写 ARCH/API（+ 说明书 ####242 一句）；**不改** FE / algo 代码

## 1. 改了哪些段

| 文件 | 段落 | 变更摘要 |
|---|---|---|
| `sdd/l2/POL-L2-DS12-SIM-ARCH.md` | §1 终态一句；§2 叶子表 238/242；§4 流程步 5；§5.2 禁扩句；**§5.5**；§6 白名单；§8 签收表 242 | §5.5 同构 §5.2：读面 + 真算 Job 写回；流程步补生成/重算；白名单加键 |
| `sdd/l2/POL-L2-DS12-SIM-API.md` | §1 公开资源 242；真推演例外；§2 内部委托 + 读面/async 口径；**§8 → 8.1/8.2**；§9 空态行；§10 禁项例外 | §8.2 镜像 §4.2；废止「242 不进 async」旧句 |
| `sdd/科技政策跟踪-系统详细设计说明书.md` | #### 242 | 轻补一句：真算走 `policy_sim_interpret` |

## 2. 键名 / 资源

| 面 | 资源 | 键 |
|---|---|---|
| 读（不变） | `POST …/simulation/jobs` | 种类=`解读报告` → `row_kind=解读段落` |
| 写（核增） | `POST …/evaluation/jobs` | `sub_type=policy_sim_interpret` |
| 下载（不变） | `POST …/situation/report/generate` | `reportType=policy-interpret-report` |

## 3. Upsert（已钉进 ARCH §5.5 / API §8.2）

- 表：`gkxlumenx_gapfill.gapfill_policy_sim_result`
- 仅当本轮 ≥1 段非空：`DELETE … WHERE policy_id=? AND row_kind='解读段落'` → `INSERT` 有效段
- 禁整表 TRUNCATE；禁误删重点/影响/路径
- 无密钥 / `generated=0`：**不** DELETE、不造假行
- `force`：有行未 force 可短路；重算必 `force=true`
- 元数据：`is_mock=1`、`fill_method=llm`、`gap_item=242 政策解读报告生成`

## 4. 禁项（文档已对齐）

- 不核增 `report/jobs` / `gapfill_policy_report_body`；不新建 ADS 解读表
- 不调用 `polan.text.parse.run`；浏览器不直连 Python
- 读面 jobs 不内嵌 PDF/Word；下载只保留 COVER 轨
- 不开完整 I2-12 工作区；不扩 239/241 真算
- 本波不改 FE / algo（留给 D）

## 5. B 收口 · 下一跳

- 本简报即 B 产物；ARCH/API 真算节已回写
- **下一跳 C**：说明书 / 四单轻会签（确认键名、upsert、禁项与 A 界面必见一致）
- 其后 D：algo `sim_interpret_job` → Java 白名单 → FE create/进度/force/读回
