# SYNTH-CHAINFIX-DOCS-L01 Handoff — 跨层链路修复第④站（文档+测试收口）

- **任务**：SYNTH-CHAINFIX-DOCS-L01（链路修复④：P2-b 总册残留修正 + P2-c A/B 批端到端 CI 用例）
- **执行**：agent:architect（claimed_by=agent:arch-agent，supervised_by=human:徐滕强）
- **仓**：`gkx-orchestration`（origin/dev，**已 commit 未 push**，等人工确认推送）
- **强度**：ponytail: full（最短 diff；零新依赖：fake-conn 纯 stdlib 内存镜像，不用 testcontainers/sqlite）
- **设计真源**：`SYNTH-L2-COLLAB.md` v1.0.8 §2/§3.2/§7、总册 v1.0.7-draft §6
- **日期**：2026-11-06

## 1. P2-b 总册残留修正 ✅

文件：`agent-delivery/agent-handoffs/综合智能分析-SYNTH/sdd/综合智能分析-系统详细设计说明书.md`

| # | 位置 | 修改 |
|---|---|---|
| 1 | §6 资源划分·图谱查询行 | `可选 snapshotId/gapfill_batch_id` → `可选 snapshotId/industry/limit_nodes/limit_edges（见协同册 §3.2 v1.0.8）`；与协同册 v1.0.8 §3.2 对齐（该册明文「本期没有 gapfill_batch_id」；`entity_types/relation_types` 可选多选参数同见该节，总册行不逐一枚举） |
| 2 | 头部日期行 | v1.0.6-draft → **v1.0.7-draft**（注明 P2-b 修正） |
| 3 | §12 修订记录 | 追加 v1.0.7-draft 行（P2-b：总册图谱参数对齐协同册 v1.0.8，删 gapfill 残留） |

修正依据：协同册 v1.0.5 已废止 gapfill 图（会签退回），v1.0.8 §3.2 请求参数表可选项为 `snapshotId/industry/entity_types/relation_types/limit_nodes/limit_edges`；总册 §6 资源表是 v1.0.2 时代残留（当时「图谱补 compare/snapshotId/gapfill_batch_id」），未被后续轮次清扫。

## 2. P2-c A/B 批端到端 CI 用例设计

### 2.1 现状与目标

- **现状**：A/B 批「AR-9 翻转 + snapshotId 回读不串 + 幂等重试」只有手工探针脚本 `vendor/entan-py/scripts/check_synth_collab.py` §3/§4 覆盖——其依赖真实 demo MySQL（`ENTAN_MYSQL_PASSWORD` 必填、连 `10.50.11.76`），还要插/清 `check_collab_*` 探针行，**进不了 CI**。
- **目标**：CI 可自动跑的同语义用例，不依赖真实库；防①PY 段 / ②JAVA 段后续改动把「A/B 批不串」改回归。

### 2.2 设计要点（首选方案：fake-conn 内存镜像）

