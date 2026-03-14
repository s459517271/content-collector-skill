#!/usr/bin/env python3
"""
Deduplication - 检查链接是否已存在
支持：飞书文档内容检查、本地缓存检查
"""

import json
import re
import os
from urllib.parse import urlparse

# 缓存文件路径
CACHE_FILE = os.path.join(os.path.dirname(__file__), '..', '.cache', 'collected_urls.json')

def ensure_cache_dir():
    """确保缓存目录存在"""
    cache_dir = os.path.dirname(CACHE_FILE)
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

def load_cache():
    """加载已收藏的 URL 缓存"""
    ensure_cache_dir()
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_cache(cache: dict):
    """保存 URL 缓存"""
    ensure_cache_dir()
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def normalize_url(url: str) -> str:
    """标准化 URL，去除追踪参数"""
    # 去除常见追踪参数
    tracking_params = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 
                       'utm_content', 'fbclid', 'gclid', 'ref', 'source']
    
    parsed = urlparse(url)
    # 重建 URL，去除查询参数
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    
    # 保留非追踪参数
    from urllib.parse import parse_qs, urlencode
    query_params = parse_qs(parsed.query)
    filtered_params = {k: v for k, v in query_params.items() if k not in tracking_params}
    
    if filtered_params:
        query_string = urlencode(filtered_params, doseq=True)
        return f"{base_url}?{query_string}"
    return base_url

def extract_url_from_text(text: str) -> list:
    """从文本中提取所有 URL"""
    url_pattern = r'https?://[^\s<>"\')\]]+(?:\([^\s]*\))?'
    urls = re.findall(url_pattern, text)
    return [normalize_url(url) for url in urls]

def is_duplicate(url: str, doc_content: str = None) -> dict:
    """
    检查 URL 是否已存在
    
    Returns:
        {
            'is_duplicate': bool,
            'source': str,  # 'cache' | 'document' | 'none'
            'normalized_url': str,
            'message': str
        }
    """
    normalized = normalize_url(url)
    
    # 1. 检查本地缓存
    cache = load_cache()
    if normalized in cache:
        return {
            'is_duplicate': True,
            'source': 'cache',
            'normalized_url': normalized,
            'message': f'链接已在缓存中 (收藏于 {cache[normalized].get("date", "未知时间")})'
        }
    
    # 2. 检查飞书文档内容
    if doc_content:
        existing_urls = extract_url_from_text(doc_content)
        if normalized in existing_urls or url in existing_urls:
            return {
                'is_duplicate': True,
                'source': 'document',
                'normalized_url': normalized,
                'message': '链接已在飞书文档中'
            }
    
    return {
        'is_duplicate': False,
        'source': 'none',
        'normalized_url': normalized,
        'message': '新链接，可以收藏'
    }

def add_to_cache(url: str, metadata: dict = None):
    """添加 URL 到缓存"""
    cache = load_cache()
    normalized = normalize_url(url)
    
    from datetime import datetime
    cache[normalized] = {
        'original_url': url,
        'date': datetime.now().isoformat(),
        'metadata': metadata or {}
    }
    save_cache(cache)

def main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 deduplicate.py <url> [doc_content_file]", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    doc_content = None
    
    if len(sys.argv) > 2:
        with open(sys.argv[2], 'r', encoding='utf-8') as f:
            doc_content = f.read()
    
    result = is_duplicate(url, doc_content)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
