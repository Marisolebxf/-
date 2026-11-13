#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把本地文件覆盖上传到飞书云空间已有文件（= 网页「上传新版本」，链接和 file_token 不变）。

官方接口：POST /open-apis/drive/v1/files/upload_all，多传 file_token 即原地覆盖（lark-cli drive +upload --file-token 同语义）。
用法：
  python push_file.py --pair <本地文件> <飞书链接或file_token> [--pair ...]          # 试跑：只取令牌、核对文件
  python push_file.py --pair ... --apply                                           # 正式覆盖
  python push_file.py --self-check                                                 # 离线自检
凭证：LARK_APP_ID/LARK_APP_SECRET 或 FEISHU_APP_ID/FEISHU_APP_SECRET；都没有时读编排仓 .env。
"""
import argparse, json, os, re, sys, time, urllib.error, urllib.request, uuid, zlib

BASE = 'https://open.feishu.cn/open-apis'
MAX_SIZE = 20 * 1024 * 1024  # upload_all 上限；更大要走分片接口
HINTS = {
    99991672: '应用没开云空间权限：开发者后台给应用开 drive:file:upload（或 drive:drive），并创建版本发布',
    99991663: 'APP_ID / APP_SECRET 不对',
    1061004: '应用不是该文件的协作者，或只有阅读权限：在飞书文件「…→ 文档权限 / 添加文档应用」里把应用加为可编辑',
    1061002: 'file_token 不对，或文件已被删除',
    1061045: '飞书内部可重试错误，稍后重跑',
}


PREFIXES = ('FEISHU_DRIVE_APP', 'LARK_APP', 'FEISHU_APP')  # 按顺序取第一组 ID+SECRET 都有的


def load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '.env')
    dotenv = {}
    if os.path.isfile(env_path):
        for line in open(env_path, encoding='utf-8', errors='replace'):
            m = re.match(r'\s*([A-Z_]+)\s*=\s*(.*?)\s*$', line)
            if m and m.group(2):
                dotenv.setdefault(m.group(1), m.group(2).strip('"\''))
    for src in (os.environ, dotenv):
        for p in PREFIXES:
            if src.get(p + '_ID') and src.get(p + '_SECRET'):
                return src[p + '_ID'], src[p + '_SECRET']
    sys.exit('[x] 缺少凭证：设置 FEISHU_DRIVE_APP_ID / FEISHU_DRIVE_APP_SECRET（环境变量或编排仓 .env）')


def parse_token(target):
    """接受 https://xxx.feishu.cn/file/<token>?... 或裸 token。只支持云空间普通文件（/file/）。"""
    m = re.search(r'/(file|docx|docs|sheets|wiki|base)/([A-Za-z0-9]+)', target)
    if m:
        if m.group(1) != 'file':
            sys.exit('[x] %s 不是云空间文件（/file/）链接；在线文档/表格不能用文件覆盖' % target)
        return m.group(2)
    if re.fullmatch(r'[A-Za-z0-9]{20,}', target):
        return target
    sys.exit('[x] 认不出 file_token：%s' % target)


def build_multipart(fields, file_name, content):
    boundary = '----gkx' + uuid.uuid4().hex
    parts = []
    for k, v in fields.items():
        parts.append(('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (boundary, k, v)).encode('utf-8'))
    parts.append(('--%s\r\nContent-Disposition: form-data; name="file"; filename="%s"\r\n'
                  'Content-Type: application/octet-stream\r\n\r\n' % (boundary, file_name)).encode('utf-8'))
    parts.append(content)
    parts.append(('\r\n--%s--\r\n' % boundary).encode('utf-8'))
    return boundary, b''.join(parts)


def api(req):
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', 'replace')
        try:
            return json.loads(body)
        except ValueError:
            return {'code': -e.code, 'msg': body[:400]}


def get_token(app_id, secret):
    req = urllib.request.Request(BASE + '/auth/v3/tenant_access_token/internal',
                                 data=json.dumps({'app_id': app_id, 'app_secret': secret}).encode('utf-8'),
                                 headers={'Content-Type': 'application/json; charset=utf-8'}, method='POST')
    r = api(req)
    if r.get('code') != 0:
        fail(r, '取令牌')
    return r['tenant_access_token']


def fail(r, what):
    code = r.get('code')
    hint = HINTS.get(code, '')
    sys.exit('[x] %s失败 code=%s msg=%s%s' % (what, code, r.get('msg'), ('\n    → ' + hint) if hint else ''))


def overwrite(tat, path, file_token, folder_token=''):
    content = open(path, 'rb').read()
    name = os.path.basename(path)
    fields = {'file_name': name, 'parent_type': 'explorer', 'parent_node': folder_token,
              'size': str(len(content)), 'checksum': str(zlib.adler32(content)), 'file_token': file_token}
    boundary, body = build_multipart(fields, name, content)
    req = urllib.request.Request(BASE + '/drive/v1/files/upload_all', data=body, method='POST',
                                 headers={'Authorization': 'Bearer ' + tat,
                                          'Content-Type': 'multipart/form-data; boundary=' + boundary})
    for attempt in range(3):
        r = api(req)
        if r.get('code') != 1061045:
            break
        time.sleep(3)
    if r.get('code') != 0:
        fail(r, '覆盖 %s ' % name)
    return r.get('data', {})


def self_check():
    t = 'CjMRbUFaWo3XHhxM2jJciLaZnEe'
    assert parse_token('https://zhipu-ai.feishu.cn/file/%s?from=x' % t) == t
    assert parse_token(t) == t
    b, body = build_multipart({'file_token': t, 'size': '3'}, '规范.md', b'abc')
    assert body.endswith(('\r\n--%s--\r\n' % b).encode()) and b'name="file_token"\r\n\r\n' + t.encode() in body
    assert '规范.md'.encode('utf-8') in body and b'\r\n\r\nabc\r\n' in body
    print('self-check ok')


def main():
    ap = argparse.ArgumentParser(description='覆盖上传本地文件到飞书云空间已有文件（保留链接）')
    ap.add_argument('--pair', nargs=2, action='append', metavar=('LOCAL', 'FEISHU'), help='本地文件 + 飞书 /file/ 链接或 file_token，可重复')
    ap.add_argument('--folder-token', default='', help='目标文件所在文件夹 token（一般不需要；飞书要求时再传）')
    ap.add_argument('--apply', action='store_true', help='正式覆盖；不加只试跑')
    ap.add_argument('--self-check', action='store_true')
    args = ap.parse_args()
    if args.self_check:
        return self_check()
    if not args.pair:
        ap.error('至少给一个 --pair')

    jobs = []
    for local, target in args.pair:
        if not os.path.isfile(local):
            sys.exit('[x] 本地文件不存在：%s' % local)
        size = os.path.getsize(local)
        if size == 0 or size > MAX_SIZE:
            sys.exit('[x] %s 大小 %d 字节，必须在 1B–20MB 之间' % (local, size))
        jobs.append((local, parse_token(target), size))

    tat = get_token(*load_env())
    for local, tok, size in jobs:
        if not args.apply:
            print('[dry-run] %s (%d B) -> https://feishu.cn/file/%s' % (local, size, tok))
            continue
        data = overwrite(tat, local, tok, args.folder_token)
        print('[ok] %s -> file_token=%s version=%s' % (os.path.basename(local), data.get('file_token', tok), data.get('version', '?')))
    if not args.apply:
        print('[i] 令牌已取到、文件已核对；加 --apply 正式覆盖')


if __name__ == '__main__':
    main()
