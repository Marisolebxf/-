# TOPIC-POL-SZ3D-DEMO-FIX-R20261107-TIER-DATA · 深圳政策现状抽取真实扶持金额

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人要求领取并执行。MCP `task-claim` 没有 `claim_type` 参数，该值写在任务 note 里。锁 4 小时。不改 `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-DATA`。 |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `full` |
| 说明 | 只建一张四列金额表，不接招标表，不造数。金额抽不到 30 条就不会建表。 |

## 图

不改调用链。结果板本轮不改。新表只在 `demo_gkxlumenx_dwd`。

## 扫描

直连 `10.50.11.76:3306`，用户 `gkxlumenx`。正式库 `gkxlumenx_dwd` 只读。两库 `policy_base_info` 都没有金额列。`policy_text_parse` 在 demo 库是 0 行。没有读 `dwd_bid_*`。

| 范围 | 行数 | 非空 |
|---|---|---|
| demo `policy_base_info` 全表 | 20008 | — |
| 正式库 `policy_base_info` 全表 | 40000 | — |
| 两库 `city='深圳市'` | 各 879 | 政策编号一一对应 |
| demo 深圳 `content` | 879 | 827 |
| demo 深圳 `abstract` | 879 | 502 |
| 正式库深圳 `content` / `abstract` | 879 | 879 / 879 |
| 正文含「万元」 | 879 | demo 与正式库各 130 |
| 正文含补贴/奖励/资助/补助 | 879 | 各 255 |

抽取规则：句子里的数字必须紧挨「给予 / 予以 / 资助 / 补贴 / 奖励 / 补助」或「最高 / 不超过」，单位只收万元、亿元。区间、支出门槛、「X万元以上/以下」丢弃。0 不写入。万元按 10000、亿元按 100000000 折成元，原文留在 `source_clause`。一条政策只留一笔：先具体资助，其次上限，再次批次总额。

| 结果 | 条数 |
|---|---|
| 深圳政策扫描 | 879 |
| 写入非空 amount | 59 |
| 其中具体资助/奖励/补贴/补助 | 33 |
| 上限 | 17 |
| 总额 | 9 |
| 句子窗口没保住数字而丢弃 | 3 |
| amount 为 0 或空条款 | 0 |

59 ≥ 30，深圳市可以进档位截面的金额来源。

## 写库

只写 `demo_gkxlumenx_dwd.policy_support_amount`。列：`policy_id`、`amount`、`caliber`、`source_clause`。59 行都能连回 demo 深圳政策。正式库没有这张表。未写 ODS、供应方库、正式库。

口径计数：奖励 18，资助 14，资助上限 10，资助总额 6，奖励总额 3，补助上限 3，奖励上限 2，补贴上限 2，补贴 1。

## 测试

写后复核：表 59 行，金额空或 0 为 0，条款空为 0，正式库深圳 `implementation_date` 仍是 879 行 NULL，正式库无 `policy_support_amount`。

## 遗留

- 具体资助、上限、批次总额混在同一张表，`caliber` 分开标。拿来做均值时要先看口径，不能把总额和单笔资助当成同一种数。
- 分档切点仍是 QPOL-02，本单不切档。
- 结果板还没读这张表。

## CI/CD

- 无业务仓代码提交，无流水线，无镜像。
- 数据落在 demo MySQL，不经 K8s。
- 注册表提交 `4dd593202`，推送到 `origin/dev` 的合并提交 `b8dde9489`。

## 架构合规

| 项 | 结果 |
|---|---|
| 不写 ODS / 正式 DWD / 供应方库 | 是 |
| 不用招标金额，不把空写成 0，不用模型编金额 | 是 |
| 算法仍不在 Java | 是 |
| 不把本单签成 done | 是 |
