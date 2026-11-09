# POLICY · 落地实效宏观结果面代理读路径（macro-eff-v1）

```yaml
---
doc_id: POLICY-ETL-MACRO-EFFECT-PROXY
element: POLICY
role: etl
status: draft            # 白名单/区划键已按 2026-11-09 实测冻结；甲方归一前一切为 QPOL-02 临时默认
version: "2026-11-09"
updated: 2026-11-09
task_id: POL-EFFECT-MACRO-DATA-L01
whitelist_version: macro-eff-v1
---
```

> 口径真源：[`M_POLICY_IMPLEMENTATION_EFFECT.md`](../../../../metrics/calc-logic/POLICY/M_POLICY_IMPLEMENTATION_EFFECT.md)「口径双轨」B 轨；详设 [`05.6.2 §3.2`](../../../../agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.6.2-深圳政策现状分析.md)。本文只冻结**取什么、怎么对城市、从哪读**。
> 证据：`third-party-source/gkx-mysql-raw/加工/_probe_macro_effect_a1.py`（可重跑，断言失败 = 冻结结论失效）→ `_probe_macro_effect_a1.json`。

## 1. 指标白名单 `macro-eff-v1`（9 个，≤12）

读法：城市截面。每指标取 **`dim_cal='TB'`（可比同比增长）· `dim_dur='DNLJ'`（当年累计）**，窗口 `occur_period ≥ 202101`，每城取窗口内**最新一期非空值**。TB 为 %，跨城可比；`JDZ·DNLJ`（绝对值，元）只给展示，不进截面分（城市体量差异会盖过政策效果）。

```yaml
whitelist_version: macro-eff-v1
window_start: 202101           # 终点 = 各城该指标最新一期（不对齐，见 §5）
primary: {dim_cal: TB, dim_dur: DNLJ, unit: "%"}
secondary_display_only: {dim_cal: JDZ, dim_dur: DNLJ, unit: "元"}
min_cities_per_index: 3        # 当次参与城不足 3 的指标本次剔除，不补 0
indicators:
  - {index_code: gmjj_gnmy_01,          name: 社会消费品零售总额,       freq: 月度, direction: up, tier: P0, tb_cities: [深圳,广州,北京,上海]}
  - {index_code: gmjj_jjzl_01_03,       name: 第三产业增加值,           freq: 月度, direction: up, tier: P0, tb_cities: [深圳,广州,北京,上海]}
  - {index_code: dwjj_dwmy_01,          name: 进出口总额(人民币计价),   freq: 月度, direction: up, tier: P0, tb_cities: [深圳,广州,北京,上海]}
  - {index_code: dwjj_dwmy_01_02,       name: 出口总额(人民币计价),     freq: 月度, direction: up, tier: P0, tb_cities: [深圳,广州,北京,上海]}
  - {index_code: dwjj_dwmy_01_01,       name: 进口总额(人民币计价),     freq: 月度, direction: up, tier: P0, tb_cities: [深圳,广州,上海]}
  - {index_code: gmjj_tzjs_01,          name: 固定资产投资总额,         freq: 月度, direction: up, tier: P0, tb_cities: [深圳,广州,上海]}
  - {index_code: gmjj_jjzl_01_02,       name: 第二产业增加值,           freq: 月度, direction: up, tier: P0, tb_cities: [深圳,广州,北京]}
  - {index_code: gmjj_jjzl_01_02_01_01, name: 按规模分:规上工业企业增加值, freq: 月度, direction: up, tier: P0, tb_cities: [广州,北京,上海]}
  - {index_code: gmjj_jjzl_01,          name: 地区生产总值,             freq: 季度, direction: up, tier: P1, tb_cities: [广州,上海]}   # 仅 2 城，4 城截面下被 min_cities 剔除；换城集合可能转正
```

要点（实测）：

