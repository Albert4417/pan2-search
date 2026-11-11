#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""搜索 pan2 资源站，返回资源结果与详情入口。"""

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlencode

import requests

BASE_URL = os.environ.get('PAN2_BASE_URL', 'https://www.pan2.cc.cd').rstrip('/')
if not (BASE_URL.startswith('https://') or BASE_URL.startswith('http://127.0.0.1')
        or BASE_URL.startswith('http://localhost')):
    raise SystemExit('PAN2_BASE_URL 必须使用 HTTPS')
CACHE_DIR = Path(os.environ.get('PAN2_CACHE_DIR', str(Path.home() / '.cache' / 'pan2-search')))
CACHE_TTL = 600
UA = 'pan2-search-skill/1.0'
SEARCH_LIMIT = 500


class Pan2Error(RuntimeError):
    pass


def _cache_path(key):
    digest = hashlib.sha256(key.encode('utf-8')).hexdigest()
    return CACHE_DIR / (digest + '.json')


def _cached(key):
    path = _cache_path(key)
    try:
        if time.time() - path.stat().st_mtime > CACHE_TTL:
            path.unlink(missing_ok=True)
            return None
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None


def _store(key, value):
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
        temp = _cache_path(key).with_suffix('.tmp')
        temp.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
        try:
            os.chmod(temp, 0o600)
        except OSError:
            pass
        os.replace(temp, _cache_path(key))
    except OSError:
        pass


def _request(params, timeout=90, use_cache=True):
    key = BASE_URL + '/api?' + urlencode(params)
    if use_cache:
        cached = _cached(key)
        if cached is not None:
            return cached
    try:
        response = requests.get(BASE_URL + '/api', params=params,
                                headers={'User-Agent': UA}, timeout=(5, timeout))
    except requests.Timeout as error:
        raise Pan2Error('搜索超时：冷门关键词首次聚合可能需要 30 秒以上，请重试') from error
    except requests.RequestException as error:
        raise Pan2Error('网络请求失败：%s' % type(error).__name__) from error

    if response.status_code == 403:
        raise Pan2Error('站点公开搜索接口已关闭')
    if response.status_code == 429:
        retry = response.headers.get('Retry-After', '60')
        raise Pan2Error('请求过于频繁，请等待 %s 秒' % retry)
    if response.status_code != 200:
        raise Pan2Error('接口返回 HTTP %s' % response.status_code)
    try:
        payload = response.json()
    except ValueError as error:
        raise Pan2Error('接口返回不是有效 JSON') from error
    if not payload.get('success'):
        raise Pan2Error(payload.get('message') or '搜索失败')
    if use_cache:
        _store(key, payload)
    return payload


def search(query, limit=10, cloud='', start_page=1, use_cache=True):
    limit = min(max(int(limit), 1), SEARCH_LIMIT)
    results, page, total, has_more = [], start_page, 0, True
    max_pages = min(6, (limit + 99) // 100)
    while len(results) < limit and has_more and page < start_page + max_pages:
        size = min(100, limit - len(results))
        params = {'keyword': query, 'page': page, 'page_size': size}
        if cloud:
            params['cloud_name'] = cloud
        payload = _request(params, use_cache=use_cache)
        try:
            total = int(payload.get('total') or total)
        except (TypeError, ValueError):
            pass
        batch = payload.get('results')
        if not isinstance(batch, list):
            raise Pan2Error('接口返回结构异常')
        results.extend(batch)
        has_more = bool(payload.get('has_more'))
        page += 1
        if not batch:
            break
    return results[:limit], total


def render(results, total, query):
    if not results:
        return '未找到「%s」的相关资源。可尝试缩短关键词或去掉年份、清晰度。' % query
    lines = ['「%s」共 %d 条，展示 %d 条：' % (query, total, len(results))]
    for index, item in enumerate(results, 1):
        detail = item.get('detail_url') or ''
        if detail.startswith('/'):
            detail = BASE_URL + detail
        if not (detail.startswith(BASE_URL + '/detail?') or detail.startswith(BASE_URL + '/detail/')):
            detail = '暂无'
        lines.append('%d. %s — %s' % (index, item.get('name') or '未命名资源',
                                      item.get('cloud_name') or '未知网盘'))
        lines.append('   详情：%s' % detail)
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='搜索 pan2 资源站')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--limit', type=int, default=10, help='返回条数，默认 10，上限 500')
    parser.add_argument('--page', type=int, default=1, help='起始页码')
    parser.add_argument('--cloud', default='', help='按网盘筛选，如 夸克网盘、百度网盘、115网盘、磁力链接')
    parser.add_argument('--json', action='store_true', help='输出 JSON')
    parser.add_argument('--no-cache', action='store_true', help='跳过本地缓存')
    args = parser.parse_args()

    if not args.query.strip():
        print('错误：搜索关键词不能为空', file=sys.stderr)
        return 2
    try:
        results, total = search(args.query.strip(), args.limit, args.cloud.strip(),
                                max(args.page, 1), not args.no_cache)
    except Pan2Error as error:
        print('错误：%s' % error, file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({'query': args.query, 'total': total, 'results': results,
                          'base_url': BASE_URL}, ensure_ascii=False, indent=2))
    else:
        print(render(results, total, args.query))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
