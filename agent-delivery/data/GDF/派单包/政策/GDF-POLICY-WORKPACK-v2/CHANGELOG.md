# CHANGELOG · GDF-POLICY-WORKPACK

## v2.0.4 · 2026-10-30

- 增加 `22`。签收 GDF round1 回包（指纹、函数差异），并逐条回答交付说明里的问题和建议。
- 建议 A–D 已确认并落入设计：`scripts/` 换为回包并加上补偿软删；`12`、`15` 写上状态表、退出码 7、`--force` 必须带 `--policy-id`；`script_state` 收进 `10` 与 `dwd.md`。产线未建表，未 ALTER。目标唯一键只写在设计旁注，清重口径仍待确认。
- `22` 与 `12` 补上现网参数：Milvus `http://10.50.69.111:19530`。代理机经 `10.50.69.111` 加嵌入服务的 NodePort 访问，不编端口数字。`LLM_API_KEY` 用测试密钥。锚点由产业链产线完成后的「产业链入向量库」产生。`policy_support` 字面 `'null'` 是源上就没有。清重口径仍待确认。代理机归 GDF 独立使用，可自行安装 `python3-pip` 和 `pymysql`。
- 产线要执行的 SQL 收进 `sql/`。目前只有 `script_state.sql`。唯一键不进可执行脚本。

## v2.0.3 · 2026-10-26

- 增加 `17` / `18` / `19` / `20`。MDC、Graph、MRC 分开写。口径未闭合的指标只列表，不建作业、不建表、不灌数。
- 第一批 STAT 的落表名写在 `17`。`scripts/mdc/` 本版不带，生成任务 `GDF-POLICY-MDC-STAT-L01`。未进包前 GDF 不要建 MDC 作业。
- 不复制 `metrics/repro/`。不改 `09`，不重开 MAP-01。C1 / C2 仍按 `12`。
- 同日补 `19` 文末与 `21-数据血缘.md`。实时指标的血缘导入工位后，由接口对外提供。任务 `GDF-POLICY-LINEAGE-L01`。接口未接通。

## v2.0.2 · 2026-10-26

- Wave C 改成 GDF 可配置的两份 Python：`scripts/policy_c1_industry.py`、`scripts/policy_c2_clauses.py`。`12` 写总流程、C1、C2 三张流程图和逐步说明。
- 不再把内部 HTTP 或 Java 任务接口写成 GDF 要配的入口。`15` 改为两张平面 B 都成功后在 GDF 节点上跑脚本。
- 不改 `09`，不重开 MAP-01。`16` 仍只核对字典。

## v2.0.1 · 2026-10-26

- 增 `16-Mapping过程与字典核对.md`。对照要素库值域与国内 20,000 行快照（2026-10-23）。
- 不改 `09` 字段矩阵，不重开 MAP-01。`rank` / `type` 仍按原文拷贝，核对文件里的实值不是白名单。

## v2.0 · 2026-10-26

相对当时工作区里的政策 v1.0.4。任务原文写「继承 v1.0.3」，同日用户已把 `is_deleted` / `is_history` 改成取数不过滤，v2 继承这一版，不把历史行过滤加回去。

- 新建本目录为现行施工包。v1 只留历史对照，09 字段矩阵不重开、UK 仍是 `(source_plane, policy_id)`。
- 补 `05` 验收回签、`13` 现网差集、`15` 触发与回执。对标企业 v4 的这三件，不抄企业的 ES / 图谱表。
- `12` 写明 C1 / C2 的读写、增量跳过、失败不写假结果、中台函数名，以及 GDF 只触发。
- 不补 `07` / `08` / `14`。不并进国内政策、国外政策另叶。不出 CDC 预填。

## v1.0.4 · 2026-10-26

- 取数无行过滤。`is_deleted`、`is_history` 都原样进 ODS，Wave B 直接映射到 `policy_base_info` 同名列。`is_history` 的 `NULL` 不改写成 `0`。
- DWD `policy_base_info` 增加 `is_history`（`10/policy_base_info-MySQL.md`）。
- 应用读 DWD 时自行加 `is_deleted = 0` 与 `IFNULL(is_history, 0) = 0`。见 `04`、`02`、`09` §1.3 / §3。

## v1.0.3 · 2026-10-23

- 生产规约：抽取产业、条款结构化必须提供 Python 脚本，逻辑与算法 demo 中台同一模块（`industry_enrich` / `industry_job`、`clause_job`）。禁止 CDC / SeaTunnel 另写。见 `12` 脚本规约。
- 目标库仍是 `gkxlumenx_dwd` / `gkxlumenx_ads`。本包不复制算法源码。

## v1.0.2 · 2026-10-23

- Wave B 成功后增加 Wave C：抽取产业、条款结构化（派单口语「条件结构化」）。说明见 `12`。  
- 抽取只写 `policy_industry_rel`（DWD 写完同步 ADS），不改 `policy_base_info`。  
- 条款只合并 ADS `policy_text_parse.structured_elements.clauses`，不 TRUNCATE、不写 ES。  
- 两作业不进 09 字段矩阵，也不进 CDC 预填。

## v1.0.1 · 2026-09-01

- `human:淮政玮` 拍板 **OPEN-POLICY-MAP-01 = 方案 A 永远分 UK**。禁止 `gbl:` 改 `policy_id`。

## v1.0 · 2026-09-01

- 首包：Wave A 贴源两张 `gkx` 政策表 → `gkxlumenx_ods`。  
- Wave B 洗入 **一张** `policy_base_info`（`source_plane` + `policy_id`）。  
- 不含 ES / ADS / Nebula。  
- 作废 `dwd_zck_*`、旧 v1 37 列贴源、Demo `ods_sync` 当产线。  
- Mapping 已冻结可投递；尚未执行建表或灌数。CDC 预填不在本版本。  
- 通用解析器尚未识别 `policy_base_info` 字段矩阵，自动预填前须补规则或按 09 人工配置。
