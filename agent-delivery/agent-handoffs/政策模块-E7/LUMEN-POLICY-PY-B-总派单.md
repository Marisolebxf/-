# B 段总派单 · polan 迁入 + harness 包装

> **管线**：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)  
> **对照仓 / 算子 demo**：`demo-algo-ent-analysis/polan`（只读对照，禁止 merge）  
> **联调台参考**：`lumen-ui-algo-apiview` 已跑通的政策算子页（只参考调用方式，不把 `/v1` 暴露给专题前端）  
> **目标仓**：`lumen-algo-py/vendor/polan` + harness（`vendor/polan/harness/` 或 `lumen_algo_worker` 政策 runner）  
> **铁律**：对照已有算子实现；**禁止修改算子方法**（签名 / 公式 / 函数体）。专题场景只加包装。

---

## `/goal` 头（BOOT 叶）

```
/goal LUMEN-POLICY-PY-BOOT-L01
角色：algorithm-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
仓：lumen-algo-py · origin/dev
强度：ponytail full
图：必含 POLICY-STORAGE-FLOW（Python 边改指向 lumen-algo-py；harness 不改工厂拓扑）
必读：总控 §0 #4 #13 · 本文件 · vendor/entan-py 迁入方式对照
禁止：改 polan.eval/basic/graph/text 算子方法；对外暴露 /v1 给前端；CREATE SPACE gkx_policy；写 gkx_chain。
settings / JDBC：demo_gkxlumenx_*（lumen 现网数仓 = demo 源，禁止改正式前缀数据面）。
内部前缀：/internal/policy/**
```

## `/goal` 头（HARNESS 叶）

```
/goal LUMEN-POLICY-PY-HARNESS-L01
角色：algorithm-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
仓：lumen-algo-py · origin/dev
强度：ponytail full
必读：总控 §0 #13 · lumen_algo_worker/main.py（已有多线程 claim）· polan.eval.focus_one（单条入口）
包装场景：时序 / 区域对比 / 深圳三维 / 单条焦点。按用量选同步 | ThreadPool 分片 | worker 子任务。
大数据：分片 policy_id、限流、流式/按批读库；禁止改算子内部去「一次 load 全表优化」。
禁止：修改算子方法；专题 Job 一次灌入全库 4 万+ 行进算子。
```

---

## 1. 算子冻结（对照 demo，原样迁入）

| 目录 | 角色 | B 段动作 |
|------|------|----------|
| `polan/eval/*.py` | 焦点/力度/效果/短板/机遇/布局等 | **原样**迁入。`run()` 仍是灌数批入口 |
| `polan/eval/focus_one.py` | 单条在线算子 | **原样**；harness 优先调这类入口做分片 |
| `polan/basic/indicators.py` | 基础指标 | **原样** |
| `polan/graph/*` | 投影/挂接 | **原样**（VID 规则已含图上链码兜底，保持） |
| `polan/text/*` · `models/registry.py` | 解析 / 注册 | **原样** |

「改」只允许：包路径/import、settings 库名切 `demo_gkxlumenx_*`、space=`demo_gkx_chain`、OTel 埋点**加在调用点外**。公式、参数顺序、返回字段语义变了 = 违规。

---

## 2. Harness（按使用场景包装）

新模块，**不要**写进算子文件。建议 `vendor/polan/harness/`：

| 场景 | 用量 | 包装 |
|------|------|------|
| 联调/单条 | 1 条政策或小过滤集 | 同步直调已有入口（`focus_one` / 已有 `analysis/{model_id}` 内部函数） |
| 三项分析 Job | 一产业/一区域下成百上千条 | `ThreadPoolExecutor` 按 `policy_id` 分片，每片调已有入口，主任务聚合 |
| 全量/重灌/大图 | 万级（现网 ODS ~4 万+） | `lumen_algo_worker` 多 worker claim；主任务拆 **子任务**（子 agent / child task_id），分片跑完再 fan-in。复用已有 `lumen_common.tasks` CAS claim，不自造 Redis 队列 |

大数据只在 harness 做：

- 分片键：`policy_id` / 区域码 / 产业图上 VID  
- 批大小可配（默认小批，避免单次把 LONGTEXT 全列扫进内存）  
- 读超时、连接归还、失败分片可重试  
- OTel span：harness 一层 + 每片一层；算子内部不强改

**禁止**：为跑全量去改 `eval/focus.run` 的 `load_policies`；禁止在算子里加线程。

---

## 3. 切法（同仓串行）

1. `PY-BOOT`：目录迁入、库名、space、OTel、内部 `/internal/policy/**`、不对外 `/v1`。  
2. SHARED。  
3. **`PY-HARNESS`**：三种场景包装 + 单测（小集合同步、中等线程池、大集分子任务接口契约；可用假算子桩证明 harness，**真算子回归仍调原方法**）。  
4. METRIC / GRAPH 读面（source 诚实）→ RUNTIME → 分析 Job **只调 harness**，不直接 `eval.*.run()` 当在线 Job。  
5. 灌数/重灌批处理仍可调原 `run()`（与 demo 一致）。

挂接 VID 只用图上链码。