| 设计项 | 决定 | 理由 |
|---|---|---|
| 打桩点 | `entan.synth_collab.pack._ads()`（模块级薄封装，`from entan.common.db import connect; return connect()`） | 全部 DB 访问经 `pack._ads()` 收敛为单点（快照/装包/graph 三入口同源）；`monkeypatch.setattr(pack, "_ads", ...)` 一处生效，不动生产代码 |
| 镜像介质 | 纯内存 dict（`dict[table, list[row]]`），**不用 sqlite** | 镜像对象是 pack.py 发出的 8 类 SQL 语义（SELECT 过滤排序 / INSERT meta / UPDATE is_latest 翻转），不是通用 SQL 引擎；fake-conn 约 80 行，比 sqlite 建表+SQL 方言适配更短；零依赖 |
| conn 接口 | `ads` 属性（表前缀）+ `query(sql, params)` / `execute(sql, params)` / `commit()` / `rollback()` / `close()` | 与 `entan.common.db.connect()` 返回的自定义 conn 接口逐字对齐（pack.py 调用形态：`conn.query(...)`、`conn.execute(...)`、`{conn.ads}.\`表\``、`%s` 占位） |
| SQL 路由 | 按语句前缀+表名路由到内存操作；未识别语句返回 `[]`（graph 的 node/edge SELECT 即落此分支，本期 0 行语义天然成立） | `ponytail:` 天花板——pack.py 新增 SQL 形态须同步扩路由；路由表逐条对照 pack.py 实发语句（§4 草稿内注释） |
| AR-9 事务语义 | `execute` 前深拷贝 meta 表作备份；`rollback()` 恢复备份、`commit()` 丢弃 | 验证「meta 写失败回滚后 is_latest 不半翻」的钩子留接口不写用例（故障注入属过度设计；翻转结果+幂等已覆盖 §7.3/§7.4 验收） |
| 数据前置 | **串行前置**：灌批 A → 发布 tA → 灌批 B → 发布 tB（发布语义=读「当前最新 succeeded 批」，两批同灌会让 tA 也读到 B 批——实跑抓出过此坑）；固定时间戳（A=`2026-01-01 10:00:00`、B=`2026-01-02 10:00:00`，防 MAX(calc_batch_created_at) 排序歧义）；**meta 行由生产代码自己写**（被测行为就是 `_publish_batch_meta`） | 任务链发布走 `execute_collab_job()`，snapshotId=`task:{task_id}` 固定值（`ci-ab-tA`/`ci-ab-tB`），内存库无残留 → CI 任意重跑幂等 |
| `relation_input` 不 seed | 缺行合法（null+reason=relation_row_missing），不影响 A/B 断言点 | 探针脚本同样不依赖它做 A/B |
| LLM 静音 | fixture 删 `ENTAN_LLM_API_KEY`/`GKX_LLM_API_KEY`/`LLM_API_KEY`/`OPENAI_API_KEY`（探针 `_silence_llm_env` 同款） | 实跑抓出：环境残留 key 会真网外呼重试（401×2×2，拖慢 13s 且不确定）；CI 必须静音 |

### 2.3 断言清单 ↔ 验收映射

| 用例 | 断言 | 验收出处（SYNTH-L2-COLLAB v1.0.8） |
|---|---|---|
| `test_ab_publish_flip` | A 批 `execute_collab_job(task_id="ci-ab-tA")` → succeeded + `snapshotId=="task:ci-ab-tA"`；B 批后 meta 两行；A 行 `is_latest=0`、B 行 `is_latest=1` | §7.3（成功发布必有 meta 行）+ AR-9（同 cache_key 翻转）+ 协同册 §7.4 |
| `test_snapshot_readback_no_crosstalk` | `build_collab_snapshot(..., snapshot_id="task:ci-ab-tA")` → `isLatest==0` 且 `graph_batch_id` 仍为 A 批值（≠B）；B 同理为 1 | §7.4（用 A 打开图谱/快照仍返回 A 的批，cache_key 可改指 B） |
| `test_idempotent_retry` | 同 task_id 二次发布 → succeeded、`snapshotId` 不变、meta 行数仍 1（不撞 `uk(snapshot_id)`）、A 重新 `is_latest=1`（重试=重新发布语义，pack.py `_publish_batch_meta` 注释明文「UPDATE 仍执行」） | 探针脚本 §4 P3 同款；册 §3.1 幂等 |
| `test_graph_batch_isolation` | `build_collab_graph(..., snapshot_id="task:ci-ab-tA"/"ci-ab-tB")` → 各自 `graph_batch_id`/`calc_batch_id`/`snapshotId` 三件套对应本批、互不相等；本期 0 行 → `reason="no_year_on_source"`、HTTP 语义层 `nodes=[]` | §3.2 批次解析三步 + §7.4 |

### 2.4 skip 条件与升级路径

- **不需要 testcontainers**：fake-conn 已覆盖全部被测语义；真实库语义（DDL/唯一键/InnoDB 事务）由既有手工探针脚本继续承担（联调环境）。
- **不需要 skip**：无环境依赖（纯内存），CI 必跑必绿。
- 升级路径（仅当 pack.py SQL 面大幅膨胀使路由表失控）：`pytest + testcontainers-mysql` 挂真 DDL（`scripts/mysql/synth_collab.sql`），届时用例断言不变、只换 fixture。

