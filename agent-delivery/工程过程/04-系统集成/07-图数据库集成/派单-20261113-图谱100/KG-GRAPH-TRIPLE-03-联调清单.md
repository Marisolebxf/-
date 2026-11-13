# 三域联调清单（全部待执行）

## 1. 恢复与登记

- [ ] coordinator 建 COVER-01/TRIPLE-03；MCP 读回依赖与真实认领字段，不绕过依赖。
- [ ] PLAT-09 回执确认图库恢复/容量；从实际运行容器完成认证与精确VID取数。
- [ ] DESCRIBE三域Tag/相关Edge，小样本验证 tech_rel.confidence/weight 等实际属性；不改schema。
- [ ] COVER-01 回执决定技术机构关联 partial/complete；不硬编码“已补齐”。

## 2. Python（步1完后）

- [ ] 21 op 的 /v1 与 /internal 成对注册；未知op 404、跨域op/非法参数400。
- [ ] dry_run true/false均无写调用；拒绝第二空间、错误VID前缀、超长ID及注入输入。
- [ ] 正确解码Nebula null/数字/map，不通过str(map)丢字段；边属性用原生字段。
- [ ] person/research合作正反邻接均能查到；三组cooperate不串域；M04/M02排除company。
- [ ] 二跳边界200点/500边且有truncated；无悬空输出；游标绑定请求/版本/签名。
- [ ] 排名索引完整性、唯一邻居去重、0度节点、相同分数VID稳定排序、跨页不漏不重。
- [ ] 无索引503，不将样本或第一页当全域Top榜。缓存过期显示stale或明确不可用。
- [ ] 图库不可用503，空数据200 empty，中心不存在404，缺schema503，超时504。

## 3. Java（/internal齐后）

- [ ] 纯透传，请求/响应结构一致；400/404/501/503/504原样，不包装200。
- [ ] Feign指实际lumen-algo-py部署实例，不指demo，不直连图库。
- [ ] 仅三域 /topic/v1/*/graph/ops/** 精确路由置catch-all前；GlobalFilter只剥一次。
- [ ] 不抢已有M10 /topic/v1/tech/graph/changes等路由；不改CHAIN/POLICY/ENT/SVC/COMP。
- [ ] 配置发布需平台人员按单dataId流程执行，不整包覆盖Nacos、不假称已部署。

## 4. UI（Java网关齐后）

- [ ] 三域入口可达；21op分别触发Java；正常、空态、501、不可用有真实/受控证据。
- [ ] 查询条件改变不自动跑全图；并发取消/请求序号防旧结果覆写；分页与详情可回退。
- [ ] 无Mock、无硬填数；source正确、partial机构提示、company类型/缺字段诚实显示。
- [ ] apiview逐op保存实际request/response/time/status/trace/diagram，不泄露授权头。
- [ ] type-check/构建/行为自检与走查通过；发布前按AGENTS要求当前用户确认push。

## 5. 交付

- [ ] 经网关curl记录21操作；curl依赖已配置的网关变量和运行时鉴权，不把秘密写文档。
- [ ] 源码提交/CI/部署地址/截图分别留证，离线检查与真实联调分开。
- [ ] handoff/evidence经MCP回填；实际token/费用未知则待平台回填，不编造。
- [ ] 到integration为止，签收由指定人员完成，不自行done。
