# KG-7ELEM-BUILD-REQ-L04 · 必须三元组的建图动作与缺口

> 日期：2026-10-30  
> 任务：`KG-7ELEM-BUILD-REQ-L04`  
> 输入只认当前 `KG-7ELEM-BUILD-REQ-L03-必须三元组与关系.md` 的必须边 M01–M24。该稿必须 24 条，可选 0 条。编号以该稿为准，不沿用上一版 M 号。不新增、不删除必须边。  
> 服务机构 `participates` 服务机构不进本表。L03 写 A21 方向待确认。L06 `SVC_RE_SVC_SVC` 即使写了 `participates`，也不加回。  
> 流水线只对照 `SYSINT-SCHEME-07-L03-算法中台上图台账.md` 与 `SYSINT-SCHEME-07-L06-算法中台入图流程.md`。表名只抄这两份里已经写出的名字。没有写死的写待确认。  
> 建图不放进页面请求。正式空间仍是技术方案里的 `demo_gkx_chain`。本叶不写接口，不改图空间，不配 GDF。

判定：

- **沿用**：台账或 L06 里已有写图，边名与本行必须边相同，起终点都落在同一对七要素上。触发改为离线，不进页面请求。
- **离线补边**：上述材料里没有这条同名同端点的写图。离线补边，不进页面请求。
- 只同名、或只同端点，都记「无」。`cite` 的技术—技术是 M06，政策—政策是 M16，不互相并。`research_coop` 不并进 M02，`talent_coop` 不并进 M01。

