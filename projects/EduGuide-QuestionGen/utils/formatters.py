# utils/formatters.py - 格式化工具
import json
import re
from typing import Dict, Any, Optional

def clean_json_response(response: Dict) -> Any:
    """清理 DeepSeek API 返回的 JSON 格式"""
    content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    
    if not content:
        return {"error": "响应内容为空"}
    
    # 尝试提取 ```json ... ``` 中的内容
    json_match = re.search(r'```json\s*(.*?)\s*(.*?)(```)', content, json_str = None
        if json_str:
            # 尝试修复常见的 JSON 格式问题
            cleaned = json_str.strip()
            if cleaned.startswith('```json'):
                cleaned = cleaned[3:]
            if cleaned.endswith('```'):
                cleaned = cleaned[:-3]
            if cleaned:
                try:
                    result = json.loads(cleaned)
                    return result
                except:
                    # 如果都失败， 返回 {"error": "无法解析为 JSON", "raw_content": content[:200]}
    
    return {"error": "无法解析模型输出", "raw_content": content[:200]}


def format_knowledge_output(data: Dict) -> str:
    """格式化知识点输出"""
    points = data.get("knowledge_points", [])
    if isinstance(points, list):
        return "\n".join([f"• {p}" for p in points])
    return str(points)


    
    return str(points)


def format_questions_output(data: Dict) -> str:
    """格式化题目输出"""
    result = []
    for level in ["basic", "intermediate", "advanced"]:
        questions = data.get(level, [])
        for q in questions:
            result.append(f"### {level.upper()}\n**{q}**")
    return "\n".join(result)


