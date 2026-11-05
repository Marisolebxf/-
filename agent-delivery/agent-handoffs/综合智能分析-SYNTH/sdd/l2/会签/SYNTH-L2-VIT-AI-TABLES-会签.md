# SYNTH-L2-VIT-AI-TABLES 会签

- 日期：2026-11-05
- 稿本：`SYNTH-L2-VIT-AI-TABLES.md` v1.0.5 现行正文。修订表旧口径不是现行要求。
- 意见来源：`会签/_role/` 第二轮（architect-agent、api-agent、algorithm-agent、data-agent）
- 签收：四角色均为同意。本册可进入签收。签收由 human:淮政玮 执行。本文件不新建任务，不改任务状态。

## architect-agent

- 结论：同意
- 按稿能否实现：是。五张 `synth_vit_*` 在 `demo_gkxlumenx_ads` / `gkxlumenx_ads`，`seed_synth_vit_*.py` 整批写入，快照只读这些表；`snapshotId` 含 `calc_batch_id`。
- 是否违反 D18：否。预填行 `is_mock=1` 在新建 ADS 表。权重缺行只回 `null`+`reason`。三张 `gapfill_synth_*` 只作输入。
- 是否与需规叶冲突：否。序号 133–135 有表和快照落点。
- 是否把维护技术图谱（34–40）做成了落库：否。
- 是否编了规划正文：否。

## api-agent

- 结论：同意
- 按稿能否实现：是。`GET /topic/v1/synth/vitality/batch-snapshot` 写明 `weight_profile` 与可选 `snapshotId`。传入只读该批，不传按 `cache_key` 取最新成功批。
- 是否违反 D18：否。接口只读 ADS。权重缺行只回 `null`+`reason`+`confidence`。
- 是否与需规叶冲突：否。133 分项、134 加权指数、135 指数与排名由五张结果表交付。
- 是否把维护技术图谱（34–40）做成了落库：否。没有技术节点或关系的增删、属性编辑、修改历史、版本保存接口。
- 是否编了规划正文：否。

## algorithm-agent

- 结论：同意
- 按稿能否实现：是。三档与已注册口径一致：`WEIGHT_MAIN`、`INDEX_MAIN`、`EQUAL`。同 profile 配对读。权重无行则 null+reason，装包不得回填三档向量。
- 是否违反 D18：否。结果写入 ADS 再读。接口不写死 JSON。
- 是否与需规叶冲突：否。本册不覆盖序号 137、139–141。
- 是否把维护技术图谱（34–40）做成了落库：否。
- 是否编了规划正文：否。

## data-agent

- 结论：同意
- 按稿能否实现：是。五张表都有粒度、唯一键、写入和读批。表数 5，与 README、总册 §11.3 一致。
- 是否违反 D18：否。结果在 ADS。不把结果放进 `gapfill_` 或 `gkxlumenx_ai`。
- 是否与需规叶冲突：否。133 在 `synth_vit_indicator`，134 在指数/维分/权重表，135 有落表。
- 是否把维护技术图谱（34–40）做成了落库：否。
- 是否编了规划正文：否。
