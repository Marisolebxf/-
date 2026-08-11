# DATA-ENT-CODE-COUNTRY-APPLY-L01 · handoff（签收）

> claimed_by: `agent:data-agent`  
> supervised_by: `human:徐滕强`  
> claim_type: `pull`  
> ponytail: `full`  
> 日期：2026-08-11  
> **建议状态**：`ready_to_sign`（tech_task；DIM 现网已灌 + 校验齐）  
> cicd: `skip`（编排仓 DDL + MySQL 现网，无业务仓必改代码）

## 1. 范围与实现

| DoD | 结果 |
|-----|------|
| 建/灌 `gkxlumenx_dim.code_country`（G20 2020 主权 19 国，ISO alpha-3） | ✅ |
| `region_scope` 增加 `bind_country_code` + L04 国家节点 19 | ✅ |
| L05：G20 热门城市挂 `g20-c-*`；海外 UN/LOCODE；中国 `bind_admin_code` | ✅ |
| 新加坡 `g20-singapore` 下线；「全国热门」枝不动 | ✅ |
| 执行顺序 `code_country → L04 → L05`；**禁止** L05 后再跑 L03 §3 G20 段 | ✅（现网未跑 L03 §3） |
| 校验 SQL + 本 handoff + cost | ✅ |

口径真源：`agent-delivery/data/ddl/CITY-CODE-G20.md`

## 2. 现网执行记录

| 项 | 值 |
|----|-----|
| 目标 | `gkxlumenx_dim` @ `111.198.38.90:34306` |
| 顺序 | `gkxlumenx_dim_code_country.sql` → `_g20_country_l04.sql` → `_g20_city_l05.sql` |
| L03 策略 | **A**：头注释 + §3 警告，不注释脚本体；本轮**未**重放 §3 |
| 脚本 exit | 三脚本均为 0 |

### 校验摘要（实测）

| 检查项 | expect | actual |
|--------|--------|--------|
| `code_country` / is_g20 | 19 / 19 | 19 / 19 |
| `g20-c-%` active | 19 | 19 |
| 国家下 active 城市 | ~29 | 29 |
| `global-all` 下 active 旧 g20 城市 | 0 | 0 |
| `g20-singapore` | is_active=0 | 0 |
| join `code_country` | 19 | 19 |
| 样例城码 | JPTYO / USNYC / JPOSA | 已对 |
| `hot-city` 子节点 | 不动 | 未下线 |
| 中文 UTF-8 | 中国/日本/美国 | HEX OK |

## 3. 产物清单

| 路径 | 说明 |
|------|------|
| `agent-delivery/data/ddl/gkxlumenx_dim_code_country.sql` | 建表 + 19 国 |
| `agent-delivery/data/ddl/gkxlumenx_dim_region_scope_g20_country_l04.sql` | ALTER（幂等探测）+ 国家叶 |
| `agent-delivery/data/ddl/gkxlumenx_dim_region_scope_g20_city_l05.sql` | 城市复活改挂 + UN/LOCODE |
| `agent-delivery/data/ddl/CITY-CODE-G20.md` | 城市码口径 |
| 本 handoff | 签收证据 |

## 4. 偏离说明

- registry 中本单曾短暂丢失（rebase）；本轮以 MCP `task-create` 重建条目并对齐本 handoff。  
- L04 ALTER 已改为 `information_schema` 探测后 ADD（可重试）。  
- 旧 `dim.city` 连字符码（`JP-TYO` 等）保留行但 **region_scope 不再引用**。

## 5. 禁止（运维）

- L04/L05 之后再跑 `gkxlumenx_dim_region_scope_seed_l03.sql` 的 **§3 G20 region_scope**（会把 `bind_city_code` 打回 `JP-OSA` 等）  
- 以「旧 g20-* 城市 is_active=0」作为通过条件（L05 必须挂国家并激活）  
- 动「全国热门科创城市」枝

## 6. 架构合规自检

1. 算法只在 Python：N/A（DIM DDL）  
2. 调用链：✅ 未越层  
3. 图谱：N/A  
4. 可观测：N/A  
5. CI/CD：`cicd: skip`  
6–8：N/A / DIM 标准维表 ✅  
9–10：N/A  

## 7. 解锁下游

| 下游 | 依赖本单？ | 备注 |
|------|------------|------|
| `/meta/region-scopes` 树形 | ✅ 已靠现网 DIM | 树已变；`bind_country_code` 经 Java 仍可能被 DTO 丢掉 |
| FE 三分取码 | ✅ DIM 就绪 | `FE-ENT-REGION-SCOPE-G20-COUNTRY-L01` |
| ES mapping | 并行 | `FIX-TOPIC-ES-TEXT-ANALYZER-L01`（mapping 已交） |
| ES 灌数 / recreate | 外派 | 不阻塞本单签收 |
| KEYANALYSIS / RECOMMEND OR | 等 ES 有值 | backlog→ready 由 coordinator 开闸 |

## 8. Cost（回填）

| 字段 | 值 |
|------|-----|
| actual_tokens | ~25000（估） |
| model_used | cursor-grok-4.5 |
| actual_cost | ~1.0 |
| cost_warn | green |
