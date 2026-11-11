# POL-L2-DS10-QRY-DEMO-FIX-R20261110-DATA

- 执行：`agent:data-agent`
- 监管：`human:淮政玮`
- 日期：2026-11-10（2026-11-11 收口软删）
- 库：`demo_gkxlumenx_dwd.policy_base_info` @ `10.50.11.76`

## 现值与用例预期

| 缺口键 | 现值（收口后） | 用例预期 | 本单动作 |
|---|---|---|---|
| `policy_base_info.197_shenzhen_ai` | `keyword=人工智能&region=深圳` total=**8**，首条 **18358631** | 8 条，首条 `18358631` | 人已批准后软删 6 条 SYN（`is_deleted=1`）。另软删收口时 Mock synth 新写入的 `SYN20261111f87812d08c` |
| `policy_base_info.200_national_opinion` | `level=国家级&policy_type=意见` total=**2**，首条 **cn-gov-7041785**，次条 cn-gov-5737584 | 2 条，首条 `cn-gov-7041785` | 同上，含 `SYN20261107ee09ee9259` |
| `policy_category_rel.sci-tech` | 关联表抽取与查询修复不在本单写数范围 | 关联表有抽取结果才可演 | 不补造关联 |
| `policy_favorite.user184` | 当前令牌用户不是 184 | 用户 184 的历史与两条收藏 | 不改任何用户的收藏 |
| `policy_share_export.missing` | 表仍不存在。来源「地方」不进请求 | 覆盖不到 | 不建表，不灌数 |

199 三个 `factor` 与这 8 条同序（服务端不因排序参数改序）。过滤拣得中。

## 软删清单（`demo_gkxlumenx_dwd.policy_base_info`）

1. `SYN2026111037764efd04`
2. `SYN202611078144c46dc8`
3. `SYN2026110711a5f41cfd`
4. `SYN20261107156dd3ed5b`
5. `SYN2026110751e24aa66a`
6. `SYN20261107ee09ee9259`
7. `SYN20261111f87812d08c`（收口当日 synth 新增，污染 197）

正式行 `18358631` / `cn-gov-7041785` / `cn-gov-5737584` 仍为 `is_deleted=0`。未改过滤口径、未改前端、未改收藏。

## 验收证据 2026-11-11

- 197：`GET /display/v1/policy/panorama/search?keyword=人工智能&region=深圳` → total=8，ids=`18358631,18323060,18378985,18320515,18369119,18398039,18340257,18341932`
- 200：`GET .../search?level=国家级&policy_type=意见` → total=2，首条 `cn-gov-7041785`

## 未闭合（本单范围外）

- 类别关联 / 用户 184 收藏 / 分享导出表：仍按上表，需另单。
