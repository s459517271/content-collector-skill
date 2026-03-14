#!/usr/bin/env python3
"""
Content Extractor - 提取社交媒体内容
支持：Twitter/X、即刻、微信公众号、通用网页
"""

import sys
import json
import re
import subprocess
from urllib.parse import urlparse

def detect_platform(url: str) -> str:
    """检测链接来源平台"""
    domain = urlparse(url).netloc.lower()
    
    if any(x in domain for x in ['x.com', 'twitter.com']):
        return 'twitter'
    elif 'mp.weixin.qq.com' in domain:
        return 'weixin'
    elif any(x in domain for x in ['okjike.com', 'jike.cn']):
        return 'jike'
    elif 'reddit.com' in domain:
        return 'reddit'
    elif 'news.ycombinator.com' in domain:
        return 'hackernews'
    else:
        return 'generic'

def extract_twitter(url: str) -> dict:
    """使用 x-tweet-fetcher 提取 Twitter 内容"""
    try:
        result = subprocess.run(
            ['python3', '/root/.openclaw/workspace/skills/x-tweet-fetcher/scripts/fetch_tweet.py', 
             '--url', url],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            tweet = data.get('tweet', {})
            return {
                'platform': 'X/Twitter',
                'author': tweet.get('author', ''),
                'username': tweet.get('screen_name', ''),
                'content': tweet.get('text', ''),
                'created_at': tweet.get('created_at', ''),
                'stats': {
                    'likes': tweet.get('likes', 0),
                    'retweets': tweet.get('retweets', 0),
                    'bookmarks': tweet.get('bookmarks', 0),
                    'views': tweet.get('views', 0),
                    'replies': tweet.get('replies_count', 0)
                },
                'url': url,
                'is_article': tweet.get('is_article', False)
            }
    except Exception as e:
        return {'error': f'Twitter extraction failed: {str(e)}'}
    
    return {'error': 'Failed to extract Twitter content'}

def extract_generic(url: str) -> dict:
    """通用网页提取（使用 web_fetch）"""
    # 返回基本结构，实际提取由 Agent 使用 web_fetch 完成
    return {
        'platform': 'Web',
        'url': url,
        'note': 'Use web_fetch tool to extract content'
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_content.py --url <url>", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[2] if sys.argv[1] == '--url' else sys.argv[1]
    
    platform = detect_platform(url)
    
    if platform == 'twitter':
        result = extract_twitter(url)
    else:
        result = extract_generic(url)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
