# TOPIC-POL-SZ3D-DEMO-FIX-R20261108-ALGO · 深圳政策截面SQL原生过滤（方案A）

- ponytail: full（最小 diff，只改一条 SQL + 一条断言测试）
- 强度：ponytail full；监管人：human:孔东；业务拍板：human:淮政玮 2026-11-08（方案A：读取侧收窄）

## 背景与决策

`demo_gkxlumenx_dwd.policy_base_info` 的 `city='深圳市'` 已被其他演示批次混灌到 1458 行：

| 批次 | 行数 | 来源 |
|---|---:|---|
| 原生 domestic（`etl_batch_id IS NULL`） | 879 | 基线（市级 757 / 区级 96 / 园区级 26，均值 0.4653） |
| `debug_one_map_20261107_v1`（`source_plane='debug'`） | 540 | 一张图调试 `SYSINT-04-01-DATA-EMP-L01` |
| `SYNTH-%`（`source='llm-synth'`） | 49 | 图2 政策演示 `POL-L2-DS10-SRCMON-SYNTH-L01` |

数据侧删除或标记 `is_deleted` 都会打断在跑的演示（多会话保护铁律）。`human:淮政玮` 在三个方案中拍板**方案 A：读取侧收窄**——结果板 SQL 只认原生行。

## 范围与实现

- `vendor/entan-py/polan/shenzhen_board.py`：`CITY_SECTION_SQL` 追加 `AND COALESCE(source_plane,'')='domestic' AND etl_batch_id IS NULL`。
- `_GRANT_AMOUNT_SQL` **不过滤**：金额按 `policy_id` 挂到已过滤的截面行上（`_attach_grant_amounts`），非原生行的金额挂不上，附表无需改。
- `tests/test_policy_shenzhen_board.py`：新增 `test_native_filter_in_section_sql` 断言原生口径关键字。
- demo 仓 `demo-algo-ent-analysis` **无副本**（rg 全仓确认 `shenzhen_board`/`CITY_SECTION_SQL` 只在 lumen-algo-py），无需同步。

## 自检证据

- `pytest tests/test_policy_shenzhen_board.py` → **14 passed**（1.73s）
- `pytest tests/test_policy_job.py` → **37 passed**（5.95s）
- 现有断言（`"amount" not in CITY_SECTION_SQL and "bid" not in CITY_SECTION_SQL`）不受影响。

## CI/CD

- 分支：`lumen-algo-py` `origin/dev`，commit `4df6ab5`（`5750342..4df6ab5`），push 触发自动发布。
- 编排仓 LOOP 计划 §1/§3 库核对口径同步修订，commit `c91a42840` → push `ad9414501`。
- 未改 Java、前端、数据。

## 架构合规

| 铁律 | 结果 |
|---|---|
| D1 调用链（FE→Java→Python /internal） | ✅ 未动调用链 |
| 算法只在 Python | ✅ 只改 Python 仓 |
| D9 血缘 / ⓘ | ✅ 结果卡不变，metric_id 不变 |
| demo→lumen 隔离（D12） | ✅ 只在 lumen 仓修改 |
| 多会话保护 | ✅ 未删任何数据行，demo 工作区其他 M 文件未触碰 |

## 验收口径（部署生效后）

重算任务后支持力度卡应为：`policy_count=879`、`level_mean=0.4653`、`score` 与 `rank` 以全表城市截面重算为准（原基线 33.5585/第 5，若其他城市行有回填漂移则以当轮 API 为准并在 LOOP 计划记录）。
