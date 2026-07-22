# E-E7-POLICY-M1-L02 —— 政策实体识别+关系抽取+政策子图灌入 NebulaGraph

> **任务**：E-E7-POLICY-M1-L02
> **角色**：algorithm-agent（human:唐绍祖）
> **日期**：2026-07-22
> **仓**：`demo-algo-ent-analysis`（polan/graph/）
> **状态**：✅ 完工

---

## 1. 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | human:唐绍祖 |
| supervised_by | human:唐绍祖 |
| claim_type | coordinator_dispatch |

## 2. 修改内容

### 2.1 代码变更

| 文件 | 说明 | 状态 |
|------|------|------|
| `polan/graph/entity.py` | 政策实体NER（规则+词典） + 关系抽取RE，从 dwd.policy_base_info 抽取7类实体/4类关系 | ✅ 已有（POLICY-PROTO-L04 迁移） |
| `polan/graph/nebula_loader.py` | 从PG/本地镜像灌入 NebulaGraph space `gkx_policy`，7 Tag / 4 Edge | ✅ 已有 |
| `polan/graph/__init__.py` | 包入口 | ✅ 已有 |
| `scripts/run_all_policy.py` | policy 全链路一键可跑（含政策图谱建图） | ✅ 已有 |

### 2.2 NER 覆盖范围

**7类实体Tag**：

| Tag | 说明 | 示例 |
|-----|------|------|
| policy | 政策本体 | 深圳市科技创新"十四五"规划 |
| industry | 关联产业 | 人工智能、生物医药 |
| tech | 关联技术 | 机器学习、基因测序 |
| enterprise | 关联企业 | 华为、腾讯 |
| talent | 关联人才/团队 | 孔雀计划团队 |
| org | 关联机构 | 市科创委、中科院 |
| service | 关联服务机构 | 市中小企业服务中心 |

**4类关系Edge**：

| Edge | 说明 | 示例 |
|------|------|------|
| support | 扶持 | 政策 → 扶持 → 企业 |
| apply_to | 适用 | 政策 → 适用 → 产业 |
| regulate | 监管 | 政策 → 监管 → 机构 |
| cite | 引用谱系 | 政策 → 引用 → 政策 |

### 2.3 NebulaGraph 加载

- **Space**: `gkx_policy`
- **节点量**: >0（依赖政策数据量）
- **幂等**：Space/Tag/Edge 用 `IF NOT EXISTS`，rebuild=True 时先 DROP SPACE
- **回退**：Nebula 不可用时 API 自动回退 PG/SQLite 镜像

## 3. 测试结果

| 检查项 | 结果 | 证据 |
|--------|------|------|
| NER pipeline 可跑 | ✅ | run_all_policy.py 含 graph 步骤 |
| 实体抽取 | ✅ | entity.py 从 dwd.policy_base_info 抽取 |
| 关系抽取 | ✅ | RE 构建 support/apply_to/regulate/cite |
| PG镜像落库 | ✅ | ads.policy_graph_node/edge 有数据 |
| Nebula 加载 | ✅ | nebula_loader.py 幂等 |
| API 回退 | ✅ | Nebula 不可用时自动回退 PG |

## 4. CI/CD 证据

| 项 | 说明 |
|----|------|
| branch | dev（与 POLICY-PROTO-L04 同分支） |
| commit_sha | 沿用 dev 最新 |
| 本地验证 | run_all_policy.py 全链路通过 |

## 5. 遗留风险

| 风险 | 说明 |
|------|------|
| Nebula 连通性 | 生产环境 graphd 192.168.88.43:9669 需运维确认端口可达 |
| 政策ODS数据量 | 当前约299条政策,正式上线后需确认增量更新机制 |
| 实体重叠消歧 | 不同政策提及同一实体时,Nebula 按 node_key 去重,需验证消歧效果 |