## 3. 落点决定：**不直接落 PY 仓，走本 handoff 附录，由 PY 站后续 chore 采纳**

判定过程（任务书给定门槛：工作区干净且无他人改动文件重叠，方可直接落）：

```
$ cd repos/lumen-algo-py && git status --short
 M lumen_common/algorithms/svcan/assembly/graph.py      ← 他人未提交
 M lumen_common/algorithms/svcan/assembly/leaves.py     ← 他人未提交
 M tests/test_svcan_assembly.py                         ← 他人未提交
?? scripts/mock_stage_health_scores.py                  ← 他人未提交
?? scripts/seed_supply_chain_relations.py               ← 他人未提交
```

- 工作区**不干净**（5 个他人未提交改动）→ **不满足直接落条件**。虽有目标文件无重叠（新增 `vendor/entan-py/tests/test_synth_collab_ab.py`，与上述 5 文件零交集），但按「干净且无重叠」的合取门槛，本次不落码。
- 另发现一个**接线要点**（PY 站采纳时必须处理）：`pytest.ini` `norecursedirs` 含 `vendor` → 根目录 `pytest` 扫不到该文件。CI 接线二选一：
  1.（推荐）`.gitlab-ci.yml` `py:test` job 加一行：`cd vendor/entan-py && python -m pytest tests/test_synth_collab_ab.py -q -p no:cacheprovider`（vendor 内已有 8 个测试文件同款运行方式，`import entan.*`/`import api.main` 以 `vendor/entan-py` 为根）；
  2. 或把文件挪根 `tests/` 并补 sys.path 注入——不推荐（vendor 内聚被拆）。

## 4. 附录：用例代码草稿（PY 站采纳稿）

> 落点：`vendor/entan-py/tests/test_synth_collab_ab.py`。零第三方新依赖（fastapi TestClient 已在仓内，本用例甚至不需要它——全部走 pack 层函数）。SQL 路由表逐条对照 `entan/synth_collab/pack.py` 实发语句，采纳时以当时 pack.py 为准微调。
>
> **草稿已实跑自证**（本机 PY 仓临时落盘验证，跑完删除未提交）：`python3 -m pytest tests/test_synth_collab_ab.py -q` → **4 passed in 0.10s**（静音 LLM 后零外呼）。首轮实跑抓出两处设计缺陷并已修正进本稿：①fixture 两批同灌违反「发布读当前最新批」时序（tA 读到 B 批）→ 改 `_publish_ab` 串行前置；②本机残留 LLM key 真网 401 重试 → fixture 静音四个环境变量。

