# 脚本质量只读扫描 · KJZTFWXT

> 父控 ad-hoc · 2026-10-15 22:10 CST  
> **范围**：结构 / `--check` 干跑 / skip 配额 / 闸门；**未**做 S3 全量机跑（不能替代 runtime 绿）。  
> **未改**任何 `cases/*.yaml`。

## 总判

| 维度 | 结论 |
|------|------|
| FUNC↔脚本 1:1 + health | ✅ 774/774；gap=0；rework=0 |
| expect 双层 / 裸串 | ✅ 无裸字符串；note 齐；manual≈38 条 expect |
| runner `--check`（解析+assert 编译） | ⚠ **33/34 入口绿**；`enterprise/pain` **1** 处编译红 |
| 金样 A `allow_skip` | ✅ 0 |
| B 档 skip≤25%/入口 | ❌ **7 入口超阈**（最高 46.7%） |
| skip `ticket`+`skip_reason` 字段 | ⚠ 约 **27** 条裸 skip（多在 note/抛错串里写 ALLOW_SKIP，缺规范字段） |
| fixtures | ⚠ `service/maintenance` 缺 `testdata.yaml`；全入口有 env-gate + coverage |
| index↔disk | ⚠ `service/maintenance` `all:` 含 **P0-11 重复** |
| 运行时通过率 | ⏸ 本扫未跑浏览器；本地 runs 多为单条自检/验收，无系统级 S3 汇总 |

**一句话**：补齐波「有文件且可解析」质量大体合格；主要债在 **B 档 skip 配额超标 + ticket 字段不齐 + 1 条 assert 编译坏**，不是缺口条数。

---

## 1. 结构（gap / health）

| 指标 | 值 |
|------|----|
| 入口 / 脚本 | 34 / 774 |
| gap / health rework | 0 / 0 |
| tier A / B | 195 / 579（无缺 tier） |
| env-gate | pass=28 · partial=2 · **fail=4** |
| env-gate fail | `enterprise/eval-business`, `enterprise/eval-tech`, `industry-center/sz-compare`, `service/org-capability` |

> PyYAML 对 15 个文件报解析错（locators 未引号含 `{ name:` 等）——**runner 极简解析器可吃**；`--check` 这些入口均为 PASS，不计入交付红。

---

## 2. runner `--check`（全 34 入口）

```text
PASS 33
FAIL  1  enterprise/pain  → P1-08.expect[0] 编译失败
         Invalid regular expression: missing /
         原因：assert 里 t.match(/诊断维度：([^  ← 字符类被 YAML 折行打断
```

其余入口 `--check` 均报告「assert 编译错误 0 处」。  
另见：`P1-08` 的 `allow_skip:` 写成了中文说明串，不是 `true`（字段形态也不合格）。

---

## 3. allow_skip 配额（method-patch §2）

全局：`74/774 ≈ 9.6%`（看起来不高），但**按入口**超 25% 的有 7 个：

| dir | skip/cases | % |
|-----|----------:|--:|
| `service/org-trend` | 7/15 | **46.7** |
| `industry-center/regional-index` | 7/16 | **43.8** |
| `enterprise/eval-business` | 12/30 | **40.0** |
| `industry-center/bottleneck` | 10/25 | **40.0** |
| `service/chain-graph` | 10/25 | **40.0** |
| `industry-center/regional-compete` | 8/25 | **32.0** |
| `service/portal` | 6/22 | **27.3** |

规范字段审计（粗）：

| 形态 | 约数 |
|------|-----:|
| `ticket:` + `skip_reason:` 齐全 | 41 |
| 正文/note 含 GAP/ENV/缺陷等（松） | 6 |
| **裸 skip**（无 ticket 字段） | **27** |

典型：`enterprise/eval-business/P0-09` 等靠 assert 内 `throw new Error('ALLOW_SKIP: …')` + `as_built_note`，未落 `ticket` / `skip_reason`。

---

## 4. 其它边角

| 项 | 状态 |
|----|------|
| `service/maintenance` `index.all` | `P0-11` 重复一行（`--only` 会跑两遍） |
| `service/maintenance` fixtures | 缺 `testdata.yaml` |
| catalog / 用例册自动化列 | 本波 kickoff 未做（另项） |

---

## 5. 建议处置（给人拍板，父控不擅自开波）

| 优先级 | 动作 |
|--------|------|
| P0 | 回炉 `enterprise/pain/P1-08`：修正则折行 + 规范 `allow_skip`/`ticket` |
| P1 | 7 个超阈入口：砍脚本改「本轮不自动化」或补环境后去 skip，使 B≤25% |
| P1 | 27 条裸 skip：补 `skip_reason` + `ticket`（或改为 coverage 声明不自动化） |
| P2 | `service/maintenance`：去重 `all:`、补 `testdata.yaml` |
| P2 | 开 S3 smoke（34×gold）才能回答「机跑绿」——本扫不能替 |

---

## 命令备忘

```bash
python3 agent-delivery/qa/as-built/tools/gap-func-vs-scripts.py --system KJZTFWXT --write
# 每入口：
node agent-delivery/qa/as-built/tools/run-scripts.mjs <功能目录> --check
```
