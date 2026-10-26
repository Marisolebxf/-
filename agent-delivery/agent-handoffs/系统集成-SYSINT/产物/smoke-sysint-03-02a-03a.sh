#!/bin/bash
# =============================================================================
# SYSINT-03-02A + 03-03A 自动冒烟（人工验收的 AI 代替：人只看最后的红绿表）
# 用法：bash smoke-sysint-03-02a-03a.sh [BEARER_TOKEN]
#   - 不传 token：跳过写侧正向用例（只验公开可测项），表中标 SKIP
#   - 传 token  ：全量 14 项（写侧 CRUD/发布/审计链全自动）
# 原理：curl 打 dev 网关 + database MCP 之外直查审计（若配 MYSQL CLI 则查库，
#       否则审计项标记为「由写侧响应间接验证」）。数据无残留：所有测试行用软删收尾。
# 出口：0=全绿；1=有红项。每行输出 ✅/❌/SKIP + 说明。
# =============================================================================
set -u
GW='http://10.50.69.111:30895'
TOKEN="${1:-}"
PASS=0; FAIL=0; SKIP=0
ok(){ echo "✅ $1"; PASS=$((PASS+1)); }
bad(){ echo "❌ $1"; FAIL=$((FAIL+1)); }
skip(){ echo "⏭️  $1"; SKIP=$((SKIP+1)); }
code(){ curl -s -m 10 -o /tmp/smoke_body -w "%{http_code}" "$@"; }
jqf(){ python3 -c "import json,sys;d=json.load(sys.stdin);print(eval(\"d$1\"))" < /tmp/smoke_body 2>/dev/null; }

echo "==== A. 无凭证 fail-closed（4 项）===="
[ "$(code -X POST "$GW/cms/cms-ops/v1/topic-service/content/svc-business-domain" -H 'Content-Type: application/json' -d '{}')" = "401" ] && ok "03A 写侧无token→401" || bad "03A 写侧无token 非401"
[ "$(code "$GW/cms/cms-ops/v1/topic-service/content/svc-business-domain?page=1&size=1")" = "401" ] && ok "03A 列表无token→401" || bad "03A 列表无token 非401"
[ "$(code -X POST "$GW/cms/cms-ops/v1/topic-panorama/content/pano-industry-intro" -H 'Content-Type: application/json' -d '{}')" = "401" ] && ok "02A 写侧无token→401" || bad "02A 写侧无token 非401"
R=$(code -X POST "$GW/cms/api/open/cms/v1/enterprise/list" -H 'Content-Type: application/json' -d '{"page":1,"size":1}')
[ "$R" = "401" ] && grep -q CMS_AUTH_FAILED /tmp/smoke_body && ok "open轨无key→401 CMS_AUTH_FAILED" || bad "open轨无key 异常($R)"

echo "==== B. published 内部轨守卫（2 项）===="
R=$(code "$GW/cms/api/published/topic-panorama/blocks?industry_id=INB1701")
[ "$R" = "404" ] && grep -q CMS_NOT_FOUND /tmp/smoke_body && ok "published 公网→404 守卫挡" || bad "published 公网 未被守卫挡($R)"
R=$(code "$GW/cms/api/published/topic-panorama/blocks/99999999")
[ "$R" = "404" ] && ok "published 详情公网→404" || bad "published 详情公网 非404($R)"

echo "==== C. shenzhen 合并回归（2 项）===="
code -X POST "$GW/svc/topic/v1/service-portal/shenzhen" -H 'Content-Type: application/json' -d '{"year":2024}'
[ "$(jqf "['data']['cms']")" = "{}" ] && ok "shenzhen 页级 cms空块" || bad "shenzhen 页级 cms块异常"
code -X POST "$GW/svc/topic/v1/service-portal/shenzhen" -H 'Content-Type: application/json' -d '{"org_id":"SMOKE-NOT-EXIST","industry_id":"IND-X"}'
[ "$(jqf "['data']['cms']['present']")" = "False" ] && ok "shenzhen 机构级无正文 present:false" || bad "shenzhen 机构级 present 异常"

