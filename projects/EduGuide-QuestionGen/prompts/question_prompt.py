# prompts/question_prompt.py - 分层出题 Prompt
from typing import Tuple

QUESTION_SYSTEM_PROMPT = """你是一个出题专家。

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
"""

QUESTION_USER_PROMPT = """
教材文本：
{material_text}

知识点：
{knowledge_points}

请根据以上知识点生成三个难度层级的题目，输出为 JSON 格式。
"""


def build_question_prompt(material_text: str, knowledge_points: str) -> Tuple[str, str]:
    """构建分层出题的 prompt"""
    user_prompt = QUESTION_USER_PROMPT.format(
        material_text=material_text,
        knowledge_points=knowledge_points
    )
    return QUESTION_SYSTEM_PROMPT, user_prompt
