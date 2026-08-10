# ENT-REGION-SCOPES-NATIONAL-EXPAND · 运营地域「全国」挂接国标三级树

> 格式参考 `templates/handoff-template.md`。  
> **范围修正**：仅 Python + Java；前端已撤回本地改动，另开草稿工单 `FE-ENT-REGION-SCOPES-PATH-FIX-派单草稿.md`（**未入库**）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:徐滕强` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 用户确认接口组装；明确前端不随本单提交 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 `code_region`，扩展既有 `/meta/region-scopes`，未新建第三套码表 |

## 问题清单

- 结果区 / 重点企业分析 `RegionSelect` 走 `region-scopes`，原先「全国」仅 `china-all` 占位
- 高筛 `/meta/regions` 已有全量 `code_region`；用接口组装挂到「全国」下即可

## 修改内容

### Python（`demo-svc-topic-py`）— 本单交付

- `gkx_search_service/views/meta.py`
  - `expand_national` 默认 `true`：tree/children 下将 `national` 子树替换为 `code_region`（parent=`0`）
  - 国标节点：`scope_code=admin_code`、`node_kind=admin|district`、`bind_admin_code`
  - 加载失败回退 `china-all`；`expand_national=false` 保持旧行为
- `tests/test_region_scopes_national_expand.py`：3 例
- `docs/API-接口文档.md`：补充契约

### Java（`lumen-svc-platform`）— 本单交付

- `EnterpriseRegionScopeRequest` 增加可选 `expand_national`（透传；默认由 Python 兜底 true）
- Controller / Feign / Service **无业务逻辑变更**，继续透传

### Frontend（`lumen-ui-topic`）— **不在本单**

- 本地曾误改文件已 `git checkout` 撤回（工作区干净）
- 适配拆至草稿：`FE-ENT-REGION-SCOPES-PATH-FIX-派单草稿.md`（待与其他码表同批入库，**先不 task-create / 不 push registry**）

## 验收证据

```bash
cd demo-svc-topic-py && .venv/bin/python -m pytest tests/test_region_scopes_national_expand.py -q
# 3 passed
```

```bash
curl -X POST '.../topic/v1/search/meta/region-scopes' \
  -H 'Content-Type: application/json' \
  -d '{"mode":"tree","include_members":true}'
# national.children 应为 6 位国标码树，不再只有 china-all
```

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 组装在 topic-py |
| 调用链 FE→Java→Python | ✅ Java 仅透传 |
| 图谱 Nebula | N/A |
| demo2 不 merge lumen | ✅ 本单不改 lumen-ui |
| 数据策略 ADS/码表 | ✅ 读 DIM，分表不混 |

## 开放项

- 前端 Cascader path / 入参适配：见 FE 草稿工单，与其他码表同批再派
- 场景禁用（全球/全国/区域/深圳）：另议
