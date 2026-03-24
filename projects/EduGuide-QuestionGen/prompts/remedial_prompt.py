# prompts/remedial_prompt.py - 补救题生成 Prompt
from typing import Tuple

REMEDIAL_SYSTEM_PROMPT = """你是一个补救题生成专家。

任务：针对学生的错误理解，生成针对性的补救题。

输出格式（JSON）：
{
  "remedial": [
    {
      "original_question": "原题目",
      "wrong_point": "错误知识点",
      "remedial_question": "补救题",
      "explanation": "解析",
      "difficulty": "基础"
    }
  ]
}

要求：
1. 补救题要比原题更简单
2. 针对具体错误点，不要超纲
3. 解析要说明为什么需要补救
4. 生成 2-3 道补救题
"""

REMEDIAL_USER_PROMPT = """
教材文本：
{material_text}

知识点：
{knowledge_points}

题目和答案：
{questions_answers}

错误知识点：{wrong_point}

请针对错误知识点生成补救题，输出为 JSON 格式。
"""


def build_remedial_prompt(
    material_text: str, 
    knowledge_points: str, 
    questions_answers: str,
    wrong_point: str
) -> Tuple[str, str]:
    """构建补救题生成的 prompt"""
    user_prompt = REMEDIAL_USER_PROMPT.format(
        material_text=material_text,
        knowledge_points=knowledge_points,
        questions_answers=questions_answers,
        wrong_point=wrong_point
    )
    return REMEDIAL_SYSTEM_PROMPT, user_prompt
