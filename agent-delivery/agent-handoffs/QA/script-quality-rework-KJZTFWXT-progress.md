# 脚本质量回炉进度 · KJZTFWXT

- **父控**：qa-agent（本对话）
- **依据**：`qa/as-built/script-quality-scan-KJZTFWXT.md`
- **规约**：`script-backfill-playbook.md` 三角色；强度 ponytail full
- **验收**：独立子 agent；写手自检不算验收

## 回炉队列（人工质量债 · 非 gap 工具）

| 优先级 | 类 | 说明 |
|--------|----|------|
| P0 | COMPILE | assert 编译失败 |
| P1 | SKIP_FIELD | `allow_skip:true` 缺 `ticket`/`skip_reason` |
| P1 | SKIP_QUOTA | 入口 skip>25%（补 ticket 不够，须砍条或修环境） |
| P2 | INDEX/FIX | index 重复 / 缺 testdata |

## 批 1（已收口 · 4/4 独立验收 pass）

| # | kind | CASE | FUNC | DIR | 写稿 | 验收 |
|---|------|------|------|-----|------|------|
| 1 | COMPILE | P1-08 | FUNC-01093 | `enterprise/pain` | [写稿](10a8554d-773a-4406-a640-c091c5415d12) ✅ | [验收](aeba8e9f-eedd-4483-a164-07e686a36f94) **pass** |
| 2 | SKIP_FIELD | P0-09 | FUNC-00934 | `enterprise/eval-business` | [写稿](be2085fc-5f72-40c8-8657-b3332f5ce809) ✅ | [验收](865a69c9-d7f5-4c41-8516-92212dcb40e3) **pass** |
| 3 | SKIP_FIELD | P0-13 | FUNC-01112 | `industry-center/regional-compete` | [写稿](41c3317e-db2e-4308-a3d6-f3411fe002a0) ✅ | [验收](8e40a8f6-e497-44e2-aec8-dbec2e5d8ace) **pass** |
| 4 | SKIP_FIELD | P0-06 | FUNC-00660 | `service/org-trend` | [写稿](ab7ef906-3cdb-4547-bfb1-ef64f0a730b3) ✅ | [验收](f839f533-f6a8-422e-8984-f739a13a284b) **pass** |

## 批 2（已收口 · 4/4 独立验收 pass）

| # | kind | CASE | FUNC | DIR | 写稿 | 验收 |
|---|------|------|------|-----|------|------|
| 5 | SKIP_FIELD | P0-13 | FUNC-00611 | `industry-center/bottleneck` | [写稿](946fbe49-6e14-48b5-808e-41654198f758) ✅ | [验收](62d851ff-deb7-4f20-87c1-d12c9cbdb11e) **pass** |
| 6 | SKIP_FIELD | P0-07 | FUNC-00567 | `industry-center/regional-index` | [写稿](29a5c43d-c2a1-40bb-a14e-a0d3142eeb16) ✅ | [验收](291d394a-2ff8-46d6-9252-c075d9900d64) **pass** |
| 7 | SKIP_FIELD | P0-10 | FUNC-00936 | `enterprise/eval-business` | [写稿](5c47f533-876e-43ac-a2f8-1f2b33db0fc3) ✅ | [验收](ea9dacb1-c298-4ca0-a2c8-8e7d3343f64e) **pass** |
| 8 | INDEX/FIX | — | — | `service/maintenance` | [写稿](9f25bb58-4638-476c-bcf5-77ad1a0e62a5) ✅ | [验收](81ef7535-6a3c-40a9-882c-3170ded74ebb) **pass** |

## 批 3（已收口 · 4/4 独立验收 pass；含 2 条机跑绿去 skip）

| # | kind | CASE | FUNC | DIR | 写稿 | 验收 |
|---|------|------|------|-----|------|------|
| 9 | SKIP_FIELD | P0-14 | FUNC-00945 | `enterprise/eval-business` | [写稿](ebe98fd7-8396-4e24-aaa1-14485ef2726c) ✅ 去 skip | [验收](815a2da6-52cf-4dc4-8468-342790c31b1d) **pass** |
| 10 | SKIP_FIELD | P0-14 | FUNC-01113 | `industry-center/regional-compete` | [写稿](1cd2559e-c935-4623-b81e-99567b641838) ✅ | [验收](6ad9274a-0b2e-45e6-8cca-dad3b784ec43) **pass** |
| 11 | SKIP_FIELD | P0-08 | FUNC-00568 | `industry-center/regional-index` | [写稿](a5f68e88-8e63-4a14-888c-4051e144b509) ✅ 去 skip | [验收](2a901029-e417-472d-8e49-b3c497600b2a) **pass** |
| 12 | SKIP_FIELD | P0-07 | FUNC-00661 | `service/org-trend` | [写稿](492ac1aa-80c5-41d6-b9d5-74f0e14e8871) ✅ | [验收](8e81563e-4417-40b9-9fd8-04104693643b) **pass** |

## 批 4（已收口 · 4/4 独立验收 pass；含 2 条机跑绿去 skip）

