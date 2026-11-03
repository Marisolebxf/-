# 22 — round1 回包签收与答复

> **日期**：2026-10-30  
> **任务**：`GDF-POLICY-ROUND1-REPLY-L01`（WBS-06-03M）  
> **回包**：`工程过程/04-系统集成/06-GDF数据治理集成/对接文档/GDF侧提交/政策/GDF-POLICY-WORKPACK-v2/round1/`  
> **读者**：GDF。本章是对首次派单回包的签收和答复。不是 Wave A/B 执行结果，也不是产线已跑通。

2026-10-30 已确认四条建议。现行包 `scripts/` 是回包两份再加上补偿软删。`12`、`15`、`10` 和表设计已按确认改过。本轮要执行的语句在 `sql/update_round1.sql`，本仓没有在库上跑。本章第 1 节的函数对照，是签收当时相对派单脚本的记录。

## 1. 签收

回包四件都在：`交付说明.md`、`scripts/policy_c1_industry.py`、`scripts/policy_c2_clauses.py`、`sql/script_state.sql`。

交付说明里的两个指纹，按 LF 换行计算，与落盘文件一致：

| 文件 | LF SHA-256 |
|---|---|
| `policy_c1_industry.py` | `cdc9a4d5a176d3664648b8f8820c1df9b2e7277e32a228044f9f0e243afcf8b4` |
| `policy_c2_clauses.py` | `2e9b5de0771af61a4219177f14073ab310036990df91c84b08159bc64271033c` |

本机检出若是 CRLF，整文件哈希会不同。以 LF 为准。`script_state.sql` 交付说明没有给指纹。

和现行包同名脚本按函数对照：

| 脚本 | 与现行包逐字节相同 | 有差异 | 对方新增 |
|---|---|---|---|
| C1 | 切块、检索、聚合、`plan_rel`、`write_slot`、`embed_query`、`milvus_search` | `load_rows`、`run`、`main`、`self_check` | 状态表、内容指纹、环境检查、`process_one` |
| C2 | 切条、分类、要素抬升、模型接受、`content_hash`、`save` | `structure_one`、`load_rows`、`run`、`main`、`self_check` | 状态表、状态跳过、环境检查 |

不确认「五个核心业务函数全部逐字节一致」这句笼统说法。C1 的切块、打分、写槽没变。C2 的切条、分类、要素、模型接受没变。`structure_one` 变了：现行包是「已有条款且未 `--force` 就跳过」；回包改成「已有条款且内容指纹相同，或旧数据没有指纹，才跳过」。这是交付说明问题 2 已经写明的改动。

交付说明第九节的代理机实测（`10.50.238.250`，自称 `policy_base_info` 40,000 行，退出码和单条出数）只记为对方自述。本叶没有复跑，没有查行数，不把它写成产线已跑通，也不代替 WBS-06-03。

## 2. 对他们指出的四个问题

对照现行包脚本，这四条属实：

1. 检索失败、没有过线、没有切块时不写 `policy_industry_rel`。增量又只看目标表里有没有非空链码。这类行会留在队头。`run` 最后仍 `return 0`。
2. C2 已计算 `content_hash` 并写入 `clause_meta`，但跳过时只看有没有条款，不比较指纹。
3. `EMBED_BASE_URL` 为空时 `embed_query` 返回空，不写行，进程仍以 0 结束。
4. `--force` 可以不带 `--policy-id`。

这四条说明回包想改运行层的理由成立。2026-10-30 已确认用回包替换 `scripts/`，并在 C1 上加了补偿软删。见第 4 节。

## 3. 有问必答

环境变量里如果现在写的是字面「（留空）」，改成空字符串，不要把这四个字当成地址。下面的地址来自现网部署记录，本答复没有再连这些服务。`LLM_API_KEY` 用本节给出的测试密钥。

