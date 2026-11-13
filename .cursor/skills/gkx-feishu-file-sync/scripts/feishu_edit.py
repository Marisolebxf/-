#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""飞书内容「拉下来改、改完推回去」：云空间文件（/file/）与在线文档（/docx/、指向 docx 的 /wiki/）。

  python feishu_edit.py pull <飞书链接> --out <本地路径>     # 拉取；同时写 <本地路径>.feishu.json 快照
  python feishu_edit.py push <本地路径>                     # 试跑：列出将要改的内容、检查线上是否被别人改过
  python feishu_edit.py push <本地路径> --apply             # 正式写回
  python feishu_edit.py --self-check

在线文档：pull 出来的 md 每段前有 <!-- b:<block_id> <类型> --> 标记，只改标记下面的文字；
不要删改标记，新增/删除段落不支持。push 只更新文字有变化的段落，其余段落与格式不动。
"""
import argparse, hashlib, json, os, re, sys, urllib.error, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import push_file as pf  # 复用凭证、令牌、覆盖上传

TEXT_KEYS = {2: 'text', 3: 'heading1', 4: 'heading2', 5: 'heading3', 6: 'heading4', 7: 'heading5', 8: 'heading6',
             9: 'heading7', 10: 'heading8', 11: 'heading9', 12: 'bullet', 13: 'ordered', 14: 'code', 15: 'quote', 17: 'todo'}
MARK = re.compile(r'^<!-- b:(\S+) (\w+)( readonly)? -->$')
HEADER = '<!-- feishu-doc {"doc": "%s"} 只改标记下面的文字；不要删改 <!-- b:... --> 标记 -->'


# ---------- HTTP ----------
def call(tat, method, path, body=None, raw=False):
    data = json.dumps(body, ensure_ascii=False).encode('utf-8') if body is not None else None
    req = urllib.request.Request(pf.BASE + path, data=data, method=method,
                                 headers={'Authorization': 'Bearer ' + tat, 'Content-Type': 'application/json; charset=utf-8'})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            b = r.read()
    except urllib.error.HTTPError as e:
        b = e.read()
        if raw:
            pf.fail(_json_or(b, e.code), '下载')
    if raw:
        return b
    r = _json_or(b, 0)
    if r.get('code') != 0:
        pf.fail(r, '%s %s ' % (method, path.split('?')[0]))
    return r.get('data', {})


def _json_or(b, status):
    try:
        return json.loads(b.decode('utf-8'))
    except ValueError:
        return {'code': -status, 'msg': b[:300].decode('utf-8', 'replace')}


# ---------- 链接 ----------
def resolve(tat, url):
    """返回 (kind, token)；kind = file | docx。wiki 节点换成真实对象。"""
    m = re.search(r'/(file|docx|wiki)/([A-Za-z0-9]+)', url)
    if not m:
        sys.exit('[x] 只支持 /file/、/docx/、/wiki/ 链接：%s' % url)
    kind, tok = m.groups()
    if kind == 'wiki':
        node = call(tat, 'GET', '/wiki/v2/spaces/get_node?token=' + tok)['node']
        kind, tok = node['obj_type'], node['obj_token']
        if kind not in ('file', 'docx'):
            sys.exit('[x] 该 wiki 节点是 %s，暂只支持 file / docx' % kind)
    return kind, tok


# ---------- 在线文档 ----------
def block_text(block):
    key = TEXT_KEYS.get(block.get('block_type'))
    if not key:
        return None, None, False
    els = block.get(key, {}).get('elements', [])
    only_runs = all('text_run' in e for e in els)
    text = ''.join(e['text_run']['content'] if 'text_run' in e else '[%s]' % next(iter(e), '?') for e in els)
    return key, text, only_runs


def list_blocks(tat, doc):
    out, page = [], ''
    while True:
        q = 'page_size=500&document_revision_id=-1' + ('&page_token=' + page if page else '')
        d = call(tat, 'GET', '/docx/v1/documents/%s/blocks?%s' % (doc, q))
        out += d.get('items', [])
        page = d.get('page_token', '')
        if not d.get('has_more'):
            return out


def render_doc(doc, blocks):
    lines, snap = [HEADER % doc], {}
    for b in blocks:
        key, text, editable = block_text(b)
        if key is None:
            continue
        lines += ['<!-- b:%s %s%s -->' % (b['block_id'], key, '' if editable else ' readonly'), text]
        snap[b['block_id']] = text
    return '\n'.join(lines) + '\n', snap


def parse_doc(content):
    blocks, cur, buf = {}, None, []
    for line in content.split('\n')[1:]:
        m = MARK.match(line)
        if m:
            if cur:
                blocks[cur] = '\n'.join(buf)
            cur, buf = m.group(1), []
        elif cur:
            buf.append(line)
    if cur:
        blocks[cur] = '\n'.join(buf).rstrip('\n')
    return blocks


def new_elements(block, text):
    key = TEXT_KEYS[block['block_type']]
    els = block[key].get('elements', [])
    style = els[0]['text_run'].get('text_element_style', {}) if els and 'text_run' in els[0] else {}
    # ponytail: 改过的段落合并成一个 text_run、沿用首段样式；段内局部加粗/链接会丢。要保留得按字符 diff 拆 run。
    return [{'text_run': {'content': text, 'text_element_style': style}}], len(els) > 1


# ---------- 子命令 ----------
def cmd_pull(tat, url, out):
    kind, tok = resolve(tat, url)
    meta = {'kind': kind, 'token': tok, 'url': url}
    if kind == 'file':
        data = call(tat, 'GET', '/drive/v1/files/%s/download' % tok, raw=True)
        open(out, 'wb').write(data)
        meta['sha256'] = hashlib.sha256(data).hexdigest()
    else:
        content, meta['blocks'] = render_doc(tok, list_blocks(tat, tok))
        open(out, 'w', encoding='utf-8', newline='\n').write(content)
    json.dump(meta, open(out + '.feishu.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('[ok] %s -> %s（%s）' % (url, out, '文件' if kind == 'file' else '在线文档，%d 段' % len(meta.get('blocks', {}))))


def cmd_push(tat, path, apply):
    side = path + '.feishu.json'
    if not os.path.isfile(side):
        sys.exit('[x] 找不到 %s：先用 pull 拉取，或用 push_file.py 直接覆盖文件' % side)
    meta = json.load(open(side, encoding='utf-8'))
    if meta['kind'] == 'file':
        online = hashlib.sha256(call(tat, 'GET', '/drive/v1/files/%s/download' % meta['token'], raw=True)).hexdigest()
        if online != meta['sha256']:
            sys.exit('[x] 线上文件在你 pull 之后被改过，已停止。重新 pull 合并后再推')
        if hashlib.sha256(open(path, 'rb').read()).hexdigest() == meta['sha256']:
            return print('[i] 本地没有改动')
        if not apply:
            return print('[dry-run] 将覆盖 %s；加 --apply 正式写回' % meta['url'])
        d = pf.overwrite(tat, path, meta['token'])
        meta['sha256'] = hashlib.sha256(open(path, 'rb').read()).hexdigest()
        json.dump(meta, open(side, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        return print('[ok] 已覆盖 version=%s' % d.get('version', '?'))

    doc, snap = meta['token'], meta['blocks']
    local = parse_doc(open(path, encoding='utf-8').read())
    missing = set(snap) - set(local)
    if missing:
        sys.exit('[x] 本地缺少 %d 个段落标记（不支持删段落）：%s' % (len(missing), ', '.join(sorted(missing)[:5])))
    changed = [bid for bid in snap if local[bid] != snap[bid]]
    if not changed:
        return print('[i] 本地没有改动')
    online = {b['block_id']: b for b in list_blocks(tat, doc)}
    plan, problems = [], []
    for bid in changed:
        b = online.get(bid)
        _, text, editable = block_text(b) if b else (None, None, False)
        if b is None:
            problems.append('%s 线上已被删除' % bid)
        elif text != snap[bid]:
            problems.append('%s 线上在你 pull 之后被改过' % bid)
        elif not editable:
            problems.append('%s 含 @人/公式等，不支持改（readonly）' % bid)
        else:
            plan.append(b)
    for p in problems:
        print('[!] 跳过 ' + p)
    for b in plan:
        print('[%s] %s\n    - %s\n    + %s' % ('apply' if apply else 'dry-run', b['block_id'], snap[b['block_id']][:80], local[b['block_id']][:80]))
    if not apply:
        return print('[i] 共 %d 段待改、%d 段跳过；加 --apply 正式写回' % (len(plan), len(problems)))
    for b in plan:
        els, merged = new_elements(b, local[b['block_id']])
        call(tat, 'PATCH', '/docx/v1/documents/%s/blocks/%s?document_revision_id=-1' % (doc, b['block_id']),
             {'update_text_elements': {'elements': els}})
        snap[b['block_id']] = local[b['block_id']]
        if merged:
            print('[!] %s 原有多段行内样式，已合并为首段样式' % b['block_id'])
    json.dump(meta, open(side, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('[ok] 已更新 %d 段' % len(plan))


def self_check():
    blocks = [{'block_id': 'A', 'block_type': 3, 'heading1': {'elements': [{'text_run': {'content': '标题'}}]}},
              {'block_id': 'B', 'block_type': 2, 'text': {'elements': [{'text_run': {'content': '第一行\n第二行'}}]}},
              {'block_id': 'C', 'block_type': 2, 'text': {'elements': [{'mention_user': {}}, {'text_run': {'content': ' 你好'}}]}},
              {'block_id': 'D', 'block_type': 27, 'image': {}}]
    content, snap = render_doc('DOC', blocks)
    assert snap == {'A': '标题', 'B': '第一行\n第二行', 'C': '[mention_user] 你好'}
    assert '<!-- b:C text readonly -->' in content and 'b:D' not in content
    assert parse_doc(content) == snap
    edited = parse_doc(content.replace('第二行', '第二行（改）'))
    assert [k for k in snap if edited[k] != snap[k]] == ['B']
    els, merged = new_elements(blocks[1], '新')
    assert els == [{'text_run': {'content': '新', 'text_element_style': {}}}] and not merged
    print('self-check ok')


def main():
    ap = argparse.ArgumentParser(description='飞书文件 / 在线文档：拉取到本地修改后写回')
    ap.add_argument('--self-check', action='store_true')
    sub = ap.add_subparsers(dest='cmd')
    p1 = sub.add_parser('pull')
    p1.add_argument('url')
    p1.add_argument('--out', required=True)
    p2 = sub.add_parser('push')
    p2.add_argument('path')
    p2.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    if a.self_check:
        return self_check()
    if not a.cmd:
        ap.error('需要子命令 pull 或 push')
    tat = pf.get_token(*pf.load_env())
    cmd_pull(tat, a.url, a.out) if a.cmd == 'pull' else cmd_push(tat, a.path, a.apply)


if __name__ == '__main__':
    main()
