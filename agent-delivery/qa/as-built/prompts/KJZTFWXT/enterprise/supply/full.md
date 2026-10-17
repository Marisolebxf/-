# 企业供应链关系分析 · 全量执行顺序（2026-10-14 BATCH32，24 条）

入口：`/enterprise/risk?workspace=supply-chain&tab=supply-chain`（catalog `ent-supply`）。
脚本：`as-built/scripts/KJZTFWXT/enterprise/supply/`（`scripts.yaml` includes `gold.yaml`）。

## 推荐顺序

1. **配置空态与构成**：P0-01 → P0-07 → P0-08 → P0-02（门控）→ P0-11（预检空态段）
2. **对象回填**：P0-09 → P0-11（回填预检）→ P0-10（浮层超限）→ P1-01 / P1-04 / P1-05
3. **发起过程**：P0-12（可能分析失败，过程页仍应出现）
4. **历史与结果**：P0-18 → P0-17 → P0-03 → P0-05 → P1-03 → P0-04 / P0-13~P0-16（多项 allow_skip）
5. **Tab / 隔离 / 评审**：P1-02 → P0-06 → P1-06

## 易错点

- **先登录再深链**：`survey-page` 直开带 query 的 path 易停 login；二次探针先 `/login`。
- **对比篮关闭钮**：`aria-label=关闭对比篮` **可见再点**，不可见勿盲点。
- **对象带入**：页内 CTA「前往对比篮选择企业」→ 浮层「确定」；不是系统篮「发起分析」六类型。
- **超限**：勾选第 3 家后浮层「确定」禁用，不要期望配置页预检「最多 2 家」文案。
- **结果态**：优先「最近分析→恢复结果」；新任务可能失败。
- **兄弟页**：禁止写痛难点正向；仅 P0-06 隔离。
- **评审开关**：`aria-label="内部评审模式"`，勿 `first()` 盲点；操作前关 persona 菜单。

判定铁律见 `prompts/_result.md`（本步不建 `runs/`）。