| # | 问题 | 答复 |
|---|---|---|
| 1 | `EMBED_BASE_URL` | 网络是通的。代理机填 `http://10.50.69.111:30903`。2026-11-02 devops 另开 `gkxlumen-embed-tei-nodeport`，对应容器端口 8080。不要填集群内短名 `gkxlumen-embed-tei:8080`。脚本会自己补 `/v1/embeddings`。 |
| 2 | `EMBED_API_KEY` | 不设。当前 TEI 没有 token。留空字符串，脚本不送 `Authorization`。不要写字面「（留空）」。 |
| 3 | `MILVUS_URI` | `http://10.50.69.111:19530`。现网 Milvus 2.5.4 standalone。正式批用数据库 `gkxlumen`，demo 用 `default`。不要用设计稿里已作废的 `192.168.88.48:19530`，也不要用 `.env.example` 里的 `10.50.75.136:19530`。 |
| 4 | `MILVUS_TOKEN` | 不设。现网 `authorizationEnabled=false`。留空字符串，脚本不加令牌。 |
| 5 | `LLM_BASE_URL` | `https://open.bigmodel.cn/api/paas/v4`。不要自己再加 `/chat/completions`，脚本会补。没有这个地址也不阻断 C2 的规则切条。 |
| 6 | `LLM_API_KEY` | 现在用测试密钥 `2d4129c2df4740f79cb3f0cba3edcd2a.2i5TTfMfeKO7mcCA`，键名 `LLM_API_KEY`。这是测试密钥，不是生产 Secret。无密钥时不写假条款。模型用 `glm-5.3-flash`，与脚本默认一致，不必另设 `LLM_MODEL`。 |
| 7 | `EMBED_MODEL` | `BAAI/bge-base-zh-v1.5`。与 `lumen-algo-py` 现网和脚本默认一致，向量长度 768。不必另设。不要改成别的模型。 |
| 8 | `MILVUS_COLLECTION_PREFIX` | 正式批默认 `gkxlumen_industry_`，集合名 `gkxlumen_industry_anchor`。与产业链包 `12` 写入的集合同名。正式批的库是 `gkxlumen`（`MILVUS_DB_NAME`），不是 demo 的 `default`。 |
| 9 | 集合全名 | `gkxlumen_industry_anchor`，数据库 `gkxlumen`。 |
| 10 | `metric_type` | 设计已定 `COSINE`，且写明不改。脚本把 `distance` 当越大越相似，与余弦一致。不是 L2。 |
| 11 | 维度 | 768。与 `EMBED_MODEL` 默认模型一致。 |
| 12 | 锚点是否已有数据 | 锚点是产业链维度的处理流程建的，不是政策这条产线建的。要等产业链维度的产线完成后才产生。生产环境上线时，必须先做「产业链入向量库」，之后才有锚点。库 `gkxlumen` 的集合 `gkxlumen_industry_anchor` 已建并 load，当前 0 条。没有锚点时 C1 对不上链码。COSINE，768 维。 |
| 13 | 锚点谁灌的、何时验收 | 「产业链入向量库」这一步负责灌。时机是产业链产线完成之后、政策 C1 要出链码之前。政策重灌做完不会产生锚点。 |
| 14 | 能否安装 `python3-pip` 和 `pymysql` | 可以。代理机 `10.50.238.250` 完全给 GDF 独立使用，GDF 自行安装。脚本依赖 Python 3.9+ 和 `pymysql`。临时 `PYTHONPATH` 不算正式运行。 |
| 15 | `/opt/policy/scripts` 能否创建 | 本包不规定这个路径，不创建，也不授权写入工作区外的目录。节点上的目录由 GDF 自定。 |
| 16 | 正式环境 `script_state` 谁建 | GDF 执行本包 `sql/update_round1.sql`。建表在这一份里，不要再单独跑 `script_state.sql`，不要 `DROP`。本侧不代跑。缺表时脚本退出码 4，不要在作业里建表。 |
| 17 | 数据库口令 | 不重复提供。不进本包，不进 handoff，不进对话。 |
| 18 | 三张目标表要不要改结构 | 要改的只有索引，不改列类型。语句在 `sql/update_round1.sql`。见第 25 条和第 4 节。 |
| 19 | embedding / Milvus 服务端要不要改 | 不要。只要地址、鉴权和上面已写明的模型、余弦、768 维。 |
| 20 | 锚点集合要不要重建 | 不要。设计写明不重建、不改 `METRIC_TYPE=COSINE`。 |
| 21 | Milvus 距离度量必须是 IP 或 COSINE | 采用设计里的 `COSINE`。不是 L2。IP 不作为本包口径。 |
| 22 | 向量维度与灌库模型一致 | 是。默认模型 `BAAI/bge-base-zh-v1.5`，768 维。 |
| 23 | `kind` 只能是 `chain` 或 `segment` | 是。现行 `milvus_search` 已丢掉其他值。 |
| 24 | `policy_support` 全是字面 `'null'` | 源上就没有结构化要素。不是洗入时弄丢的。`09` 仍是「JSON 原样」，不改、不回刷。字面 `'null'` 不能走要素抬升，C2 只能切条或走模型。这是预期。 |
| 25 | 给关联表和解析表加唯一键 | 按回包建议加。清重口径已定，语句在 `sql/update_round1.sql`。关联表 DWD 与 ADS：键 `(policy_id, industry_link_code)`，空串也算；同一键留 `is_deleted=0`，同状态留 `update_time` 最新，时间相同留 `id` 最大，其余物理删除。ADS `policy_text_parse`：完整 `policy_id` 相同的重复行留最新；全文不同、仅前 64 字相同的不删，加索引会停住。类型仍是 `longtext`。主表只加普通索引 `idx_pid`，不删行，不改 `(source_plane, policy_id)`。DWD `policy_text_parse` 本轮不改。本侧不代跑。 |
| 26 | 源侧 `is_deleted` / `is_history` 之后，目标行怎么办 | Wave A/B 取数仍不过滤这两列。C1 每趟开始前：关联仍有效、但主表没有当前行的 `policy_id`，软删关联并同步 ADS。源行同时还有当前行时不动。C2 不删条款，只在 `script_state`（`job=c2`）把备注写成「源行已非当前，条款保留」。 |
| 27 | 以后你们升级脚本，运行层怎么合并 | 现行包 `scripts/` 已是回包加上补偿软删。以后只把业务函数的差异贴回来，保留状态表、退出码和补偿。贴完跑 `--self-check`。 |

