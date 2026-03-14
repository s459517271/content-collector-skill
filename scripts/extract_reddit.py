#!/usr/bin/env python3
"""
Reddit 内容提取器
支持：reddit.com 帖子
"""

import json
import re
import sys
from urllib.parse import urlparse

def extract_post_info(url: str) -> dict:
    """从 Reddit URL 提取帖子信息"""
    # 格式：
    # https://www.reddit.com/r/subreddit/comments/abc123/title/
    # https://reddit.com/r/subreddit/comments/abc123/title/
    
    pattern = r'/r/([^/]+)/comments/([a-z0-9]+)'
    match = re.search(pattern, url)
    
    if match:
        return {
            'subreddit': match.group(1),
            'post_id': match.group(2)
        }
    
    return {}

def parse_reddit_content(url: str) -> dict:
    """
    解析 Reddit 帖子
    返回结构供 Agent 使用 web_fetch 或 JSON API
    """
    info = extract_post_info(url)
    
    if not info:
        return {
            'error': '无法解析 Reddit URL',
            'url': url
        }
    
    # Reddit JSON API: 在 URL 后加 .json
    json_url = url.rstrip('/') + '.json'
    
    return {
        'platform': 'Reddit',
        'url': url,
        'json_api_url': json_url,
        'subreddit': info.get('subreddit'),
        'post_id': info.get('post_id'),
        'note': 'Reddit 提供 JSON API，在 URL 后添加 .json 即可获取结构化数据',
        'web_fetch_ready': True,
        'json_api': {
            'url': json_url,
            'method': 'GET',
            'headers': {
                'User-Agent': 'Mozilla/5.0 (compatible; ContentBot/1.0)'
            }
        }
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_reddit.py <url>", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    result = parse_reddit_content(url)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
