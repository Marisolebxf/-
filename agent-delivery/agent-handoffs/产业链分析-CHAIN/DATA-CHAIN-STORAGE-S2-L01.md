# DATA-CHAIN-STORAGE-S2-L01 路 浜т笟閾惧瓨鍌?S2 鈥?sources/etl/seeds + Demo ODS 寤鸿〃

> **鏃ユ湡**锛?026-08-13  
> **纭**锛歚human:鏉庝紵`锛堢洃绠?寤鸿〃 Owner锛壜?瀹炶川瀹屾垚骞舵斁琛岃繘鍏ヤ細绛?绛炬敹璺緞  
> **娣斂鐜彛寰?*锛氫富璐?= `demo_gkxlumenx_ods` 鎸夊湪绾跨害瀹氬缓琛紱鍓骇鍝?= 鍦ㄧ嚎 md vs 涓夋柟鐪熷疄鍥涜〃宸紓 md

## 浠诲姟璁ら锛堝繀濉級

| 瀛楁 | 鍊?|
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:鏉庝紵` |
| claim_type | `pull` |

## Ponytail

| 瀛楁 | 鍊?|
|------|-----|
| ponytail | `full`锛堝缓琛?鑴氭湰锛? 鏂囨。渚ф寜娲惧崟 `lite` |
| 璇存槑 | 鏈敤 YAGNI 璺宠繃鐪熸簮閾佸緥 / handoff锛涚閬撲笅娓镐粎鎸囬拡銆佺粏琛ㄧ暀缁?S3 |

## Headroom

| 瀛楁 | 鍊?|
|------|-----|
| headroom | `skip` |
| 璇存槑 | 鏈満 MCP 闈㈡澘鏈ǔ瀹氭寕杞斤紱鐢?`scripts/task-mcp-cli.mjs` |

## 闂娓呭崟

- Demo 榛樿鍐呯綉 `192.168.88.43` 瓒呮椂 鈫?鏀圭敤鍙揪鍏ュ彛 `111.198.38.90:34306` 瀹屾垚 `--apply`
- 涓夋柟 live 璧勮缂栫爜 `IC*` 涓庨摼琛?`INB*` 涓嶄竴鑷达紙寮€鏀鹃」 DIFF-03锛屼笉鎸?S2 寤鸿〃锛?
- 浠撳唴 `gkx_schema_ddl.sql` 浜т笟閾炬棫鐗囨婊炲悗锛圖IFF-04锛?

## 淇敼鍐呭

### A. 鏂囨。锛坥rchestration 路 `storage/CHAIN`锛?

- `sources/inventory.md`锛氬洓琛ㄥ瓧娈垫憳瑕?+ 寤鸿〃鍏ュ彛
- `sources/md-extract-vs-live-ods-diff.md`锛?*鍓骇鍝?*锛?026-08-13 live DESCRIBE `@183.240.141.251:3318/gkx`
- `etl/`锛歚pipeline-demo-mock` + ods/dwd/ads/es/nebula/minio/mock-ads 鎸囬拡榻愬锛汥DL 蹇収
- `seeds/README.md`锛氳鐩栫煩闃甸鏋?
- README / CHANGELOG 鍥炲～

### B. 寤鸿〃锛坉emo-algo-ent-analysis锛?

- `scripts/run_chain_ods.py`锛歮d-extract銆屼骇涓氶摼瑕佺礌搴撱€嶁啋 `demo_gkxlumenx_ods`
- `entan/llm_ods/schema.py` / `load.py`锛氭寜琛ㄥご瑙ｆ瀽涓婚敭锛汿EXT 鍓嶇紑绱㈠紩
- 宸?`--apply` 鍥涜〃锛涙嫆鍐欐寮?`gkxlumenx_ods`

### C. 涓夋柟鎺㈡祴璇佹嵁

- `gkx-mysql-raw/鍔犲伐/_chain_four_tables_live_2026-08-13.json`锛堢粨鏋勶紱瀵嗙爜浠呮湰鏈?`.env.local`锛?

## 娴嬭瘯缁撴灉

| 妫€鏌?| 缁撴灉 |
|---|---|
| `run_chain_ods.py --self-check` | OK锛堝洓琛?+ 涓氬姟閿柇瑷€锛?|
| `run_llm_ods.py --self-check` | OK锛圗NT 鍥炲綊锛?|
| `--apply` 鈫?`demo_gkxlumenx_ods` | OK 路 鍥涜〃 present锛堢粡 `111.198.38.90:34306`锛?|
| Live DESCRIBE 涓夋柟鍥涜〃 | OK 路 琛屾暟 1273 / 20000 / 20000 / 476 |

### Demo 鍥涜〃

- `dwd_industry_chain_info`
- `dwd_org_industry_tags`
- `dwd_org_industry_product_tags`
- `dwd_industry_chain_news_info`

DDL 浠撳唴锛歚storage/CHAIN/etl/demo_gkxlumenx_ods_chain_tables.sql`  
`SHOW CREATE` 鏈満鏃佽矾锛歚repos/demo-algo-ent-analysis/out/chain_demo_ods_show_create.sql`锛坄out/` gitignore锛?