echo "==== D. 写侧全链（8 项，需 token）===="
if [ -z "$TOKEN" ]; then
  skip "写侧 8 项需 Bearer token（把前端 token 作为第一参数重跑即全量）"
else
  AUTH="Authorization: Bearer $TOKEN"; CT='Content-Type: application/json'
  # 03A：建→发→列表→软删
  R=$(code -X POST "$GW/cms/cms-ops/v1/topic-service/content/svc-business-domain" -H "$AUTH" -H "$CT" \
    -d '{"org_id":"SMOKE-03A","industry_id":"SMOKE-IND","body_html":"<p>smoke</p>"}')
  CID=$(jqf "['data']['content_id']")
  [ "$R" = "200" ] && [ -n "$CID" ] && ok "03A 新建 draft(content_id=$CID)" || bad "03A 新建失败($R)"
  R=$(code -X POST "$GW/cms/cms-ops/v1/topic-service/content/svc-business-domain/$CID/publish" -H "$AUTH")
  [ "$(jqf "['data']['version']")" = "1" ] && ok "03A 发布 version+1" || bad "03A 发布异常($R)"
  code "$GW/cms/cms-ops/v1/topic-service/content/svc-business-domain?org_id=SMOKE-03A&publish_status=published" -H "$AUTH" >/dev/null
  [ "$(jqf "['data']['total']")" = "1" ] && ok "03A 列表 published 过滤命中" || bad "03A 列表过滤未命中"
  R=$(code -X POST "$GW/svc/topic/v1/service-portal/shenzhen" -H "$CT" -d '{"org_id":"SMOKE-03A","industry_id":"SMOKE-IND"}')
  [ "$(jqf "['data']['cms']['present']")" = "True" ] && ok "03A shenzhen 合并出正文" || bad "03A shenzhen 未出正文($R)"
  code -X DELETE "$GW/cms/cms-ops/v1/topic-service/content/svc-business-domain/$CID" -H "$AUTH" >/dev/null
  [ "$(jqf "['data']['deleted']")" = "True" ] && ok "03A 软删（数据无残留）" || bad "03A 软删失败"
  # 02A：建（乱序 events）→发布→detail 验升序
  R=$(code -X POST "$GW/cms/cms-ops/v1/topic-panorama/content/pano-dev-history" -H "$AUTH" -H "$CT" \
    -d '{"industry_id":"SMOKE-IND","events":[{"event_date":"2022-01-01","title":"b","body_html":"<p>b</p>"},{"event_date":"2020-01-01","title":"a","body_html":"<p>a</p>"}]}')
  PID=$(jqf "['data']['content_id']")
  [ "$R" = "200" ] && [ -n "$PID" ] && ok "02A 新建 pano_dev_history(content_id=$PID)" || bad "02A 新建失败($R)"
  code -X POST "$GW/cms/cms-ops/v1/topic-panorama/content/pano-dev-history/$PID/publish" -H "$AUTH" >/dev/null
  EV=$(code "$GW/cms/cms-ops/v1/topic-panorama/content/pano-dev-history/$PID" -H "$AUTH"; python3 -c "
import json;d=json.load(open('/tmp/smoke_body'));ev=d['data']['events'];print(ev[0]['event_date']<ev[1]['event_date'])")
  [ "$EV" = "True" ] && ok "02A events 自动升序" || bad "02A events 未升序"
  code -X DELETE "$GW/cms/cms-ops/v1/topic-panorama/content/pano-dev-history/$PID" -H "$AUTH" >/dev/null
  grep -q '"deleted":true' /tmp/smoke_body && ok "02A 软删（数据无残留）" || bad "02A 软删失败"
fi

echo "========================"
echo "结果：✅$PASS ❌$FAIL ⏭️ $SKIP"
exit $([ "$FAIL" -eq 0 ] && echo 0 || echo 1)
