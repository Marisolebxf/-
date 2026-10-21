# QA-KJZTFWSFK-CASE-FUNC-R3-L01 · 算法库第三轮用例改写为 FUNC 并作废 API 册

> **状态**：用例册已落盘，待签收  
> **执行**：agent:qa-agent  
> **监管**：human:黄敬洲  
> **日期**：2026-10-21  
> **认领**：claim_type `pull`，supervised_by `human:黄敬洲`

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:黄敬洲` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 用例文档交付，不改业务代码 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶只归集已写好的用例册，未挂载压缩 |

## 范围与实现

算法库 `SDWJSF/KJZTFWSFK` 第三轮用例：89 个 catalog 页改为 `FUNC-*-用例.md`，编号从 `FUNC-00001` 起。`API-00001`～`02210` 作废，页内 `API-*-用例.md` 删除。`code-registry.yaml` 的 `next_seq.FUNC` 回写到 1501（收官至 01500）。工作区 FUNC 合表与 `delivery/SDWJSF-KJZTFWSFK/6.国际科技信息中心项目_科技专题服务算法库_测试用例.xlsx` 随册提交。

编写规则见 `qa/algo-lib-api-case-playbook.md`「长任务返工」。环境 `https://edu.itic-sci.com/dma/algovwz/`。

页名变更：`ENTANATTRACT-招引企业综合推荐` 的 API 册已删，现行册在 `ENTANATTRACT-企业招引潜力评估`。

## 偏离

- 不合 A 线，与 playbook 第三轮一致。
- 交付 Excel 仍是客户模板 17 列投影，不是脚本执行结果。

## 产物清单

- `agent-delivery/qa/test-cases/SDWJSF-KJZTFWSFK/`：89 本 FUNC 册、coverage、`run-log.md`
- `agent-delivery/qa/code-registry.yaml`
- `agent-delivery/qa/algo-lib-api-case-playbook.md`、`algo-lib-playbook-index.md`
- `agent-delivery/qa/as-built/catalog/SDWJSF-KJZTFWSFK.yaml`
- `agent-delivery/qa/delivery/SDWJSF-KJZTFWSFK/6.国际科技信息中心项目_科技专题服务算法库_测试用例.xlsx`
- `agent-delivery/scripts/_gen_sdwjsf_delivery_func.py`、`_rewrite_sdwjsf_func_text_r3.py`

## 验收证据

- 工作区 FUNC 册 89、API 用例册 0。
- 提交信息：`docs(qa): 算法库第三轮用例改为 FUNC [agent:qa-agent]`
- 分支：`dev`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 调用链 / 算法只在 Python / 图谱 / 可观测 | ✅ 本叶不改业务代码 |
| demo 不 merge 进 lumen / D12 | ✅ 只提交编排仓用例 |
| D8 / D9 / D10 | ✅ 不涉及界面与指标展示 |
| D14 对象存储 | ✅ 不涉及 |

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 未单独计量 |
| model_used | 未单独计量 |
| actual_cost | 未单独计量 |
| cost_warn | green |

## 遗留

- 专题用例册、专题环境手册、本机 `.cursor/hooks` 不在本任务。
- 签收前不改 `API` 号段。