## 閬楃暀椋庨櫓 / 寮€鏀鹃」

| ID | 璇存槑 | 鏄惁鎸?S3 |
|---|---|---|
| OPEN-CHAIN-DIFF-03 | 璧勮 `IC*`鈫擿INB*` | 鍚︼紙鐏屾暟/鎸傞摼鏃跺鐞嗭級 |
| OPEN-CHAIN-DIFF-04 | 鍒锋柊娌欑 DDL 鏃х墖娈?| 鍚?|
| OPEN-CHAIN-S2-02 | 浜у搧琛?`id` live=bigint锛堝湪绾挎爣銆屾暟瀛椼€嶏級宸插榻愶紱鏍蜂緥褰㈡€佹寔缁瀵?| 鍚?|
| seeds 鏍蜂緥鍊?| 鐭╅樀楠ㄦ灦宸叉湁锛屽叿浣?INSERT 灞?S3/鐏屾暟 | 鍚?|

**鏀捐 S3**锛歚DATA-CHAIN-STORAGE-S3-L01`锛坰tores mysql/es/nebula 缁嗚〃锛夆€?`human:鏉庝紵` 纭鍙紑銆?

## CI/CD

- 鍒嗘敮锛歚gkx-orchestration` 鈫?`dev`锛沗demo-algo-ent-analysis` 鈫?`dev`
- commit锛歛lgo `5c0f575`锛沷rchestration `bbdbf57`
- pipeline锛氭枃妗?鑴氭湰涓轰富锛涙棤寮哄埗 K8s rollout
- 寤鸿〃楠岃瘉锛氱洿杩?MySQL `--apply`锛堣涓婏級

## 鍙娴嬫€?

- N/A锛堝瓨鍌ㄥ畾涔?+ Demo DDL锛涙棤鏂版湇鍔★級

## 鏋舵瀯鍚堣鑷

| # | 閾佸緥 | |
|---|---|---|
| 1 | 绠楁硶鍙湪 Python | 鉁?寤鸿〃鑴氭湰鍦?Python |
| 2 | 璋冪敤閾?| 鉁?鏈秺灞?|
| 3 | Nebula | 鉁?鏈紩鍏?Neo4j |
| 4 | 鍙娴?| N/A 鏈崟 |
| 5 | CI/CD | 鉁?push 鍚庨殢浠撴祦姘寸嚎 |
| 6 | demo鈫抣umen | 鉁?浠?demo ODS |
| 7 | 鍏变韩鏍稿績 | N/A |
| 8 | ADS 鍏堣 | 鉁?S3 鍐嶇亴 stores |
| 9 | D8 Design | N/A 鏃?UI |
| 10 | D9 琛€缂?| N/A 鏈崟鏃犳寚鏍囬〉 |
| 11 | D10 浜や簰 | N/A |

## 娑夊強鏂囦欢

- `agent-delivery/data/data-design/storage/CHAIN/**`
- `agent-delivery/data/third-party-source/gkx-mysql-raw/鍔犲伐/_chain_four_tables_live_2026-08-13.json`
- `repos/demo-algo-ent-analysis/scripts/run_chain_ods.py`
- `repos/demo-algo-ent-analysis/entan/llm_ods/{schema,load}.py`
- 鏈?handoff

## Cost锛堜及锛?

| 瀛楁 | 鍊?|
|---|---|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 浼?~8鈥?2 涓囷紙澶氳疆锛?|
| actual_cost | 浼?<$5 |
| cost_warn | false |
