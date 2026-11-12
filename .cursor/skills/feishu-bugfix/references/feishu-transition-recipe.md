# 飞书缺陷状态迁移配方（issue → RESOLVED）

> 来源：2026-11-12 缺陷 7167110078（#2461，技术市场潜力与需规不符）实迁成功记录。
> 目的：避免每次在 `transition_state` 上反复试错 `ErrFieldRequired` / option_id 格式错误。

## 1. 先取合法迁移与必填项

```text
get_transitable_states(project_key, work_item_id, work_item_type="issue")
get_transition_required(project_key, work_item_id, state_key="RESOLVED")
```

`IN PROGRESS → RESOLVED` 的 confirm_form 通常包含：

| 字段 | field_key | 说明 |
|---|---|---|
| 阶段分类 | `issue_stage` | 例：开发测试阶段 `9njhi405p` |
| 解决结果 | `field_f39ef6` | 必填 select |
| 问题归类 | `field_edcb35` | 例：功能逻辑问题 |
| 所属需求 | `_field_linked_story` | 关联需求 ID |
| 解决版本 | `resolve_version` | 可为空时仍需确认 |

## 2. 先补必填字段，再迁移

`update_field` 的 select 字段**只传纯 option_id 字符串**，不要传 `{value,label}` JSON：

```json
{
  "fields": [
    { "field_key": "field_f39ef6", "field_value": "ou802bb28" }
  ]
}
```

常用选项（`field_f39ef6` 解决结果）：
- `ou802bb28` 已修复
- `i54knwdkg` 无法复现
- `7dzp1g1y_` 无需修复
- `gw_btfk9a` 无效缺陷
- `ymd1l8kp0` 重复缺陷
- `e2v8k31gz` 转需求
- `7fcnxip7r` 重新打开

然后再调用：

```text
transition_state(project_key, work_item_id, transition_id=<RESOLVED transition id>)
```

## 3. 成功判据

- `transition_state` 返回 `success`
- 飞书 work item status = `RESOLVED`
- 必须回写验收总结评论（修复内容、需规依据、commit、pipeline、验收口令、已知缺口）

## 4. 常见错误

| 错误 | 原因 | 处理 |
|---|---|---|
| `ErrFieldRequired ... 解决结果(field_f39ef6) 必填` | 迁移前未补字段 | 先 `update_field` |
| `ErrInvalidParam ... option_id is empty` | select 传了 JSON 对象 | 传纯 option_id 字符串 |
| `ErrMetadataError attr label not found` | MQL SELECT 用了不存在的字段 | 用 `get_workitem_brief(fields=["_all"])` 查真实 key |
