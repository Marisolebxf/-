# 602 · 代码第一段 · Python 只读

仓：`repos/lumen-algo-py`。只加两条只读路由和一份不执行的建表脚本。不改 Java，不改前端，不连库，不 commit。

路由加在已经提供 `GET /internal/policy/search` 的那个文件旁边，不要再开一个应用。

## 路由

1. `GET /internal/policy/clean-candidates`
   - 查询：`mode` = `search` 或 `id`；`source` 可空（空则两源都查）；`q` 搜索词；`policy_id` 精确 id。
   - 只 SELECT 演示贴源 `{ods}.dwd_policy_base`、`{ods}.dwd_global_policy_base`。国内搜索 `title`、`publish_code`、`ministry`。海外只搜 `title`。
   - 当前行：列在时 `is_deleted = 0 AND IFNULL(is_history,0)=0`；`is_history` 不在时只滤 `is_deleted = 0`。
   - 每源一块：`rows` / `empty`（文案「这一源还没有贴源数据」）/ `id_missing`（「该 ID 不在贴源」）/ `no_hit`（「这次没搜到」）/ `read_failed`（「读取失败」）。表不存在是 `read_failed`，不是 `empty`。
   - 国内行：id、title、publish_code、ministry、publish_date。海外行：id、title、organ、publish_date。
   - 不写任何库。不读 `gkx`、不读 `policy_base_info`、不读 `script_state`。不复用 `/internal/policy/search`。

2. `POST /internal/policy/clean-judge`
   - 体：`items` = `[{source, id}]`，`rules` = 启用的规则名列表。规则名只用：去重合并、格式标准化、噪声过滤、完整性校验、一致性校验。准确性不在这条路由里算。
   - 只 SELECT 上面两表里这些 id 的列。去重合并、格式标准化有列时给出判定文案「应合并」「待标准化」，不改行。噪声、一致性没有可判定列时 `hit` 为 null，`sample` 为 null。完整性只在缺 `publish_date` 或国内缺 `ministry` 时给一条脱敏样例，否则 hit 为条数、sample 为 null。
   - 缺列不是读取失败。查询抛错才是 `read_failed`，并且不要返回 0。

## 建表脚本

新增 `scripts/mysql/policy_accuracy_demo.sql`，只建演示 ADS 的 `policy_accuracy_demo`：来源、贴源 id、演示命中说明、演示条数、写入批次标记（`demo_` 前缀）。不要在应用启动时执行。不要灌数。

## 自检

用现有测试方式加一个不连库的测试：海外搜索 SQL 不得出现 `publish_code` 或 `ministry`；读取失败不得是 0。跑这个测试。

强度：ponytail full。
