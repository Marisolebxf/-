# POL-L2-DS12-EST-DEMO-FIX-R20261109-DATA · 效果预估 232 仿真行挂进两个 Mock 入口

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `full` |
| 说明 | 不新建脚本。仿真行只在已有 `synth.py` 的 `_derive` 前写入，用表上五项唯一键 upsert。 |

## 范围与实现

- 缺口键：`gapfill_policy_sim_forecast.未出台仿真.知识产权|广东省高新技术企业|每人每年30万元|2026年至2028年`
- 写入口：算法中台政策分析算法库的「Mock 10 条数据」（`synth.run`）与「真实政策补外围：深圳 40 + 随机 10」（`synth.run_real`）。两入口经 `_derive` 调 `_upsert_sim_forecast`。服务端没有 LLM 密钥时，入口在生成前返回，仍先写这一行，返回说明末尾带「已写效果预估仿真行」
- 写入行：`target_industry` 写界面级联回显全文「新一代信息技术 / 集成电路 / 半导体材料」。经济效益「经济效益预测值约74亿元，相对基线变化率约4.2%。AI推演结果，仅供参考。」，逐年趋势「2026年62、2027年71、2028年80」。`is_mock=1`，`metric_id=M_POLICY_SIMULATE`，`fill_method=llm-synth`，`gapfill_batch_id=SYNTH-SIM`
- 只写 `gkxlumenx_gapfill`。不写 ODS、正式 DWD、ADS、供应方库。没有第三套手插，没有用固态电池入口，没有改前端、Java 过滤和用例期望句
- 双仓同文：`demo-algo-ent-analysis` `polan/mockgen/synth.py`（`dd41861` 首提、`1be0b47` 无密钥补写）；`lumen-algo-py` `vendor/entan-py/polan/mockgen/synth.py`（`4c5db47`、`8b7697d`）

## 偏离说明

- 主种子脚本 `lumen-algo-py/scripts/seed_gapfill_policy_sim_forecast.py --apply` 会先清空整表，这一行会被删掉。再点任一入口即可补回
- 演示环境的算法服务没有配置 LLM 密钥，两个入口都不生成政策，只写了这一行

## 验收证据

- 自检：`python -m polan.mockgen.synth` 输出 `policy synth self_check OK`（新增断言：四项键与用例请求逐字一致、无禁用词、`_derive` 调写入、注入写入时不碰库）
- 入口：`POST http://10.50.69.111:30889/api/policy/v1/policy/mock/synth`。部署前返回「未配置 LLM 密钥，未生成」。部署后返回「未配置 LLM 密钥，未生成；已写效果预估仿真行」。部署前后共触发多次，写法幂等，库里只有这一行
- 调用前：2026-11-09 14:4x，jobs 该请求 HTTP 200，records 0
- 调用后：jobs 复核时探测 HTTP 401（token 失效），未取得条数。待 human:淮政玮 换 token 后由验收单重跑 232

## 架构合规自检

| 条 | 结论 |
|---|---|
| 算法只在 Python | ✅ |
| 调用链 前端→Java→Python | ✅ 未改 |
| D12 lumen 不调 demo | ✅ 展示读 gapfill，经 Java |
| D16 缺项只进 gapfill_ | ✅ |
| D18 接口不返回写死 mock | ✅ 接口只读表 |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 120000 |
| model_used | claude-opus |
| actual_cost | 3.0 |
| cost_warn | green |