`policy_id` 与 `script_state.policy_id` 比较时，排序规则必须同为 `utf8mb4_0900_ai_ci`。设计已按此写。产线尚未建这张表。

## 4. 建议：2026-10-30 已确认

四条都已写入设计。清重口径已定，本轮改表语句在 `sql/update_round1.sql`。本仓不代跑。不改 `09`，不改 `01-data-flow.md`。

| # | 建议 | 已写入 |
|---|---|---|
| A | 用 round1 两份脚本替换现行包 `scripts/` | `scripts/`、`12`、`15`。退出码 7 是未追平，不记失败 |
| B | `script_state` 收进建表设计 | `10/script_state-MySQL.md`、`dwd.md`。未执行 |
| C | 唯一键与主表 `policy_id` 普通索引 | 口径已定。可执行语句在 `sql/update_round1.sql` |
| D | C1 补偿软删；C2 保留条款并备注 | `scripts/` 与 `12`。`--self-check` 已覆盖名单判定 |

代理机用 `http://10.50.69.111:<嵌入服务 NodePort>` 访问嵌入服务，NodePort 数字不在本包。锚点要等产业链产线完成并做完「产业链入向量库」才有。`policy_support` 源上就没有。清重口径见第 25 条。`LLM_API_KEY` 现用测试密钥，见第 6 条。
