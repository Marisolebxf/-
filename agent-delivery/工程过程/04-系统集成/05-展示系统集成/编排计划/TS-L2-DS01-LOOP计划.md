# TS-L2-DS01 科技全域态势 · 演示样本循环（LOOP）计划

> 依据：`产品实现规程.md` §6.5（含 §6.5.7 监管人操作）。用例真源：`../合规演示用例/TS-L2-DS01-合规演示用例.md`（16 行零缺格，2026-11-07 已填）。
> 验收单：`TS-DS01-DEMO-ACCEPT-LOOP`（tech_task / qa-agent / 未收尾留 ready）。
> 监管人：human:李伟（缺省 human:淮政玮升级）。

## 状态行（每轮回写）

| 轮次 | 日期 | 探测 | 对得上 | 缺口 | 子任务 | 结论 |
|---|---|---|---|---|---|---|
| R1 | 2026-11-07 | 401「访问令牌不存在」→ 熔断 | 0/11（熔断未对照） | 熔断未评估 | 不建（熔断） | blocked：token 失效，已通知 human:李伟 |
| R2 | 2026-11-07 | 200（11 笔全 200） | 9/11 | G-R2-1 图层切换过滤回归（建议 QUERY）；观察：currentYear 空 / influence totalCount 漂移 / timeline 标签未随动 | 不建（等监管人） | 有缺口待分类；验收单保持 blocked 待监管人核对 |
| R3 | 2026-11-07 | 200（Q01 修复已部署：单选 paper 仅 paper 亮、多选 paper+patent 双亮、未选 10/10 灭） | 11/11 | 无新增（G-R2-1 已闭环：子任务 TS-DS01-LOOP-R2-Q01 done 并部署） | TS-DS01-LOOP-R2-Q01（已 done） | **样本满足，待监管人签收** |

## 1. 探测（每轮第一笔，只读）

- `POST {网关}/display/v1/situation/overview`，body `{}`，头 `Authorization: Bearer <本机 token>` + `systemCode: display`。
- 网关 `http://10.50.69.111:30895`（StripPrefix=1）。token 读 `%USERPROFILE%\.gkx\display-loop-token`，不打印、不进 git。
- **熔断**：401/424 或令牌失效文案 → 验收单 `blocked`，note「token 失效，已通知 human:李伟」，停止，不建子任务；404 → 停止，原因「接口映射不存在」，不是补数缺口。200 才进对照。

## 2. 用例集（R1 全量对照，11 行可演）

| 行 | 内容 | 端点 | 判定要点 |
|---|---|---|---|
| 1/2/3 | 总览统计/领域分布/图层切换 | situation/overview、situation/map | stats 非空、domainRows≥6、factorItems=11、切换 factor 有值 |
| 5 | 地区切换（9 市+区级） | situation/map 带 region | regions=9、区级级联可取 |
| 6（部分） | 对象点位 | situation/map | objectPoints 非空（基线 99） |
| 10 | 事件流 | situation/events | events 非空（基线 34）、类型/重要性值域齐 |
| 11/12（部分） | 时间趋势/年份切换 | situation/timeline | years 含 2025/2026、切换有数 |
| 13 | 要素对比 | overview/map 带比较参数 | 5 比较要素可切、返回有差值 |
| 14（部分） | 影响力卡片 | overview | 卡片返回（基线 5，原 6→5 已记录） |
| 15 | 主路径端到端 | 上述串行 | 开页→切图层→切地区→看趋势→看事件 全链有数 |

- **覆盖不到 5 行（4/7/8/9/16）**：检索降级、M10 未建表、详情接口未冻结——属开发/契约缺口，**不建 DATA/QUERY/ALGO 补数单**，登记「待开发完成」清单；连续两轮仍在 → 交监管人裁定（§6.5.7 步 9）。
- mock 口径：仅「会议」要素为模拟数据（1,280），演示明示；期刊/服务机构已切真源。

## 3. 判定与退出

- **对得上**：11 行全过 → 回写状态行 → 通知监管人核对；监管人说「签收」且再校验一次通过 → 验收单 `done`，操作人写 human:李伟。
- **有缺口**：按 DATA/QUERY/ALGO 分类、去重后建子任务（`ready`，**不派**——等监管人「可以派了」）；子任务只改后端数据/查询/算法，不碰本计划与用例。
- **签发**：本轮只读、只 GET/POST 查询，不创建分析任务；要补发须监管人明确说「签发」。
- **单飞**：同页同条件同时只跑一轮；已 done 验收单不改回 ready，下一轮另建。

## 4. 已知记录（不阻塞）

- events 接口不消费 regionPaths（地域筛选不生效）——演示台词回避"按地区过滤事件"。
- influence 卡片 6→5——以实测为准。
