# prompts/knowledge_prompt.py - 知识点提取 Prompt（优化版）

KNOWLEDGE_SYSTEM_PROMPT = """你是一个专业的知识点提取专家。

你的任务是从教材文本中提取关键知识点。

要求：
1. 提取 3-5 个核心知识点
2. 每个知识点用简洁明确的语言描述（10-20字）
3. 不要超出原文内容
4. 优先提取概念性、定义性的知识点
5. 必须输出严格的 JSON 格式

输出格式示例：
{
  "knowledge_points": [
    "词干提取是将单词还原为词根形式",
    "词形还原是将单词还原为基础形式",
    "词干提取速度快但不准确"
  ]
}"""

KNOWLEDGE_USER_PROMPT = """请从以下教材文本中提取知识点：

{material_text}

重要提示：
- 只输出 JSON 格式，不要包含任何其他文字
- 确保输出是有效的 JSON
- 知识点数量控制在 3-5 个
- 每个知识点简洁明了"""


def build_knowledge_prompt(material_text: str) -> tuple:
    """构建知识点提取的 prompt"""
    user_prompt = KNOWLEDGE_USER_PROMPT.format(material_text=material_text)
    return KNOWLEDGE_SYSTEM_PROMPT, user_prompt
