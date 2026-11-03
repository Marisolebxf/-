# POL-L2-DS11-PLAN-METRIC-SIGNOFF-ALGO · 政策分析评价 · 推荐方案报告交互展示 · 后台指标设计算法会签

- 角色：agent:algorithm-agent（监管 human:淮政玮）
- 日期：2026-11-03
- 对象：`sdd/l2/POL-L2-DS11-PLAN-METRIC.md`（只读会签，不改分册）
- 监管：human:淮政玮
- 对照：`sdd/l2/POL-L2-DS11-PLAN-ARCH.md`（已签收架构）；代码实读 `repos/lumen-algo-py/vendor/entan-py/polan/text/simulate.py`、`repos/lumen-algo-py/vendor/entan-py/conf/cfg_model_registry.yaml`（均只读）
- 范围：SRS 227–231 五叶的指标挂接核对。格式沿同目录 VIZ 侧算法会签；会签环境同样未见 metric-registry MCP，本文与分册一样不做指标注册查询

## 结论

同意会签

## 核对

| 项 | 分册写法 | 对算法判定 |
|---|---|---|
| `simulate.run` 行为声称 | 第 3 节：「`run()` 只做省级力度情景：从 `ads.policy_intensity` 取 `scope_type='province'` 且力度指数非空的省，按指数从高到低最多 12 个省，用文件内已有的三条情景弹性写出基线、推演值、变化率和逐年曲线，写入 `ads.policy_simulate`。每一行的 `metric_id` 固定为字面量 `M_POLICY_SIMULATE`。函数不写方案、参数档、路径节点、风险、专家意见，插入行里也没有 `M_POLICY_DS_11_POLICY_EVAL_015`」 | ✅ 逐句与 `simulate.py` 相符：`WHERE scope_type='province' AND intensity_index IS NOT NULL`、`ORDER BY intensity_index DESC`、`provs[:12]`、文件内 `SCENARIOS` 三条、truncate 后 insert `ads.policy_simulate`、行上 `"metric_id": "M_POLICY_SIMULATE"` 字面量；全文件无 015、无方案/路径/意见字段 |
| 模型注册表描述 | 第 2 节末段与第 7 节表：`POLICY_SIMULATE` 把 `M_POLICY_SIMULATE` 与 `M_POLICY_DS_11_POLICY_EVAL_015` 列在同一 `metric_ids` 下，`handler_module` 是 `polan.text.simulate`，`ads_table` 是 `ads.policy_simulate`；「函数本身不产出 015」 | ✅ 与 `cfg_model_registry.yaml` `POLICY_SIMULATE` 项逐字吻合；「并列表 ≠ 有产出」的区分准确，且据此正确推出 229 不去读 `ads.policy_simulate` |
| 229 沿用 015、GRAPH、D4=mock | 第 1 节表、第 2 节表、第 4 节、第 5 节：沿用已有号，不新注册，不改 D4 | ✅ 判定成立。015 无产出函数（代码侧证实）；类型与 D4 只转述 `指标与501.md` 229 行与架构稿，分册诚实标注「不是 metric-get 的返回」；本次会签同样未见 metric MCP，D4=mock 以两份纸面一致转述为准 |
| 227/228/230/231 留空、不新注册、不改 D4 | 第 6 节总段与 6.1–6.4、第 8 节：指不到专属 id 就留空；不把 015 指进四叶，不把 `M_POLICY_SIMULATE` 指进 228，不把 `M_POLICY_LAYOUT_REC_COUNT` / `M_POLICY_DEEP_171_1` 指进 227 | ✅ 与 API/DATA 两册一致；点名不挂表逐条成立，无错挂 |
| `M_POLICY_SIMULATE` 不挂 228、不读 `ads.policy_simulate`、不现算 | 第 6.2 节、第 7 节表、第 8 节 | ✅ 三重封死（不挂、不读、不调用 `run()`），与代码事实一致：省级力度情景与方案参数模拟粒度不同，不可复用 |
| 八件套诚实性 | 第 3 节：未见 MCP 不填中文名、口径、公式、注册源表、源系统、更新频率、`version`；不手抄公式、不把情景弹性收成 228/229 可算的新公式 | ✅ 算法侧认可：不伪造身份字段，不把 `SCENARIOS` 弹性包装成方案/路径公式 |
| 不改代码与注册表 | 第 8 节：不改 `simulate.py`、不改 `cfg_model_registry.yaml` | ✅ 分册未触碰；本会签同样只读 |
| 015 与 241 互不顶替 | 第 5 节、第 7 节表：015 只留在 229；241 仍无专属号，不让 241 顶替 229 | ✅ 双向封死，与架构稿 5.3 一致 |

### 算法侧补充

- 本分册对「注册表把 015 列在 `POLICY_SIMULATE` 下」这一登记噪音的处理是本次会签的关键点：以 `handler_module` 实际产出为准判定 015 无产出方，而不是以 `metric_ids` 并列表推断能力。这一读法正确，避免了把推演函数误配给 229。
- 分册头部声明「本叶未调用 metric-get / metric-query」与会签环境一致（两侧都未见 metric-registry MCP），未把未查字段写成已查，诚实性成立。

## 签收边界

- 本页只做算法角色会签。未改分册、未改代码与注册表、未碰 task-registry MCP、未 commit/push。
- 不把 `POL-L2-DS11-PLAN-METRIC` 标 done 或 ready_to_sign；签收由 human:淮政玮 做。