| 必须边 | 建图动作 | 抽取来源占位 | 同名同端点写图流水线 | 缺口 |
|---|---|---|---|---|
| M01 人才 cooperate 人才 | 离线补边。不进页面请求 | 待确认 | 无。台账 `cooperate` 的两端是企业。台账 `talent_coop` 是人才—人才，边名不同 | 无同名同端点写图。人才—人才的 `talent_coop` 是 M20，不并进本行 |
| M02 科研机构 cooperate 科研机构 | 离线补边。不进页面请求 | 待确认 | 无。台账 `cooperate` 的两端是企业。台账 `research_coop` 是科研机构—科研机构，边名不同 | 无同名同端点写图。科研机构—科研机构的 `research_coop` 是 M19，不并进本行 |
| M03 人才 cooperate 科研机构 | 离线补边。不进页面请求 | 待确认 | 无。台账没有人才—科研机构的 `cooperate` | 无同名同端点写图 |
| M04 人才 belong 科研机构 | 离线补边。不进页面请求 | 待确认 | 无。材料里的边名是 `belongs_to`、`industry_belong`、`parent_sub`，没有 `belong` | 无同名写图。`belongs_to` 的端点是环节→链，或机构→产业 |
| M05 科研机构 belong 科研机构 | 离线补边。不进页面请求 | 待确认 | 无。没有科研机构→科研机构的 `belong` | 无同名写图。`parent_sub` 的两端是企业，那是 M24 |
| M06 技术 cite 技术 | 离线补边。不进页面请求 | 待确认 | 无。L06 `POLICY_RE_CITE` 的 `cite` 两端是政策 | 同名不同端点。政策—政策的 `cite` 是 M16，不并进本行。台账写算法中台无论文、专利、项目写图 |
| M07 人才 participate 技术 | 离线补边。不进页面请求 | 待确认 | 无。台账写技术域无论文、专利、项目写图。L06 `CHAIN_RE_INDUSTRY_TECH` / `_TALENT` 写明不写 | 边名是 `participate`。已有的 `participates` 是挂到环节，端点不是技术 |
| M08 科研机构 participate 技术 | 离线补边。不进页面请求 | 待确认 | 无。台账写技术域无写图 | 没有科研机构→技术的 `participate` |
| M09 人才 author_of 技术 | 离线补边。不进页面请求 | 待确认 | 无。台账与 L06 都没有 `author_of` | 无同名写图。技术域台账写无写图 |
| M10 科研机构 publish 政策 | 离线补边。不进页面请求 | 政策点：L06 写 `policy_base_info`。`publish` 关系表名待确认 | 无。L06 `POLICY_NER_POLICY` 只写政策点。台账写无 Policy 写图；L06 已取代该句，取代后的算子里仍没有 `publish` | 无 `publish` 写图 |
| M11 政策 policy_relate 政策 | 离线补边。不进页面请求 | 待确认 | 无。L06 政策—政策写的边名是 `cite` | 边名不同。政策—政策的 `cite` 是 M16，不并进本行 |
| M12 政策 policy_apply_to 企业 | 离线补边。不进页面请求 | 待确认 | 无。L06 `POLICY_RE_SUPPORT` 的边名是 `support`，对端写成产业或企业 | 边名不同。不把 `support` 当成 `policy_apply_to` |
| M13 政策 policy_apply_to 人才 | 离线补边。不进页面请求 | 待确认 | 无。L06 没有政策→人才的边 | 无同名同端点写图 |
| M14 政策 policy_apply_to 科研机构 | 离线补边。不进页面请求 | 待确认 | 无。L06 `POLICY_RE_APPLY_TO` 的边名是 `apply_to`，对端写成机构或服务 | 边名不同，对端也没有限定科研机构 |
| M15 产业链环节 depends_on 产业链环节 | 沿用。离线触发，不进页面请求 | 待确认。L03 写这两行只缺表名。L06 只写「环节上下游」，没有表名 | 有。台账 `depends_on`：segment → segment。L06 `CHAIN_RE_DEPENDS_ON` 同名同端点 | 对端不在图上则 `no_stable_id`。现行入口是图谱接口，本叶不沿用该入口 |
| M16 政策 cite 政策 | 沿用。离线触发，不进页面请求 | 政策点：L06 写 `policy_base_info`。`cite` 关系表名待确认。L06 只写上位政策须能解析成已有 `policy_id` | 有。L06 `POLICY_RE_CITE` 边名 `cite`，两端都是 `pol:`。台账写无 Policy 写图，L06 已取代该句 | 不并进 M06。现行入口是图谱接口，本叶不沿用该入口 |
| M17 企业 participates 产业链环节 | 沿用。离线触发，不进页面请求 | `industry_chain_entity_rel`（L06） | 有。台账 `participates`：enterprise → segment。L06 `CHAIN_RE_INDUSTRY_ENTERPRISE` 边名 `participates`，企业端 `ent:` | L03 写 A03 终点待确认，不并进本行。企业端要已有 `ent:`，否则 `no_stable_id`。现行入口是图谱接口，本叶不沿用该入口 |
| M18 服务机构 participates 产业链环节 | 沿用。离线触发，不进页面请求 | 待确认。L03 写 A26 表名未写。L06 `CHAIN_RE_INDUSTRY_SERVICE` 来源格只写「同上」 | 有。台账 §2.3 `participates`：service_institution → segment。台账 §8.3 `participates`：institution → 产业环节，且有 `upsert_participates`。L06 `CHAIN_RE_INDUSTRY_SERVICE` 边名 `participates` | 服务机构—服务机构的 `participates` 不进本表。L06 `SVC_RE_INDUSTRY` 写的是 `belongs_to`，不拿来顶本行。产业链机构端前缀是 `inst:`，产业服务 A 档是 `institution:`。本叶不改 VID。现行入口是图谱接口，本叶不沿用该入口 |
| M19 科研机构 research_coop 科研机构 | 沿用。离线触发，不进页面请求 | 关系表名待确认 | 有。台账 `research_coop`：research ↔ research。L06 `ENT_RE_RESEARCH` 边名 `research_coop` | 台账 §6 写实际写入未验证。方向与 L03 的双向一致。不并进 M02。现行入口是图谱接口，本叶不沿用该入口 |
| M20 人才 talent_coop 人才 | 沿用。离线触发，不进页面请求 | 关系表名待确认 | 有。台账 `talent_coop`：talent ↔ talent。L06 `ENT_RE_TALENT` 边名 `talent_coop` | 台账 §5 写实际写入未验证。方向与 L03 的双向一致。L06 `CHAIN_RE_INDUSTRY_TALENT` 写明不写，端点不是人才—人才。不并进 M01。L03 写 A13 终点待确认，不并进本行。现行入口是图谱接口，本叶不沿用该入口 |
| M21 服务机构 service_provide 企业 | 沿用。离线触发，不进页面请求 | 关系表名待确认。台账灌图读取 `ads.graph_node`、`ads.graph_edge`。L06 未另写 `service_provide` 的关系表名 | 有。台账 `service_provide`：service → enterprise。L06 `ENT_RE_SERVICE` 边名 `service_provide` | L03 写 A16 终点待确认，不并进本行。台账写：不在五个硬编码 TAG 里的 `node_type` 会兜底写成 `service`。现行入口是图谱接口，本叶不沿用该入口 |
| M22 企业 cooperate 企业 | 沿用。离线触发，不进页面请求 | 企业点：L06 读 `enterprise_base`。`cooperate` 关系表名待确认 | 有。台账 `cooperate`：enterprise ↔ enterprise。L06 `ENT_RE_COOP` 边名 `cooperate` | 方向与 L03 的双向一致。L03 写 A07 方向待确认，不并进本行。对端不在 `enterprise_base` 或图上无稳定 ID 则 `no_stable_id`。L06 §3.4：未发布前探活失败会停在 ADS。现行入口是图谱接口，本叶不沿用该入口 |
| M23 企业 supply 企业 | 沿用。离线触发，不进页面请求 | 关系表名待确认 | 有。台账 `supply`：enterprise → enterprise。L06 `ENT_RE_SUPPLY` 边名 `supply` | L03 写 A10 方向待确认，不并进本行。产业链 `CHAIN_RE_SUPPLIES` 写明不写，边名是 `supplies`，不拿来顶本行。现行入口是图谱接口，本叶不沿用该入口 |
| M24 企业 parent_sub 企业 | 沿用。离线触发，不进页面请求 | 关系表名待确认 | 有。台账 `parent_sub`：enterprise → enterprise。L06 `ENT_RE_BELONG` 边名 `parent_sub` | L03 写 A09 方向待确认，不并进本行。本行方向已是 enterprise→enterprise，本叶不改方向。现行入口是图谱接口，本叶不沿用该入口 |

## 计数

| 动作 | 条数 | 编号 |
|---|---:|---|
| 沿用 | 10 | M15、M16、M17、M18、M19、M20、M21、M22、M23、M24 |
| 离线补边 | 14 | M01、M02、M03、M04、M05、M06、M07、M08、M09、M10、M11、M12、M13、M14 |

必须边 24 行，编号 M01–M24，与当前 L03 必须档一一对应。可选 0 条。服务机构之间的 `participates` 无行。存储设计里的表名不进本表。
