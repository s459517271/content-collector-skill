#!/usr/bin/env python3
"""
微信公众号文章提取器
支持：mp.weixin.qq.com
"""

import json
import re
import sys
from urllib.parse import urlparse, parse_qs

def extract_article_info(url: str) -> dict:
    """提取公众号文章信息"""
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    
    # 提取参数
    biz = query.get('__biz', [''])[0]
    mid = query.get('mid', [''])[0]
    idx = query.get('idx', [''])[0]
    sn = query.get('sn', [''])[0]
    
    return {
        'biz': biz,
        'mid': mid,
        'idx': idx,
        'sn': sn
    }

def parse_weixin_content(html_content: str = None, url: str = '') -> dict:
    """
    解析公众号文章内容
    返回结构供 Agent 使用 web_fetch 提取
    """
    info = extract_article_info(url) if url else {}
    
    return {
        'platform': '微信公众号',
        'url': url,
        'article_info': info,
        'note': '微信公众号文章可直接使用 web_fetch 提取',
        'web_fetch_ready': True,
        'selectors': {
            'title': '#activity_name, .rich_media_title',
            'author': '#js_name, .profile_nickname',
            'content': '#js_content, .rich_media_content',
            'publish_time': '#publish_time, em#publish_time',
            'read_count': '.read-count, #js_read_count3'
        },
        'content_cleanup': [
            '移除 .rich_media_tool 工具栏',
            '移除 .qr_code_pc 二维码',
            '保留纯文本内容'
        ]
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_weixin.py <url>", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    result = parse_weixin_content(url=url)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