| # | kind | CASE | FUNC | DIR | 写稿 | 验收 |
|---|------|------|------|-----|------|------|
| 13 | SKIP_FIELD | P0-15 | FUNC-00946 | `enterprise/eval-business` | [写稿](4b405eab-8478-43b6-8c0b-4242345cf6b7) ✅ 去 skip | [验收](f45fa585-3817-4b08-a9d2-047e983d816a) **pass** |
| 14 | SKIP_FIELD | P0-15 | FUNC-01114 | `industry-center/regional-compete` | [写稿](c9574224-4213-4402-b6b7-bded87369822) ✅ | [验收](3aa32104-42a2-4e93-af66-827bb56a4b40) **pass** |
| 15 | SKIP_FIELD | P0-09 | FUNC-00569 | `industry-center/regional-index` | [写稿](e972456d-ad32-4511-bb06-9283eb658759) ✅ 去 skip | [验收](0b582589-970f-47e1-b8b6-8a55f30fc7e1) **pass** |
| 16 | SKIP_FIELD | P0-08 | FUNC-00662 | `service/org-trend` | [写稿](b1513935-e4ac-40ef-9ead-5df4573bbf82) ✅ | [验收](cbcf00e0-52da-4a64-a05e-b085be4d1635) **pass** |

## 批 5（已收口 · 4/4 独立验收 pass · 2026-10-15）

| # | kind | CASE | FUNC | DIR | 写稿 | 验收 |
|---|------|------|------|-----|------|------|
| 17 | SKIP_FIELD | P0-16 | FUNC-00947 | `enterprise/eval-business` | [写稿](638210ed-a813-48f0-bbe8-a589ba162d10) ✅ 去 skip | [验收](2a197226-bd42-4f50-8d3c-df785419353a) **pass** |
| 18 | SKIP_FIELD | P0-16 | FUNC-01115 | `industry-center/regional-compete` | [写稿](34dbf860-7379-4f1a-9235-929f04723c53) ✅ | [验收](e4c997ad-45f5-4940-a080-a9aaa54fa05c) **pass** |
| 19 | SKIP_FIELD | P1-03 | FUNC-00573 | `industry-center/regional-index` | [写稿](da9f2485-0268-4819-9c80-d280f5833f0e) ✅ | [验收](9eea98c2-0542-4549-b913-b93af25de040) **pass** |
| 20 | SKIP_FIELD | P0-14 | FUNC-00612 | `industry-center/bottleneck` | [写稿](4eb20658-b1c9-4ac1-88ef-b94d0bc212b2) ✅ | [验收](3be33827-e596-4c9d-b5ec-b22149d890c2) **pass** |

## 批 6（已收口 · 4/4 独立验收 pass）

| # | kind | CASE | FUNC | DIR | 写稿 | 验收 |
|---|------|------|------|-----|------|------|
| 21 | SKIP_FIELD | P0-09 | FUNC-00663 | `service/org-trend` | [写稿](fad2c223-94bb-4be8-8171-bb307c27b6c5) ✅ | [验收](5dd3fe00-8606-46c5-a0e4-534e87e2d012) **pass** |
| 22 | SKIP_FIELD | P0-18 | FUNC-00959 | `enterprise/eval-business` | [写稿](7ca25d57-c301-46cc-adb8-6a23a0550c45) ✅ 去 skip | [验收](8573323b-38fc-45a8-92aa-0569c53fcd68) **pass** |
| 23 | SKIP_FIELD | P0-17 | FUNC-01116 | `industry-center/regional-compete` | [写稿](f393c484-d803-4c20-8a34-e7b51ddd53c5) ✅ | [验收](a9d098f3-5028-43a4-a52c-5544bbb0a576) **pass** |
| 24 | SKIP_FIELD | P1-04 | FUNC-00574 | `industry-center/regional-index` | [写稿](fb5d633f-dcbb-4a1c-8f1f-990fb92c1b95) ✅ | [验收](a8ea185c-de4b-45fc-8830-714c61e94fe9) **pass** |

## 批 7（已收口 · 3/3 独立验收 pass）

| # | kind | CASE | FUNC | DIR | 写稿 | 验收 |
|---|------|------|------|-----|------|------|
| 25 | SKIP_FIELD | P1-06 | FUNC-00951 | `enterprise/eval-business` | [写稿](2c3925f1-49eb-4a74-931e-82c3db9ae8bf) ✅ 去 skip | [验收](fba7a26d-038b-451a-b7ee-3a5be1192afc) **pass**（SKIP_FIELD；机跑 C6 红·后续另单） |
| 26 | SKIP_FIELD | P1-02 | FUNC-01118 | `industry-center/regional-compete` | [写稿](d06644ee-63ee-4f2e-b8b2-cbc645f9e6dd) ✅ | [验收](f80556a5-f269-4fd9-bd9a-3f617f6e667c) **pass** |
| 27 | SKIP_FIELD | P1-06 | FUNC-00576 | `industry-center/regional-index` | [写稿](fda590bd-f349-4c66-bd35-590530a1b6ef) ✅ | [验收](239d654f-46cc-495d-9f83-6e515555205a) **pass** |

