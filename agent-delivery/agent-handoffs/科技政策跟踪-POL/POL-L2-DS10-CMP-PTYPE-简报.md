# POL-L2-DS10-CMP-PTYPE · FDE 波次简报（216 政策类型列出数）

- 触发：`human:淮政玮` 2026-11-11 报障「对标结果可视化展示 · 政策类型为空」
- FDE 判定：**需求**（设计没写到），非缺陷；当次会话口径裁定 = **文种临时默认 🟡**，增补 QPOL-01（客户决策清单跟踪表 §2.aa）
- 总控：`POL-L2-DS10-CMP-PTYPE-FDE` · 五波次 A→E 全部落地

## 波次产物

| 波次 | 任务 | 产物/证据 |
|---|---|---|
| A 产品定义 | `...-PROD-L01` | 说明书 216 功能设计回写；QPOL-01 登记 |
| B 架构定档 | `...-ARCH-L01` | 定档=中档（数据源/读口变化）；读法=DWD 文种按省聚合、计件下推库端 |
| C 会签 | （并入 A/B 收口） | product+arch 会签通过，data/api 知会 |
| D 实现 API | `...-API-L01` | `lumen-svc-platform` `a795cd1`：`PolicyGapfillController` 增 `policy_types` 块；display 透传；CI 绿 |
| D 实现 FE | `...-FE-L01` | `lumen-ui-science-pc` `48f486b`+`a647090`：`compareLive.ts` 映射 + 表格列 + 🟡 QPOL-01 角标 + 图轴过滤；自检/CI 绿 |
| E 用例+复测 | `...-QA-L01` | 合规演示用例 216 行冻结；LOOP 第四轮读面全绿；handoff `POL-L2-DS10-CMP-PTYPE-QA-L01.md` |

## 复测结论（2026-11-11 LOOP 第四轮）

- `GET /display/v1/policy/panorama/stats`（`compare_field=支持力度+政策类型`）→ `policy_types.records` 2 行：**北京市 `实施细则 3`、广东省 `目录 14`**
- 回归锚点：`support_strength`（58 / 时点 2026-11-10）、`benchmark_objects`（31 行）未回归
- 218 可视化：政策类型列不进雷达/柱状/热力数值轴（文本值）
- 空态：无文种省份显示 `—`，不造 0

## 签收与遗留

- 签收：**2026-11-11 17:32 `human:hzw` 会内确认「确认并签收」，五张波次单 + FDE 总控全部签收 `done`，本 FDE 闭环。**（原「现态：五张波次单 ready_to_sign」条目已被本条替代）
- **QPOL-01 仍 🟡**：文种临时默认口径待甲方确认；确认前界面角标不得去；甲方定级分类后按 §6.4 重冻结用例 216 行。
- 界面目检：接口读面已验；K8s dev 页面上「政策类型」列建议人工过一眼（本地不编译，未做浏览器截图证据）。