```python
"""SYNTH-CHAINFIX-DOCS-L01 附录:P2-c A/B 批端到端用例(设计真源=ORCH handoff)。

覆盖(协同册 v1.0.8 §7.3/§7.4 + AR-9):
  [1] A/B 批发布 → 同 cache_key is_latest 翻转(AR-9)
  [2] snapshotId 回读不串 A/B(cache_key 改指后 A 仍可回溯)
  [3] 同 task_id 幂等重试(不撞 uk(snapshot_id),行数不增)
  [4] graph 批次解析不串(snapshotId 精确读 meta,未传读 is_latest)
不依赖真实 MySQL:monkeypatch pack._ads() → FakeConn(内存镜像 SQL 语义)。
⚠️ 时序语义:发布读「当前最新 succeeded 批」,A/B 必须串行前置
(灌批 A→发布 tA→灌批 B→发布 tB;同探针脚本 §3/§4;禁 fixture 里两批同灌)。
"""
from __future__ import annotations

import copy
import os
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # vendor/entan-py

import entan.synth_collab.pack as pack  # noqa: E402
from entan.synth_collab.pack import (  # noqa: E402
    build_collab_graph,
    build_collab_snapshot,
    execute_collab_job,
)

ADS = "demo_gkxlumenx_ads"
COND = ("深圳市", "全国重点城市", "最近3年")          # resolve_region_cities("深圳")→"深圳市"
BODY = {"leaf": "collaboration", "region": "深圳",
        "compare": "全国重点城市", "window": "3y"}


class FakeConn:
    """内存镜像 pack.py 对 ADS 的实发语句(ponytail: 只路由实发形态,新增 SQL 须扩表)。

    支持语句(逐条对照 pack.py):
      SELECT calc_batch_id, MAX(calc_batch_created_at)...GROUP BY   (_latest_batch)
      SELECT * FROM `t` WHERE calc_batch_id=%s AND <cond>...succeeded (_read_batch)
      SELECT * FROM `synth_collab_relation_input` WHERE region/compare/metric_id...
      SELECT * FROM `synth_collab_batch_meta` WHERE snapshot_id=%s   (_meta_by_snapshot)
      SELECT * FROM `synth_collab_batch_meta` WHERE cache_key=%s AND is_latest=1...
      INSERT INTO `synth_collab_batch_meta` (...9列...is_latest=0)   (_publish_batch_meta)
      UPDATE ... SET is_latest=1 WHERE snapshot_id=%s
      UPDATE ... SET is_latest=0 WHERE cache_key=%s AND is_latest=1 AND snapshot_id<>%s
    其余语句(graph 的 node/edge SELECT 等)返回 [] — 本期 0 行语义成立。
    rollback 恢复 execute 前备份(AR-9 同事务失败不半翻),commit 丢弃备份。
    """

    META_COLS = ("snapshot_id", "calc_batch_id", "graph_batch_id", "cache_key",
                 "region", "compare", "window", "published_at")  # 第9参 is_latest 固定0

    def __init__(self) -> None:
        self.ads = ADS
        self.tables: dict[str, list[dict]] = {
            "synth_collab_index": [], "synth_collab_network_stat": [],
            "synth_collab_relation_input": [], "synth_collab_output_corr": [],
            "synth_collab_batch_meta": [], "synth_collab_node": [], "synth_collab_edge": [],
        }
        self._backup: list[dict] | None = None

    # ── 测试数据注入(只 seed 指标表;meta 由被测代码自己写) ──
    def seed_batch(self, batch: str, ts: str) -> None:
        """灌一个 succeeded 指标批(index+network_stat density+output_corr insufficient)。"""
        base = {"region_code": COND[0], "region_name": "深圳", "compare_scope": COND[1],
                "window_label": COND[2], "calc_batch_id": batch,
                "calc_batch_created_at": ts, "calc_status": "succeeded",
                "is_mock": 1, "method_version": "ci", "value_json": None}
        rows = [
            {"metric_id": "M_SYNTH_COLLAB_INDEX", "stat_type": None,
             "value_num": 66.66, "relation_type": None, "reason": None,
             "status": None, "id": len(self.tables["synth_collab_index"]), **base},
            {"metric_id": "M_SYNTH_COLLAB_DENSITY", "stat_type": "density",
             "value_num": 0.4242, "relation_type": None, "reason": None,
             "status": None, "id": len(self.tables["synth_collab_network_stat"]), **base},
            {"metric_id": "M_SYNTH_COLLAB_OUTPUT_CORR", "stat_type": None,
             "value_num": None, "relation_type": None, "reason": "年度序列未落盘(C-05)",
             "status": "insufficient", "id": len(self.tables["synth_collab_output_corr"]),
             **base},
        ]
        for row in rows:
            table = ("synth_collab_index" if row["metric_id"].endswith("_INDEX")
                     else "synth_collab_network_stat"
                     if row["metric_id"].endswith("_DENSITY")
                     else "synth_collab_output_corr")
            self.tables[table].append(row)

    # ── conn 接口(entan.common.db.connect 同款) ──
    def _table_of(self, sql: str) -> str:
        m = re.search(r"`([a-z_]+)`", sql)
        return m.group(1) if m else ""

    def query(self, sql: str, params: tuple = ()) -> list[dict]:
        tbl = self._table_of(sql)
        rows = self.tables.get(tbl, [])
        if sql.startswith("SELECT calc_batch_id, MAX"):          # _latest_batch
            hit = [r for r in rows if r["calc_status"] == "succeeded"
                   and (r["region_code"], r["compare_scope"], r["window_label"]) == tuple(params)]
            if not hit:
                return []
            best = max(hit, key=lambda r: r["calc_batch_created_at"])
            return [{"calc_batch_id": best["calc_batch_id"],
                     "t": best["calc_batch_created_at"]}]
        if sql.startswith("SELECT *") and "WHERE snapshot_id=%s" in sql:      # _meta_by_snapshot
            return [r for r in rows if r["snapshot_id"] == params[0]]
        if sql.startswith("SELECT *") and "cache_key=%s AND is_latest=1" in sql:  # _meta_latest
            hit = [r for r in rows if r["cache_key"] == params[0] and r["is_latest"] == 1]
            return sorted(hit, key=lambda r: r["published_at"], reverse=True)[:1]
        if "synth_collab_relation_input" in tbl:                  # _read_relation_input
            hit = [r for r in rows if r["calc_status"] == "succeeded"
                   and r["region_code"] == params[0] and r["compare_scope"] == params[1]
                   and r["metric_id"] == params[2]]
            return sorted(hit, key=lambda r: (r["calc_batch_created_at"], r["id"]),
                          reverse=True)
        if sql.startswith("SELECT *") and "WHERE calc_batch_id=%s" in sql:    # _read_batch
            return [r for r in rows if r["calc_batch_id"] == params[0]
                    and r["calc_status"] == "succeeded"
                    and (r["region_code"], r["compare_scope"], r["window_label"]) == tuple(params[1:4])]
        return []                                                 # node/edge 等未识别 → 空

    def execute(self, sql: str, params: tuple = ()) -> None:
        tbl = self._table_of(sql)
        if tbl == "synth_collab_batch_meta":
            self._backup = copy.deepcopy(self.tables[tbl])        # AR-9: 回滚备份点
        if sql.startswith("INSERT INTO"):                         # 第9参 is_latest 固定 0
            row = dict(zip(self.META_COLS, params))
            row["is_latest"] = 0
            row["id"] = len(self.tables[tbl])
            self.tables[tbl].append(row)
        elif "SET is_latest=1 WHERE snapshot_id=%s" in sql:
            for r in self.tables[tbl]:
                if r["snapshot_id"] == params[0]:
                    r["is_latest"] = 1
        elif "SET is_latest=0 WHERE cache_key" in sql:            # 翻旧:同 cache 除本快照
            for r in self.tables[tbl]:
                if r["cache_key"] == params[0] and r["is_latest"] == 1 \
                        and r["snapshot_id"] != params[1]:
                    r["is_latest"] = 0

    def commit(self) -> None:
        self._backup = None

    def rollback(self) -> None:
        if self._backup is not None:
            self.tables["synth_collab_batch_meta"] = self._backup
            self._backup = None

    def close(self) -> None:
        pass


def _publish_ab(conn: FakeConn) -> None:
    """串行前置(⚠️ 发布读当前最新批,禁两批同灌):灌A→发tA→灌B→发tB。"""
    conn.seed_batch("ci-ab-A", "2026-01-01 10:00:00")
    assert execute_collab_job({**BODY, "task_id": "ci-ab-tA"})["status"] == "succeeded"
    conn.seed_batch("ci-ab-B", "2026-01-02 10:00:00")
    assert execute_collab_job({**BODY, "task_id": "ci-ab-tB"})["status"] == "succeeded"


@pytest.fixture()
def fake(monkeypatch: pytest.MonkeyPatch) -> FakeConn:
    # 静音 LLM(同探针 _silence_llm_env):防 CI 环境残留 key 真网外呼/烧 token
    for key in ("ENTAN_LLM_API_KEY", "GKX_LLM_API_KEY", "LLM_API_KEY", "OPENAI_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    conn = FakeConn()
    original = pack._ads
    pack._ads = lambda: conn            # 单点打桩:快照/装包/graph 三入口同源
    yield conn
    pack._ads = original


def _meta(fake: FakeConn, snap: str) -> dict:
    return next(r for r in fake.tables["synth_collab_batch_meta"]
                if r["snapshot_id"] == snap)


def test_ab_publish_flip(fake: FakeConn) -> None:            # AR-9 + 册 §7.3
    _publish_ab(fake)
    meta_a = _meta(fake, "task:ci-ab-tA")
    meta_b = _meta(fake, "task:ci-ab-tB")
    assert meta_a["calc_batch_id"] == "ci-ab-A"              # 串行时序:A 发 A 批
    assert meta_b["calc_batch_id"] == "ci-ab-B"
    assert meta_a["is_latest"] == 0 and meta_b["is_latest"] == 1   # AR-9 翻转
    assert meta_a["cache_key"] == meta_b["cache_key"] == "|".join(COND)


def test_snapshot_readback_no_crosstalk(fake: FakeConn) -> None:   # 册 §7.4
    _publish_ab(fake)
    back_a = build_collab_snapshot("深圳", "全国重点城市", "最近3年",
                                   snapshot_id="task:ci-ab-tA")
    back_b = build_collab_snapshot("深圳", "全国重点城市", "最近3年",
                                   snapshot_id="task:ci-ab-tB")
    assert back_a["isLatest"] == 0 and back_b["isLatest"] == 1
    assert back_a["result"]["graph_batch_id"] == _meta(fake, "task:ci-ab-tA")["graph_batch_id"]
    assert back_b["result"]["graph_batch_id"] != back_a["result"]["graph_batch_id"]  # 不串


def test_idempotent_retry(fake: FakeConn) -> None:           # 探针 §4 P3 同款
    _publish_ab(fake)
    retry = execute_collab_job({**BODY, "task_id": "ci-ab-tA"})   # 同 task 重发
    assert retry["status"] == "succeeded"
    assert retry["result"]["snapshotId"] == "task:ci-ab-tA"
    assert len([r for r in fake.tables["synth_collab_batch_meta"]
                if r["snapshot_id"] == "task:ci-ab-tA"]) == 1     # 不重复插行(不撞 uk)
    assert _meta(fake, "task:ci-ab-tA")["is_latest"] == 1         # 重试=重新发布


def test_graph_batch_isolation(fake: FakeConn) -> None:      # 册 §3.2 批次解析三步
    _publish_ab(fake)
    g_a = build_collab_graph("深圳", "全国重点城市", "最近3年", snapshot_id="task:ci-ab-tA")
    g_b = build_collab_graph("深圳", "全国重点城市", "最近3年", snapshot_id="task:ci-ab-tB")
    for g, snap in ((g_a, "task:ci-ab-tA"), (g_b, "task:ci-ab-tB")):
        meta = _meta(fake, snap)
        assert g["snapshotId"] == snap
        assert g["graph_batch_id"] == meta["graph_batch_id"]
        assert g["calc_batch_id"] == meta["calc_batch_id"]
    assert g_a["graph_batch_id"] != g_b["graph_batch_id"]         # 不串
    assert g_a["nodes"] == [] and g_a["reason"] == "no_year_on_source"  # 本期 0 行
    g_latest = build_collab_graph("深圳", "全国重点城市", "最近3年")     # 未传 → is_latest
    assert g_latest["snapshotId"] == "task:ci-ab-tB"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
```

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| D8/D9/D10 | ✅ 本单只改文档与用例设计，不动 UI/指标/交互 |
| D16/D18 gapfill 边界 | ✅ P2-b 正是清除 `gapfill_batch_id` 残留（协同册 v1.0.5 已废止 gapfill 图）；用例不含 gapfill 语义 |
| 调用链 | ✅ 用例只测 PY pack 层（Java 下游消费同契约）；不越层 |
| demo2 只读 merge | ✅ 不涉及 |
| git 策略 | ✅ ORCH origin/dev 直推语义，commit 不 push 等人工确认（前端闸门不适用本仓，但本单按任务书同样不 push） |
| 多会话保护 | ✅ 未动 `task-registry.yaml` 工作区脏块（PY/JAVA 站在途产物）；MCP 回填走工具不手工改 YAML |

## 6. Cost

| 字段 | 值 |
|---|---|
| actual_tokens | ~65,000 |
| model_used | glm-5.3-Flash |
| actual_cost | 0.25 |
| cost_warn | green（< $10 阈值） |

evidence：`agent-delivery/agent-handoffs/SYNTH-CHAINFIX-DOCS-L01.md`（本文件）
