# POL-DS10-CASE-FILL · 总派单

监管人 `human:淮政玮`。总控 `POL-DS10-CASE-FILL-长任务总控.md`。规程 `agent-delivery/产品实现规程.md` §6.4。

## 共同做法

1. 读本叶现有用例、`sdd/科技政策跟踪-系统详细设计说明书.md` §2 里本叶序号、`sdd/契约输入清单.md` 全景资源表。
2. 顺着展示服务实际读取的表做只读 SELECT。连接方式只从 `lumen-algo-py/scripts/seed/seed_synth_elem.py` 看主机和用户；口令用环境变量 `LUMEN_ALGO_MYSQL_PASSWORD`，不打印、不写入文件。
3. 优先查接口真正读的库。全景统计与目录若读 `gkxlumenx_ads` / `gkxlumenx_dwd` / `gkxlumenx_gapfill`，就查那张表。不要拿演示库行冒充正式读面，除非代码确认展示读的就是那张表。
4. 每条需规选一组现在库里存在的输入。覆盖表八列写全。主路径只串 `可演` 行。
5. 用例文首注明查库时间、库名、表名。期望旁边能回溯到哪条 SELECT。
6. handoff 写：查了哪些表、每条序号的结论、引用的原句出处。`ponytail: N/A（文档）`。不写「联调通过」。

## 禁止

不 `--apply`。不改业务仓。不改索引和另外三份用例。不建注册表任务。不打 `https://edu.itic-sci.com`。不把历史测试用例里的 401、404 改成通过。
