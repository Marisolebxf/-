# DATA-ENT-STORAGE-S4-L01 · 旧路径 stub 指向 storage/ENT

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `lite` |
| 说明 | chore/文档 stub；未删 as-built DDL 正文 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 纯文档 |

## 修改内容

1. 新增 `data-design/企业/README.md` → 强制导航 `storage/ENT`  
2. 已归档 stub（PG 大稿 / 域设计 / vs-demo / 详细设计）统一改指 storage/ENT  
3. MySQL v3 / ES / 功能设计 / 血缘契约 / 字典盘点：文首 S4 横幅  
4. 更新 `storage/README` §7–9、`ENT/README`、流图 §6、CHANGELOG、archive README  

**未做**：删除 MySQL/ES DDL 正文（仍作 stores 外链真源）；功能设计不迁入 storage。

## 架构合规

| 项 | 结果 |
|---|---|
| 冲突以 storage/ENT 为准 | ✅ |
| 功能设计不进 storage | ✅ |
| MySQL only / 三方 ODS≠live | ✅ 未改口径 |

## CI/CD

- 分支：`dev` · 纯文档 · N/A K8s

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~40k（估） |
| model_used | Cursor Grok 4.5 |
| actual_cost | <$1 |
| cost_warn | false |

## 签收说明

S4 stub 完成；storage 四阶段 S1–S4 文档闭环。后续：细表 approved 评审、LLM→ODS 工程。
