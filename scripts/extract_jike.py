#!/usr/bin/env python3
"""
即刻内容提取器
支持：m.okjike.com 和 web.okjike.com
"""

import json
import re
import sys
from urllib.parse import urlparse

def extract_post_id(url: str) -> str:
    """从即刻链接中提取帖子 ID"""
    # 支持的格式：
    # https://m.okjike.com/originalPosts/67d2e5b7c5c3d3d7e8f9a0b1
    # https://web.okjike.com/post/67d2e5b7c5c3d3d7e8f9a0b1
    # https://okjike.com/post/67d2e5b7c5c3d3d7e8f9a0b1
    
    patterns = [
        r'/originalPosts/([a-f0-9]+)',
        r'/post/([a-f0-9]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def parse_jike_content(html_content: str, url: str) -> dict:
    """
    解析即刻网页内容
    注意：即刻需要登录才能查看完整内容，这里返回结构供 Agent 使用 web_fetch
    """
    return {
        'platform': '即刻',
        'url': url,
        'post_id': extract_post_id(url),
        'note': '即刻内容需要登录查看，建议使用 web_fetch 获取完整内容',
        'extracted_fields': {
            'author': '从页面 meta 或 JSON-LD 提取',
            'content': '从 .content 或 [data-testid="post-content"] 提取',
            'created_at': '从 time 标签提取',
            'likes': '从 .like-count 或互动按钮提取',
            'comments': '从 .comment-count 提取',
        }
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_jike.py <url>", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    post_id = extract_post_id(url)
    
    if not post_id:
        print(json.dumps({
            'error': '无法提取帖子 ID',
            'url': url
        }, ensure_ascii=False))
        sys.exit(1)
    
    result = {
        'platform': '即刻',
        'url': url,
        'post_id': post_id,
        'note': '即刻网页版需要登录，建议：\n1. 使用 web_fetch 获取页面内容\n2. 或使用移动端分享链接',
        'web_fetch_ready': True,
        'selectors': {
            'author': 'meta[property="og:title"], .user-name, [data-testid="user-name"]',
            'content': 'meta[property="og:description"], .content, [data-testid="post-content"]',
            'time': 'time, .time, [data-testid="post-time"]'
        }
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
