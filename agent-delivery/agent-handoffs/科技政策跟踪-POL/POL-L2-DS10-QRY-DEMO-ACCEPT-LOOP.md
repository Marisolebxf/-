# POL-L2-DS10-QRY-DEMO-ACCEPT-LOOP

## 运行 2026-11-10

- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS10-QRY-合规演示用例.md`
- 库：未读。探测未过，不对照样本
- 样本满足：否
- 停止：token 失效
- 探测：`GET https://edu.itic-sci.com/tid/api/display/v1/policy/panorama/search`，参数 `keyword=人工智能&q=人工智能&limit=2`，请求头 `systemCode: display` + Bearer（本机 token 文件，不落文）。HTTP **401**，正文「访问令牌不存在」
- 验收单：`blocked`。不建 DATA / QUERY / ALGO 子任务

### 缺口

无。本轮不是样本缺口。

## 运行 2026-11-10（换令牌后再探）

- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS10-QRY-合规演示用例.md`
- 库：未直连。只读打展示网关 `https://edu.itic-sci.com/tid/api`。令牌读本机文件，不落文
- 样本满足：否
- 停止：继续
- 探测：`GET /display/v1/policy/panorama/search?limit=1`，HTTP **200**

对得上的可演行：首页单条件关键词（total 88，抽查首条标题和关键词含「人工智能」）、地区（首条城市深圳市，total 968）、发布部门（发布机关含「科技部」，total 40）、效力级别与来源国家（`rank` 为国家级，total 23）、来源海外（空列表，HTTP 200）、行业（与关键词同一请求）、198（唯一一条 `cn-gov-5737584`）、智能检索（`narration=fallback`，整句留在残差，用例允许无 Key 时回退）。

### 缺口

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| `policy_base_info.197_shenzhen_ai` | DATA | 组合检索 total=13，首条 `SYN2026111037764efd04`。199 三个 factor 与这 13 条同序，响应顺序不随 factor 变 | 8 条，首条 `18358631` | 多出来的是合成行，过滤本身拣得中。不要改查询口径去藏行 | `POL-L2-DS10-QRY-DEMO-FIX-R20261110-DATA` |
| `policy_base_info.200_national_opinion` | DATA | total=3，首条 `SYN20261107ee09ee9259`，其后 `cn-gov-7041785`、`cn-gov-5737584` | 2 条，首条 `cn-gov-7041785` | 同上，合成行也是国家级意见 | 同上 |
| `policy_favorite.user184` | DATA | 历史最新 id=297，关键词仍是电池；收藏只有 `SYN202611078144c46dc8` | 用户 184 历史 id=42；收藏 `cn-gov-6999382`、`cn-gov-7067354` | 当前令牌用户不是用例用户。不要改其他用户收藏 | 同上 |
| `policy_category_rel.sci-tech` | DATA | 覆盖不到，本轮未请求 | 关联表有「科创政策」抽取行后才可演 | 补抽取，不改主表文种 | 同上 |
| `policy_share_export.missing` | DATA | 覆盖不到 | 有导出记录才可演 | 缺表。来源「地方」不进请求，不要靠灌数冒充 | 同上 |
