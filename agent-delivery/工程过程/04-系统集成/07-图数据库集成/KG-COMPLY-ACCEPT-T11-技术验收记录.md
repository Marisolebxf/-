# T11 技术验收记录（KG-COMPLY-ACCEPT-T11）

- 验收人：唐绍祖（总集）
- 被验交付：李周，提交 `453106752`（`docs(kg-comply): record formal graph decisions and submit T11`，2026-11-12 18:53）
- 交付物：[KG-COMPLY-T11-正式线结构覆盖对照清单.md](./KG-COMPLY-T11-正式线结构覆盖对照清单.md)、[agent-handoffs/KG-COMPLY-LOAD-T11.md](../../../agent-handoffs/KG-COMPLY-LOAD-T11.md)
- 日期：2026-11-12

## 一、结论

**签收，`review` → `done`。** 六项书面决定已回填，DoD 三条实质达成；清单从「待办提问稿」转成「本期对照口径 + 后续建线基线」两份用途合一。

本次不是简单加一节，还顺手修掉原稿两处硬错（下节 2、3），并把我 15:40 原稿里的一处数错纠正了。

## 二、我复核过的五项（逐项可复跑）

| # | 复核项 | 结果 |
|---|---|---|
| 1 | F1–F6 六项书面决定与淮政玮飞书答复是否一一对应 | 一致。F1 本期不建正式线、沿用 `10.50.75.136:9669`；F2 沿用 `demo_gkx_chain` 作对照、正式空间名留待后续；F3 VID 沿用 `inst:` / `institution:` / `proj:`；F4 `first_year` 留 `props`；F5 `participates` 不补 `weight`；F6 技术点层保留结构、上线重算 |
| 2 | 边型去重段落计数（原稿「`policy_apply_to` 装 2 条」） | **原稿错，李周改对**。M12 / M13 / M14 三条都压 `policy_apply_to`，应为 **3 条**。改后自算：`cooperate` 4 + `policy_apply_to` 3 + `cite` 2 + `belong` 2 + `participate` 2 + `participates` 2 = 15，其余 9 个边型各 1 条 = 9，合计 **15 边型 / 24 关系**，与正文一致 |
| 3 | `architecture-baseline` 相对路径（原稿 `../../../../`） | **原稿链接是坏的**，李周改成 `../../../` 后指向 `agent-delivery/architecture-baseline.md`，该文件存在；v2.2.15 原文「只迁 `demo_gkx_chain`」「不建正式名 `gkx_chain`」，与 §一 引用一致，属正确引用而非自制依据 |
| 4 | 章节交叉引用是否自洽 | 一致。原「见 §五 陷阱」随 _D 段_ 占 §五、_E 段_ 进 §六 同步改到 §六；B22 备注指向「§五 D3」正确 |
| 5 | 是否越过「只读」红线 | 未越。清单全程坐标/属性均为 15:40 已归档的 `SHOW` / `DESCRIBE` 实测，无新写入、无 `gkx_chain` 建空间动作 |

## 三、DoD 逐条判定

| DoD | 判定 | 说明 |
|---|---|---|
| ① 9 Tag + 24 边逐行列「已有 / 待补 / 不适用」，不适用有书面理由 | 实质达成 | 33 行齐全，A 段 9 + B 段 24 逐行有状态、有 VID 规则、有字段、有演示库实测条数；D 段 6 项「不适用」各有书面理由。**唯一保留意见见 §四** |
| ② 技术点层单列可选段，不计入最低覆盖 | 达成 | C 段 5 Tag + 6 边单列，明写「不计入 A、B 两段的最低覆盖范围」；`weighted_degree` 与边集不自洽的老问题已改为「上线后随线上总集重算」，不再要求原样搬运 |
| ③ 不往 `gkx_chain` 写任何点边；交 WBS-07-00G/00H 消费 | 达成 | 无写入动作；F 段明写「供 WBS-07-00G / 00H 参考」，§九 给出后续对照用法 |

## 四、唯一保留意见（P2，不阻塞 done）

**「不适用」一词在文内被用了两种含义**：

- A、B 两段 33 行：`不适用（本期）` = 本期没有正式线实例可核验，**将来要建**；
- D 段 6 项：`不适用` = **永不建议照搬**（历史混装边、M22 碎片形态等）。

同一个词在 A/B 段与 D 段含义相反，WBS-07-00G/00H 的读者容易把「将来要建」读成「不用建」。§一 已就地定义，本轮不返工；**建议将来正式线立项时，把 A/B 段标签改回「待补」**，词义即恢复与 DoD 原文一致。

## 五、15:40 原稿需要我自己认的两处

1. `policy_apply_to` 数 2 条 → 实为 3 条（见 §二 #2）：这是我原稿错，李周修掉的；
2. 相对路径 `../../../../architecture-baseline.md` → 实际应为 `../../../`（见 §二 #3）：原稿链接指到仓根找不到文件。

两处都不影响结论，但说明交付件到第二手会被人逐字核，我原稿的算术错和路径错属于我这一侧的质量问题，记在此留档。

## 六、复核命令（可复跑）

```bash
# 15 边型 / 24 关系自算
python3 -c "
from collections import Counter
c=Counter({'cooperate':4,'cite':2,'belong':2,'participate':2,'participates':2,'policy_apply_to':3})
print('边型数',len(c)+9,'关系数',sum(c.values())+9)"

# 基线路径是否可达
ls agent-delivery/architecture-baseline.md

# 基线 v2.2.15 原文
grep -n 'v2.2.15' agent-delivery/architecture-baseline.md
```
