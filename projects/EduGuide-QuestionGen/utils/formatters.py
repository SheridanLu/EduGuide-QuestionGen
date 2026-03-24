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
    json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
    if json_match:
        json_str = json_match.group(1).strip()
        try:
            result = json.loads(json_str)
            return result
        except:
            pass
    
    # 没有找到 ```json...```，尝试直接解析
    try:
        cleaned = content.strip()
        if cleaned.startswith('```'):
            cleaned = cleaned[3:]
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]
        result = json.loads(cleaned)
        return result
    except:
        # 如果都失败，返回原始内容和错误信息
        return {"error": "无法解析 JSON", "raw_content": content[:500]}


def format_knowledge_output(data: Dict) -> str:
    """格式化知识点输出"""
    points = data.get("knowledge_points", [])
    if isinstance(points, list):
        return "\n".join([f"• {p}" for p in points])
    return str(points)


def format_questions_output(data: Dict) -> str:
    """格式化题目输出"""
    result = []
    for level in ["basic", "intermediate", "advanced"]:
        questions = data.get(level, [])
        if questions:
            result.append(f"### {level.upper()}")
            for i, q in enumerate(questions, 1):
                result.append(f"{i}. {q}")
            result.append("")
    return "\n".join(result)


def format_answers_output(data: Dict) -> str:
    """格式化答案输出"""
    result = []
    for level in ["basic", "intermediate", "advanced"]:
        answers = data.get(level, [])
        if answers:
            result.append(f"### {level.upper()}")
            for item in answers:
                if isinstance(item, dict):
                    result.append(f"**Q:** {item.get('question', 'N/A')}")
                    result.append(f"**A:** {item.get('answer', 'N/A')}")
                    result.append(f"**解析:** {item.get('explanation', 'N/A')}")
                    result.append("")
    return "\n".join(result)