- **方向**：9 个全为「越大越好」。库内 7 个指标名含失业/能耗/污染/不良/死亡（越小越好类），但都不在四城共有集合内，白名单不含；`direction` 字段保留，日后引入须显式写 `down`。
- **单位坑**：`dwd_dim_index_attribute.unit_use` 恒为「元」（库存单位），**TB 行的真实单位取事实表 `dwd_macro_index_data.unit_use`（`%`）**，不得拿属性表单位标注 TB 值。四城 TB 行 `unit_use` 实测全为 `%`。
- **值域**：白名单窗口内 TB 实测 -16.6 ~ 53.4（%）。四城全期 TB 有 +3255 的基数效应极值，B 叶对 |TB| 过大值做裁剪或剔除并在 `proxy_notes` 记录，截面 min-max 不得被单个极值拉平。
- **键唯一**：`(index_code, occur_period, area_code, dim_cal, dim_dur)` 实测无重复，同一键只有一个 `source_code`（LBS/NATIONALSTAT/GACC 不并存），无需来源择优。
- `dim_cal` / `dim_dur` 事实表存的是**代码**（`TB`/`DNLJ`），与 `dwd_dim_index_cal` / `dwd_dim_index_dur` 按 `dim_cal`/`dim_dur` 列可 join（未匹配 0 行）；按名称 join 全不中。

## 2. 区划对齐

**结论：`dwd_dim_admin_area` 里没有这四个城市自己的行**（`cur_level` 2/3 仅云南省与 14 个外省市；`cur_code` 等于事实键的行数为 0）。不能 `fact.area_code = dim.cur_code` 取城。但库内下级行（街道/社区/区县）带 `city_code/city_name/province_code/province_name`，可反解城市。且**事实表的城市键并不统一**：直辖市用 2 位省码，地级市用 12 位市码。

| 政策城市名（规范化后） | dim 反解（SQL 条件 → 命中行数） | `fact.area_code` | `area_code_type` | 事实行 / 指标数 / 期区间 |
|---|---|---|---|---|
| 深圳 | `city_name='深圳市'` → 34 行；`city_code=440300000000`，`province_code=44` | `440300000000` | 1 | 368 / 128 / 198012–202605 |
| 广州 | `city_name='广州市'` → 103 行；`city_code=440100000000` | `440100000000` | 1 | 267 / 10 / 198012–202605 |
| 北京 | `province_name='北京市'` → 221 行；`province_code=11`，`city_code=110100000000` | `11` | 1 | 197 / 10 / 195112–202606 |
| 上海 | `province_name='上海市'` → 219 行；`province_code=31`，`city_code=310100000000` | `31` | 1 | 220 / 10 / 195212–202605 |

规则：

1. 名称规范化：去「市」后缀后查上表别名（深圳市/深圳 → 深圳）。其他城市先按 `city_name` 在 dim 反解出 `city_code`，再试 `fact.area_code=city_code`（12 位）；直辖市（北京/上海，另有天津 `12`、重庆 `50`，`province_code` 已在 dim 出现、事实表各 10 个指标，**未纳入 v1 白名单覆盖核验**）用 `province_code`。
2. `fact` 侧**必须带 `area_code_type=1`**：Excel 只定义 1 行政区/2 片区/3 园区，实测另有未定义的 `type=4`（132 行；同一 `area_code` 下存在平行序列，如 `'31'` 27 行、`'50'` 12 行，另有沈阳/大连/武汉/海口），`type=3` 仅长沙 49 行。含义待供应方澄清，v1 只取 `type=1`，不带 type 会把平行序列混进来。
3. 事实表 `area_code` 的 Excel 标注为「国标 12 位」，实测长度 2/3/4/12 混存（国家码、省码、市码）。读取不得假设 12 位，也不得靠 `LIKE '%深圳%'`（`area_code` 无中文，`sz_rows=0`）。
4. 别名表放在 Python 常量里（4 行 + 反解兜底），不建表、不写库。

## 3. 读路径（只读 gkx → 算法内存，不落库）

```text
gkx(183.240.141.251:3318, reader, 只读)
  dwd_macro_index_data ⋈ dwd_dim_index_attribute        # 白名单取值
  dwd_dim_admin_area                                    # 仅用来反解 city_code / province_code
        │  polan.ods_sync.source_cfg()（GKX_ODS_MYSQL_*，已有只读 profile，复用，不新增连接口径）
        ▼
  Python 内存：城市截面 → 方向统一 → min-max → 等权 → cards.effect
```

