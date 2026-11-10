# POL-L2-DS10-QRY-FDE-L01 · 多维检索蓝色区对齐专题 · K8s 冒烟收口

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:coordinator-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（本文件为冒烟/会签收口，非本会话写码） |

## 范围与实现

- 需规 #### 197 蓝色中枢：Tab 三词、示例两套、点示例只填、最近检索分桶、热门 filter 切高级待应用。
- 前端落地在 `lumen-ui-science-pc`（波次 D `bc3820b`）；本会话只做 K8s 已发布页冒烟 + 检索 API 点验。
- 合规演示用例：`工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS10-QRY-合规演示用例.md`。

## 偏离说明

- 197 主路径「人工智能+深圳」现网 `total=13`（用例写 8）：库内新增 SYN 行；旧首条 `18358631` 仍在结果集。不改用例本轮，完整 §6.5 重冻另开。

## 产物清单

- Handoff：本文件
- 已部署前端：`gkx-lumen-pc:822bd15b` @ `http://10.50.69.111:30891/policy/tech-policy-panorama`

## 验收证据

K8s 注入登录态后点验：

| 项 | 结果 |
|---|---|
| #### 197-1 Tab 三词 | ✅ 智能检索 / 关键词搜索 / 高级检索功能 |
| #### 197-2 智能示例 | ✅ 含「深圳近三年固态电池扶持政策」等四条 |
| #### 197-2 关键词示例 | ✅ 固态电池 / 高层次人才安居 / 量子信息技术 / 智能机器人产业园 |
| #### 197-3 点示例只填不搜 | ✅ 框填入示例，结果区仍 0、未自动命中 |
| #### 197-4 最近检索 | ✅ 蓝色区下分桶；智能桶空态可见 |
| #### 197-5 热门 filter | ✅ 「深圳市」→ 高级 Tab + 待应用检索（1） |
| API 197 | ✅ 200，`total=13`，含 `18358631` |
| API 198 | ✅ 唯一 `cn-gov-5737584` |

联调通过。

## 架构合规自检

- 调用链：浏览器 → Java gateway/display →（检索）专题/Python，未越层 ✅
- 算法只在 Python：本叶前端冒烟未改 Java 算法 ✅
- Nebula：本叶不涉及图谱写 ✅
- D8 Design / D10 交互：沿用已推 Arco FE，本会话未改 UI 栈 ✅
- D9 指标：本叶蓝色区交互无新增 KPI 数字角标义务 ✅
- D12：只验 lumen NodePort，未调 demo-* ✅
- 可观测 / CI：已发布镜像点验，无新码需补埋点 ✅

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 25000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 0.5 |
| cost_warn | green |

## 遗留风险

- 197 条数漂移见「偏离」；§6.5 全量 LOOP 另单。

## CI/CD（必填）

- 分支：`origin/dev`（`lumen-ui-science-pc`）
- 部署：`zhipu-tts` / `gkx-lumen-pc:822bd15b` / NodePort `30891`
- K8s rollout：成功
