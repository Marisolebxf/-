# 派单说明 · BE-TS-DATA-01

- **任务号**：`BE-TS-DATA-01`
- **名称**：科技发展态势 M2–M9 ADS 数据对接
- **监管 / 认领**：`human:李伟`（2026-10-27 认领；此前无监管人）
- **状态**：`backlog`
- **仓**：数据侧 / `lumen-etl-es-py`（写数方）
- **归属叶**：第 5 项 `WBS-05-14`（公共底座 · 数据对接）
- **派单日期**：2026-10-27

---

## 1. 派单目标

把 M2–M9 的数据按 `BE-TS-AGG-01` 的口径与 `API-TS-M1` §9.1 五域建议落到 ADS，使展示接口读到真实数据。**Python 写数，Java 只读。**

## 2. 输入真源

| 输入 | 位置 |
|---|---|
| 聚合口径与落表清单 | `TS-聚合方案-产业铺底.md` §3（矩阵）、§4（表清单） |
| 契约侧数据需求 | `API-TS-M1.md` §9.1（五域）、`API-TS-M2`～`M9`（各页数据需求） |
| 骨架复用表（企业 / 服务机构） | 聚合方案 §4.1：`enterprise_industry_summary` / `enterprise_region_summary` / `svc_metric_*` 等 |
| 事件 / 舆情三方源 | `DATA-TS-S01`（规划 §5），D3 三方库导入 |

## 3. 交付产物

| 产物 | 说明 |
|---|---|
| 五张 M1 新增标准表 DDL + 数据 | `ts_factor_stat`（要素）、`ts_object`（载体/对象）、`ts_object_metric`（指标）、`ts_event`（事件）、`ts_opinion`（舆情） |
| 骨架表实线化 | 企业 / 服务机构域由 Demo 库迁入正式 `gkxlumenx_ads`（当前 `status=draft`） |
| Mock 数据 | 按标准表由 Python 写入，供联调 |
| metric_id 登记 | 对齐 `/metrics/v1/catalog`（D9） |
| 批次发布记录 | 供 Java 只读「已发布批次」 |

## 4. 工作分解

| # | 步骤 | 现状 |
|---|---|---|
| 1 | 出五张标准表 DDL（字段见聚合方案 §4.2） | ⏳ |
| 2 | 骨架复用表接入：企业 `enterprise_*`、服务机构 `svc_*` | ⚠️ 现跑 Demo 库，需实线化（P7） |
| 3 | 要素源对接：11 类要素逐类落源（其中 10 行源未落人） | ⏳ 阻塞 |
| 4 | 事件 / 舆情三方源映射（D3） | ⏳ 随 `DATA-TS-S01` |
| 5 | Mock 先写（Python 按标准表），供批 1 联调 | ⏳ |
| 6 | 按批发布，Java 侧只读已发布批次 | ⏳ |

## 5. 技术约束（铁律）

- **写数归 Python（D7）；Java 只读已发布 ADS 批次（D3）；前端禁自算正式值。**
- **禁灌 demo `data.js` 硬编码**（`factorItems.count`、`sharedMapRegions.detail` 按 rank 推导），须由 Python 按标准表写 Mock。
- **产品站禁调 `demo-*`**（D12）：企业 / 服务机构两域现行实线跑 `demo_gkxlumenx_ads`，上正式链路前必须迁到 `gkxlumenx_ads`。
- 计数口径与聚合方案 §3 一致：去重计数 / 本 region 占比 / 相邻时间窗环比。
- 指标须带 `metric_id`，对齐 `metrics/registry/*` 与 `/metrics/v1/catalog`。

## 6. 上下游

| 方向 | 任务 |
|---|---|
| 上游 | `BE-TS-AGG-01`（口径定稿）· `DATA-TS-S01`（事件/舆情三方源）· 三方源到位（P1/P5） |
| 下游 | `BE-TS-IMPL-01`（Java 读数）· `FE-TS-01A`～`09A`（页面有数或空态） |

## 7. DoD（可验收）

1. 五张标准表 DDL 落地，字段与聚合方案 §4.2 一致
2. 骨架表（企业 / 服务机构）迁入正式 `gkxlumenx_ads`，`status` 由 `draft` 转发布态
3. Mock 数据按标准表写入，接口能读到（不造假口径）
4. 指标 `metric_id` 已在 catalog 登记
5. 每批发布留记录；Java 侧只读已发布批次验证通过
6. 代码 push `origin/dev`，registry evidence 回填

## 8. 未决与阻塞

| # | 阻塞 | 归属 |
|---|---|---|
| B1 | `BE-TS-AGG-01` 仍是草案（P1 十行要素源未落人）→ 口径未定稿 | `human:李伟` 催办 |
| B2 | P7 产品化缺口：企业 / 服务机构 ADS `status=draft`，跑 Demo 库 | 数据侧 × `human:徐腾强` |
| B3 | 事件 / 舆情三方源（`DATA-TS-S01`）未定上线时点 | 三方库 |
| B4 | 课题 / 期刊是否补行（P2）未定 | `human:李伟` × `human:徐腾强` |
| B5 | 服务机构域 Owner 口径：`human:侯佳伟` vs 本方案「我方」 | 先对齐 |

## 9. 会签

| 角色 | 人 | 结论 | 日期 |
|---|---|---|---|
| 数据侧统筹 | `human:徐腾强` | 待会签 | — |
| 域 Owner（服务机构） | `human:侯佳伟` | 待对齐 | — |
| 契约 / 监管 | `human:李伟` | 已认领 | 2026-10-27 |
