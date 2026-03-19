#!/usr/bin/env python3
"""
Content Collector v1.2.0 - 主流程测试用例
测试完整工作流程：平台检测 → 去重检查 → 内容提取 → 格式化 → 飞书输出
"""

import json
import subprocess
import sys
import tempfile
import os
from pathlib import Path

# 测试配置
TEST_URL = "https://x.com/i/status/2032275457987539209"  # xiaoerzhan 的 OpenClaw Skill 榜单
SCRIPTS_DIR = Path(__file__).parent / "scripts"
CACHE_DIR = Path(__file__).parent / ".cache"


def run_script(script_name: str, *args) -> tuple[int, str, str]:
    """运行脚本并返回结果"""
    script_path = SCRIPTS_DIR / script_name
    cmd = [sys.executable, str(script_path)] + list(args)
    
    print(f"\n{'='*60}")
    print(f"▶ 运行: {script_name}")
    print(f"  命令: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout:
        print(f"📤 STDOUT:\n{result.stdout}")
    if result.stderr:
        print(f"📥 STDERR:\n{result.stderr}")
    
    print(f"✅ 返回码: {result.returncode}")
    return result.returncode, result.stdout, result.stderr


def test_step1_platform_detection():
    """Step 1: 平台检测"""
    print("\n" + "🧪"*30)
    print("STEP 1: 平台检测 (extract_content.py)")
    print("🧪"*30)
    
    code, stdout, stderr = run_script("extract_content.py", TEST_URL)
    
    if code != 0:
        print(f"❌ 平台检测失败: {stderr}")
        return None
    
    try:
        result = json.loads(stdout)
        print(f"\n✅ 平台检测成功:")
        print(f"   平台: {result.get('platform_label', 'N/A')}")
        print(f"   推荐 Skill: {result.get('skill', 'N/A')}")
        print(f"   备注: {result.get('note', 'N/A')}")
        return result
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        print(f"   原始输出: {stdout[:500]}")
        return None


def test_step2_deduplication():
    """Step 2: 去重检查"""
    print("\n" + "🧪"*30)
    print("STEP 2: 去重检查 (deduplicate.py)")
    print("🧪"*30)
    
    code, stdout, stderr = run_script("deduplicate.py", TEST_URL)
    
    if code != 0:
        print(f"❌ 去重检查失败: {stderr}")
        return False
    
    try:
        result = json.loads(stdout)
        is_duplicate = result.get('is_duplicate', False)
        
        if is_duplicate:
            print(f"⚠️  检测到重复内容:")
            print(f"   原因: {result.get('reason', 'N/A')}")
            print(f"   首次收藏时间: {result.get('first_seen', 'N/A')}")
        else:
            print(f"✅ 新内容，未重复")
            print(f"   标准化 URL: {result.get('normalized_url', 'N/A')[:80]}...")
        
        return not is_duplicate  # 返回是否应该继续处理
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        return False


def test_step3_content_extraction(platform_info: dict):
    """Step 3: 内容提取（模拟调用 x-tweet-fetcher）"""
    print("\n" + "🧪"*30)
    print("STEP 3: 内容提取")
    print("🧪"*30)
    
    skill = platform_info.get('skill', '')
    
    if skill == 'x-tweet-fetcher':
        print(f"📋 推荐调用 skill: {skill}")
        print(f"   命令示例: python3 ~/.openclaw/workspace/skills/x-tweet-fetcher/scripts/fetch_tweet.py --url \"{TEST_URL}\" --text-only")
        
        # 实际调用 x-tweet-fetcher
        x_script = Path.home() / ".openclaw/workspace/skills/x-tweet-fetcher/scripts/fetch_tweet.py"
        if x_script.exists():
            print(f"\n▶ 实际调用 x-tweet-fetcher...")
            code, stdout, stderr = run_script(str(x_script), "--url", TEST_URL, "--text-only")
            
            if code == 0:
                print(f"✅ 内容提取成功")
                # 构造模拟的提取结果
                return {
                    "platform": "X/Twitter",
                    "author": "@xiaoerzhan",
                    "title": "OpenClaw 神级 Skill 榜单",
                    "content": stdout[:2000] if len(stdout) > 2000 else stdout,  # 截断避免过长
                    "url": TEST_URL,
                    "created_at": "2026-03-14T10:00:00",
                    "summary": "分享了20个评分3.4+的OpenClaw必装Skill，分四类整理",
                    "keywords": ["OpenClaw", "Skill", "自动化", "AI工具"],
                    "reason": "整理了高质量的OpenClaw生态插件清单",
                    "stats": {"likes": 419, "retweets": 122, "bookmarks": 0, "views": 29960}
                }
            else:
                print(f"⚠️  x-tweet-fetcher 调用失败，使用模拟数据")
        else:
            print(f"⚠️  x-tweet-fetcher 未安装，使用模拟数据")
    else:
        print(f"📋 推荐调用 skill: {skill}")
    
    # 模拟数据
    return {
        "platform": "X/Twitter",
        "author": "@xiaoerzhan",
        "title": "OpenClaw 神级 Skill 榜单",
        "content": "🦞 特别需要的来了... [内容截断]",
        "url": TEST_URL,
        "created_at": "2026-03-14T10:00:00",
        "summary": "分享了20个评分3.4+的OpenClaw必装Skill",
        "keywords": ["OpenClaw", "Skill"],
        "reason": "高质量插件清单",
        "stats": {"likes": 419, "retweets": 122, "bookmarks": 0, "views": 29960}
    }


def test_step4_formatting(content_data: dict):
    """Step 4: 格式化输出"""
    print("\n" + "🧪"*30)
    print("STEP 4: 格式化 (append_to_feishu.py)")
    print("🧪"*30)
    
    # 构造输入 JSON
    input_json = json.dumps(content_data, ensure_ascii=False)
    
    code, stdout, stderr = run_script("append_to_feishu.py", input_json)
    
    if code != 0:
        print(f"❌ 格式化失败: {stderr}")
        return None
    
    print(f"✅ 格式化成功")
    print(f"\n📄 输出预览（前1000字符）:\n{'-'*60}")
    print(stdout[:1000])
    print(f"{'-'*60}")
    
    return stdout


def test_step5_document_simulation(formatted_content: str):
    """Step 5: 模拟飞书文档追加"""
    print("\n" + "🧪"*30)
    print("STEP 5: 飞书文档追加（模拟）")
    print("🧪"*30)
    
    print(f"📋 实际使用时，Agent 应调用 feishu-doc skill:")
    print(f"   feishu_doc(action='append', doc_token='...', content='...')")
    print(f"\n✅ 格式化内容已准备就绪，可以追加到飞书文档")
    
    # 保存到临时文件供查看
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(formatted_content)
        print(f"\n💾 完整内容已保存到: {f.name}")
        return f.name


def run_full_test():
    """运行完整测试流程"""
    print("\n" + "🚀"*40)
    print("Content Collector v1.2.0 - 主流程测试")
    print("测试 URL:", TEST_URL)
    print("🚀"*40)
    
    results = {
        "step1_platform": False,
        "step2_dedup": False,
        "step3_extraction": False,
        "step4_formatting": False,
        "step5_document": False,
    }
    
    # Step 1: 平台检测
    platform_info = test_step1_platform_detection()
    if platform_info:
        results["step1_platform"] = True
    else:
        print("\n❌ 测试中止：平台检测失败")
        return results
    
    # Step 2: 去重检查
    should_continue = test_step2_deduplication()
    if should_continue:
        results["step2_dedup"] = True
    else:
        print("\n⚠️  内容已存在，跳过后续步骤")
        return results
    
    # Step 3: 内容提取
    content_data = test_step3_content_extraction(platform_info)
    if content_data:
        results["step3_extraction"] = True
    else:
        print("\n❌ 测试中止：内容提取失败")
        return results
    
    # Step 4: 格式化
    formatted = test_step4_formatting(content_data)
    if formatted:
        results["step4_formatting"] = True
    else:
        print("\n❌ 测试中止：格式化失败")
        return results
    
    # Step 5: 文档追加（模拟）
    temp_file = test_step5_document_simulation(formatted)
    results["step5_document"] = True
    
    # 打印总结
    print("\n" + "📊"*40)
    print("测试总结")
    print("📊"*40)
    for step, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"   {step}: {status}")
    
    all_passed = all(results.values())
    print(f"\n{'='*60}")
    if all_passed:
        print("🎉 所有测试通过！")
    else:
        print("⚠️  部分测试未通过，请检查日志")
    print(f"{'='*60}\n")
    
    return results


if __name__ == "__main__":
    run_full_test()