## 批 8（已收口 · 3/3 独立验收 pass · P1-03 经回炉复验）

| # | kind | CASE | FUNC | DIR | 写稿 | 验收 |
|---|------|------|------|-----|------|------|
| 28 | SKIP_FIELD | P1-04 | FUNC-00949 | `enterprise/eval-business` | [写稿](51841746-6be8-4cea-9afb-3da0a93c9464) ✅ 去 skip | [验收](9ba07d5b-9ad5-4cf9-9a58-25d6670a91dc) **pass**（SKIP_FIELD；机跑红·模板数据） |
| 29 | SKIP_FIELD | P1-03 | FUNC-01119 | `industry-center/regional-compete` | [写稿](13221a10-f8a3-4c58-be4d-2fa88f7b0379) ✅ · [回炉写](01cec299-151a-409c-a158-768d7a4ce2ee) ✅ | fail → [复验](dd40866b-047a-423b-970c-fef8c51c0ae7) **pass** |
| 30 | SKIP_FIELD | P1-07 | FUNC-00577 | `industry-center/regional-index` | [写稿](bec4eb0d-7849-47c6-9285-c69acdd46908) ✅ | [验收](1fc4dcf8-bb02-4d50-8191-ac35547433e0) **pass** |

## 批 9（已收口 · 2/2 独立验收 pass）

| # | kind | CASE | FUNC | DIR | 写稿 | 验收 |
|---|------|------|------|-----|------|------|
| 31 | SKIP_FIELD | P1-08 | FUNC-00953 | `enterprise/eval-business` | [写稿](94cc6128-417c-4d46-b70b-ed2d7974ed9a) ✅ 去 skip | [验收](1db6558c-0d1a-4ef1-9c8b-4bf8041ba02b) **pass** |
| 32 | SKIP_FIELD | P1-04 | FUNC-01120 | `industry-center/regional-compete` | [写稿](a94e8494-c00f-4c35-a324-a772ad855187) ✅ | [验收](b3361c68-4e82-43f5-91d9-397aeefc01af) **pass** |

## 批 10（已收口 · P1-09 pass）

| # | kind | CASE | FUNC | DIR | 写稿 | 验收 |
|---|------|------|------|-----|------|------|
| 33 | SKIP_FIELD | P1-09 | FUNC-00954 | `enterprise/eval-business` | [写稿](c84381e8-3292-4c4a-9b5b-a7b1c09b032f) ✅ 去 skip | [验收](df182e63-8b80-49b4-8b3b-c106d528c454) **pass** |

## 批 11（已收口 · P1-10 SKIP_FIELD pass）

| # | kind | CASE | FUNC | DIR | 写稿 | 验收 |
|---|------|------|------|-----|------|------|
| 34 | SKIP_FIELD | P1-10 | FUNC-00955 | `enterprise/eval-business` | [写稿](2f8c0f26-7de1-4761-bae1-d0dbafa5cf86) ✅ · [回炉写](65f6f4cb-e6a3-40e0-9ebf-898e19e624ac) ✅ | fail → [复验](ed47d4bf-0436-4f4b-bb46-8f02c0593473) **pass**（稿面；机跑 C6·`20261015-50892-eval-biz-p1-10-qa-r2`·过程窗 ticket 诚实红，runner 未升格 n/a） |

## 批 12（已收口 · P1-11 SKIP_FIELD pass）

| # | kind | CASE | FUNC | DIR | 写稿 | 验收 |
|---|------|------|------|-----|------|------|
| 35 | SKIP_FIELD | P1-11 | FUNC-00956 | `enterprise/eval-business` | [写稿](1317e692-999e-4067-908b-ed104a8c5626) ✅ | [验收](ea8a6b13-840b-454b-ba5a-f94f278caa62) **pass**（稿面；机跑 C6·`20261015-50892-eval-business-r3-runner`·过程窗 ticket 诚实红） |

累计独立验收：**36** 脚本 + 1 index。**SKIP_FIELD 本波队列已清空**（裸 skip 稿面 0，待父控 gap --write 刷新）。入口 **SKIP_QUOTA >25% 仍 7**（未开波）。

## 本波 SKIP_FIELD 收口

- 起：初扫 ~27 裸 skip → 止：eval-business P1-09/10/11 + 各模块共 **36** 条独立验收 pass（含 P1-10 回炉、P1-03 reg-compete 回炉）。
- **机跑债**（非本波 blocker）：eval-business **P1-06/P1-04/P1-10/P1-11** 等过程窗/模板数据 C6 红；runner `allow_skip` 仅着陆 5s 探测 target，expect 内 ticket 仍 fail。

**债单备注**：P1-10 与 P1-11 过程窗依赖同族 ticket；若 runner 仅着陆 5s 探测 `allow_skip_target`，expect 内过程窗债仍可能机跑 fail（非 SKIP_FIELD 假绿）。

## 禁止

父写 cases；父跑正式验收机跑；有头浏览器；子改 catalog；全量刷分；git push（除非人类要求）。
