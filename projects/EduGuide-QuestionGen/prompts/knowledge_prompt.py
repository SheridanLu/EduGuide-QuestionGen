# prompts/knowledge_prompt.py - 知识点提取 Prompt

KNOWLEDGE_SYSTEM_PROMPT = """你是一个知识点提取专家。你的任务是从教材文本中提取关键知识点。

要求：
1. 提取 3-5 个核心知识点
2. 每个知识点用简洁的语言描述
3. 不要超出原文内容
4. 必须输出 JSON 格式"""

KNOWLEDGE_USER_PROMPT = """请从以下教材文本中提取知识点：

{material_text}

输出格式（必须是有效的 JSON）：
{{
  "knowledge_points": [
    "知识点1",
    "知识点2",
    "知识点3"
  ]
}}

请确保输出是有效的 JSON 格式。"""

def build_knowledge_prompt(material_text: str) -> tuple:
    """构建知识点提取的 prompt"""
    user_prompt = KNOWLEDGE_USER_PROMPT.format(material_text=material_text)
    return KNOWLEDGE_SYSTEM_PROMPT, user_prompt
