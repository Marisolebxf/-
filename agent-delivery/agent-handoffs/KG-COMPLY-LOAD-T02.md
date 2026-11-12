# Handoff — KG-COMPLY-LOAD-T02

## 任务认领

claimed_by：agent:data-agent；supervised_by：human:陈芸飞；claim_type：pull。用户已明确授权M02小批量、批量及全量入图和跑后验证。本次执行与登记册留痕在有效认领窗口内。技术执行及对账于2026-11-12 00:03:17（北京时间）完成，提交review，人工验收尚待负责人签收。

Ponytail：off。本会话直接执行固定计划和数据库核验，未启用Ponytail，未据此跳过适用交付门禁。

## 结果与口径

空间demo_gkx_chain，批次comply-20261111-t02。M02最终3,442,271条research→research cooperate：原有7,617条逐条核验跳过，本轮新增3,434,654条。全部新边写后核验通过，另独立全量回读3,442,271条完整weight/props，待新增0。最终图库数量等于源应灌数，weight合计14,715,117一致；非规范方向/自环0，非零rank0。

源表ads_institution_collaboration_yearly按institution_id < collaborator_institution_id取一侧；7,190,123年度行，跨年源对3,895,106，排除company端点452,835对，得到3,442,271条合格边，对应合格年度行6,568,617。源端缺失0，46,612个research端点写前和写后均全量通过。

weight=SUM(co_paper_count)，年度strength仅留props。VID=inst:<institution_id>，不写research点；点归T03。M19与M02同源同端点同证据，按裁定停建，记0。

T07应使用M02=3,442,271作为实灌数；6,568,617是合格年度行，不是合并后的边数。

## 存量与结构验证

M15 depends_on=1,073，DAG通过；M17 enterprise→segment participates=178,731；M22 enterprise→enterprise cooperate=94,824；research=83,745，均与写前基线一致。M19 research_coop=0。没有图DDL、research点写入、M15/M17重灌或props.batch回写。

## 实现与证据

经授权新增M02适配器scripts/t02_m02.py，批量执行器scripts/t02_m02_batch.py，全量编排scripts/t02_m02_full.py及最终审计scripts/t02_m02_audit.py。545个互斥固定分片，单连接源读取和本地跨年聚合；2个图执行器，每批200条，条件插入、完整回读、原子checkpoint及同目录排他锁。

全量计划SHA256：688371d151e30721f7ebffc8370daa39922e8249ce949070566111f895b45578。源data_version=202610201700，identity_release=institution_ads_mvp_v1_20261007；提取前后、写前、审计末尾的版本/行数/权重和画像映射摘要一致。

详细报告及全部JSON证据：[T02-M02-全量入图-20261111.md](../工程过程/04-系统集成/07-图数据库集成/T02-M02-全量入图-20261111.md)。完整源计划、明细、checkpoint留在执行机E:/aminer/gkx-orchestration/.local/t02-batch/full-20261111，未提交业务明细或凭据。

## 验证结果

- 13项单元测试通过：聚合、回读拒绝、断点、哈希、分片覆盖、DAG和超时二分。
- 旧7617条与全量计划前缀逐项一致；双执行器只读实测通过；排他锁拒绝第二个进程实测通过。
- 全量写入结束：11月11日23:34:55；独立全量复核结束：11月12日00:01:06；最终audit.status=passed：00:03:17。执行管线退出码0。
- 客户端：Windows、Python3.12.13、PyMySQL1.2.4、nebula3-python3.8.3。

## CI/CD与交付范围

分支dev。执行器及范围适配提交包括7a8f2738、44780717、e0bdbc90；固定全量计划与写前证据提交7a099515。交付为数据执行器与实测证据，不涉及应用镜像或K8s部署；未单独运行仓库CI流水线。实际验证为上述单测和真实数据库全量核验，git提交前检查通过。最终证据提交以本handoff所在Git提交为准。

## 遗留事项与风险

- 源一致性为冻结版本及前后摘要证据，不是跨查询事务快照；同版本内容若被供应方修改，需重新建立计划并复核。
- 本次未人为注入全量写入中断；恢复机制有单测和幂等检查，未声称所有故障场景均经线上验证。全量锁在Windows验证，迁移平台须验证锁实现。
- 登记册旧blocked_by是已解除的历史网络记录，备注已说明；现有MCP无单独清空接口，请维护人在人工签收时清理。不是当前数据库阻塞。
- 人工签收及后续依赖解锁由有权负责人完成，执行Agent不自行置done。

实际Token和费用未由平台提供，不填写推测值。
