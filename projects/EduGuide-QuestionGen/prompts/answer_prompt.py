# prompts/answer_prompt.py - 答案解析 Prompt
from typing import Tuple

ANSWER_SYSTEM_PROMPT = """你是一个答案解析专家。

任务：为每道题目生成详细答案和解析。

输出格式（JSON）：
{
  "basic": [
    {
      "question": "题目1",
      "answer": "答案1",
      "explanation": "解析1"
    }
  ],
  "intermediate": [
    {
      "question": "题目2",
      "answer": "答案2",
      "explanation": "解析2"
    }
  ],
  "advanced": [
    {
      "question": "题目3",
      "answer": "答案3",
      "explanation": "解析3"
    }
  ]
}

要求：
1. 答案必须准确，基于教材内容
2. 解析要详细，有逻辑
3. 每个难度层级的答案要体现难度递进
4. 使用专业术语
"""

ANSWER_USER_PROMPT = """
知识点：
{knowledge_points}

题目：
{questions}

请为每道题目生成答案和解析，输出为 JSON 格式。
"""


def build_answer_prompt(knowledge_points: str, questions: str) -> Tuple[str, str]:
    """构建答案解析的 prompt"""
    user_prompt = ANSWER_USER_PROMPT.format(
        knowledge_points=knowledge_points,
        questions=questions
    )
    return ANSWER_SYSTEM_PROMPT, user_prompt
