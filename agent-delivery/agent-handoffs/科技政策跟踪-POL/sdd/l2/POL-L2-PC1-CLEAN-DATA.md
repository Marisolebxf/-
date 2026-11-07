# POL-L2-PC1-CLEAN-DATA · 政策数据治理 · 系统引用政策源数据清洗 · 后台数据架构设计

- 任务：`POL-L2-PC1-CLEAN-DATA`
- 日期：2026-11-08
- 监管：`human:淮政玮`
- 认领：`agent:data-agent`
- 强度：ponytail off
- 上游：`POL-L2-PC1-CLEAN-ARCH.md`、总控 §1.2
- SRS：**602**

## 1. 读哪些表（只读，零建表）

| 库 | 表 | 用途 |
|---|---|---|
| `gkxlumenx_dwd` | `policy_base_info` | 页眉件数基础；政策候选 id/标题可由此或全景目录出 |
| `gkxlumenx_dwd` | `script_state` | 清洗/加工校验状态；质量聚合与明细唯一真源 |
| `gkxlumenx_ads` | `policy_text_parse` / `policy_industry_rel` | 同资源 603 概览用；本叶不单独建读路径 |

**本叶零建表、零灌数、不重开 GDF。** 不写 `gkxlumenx_gapfill`。

## 2. 跨项只消费

第 6 项贴源与 C1/C2 已落库结果。展示不写回 ODS/DWD/ADS。不写 nGQL。不写第二套统计脚本。D4 保持 mock。

## 3. 与政策选择

602 库级看板不强制 `policyId`。若 API 暴露过滤，DATA 侧即对 `script_state` 按政策主键拣行，不另造映射表。

## 4. 明确不做

不加字段、不改主键、不把 demo 数组当库。结构歧义升级 `human:淮政玮`。
