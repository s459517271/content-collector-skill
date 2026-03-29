#!/usr/bin/env python3
"""
标签生成器 v2.0 - 独立生成模式

功能：
1. 根据文章内容生成 5 个标签（对象2 + 场景1 + 类型1 + 方法1）
2. 规范化标签格式
3. 校验标签结构

输出：JSON 格式的标签
"""

import json
import re
import sys
import subprocess
from typing import Dict, List, Any

# 飞书配置
BITABLE_APP_TOKEN = "ND8ObCuSya5Dv3sREZYc03Ilngh"
BITABLE_TABLE_ID = "tblaHDM5kjtikIl9"


def normalize_tag(tag: str) -> str:
    """
    标签规范化规则：
    1. 去掉首尾空格
    2. 英文转小写
    3. 英文多个单词用 `-` 连接
    4. 去重
    """
    # 1. 去掉首尾空格
    tag = tag.strip()
    
    # 2. 英文转小写
    tag = tag.lower()
    
    # 3. 英文多个单词用 `-` 连接
    # 判断是否全是英文单词组成
    if ' ' in tag:
        # 检查是否全是字母和空格
        words = tag.split()
        if all(w.isalpha() for w in words):
            tag = '-'.join(words)
    
    # 4. 去除特殊字符（只保留字母、数字、中文、连字符）
    tag = re.sub(r'[^\w\u4e00-\u9fff-]', '', tag)
    
    return tag


def normalize_tags(tags: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """规范化所有标签"""
    normalized = {}
    for category, tag_list in tags.items():
        normalized[category] = [normalize_tag(t) for t in tag_list]
    return normalized


def validate_tags(tags: Dict[str, List[str]]) -> List[str]:
    """
    校验规则：
    - 对象恰好 2 个
    - 场景恰好 1 个
    - 类型恰好 1 个
    - 方法恰好 1 个
    - 总数恰好 5 个
    - 标签无重复（跨类别也检查）
    """
    errors = []
    
    # 检查各类别数量
    if len(tags.get("对象", [])) != 2:
        errors.append(f"对象需要 2 个，当前 {len(tags.get('对象', []))} 个")
    if len(tags.get("场景", [])) != 1:
        errors.append(f"场景需要 1 个，当前 {len(tags.get('场景', []))} 个")
    if len(tags.get("类型", [])) != 1:
        errors.append(f"类型需要 1 个，当前 {len(tags.get('类型', []))} 个")
    if len(tags.get("方法", [])) != 1:
        errors.append(f"方法需要 1 个，当前 {len(tags.get('方法', []))} 个")
    
    # 检查总数
    total = sum(len(v) for v in tags.values())
    if total != 5:
        errors.append(f"标签总数需要 5 个，当前 {total} 个")
    
    # 检查重复（跨类别）
    all_tags = []
    for v in tags.values():
        all_tags.extend(v)
    if len(all_tags) != len(set(all_tags)):
        errors.append("存在重复标签")
    
    return errors


def flatten_tags(tags: Dict[str, List[str]]) -> List[str]:
    """将标签字典扁平化为列表"""
    result = []
    result.extend(tags.get("对象", []))  # 2个
    result.extend(tags.get("场景", []))   # 1个
    result.extend(tags.get("类型", []))   # 1个
    result.extend(tags.get("方法", []))   # 1个
    return result


def generate_tags_prompt(content: str) -> str:
    """生成标签的 prompt"""
    return f"""请阅读以下内容，并严格按照"对象、场景、类型、方法"四类标签体系输出 5 个标签。

【标签体系】
- 对象（2个）：内容涉及的核心主体/技术/工具，如 openclaude、agent、mcp、prompt、浏览器自动化、记忆系统、量化交易、学习资源、实战案例、产品思考
- 场景（1个）：内容应用的实际场景/用途，如 投资分析、自动化测试、知识管理、代码生成、数据处理
- 类型（1个）：内容的表现形式，如 技术教程、实战案例、产品分析、工具推荐、观点分享
- 方法（1个）：内容涉及的方法论/技巧，如 工作流、评测、prompt优化、架构设计

【规则】
1. 对象 2 个，场景 1 个，类型 1 个，方法 1 个，共 5 个
2. 不参考历史标签，只根据当前文章内容生成
3. 英文标签小写，多个单词用 `-` 连接（如 claude-code）
4. 中文标签使用简洁固定短语（如 投资分析、技术教程）
5. 不输出空泛标签，如 AI、工具、技术、效率
6. 只输出 JSON，不输出解释
7. 标签必须与内容相关，不要编造

【输出格式】
{{
  "tags": {{
    "对象": ["标签1", "标签2"],
    "场景": ["标签3"],
    "类型": ["标签4"],
    "方法": ["标签5"]
  }}
}}

【内容】
{content}
"""


def call_llm(prompt: str) -> Dict[str, List[str]]:
    """
    调用 LLM 生成标签
    这里需要根据实际环境调用 LLM
    返回格式化的标签字典
    """
    # 这里需要调用实际的 LLM
    # 临时返回示例，实际使用时替换为真实调用
    # 
    # 示例调用方式：
    # result = subprocess.run([
    #     'curl', '-X', 'POST', 'http://localhost:11434/api/generate',
    #     '-d', json.dumps({"model": "qwen", "prompt": prompt, "stream": False})
    # ], capture_output=True, text=True)
    # 
    # 这里应该返回实际的 LLM 响应
    pass


def main(content: str, max_retries: int = 2) -> List[str]:
    """
    主函数：生成并校验标签
    
    Args:
        content: 文章内容
        max_retries: 最大重试次数
    
    Returns:
        扁平化的标签列表（5个）
    """
    for attempt in range(max_retries):
        # 生成 prompt
        prompt = generate_tags_prompt(content)
        
        # 调用 LLM（这里需要替换为实际调用）
        # 假设返回的是 JSON 字符串
        # llm_response = call_llm(prompt)
        
        # 模拟 LLM 响应（实际使用时删除）
        # 示例响应
        # llm_response = '''
        # {
        #   "tags": {
        #     "对象": ["openclaude", "agent"],
        #     "场景": ["投资分析"],
        #     "类型": ["实战案例"],
        #     "方法": ["工作流"]
        #   }
        # }
        # '''
        
        # 解析响应
        # tags = json.loads(llm_response)["tags"]
        
        # 规范化
        # tags = normalize_tags(tags)
        
        # 校验
        # errors = validate_tags(tags)
        
        # if not errors:
        #     return flatten_tags(tags)
        # else:
        #     print(f"校验失败: {errors}", file=sys.stderr)
        #     if attempt < max_retries - 1:
        #         print("重试...", file=sys.stderr)
        #         continue
        #     else:
        #         raise ValueError(f"标签校验失败: {{errors}}")
        
        pass
    
    return []


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate_tags.py <content>", file=sys.stderr)
        sys.exit(1)
    
    content = sys.argv[1]
    tags = main(content)
    print(json.dumps(tags, ensure_ascii=False, indent=2))