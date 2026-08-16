# ENT · seeds（样本 / fixture 索引）

> 服务 **Demo 全链路 Mock**：少量覆盖样例，**非**性能全量，**非**第二套 DDL。  
> 主管道：[`../etl/pipeline-demo-mock.md`](../etl/pipeline-demo-mock.md)  
> ODS 口径：权威 `doc/` xlsx；**优先读** `doc/md-extract/`（见 `sources/inventory.md`）  
> S2：`DATA-ENT-STORAGE-S2-L01` · OPEN-ENT-FLOW-07 **关闭（矩阵骨架）**

## 样本策略

| 原则 | 说明 |
|---|---|
| 模型灌 ODS | **已落仓**：`demo-algo-ent-analysis/scripts/run_llm_ods.py`（`--offline` 默认；可选 `--llm`）；无权限用 `--sql-out` |
| 少而全覆盖 | 场景 × 数据特点最小集 |
| 先闭环后性能 | 全链路优先 |

## 覆盖矩阵（OPEN-ENT-FLOW-07）

| 场景 | 数据特点（须覆盖） | ODS/DWD 要点 | 脚本/入口 | 备注 |
|---|---|---|---|---|
| 企业检索列表 | 存续/注销；上市/非上市；有无产业链标签 | `dwd_org_base_info`→`enterprise_base`；tags | `run_llm_ods.py --offline`（base 含存续/注销/上市） | ES 同步见 lumen-etl-es-py |
| 企业详情-基本+扩展 | 有经营范围/地址；港澳台各 ≥1 | base + product + special_* | 同上（含港/台/澳各 1 org） | special_* 表后续扩展 |
| 财务趋势 | ≥2 年年报；上市财务指标 | annual_financial / stock_finance | 同上（年报 2023/2024） | stock_* 可选 LLM 扩 |
| 高管/资讯 | 多高管；至少 1 条新闻 | executive / important_news | 同上 | |
| 招投标 | 中标/采购角色各 ≥1 | dwd_bid_*_out | 待扩展 / `--llm` | CSV 在其他要素库 |
| 产业链位置 | 八大产业之一；含 ALL 去重语义所需样本 | industry_tags + **上链** INB 节点 | `run_ent_chain_hang.py`（消费已有 `industry_chain_node`） | 过程见 CHAIN `pipeline-ent-hang.md` |
| 风险洞察 | abnormal/punish/judicial 等至少 3 类 | 风险承诺子集 | 待扩展 | 汇总表 risk_summary |
| 报告/导出对象 | 1 个 PDF/HTML 样例对象 | MinIO `demo-**` + 任务元数据 | 编排写桶（待） | 不替代业务表 |
| 图谱 | 供应链或投资边 ≥1 | Nebula demo space | 算法灌图（待对齐 demo_*） | 过渡 space=`entan` |
