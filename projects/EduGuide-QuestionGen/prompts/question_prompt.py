# prompts/question_prompt.py - 分层出题 Prompt (多语言)
from typing import Tuple

QUESTION_SYSTEM_PROMPTS = {
    "en": """You are an expert question generator for educational content.

Task: Generate questions at three difficulty levels based on knowledge points.

Output format (JSON):
{
  "basic": [
    "Basic question 1",
    "Basic question 2"
  ],
  "intermediate": [
    "Intermediate question 1",
    "Intermediate question 2"
  ],
  "advanced": [
    "Advanced question 1",
    "Advanced question 2"
  ]
}

Requirements:
1. At least 2 questions per difficulty level
2. Questions must be based on the input knowledge points
3. Basic level: direct recall and comprehension
4. Intermediate level: application and analysis
5. Advanced level: synthesis across multiple knowledge points
6. All questions MUST be written in English
""",
    "zh-CN": """你是一个出题专家。

任务：根据知识点生成三个难度层级的题目。

输出格式（JSON）：
{
  "basic": [
    "基础题目1",
    "基础题目2"
  ],
  "intermediate": [
    "进阶题目1",
    "进阶题目2"
  ],
  "advanced": [
    "高级题目1",
    "高级题目2"
  ]
}

要求：
1. 每个难度层级至少 2 道题目
2. 题目必须基于输入的知识点
3. basic 层：直接考查记忆和理解
4. intermediate 层：需要应用和分析
5. advanced 层：需要综合多个知识点
""",
    "zh-TW": """你是一個出題專家。

任務：根據知識點生成三個難度層級的題目。

輸出格式（JSON）：
{
  "basic": [
    "基礎題目1",
    "基礎題目2"
  ],
  "intermediate": [
    "進階題目1",
    "進階題目2"
  ],
  "advanced": [
    "高級題目1",
    "高級題目2"
  ]
}

要求：
1. 每個難度層級至少 2 道題目
2. 題目必須基於輸入的知識點
3. basic 層：直接考查記憶和理解
4. intermediate 層：需要應用和分析
5. advanced 層：需要綜合多個知識點
"""
}

QUESTION_USER_PROMPTS = {
    "en": """
Teaching material:
{material_text}

Knowledge points:
{knowledge_points}

Please generate questions at three difficulty levels based on the above knowledge points. Output in JSON format. All questions MUST be in English.
""",
    "zh-CN": """
教材文本：
{material_text}

知识点：
{knowledge_points}

请根据以上知识点生成三个难度层级的题目，输出为 JSON 格式。
""",
    "zh-TW": """
教材文本：
{material_text}

知識點：
{knowledge_points}

請根據以上知識點生成三個難度層級的題目，輸出為 JSON 格式。
"""
}


def build_question_prompt(material_text: str, knowledge_points: str, lang: str = "zh-CN") -> Tuple[str, str]:
    """构建分层出题的 prompt"""
    system_prompt = QUESTION_SYSTEM_PROMPTS.get(lang, QUESTION_SYSTEM_PROMPTS["en"])
    user_prompt = QUESTION_USER_PROMPTS.get(lang, QUESTION_USER_PROMPTS["en"]).format(
        material_text=material_text,
        knowledge_points=knowledge_points
    )
    return system_prompt, user_prompt