- **不落汇聚面**：四城 × 9 指标 ≤ 数百行，现查现算 + 进程内结果缓存即可（`infra/result_cache` 同理）；不新建 ADS 表，因此 D18 mock 表条款不触发，D4 以真读真算为准。
- **禁止**：写 `gkx`；写正式 ODS/DWD/ADS；缺项补齐仍只进 `gapfill_` 前缀表（不与本代理混用）；Java 直连 `gkx`；接口写死分数。
- 取数默认 `is_deleted=0`、`index_value IS NOT NULL`。取不到 / 全缺 → `computable=false`，不写 0。
- 双仓同文：`demo-algo-ent-analysis/polan` 与 `lumen-algo-py/vendor/entan-py/polan`。白名单常量按本文 YAML 抄，`whitelist_version` 写 `macro-eff-v1`。

## 4. 行业分析辅维（P1，只作叙述，不进分母）

| 表 | 行数 | 可用过滤 | 实测 |
|---|---|---|---|
| `dwd_industry_analysis_documents` | 1,000 | `source_type_code`、`language`、`creation_date` | 来源以券商 ST21（666）/ 咨询 ST12（307）为主；**`creation_date` 全部落在 2021-06**，无法按近年窗口取；`language='Chinese'`（不是 `zh`）；标题含深圳 3 / 北京 4 / 上海 14 / 广州 2 篇，无城市字段 |
| `…_topics` | 1,052 | `topic_code` | `25 Industry` 1,000；`24 Company` 49；`2501 Industry overview and forecasts` 3。基本只有「行业」一类，区分度极低 |
| `…_content_types` | 1,000 | `code` | `TA` 分析/研究 848；`TJ` 分析评论 152 |
| `…_countries` | 1,000 | `country_code` | `CN` 998 / `TW` 2，无省市 |
| `…_industries` | 3,047 | `industry_code` | 北美式行业码（NAICS 风格：`31 Manufacturing` 564、`325 Chemical Manufacturing` 130…），与项目产业链码不同，须映射才可用 |
| `…_companies` | **102** | — | 仅 49 篇文档有公司、86 家公司。**禁用**：不当受益企业名单、不当覆盖维、不进任何分母 |

结论：行业分析库不能按城市切、不能按近年切，只能作「行业叙述素材」且需自备行业映射；**白名单不依赖它**。B 叶若要用，只能出 `proxy_notes` 的旁注，不入分数。

## 5. 已知局限（B/E1 须诚实呈现）

1. **数据是 20,000 行样本**（宏观事实 20,000、区划 20,000，均恰为整数上限），按「各城最新点」取数很稀：窗口内每城每指标仅 1–6 个点。供应方补全量后覆盖会变，白名单随之重冻（`macro-eff-v1` → `v2`）。
2. **各城最新期不对齐**（例：固投 深圳 202302、上海 202402、广州 202509；`DNLJ` 还混了 3 月累计与 12 月累计）。所以是「各城最新可得期的截面」，不是同期比较。B 叶必须在 `ext` 里带每城 `period_used`，`proxy_notes` 写明，卡面不宣称同期。
3. 深圳独有 128 个指标（战略性新兴产业、生物医药等），其他三城只有这 10 个。**跨城截面只能用共有 10 个**；深圳专属指标不进代理分，可进旁注。
4. 代理分是「宏观结果面」，不是启动率/兑现率/满意度（总控 §0.10 废作项）。

## 6. 给 B（ALGO-L01）的接口清单

| 项 | 值 |
|---|---|
| 白名单 | §1 YAML（9 个 `index_code`，`macro-eff-v1`） |
| 区划键 | §2 表；事实侧必带 `area_code_type=1` |
| 取数 SQL 骨架 | `SELECT index_code, occur_period, index_value, unit_use FROM dwd_macro_index_data WHERE is_deleted=0 AND index_value IS NOT NULL AND area_code=%s AND area_code_type=1 AND dim_cal='TB' AND dim_dur='DNLJ' AND occur_period>=202101 AND index_code IN (…)`，各城各指标取 `MAX(occur_period)` 一行 |
| `ext` 需补 | `whitelist_version`、`window`（`202101~各城最新`）、`indicator_used`、每城 `period_used`、`proxy_notes`、`track_a_status` |
| 空态 | 参与城 < `min_cities_per_index` 的指标剔除；全剔除则 `computable=false` |
