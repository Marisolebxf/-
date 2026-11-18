# KG-GRAPH-POLICY-05 · 政策线收口与空态裁定交接

日期：2026-11-18 更新。交付状态：integration；徐滕强已确认数据裁定，等待 API-04 接入及后续接口/页面联调，非 done，未代签验收。

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | agent:data-agent |
| supervised_by | human:徐滕强 |
| claim_type | pull |
| claimed_at | 2026-11-17 19:37:44 +08:00 |
| lock_until | 2026-11-17 23:37:44 +08:00 |
| 任务负责人 | 陈芸飞 |
| 开工依据 | 用户明确要求“认领并开始”；MCP ready→claimed→in_progress；无依赖/阻塞 |
| ponytail | N/A：数据只读核查与文档；未删减 M 编号 |
| headroom | skip：完整精读 T06/T07 及签收更正，不压缩替代证据核验 |
| diagram_id | N/A：未修改架构、存储或流图契约 |

## 问题与交付

任务要求确认政策边是否可补，并给 M12–M14 和空态关系明确处置。已完成政策四类边源侧核查、图中精确计数、16 条逐项表、原因码对照和源图对账。

- [政策线与空态裁定（送审）](../工程过程/04-系统集成/07-图数据库集成/派单-20261113-图谱100/KG-GRAPH-POLICY-05-政策线与空态裁定.md)
- [源图对账（非补数记录）](../工程过程/04-系统集成/07-图数据库集成/派单-20261113-图谱100/KG-GRAPH-POLICY-05-源图对账.md)
- [只读执行器及原始证据](../工程过程/04-系统集成/07-图数据库集成/派单-20261113-图谱100/KG-GRAPH-POLICY-05/)

## 结论

- policy 20,000 点；政策四类边实测 0。M12/M13/M14/M16 均建议 C / MISSING_STABLE_ID；M16 存在 pedigree 名称文本，因此不误写“缺物理列”。
- M11 建议 C / MISSING_SOURCE_FIELD；regulate 政策侧建议 C / MISSING_STABLE_ID，保持非 M 身份。
- 16 行全部按 Tag+端点复测为 0；14 条 C，M19/M20 按已有裁定归 D，不重复建边，分别由 M02/M01 承载。其余新增原因码是接口映射建议，待李周对齐契约。
- 未补数，写入/删除均 0。ADS cite=401，其中 mock 398 + seed 3，不能直接转入合规图库；3 对 seed 中 1 对缺目标点，其余也无真实引用证据。
- 明确 M12 企业 / M13 人才 / M14 科研机构，纠正旧派单端点描述；apply_to 历史 10,957 不冒充必须关系。
- 2026-11-18 徐滕强会签：M12/M13/M14/M16 本期 C 档，缺稳定 ID 返回 501 / `MISSING_STABLE_ID`，补齐 ID 后重开补边；M19/M20 不重灌、分别由 M01/M02 承载。已同意将 16 条原因码表交 API-04 接入；页面尚待联调。

## 验证

- 7 组只读查询清单与原始结果，含 schema、COUNT(*)、JSON 全量结构、批次、VID FETCH、16 条关系精确计数。
- MySQL 只读事务和语句时限；图查询均有 Tag 或固定 VID，不运行全图无锚定聚合。会话关闭，未写数据库。
- 原始失败：分组别名 tags 的 SyntaxError；改 endpoint_tags 后成功，错误保留可审计。
- 附交付自检 `validation.json`：16 编号闭集、结果零计数、链接、凭据排查、证据 SHA256、脚本语法。
- API 501 / 页面文案未在本任务实现或联调，未伪记“联调通过”。

## 遗留风险与接收方

1. **徐滕强/原快照执行人**：旧 ADS 计数目前仅能追到 11-17 补建卡 note；仓库无独立旧快照文档或原 SQL。请协助核对当时的环境和 SQL；本轮可比对语句及证据在源图对账 §0 和 `02-schema-count-*`。
2. **李周（API-04）**：按已确认裁定接入 M12/M13/M14/M16 的 501 / `MISSING_STABLE_ID` 与稳定 ID 重开条件；16 条逐编号原因码见裁定主文 §5。M19/M20 显示替代关系，不把关系能力缺失返回 200+0。
4. DWD 有 3,469 行 source=demo-mock；节点数量不代表真实政策数量；本轮不清理存量。
5. SHOW STATS 与有效端点计数差 7，暂不归因，不影响本次关系定义与零计数。
6. 未来源补齐后先做至多 1,000 条 dry-run，经徐滕强确认后写 batch=kg100-policy-01。本轮无可直接入图候选，不请求空泛补数授权。

## CI/CD

- 仓/分支：gkx-orchestration / dev。
- commit：以本文件同批提交为准，可用 `git log --oneline --all --grep=KG-GRAPH-POLICY-05` 定位。
- pipeline：本轮未运行部署 CI；文档与离线审计执行器交付，无应用部署。
- namespace / 镜像 / rollout：N/A。
- 实测命令：`uv run --with pymysql --with nebula3-python python readonly_probe.py <queries.json> <results.json>`，连接凭据通过环境变量注入；查询结果已归档。
- 后续：保留 integration。等 API-04 接入以及页面联调证据补齐后再走相应验收；不自动推进 pending_test / done。
