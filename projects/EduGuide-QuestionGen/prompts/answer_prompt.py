# prompts/answer_prompt.py - 答案解析 Prompt（苏格拉底式引导）
from typing import Tuple

ANSWER_SYSTEM_PROMPT = """你是一位耐心的苏格拉底式导师。你的目标不是告诉学生答案，而是引导学生自己得出答案。

你的教学原则：
1. 先拆解问题，让学生明确问题的关键点
2. 用提问的方式帮学生理清已知条件和逻辑链条
3. 在学生思考过程中，逐步给出提示，但每次只推进一小步
4. 等待学生的回应后再继续引导，而不是一次性讲完
5. 如果学生走偏了，用追问帮学生回到正轨，而不是直接否定

记住：你的目标是让学生自己得出答案，而不是告诉学生答案。"""

ANSWER_USER_PROMPT = """
知识点：
{knowledge_points}

题目：
{questions}

请为每道题目设计引导式教学方案，而不是直接给出答案。

输出格式（JSON）：
{{
  "basic": [
    {{
      "question": "题目",
      "guidance": {{
        "step1": "第一个引导问题（帮助学生理解题目要求）",
        "step2": "第二个引导问题（帮助学生回忆相关知识点）",
        "step3": "第三个引导问题（帮助学生建立逻辑链条）",
        "hints": ["提示1：...", "提示2：...", "提示3：..."],
        "key_points": ["关键点1", "关键点2"],
        "common_mistakes": ["常见错误1：...", "常见错误2：..."]
      }}
    }}
  ],
  "intermediate": [
    {{
      "question": "题目",
      "guidance": {{
        "step1": "第一个引导问题",
        "step2": "第二个引导问题",
        "step3": "第三个引导问题",
        "hints": ["提示1：...", "提示2：...", "提示3：..."],
        "key_points": ["关键点1", "关键点2"],
        "common_mistakes": ["常见错误1：...", "常见错误2：..."]
      }}
    }}
  ],
  "advanced": [
    {{
      "question": "题目",
      "guidance": {{
        "step1": "第一个引导问题",
        "step2": "第二个引导问题",
        "step3": "第三个引导问题",
        "hints": ["提示1：...", "提示2：...", "提示3：..."],
        "key_points": ["关键点1", "关键点2"],
        "common_mistakes": ["常见错误1：...", "常见错误2：..."]
      }}
    }}
  ]
}}

要求：
1. 每个引导问题都要引导学生思考，而不是直接告诉答案
2. 提示要循序渐进，从简单到复杂
3. 关键点要突出核心概念
4. 常见错误要帮助学生避免陷阱
5. 必须是有效的 JSON 格式"""


def build_answer_prompt(knowledge_points: str, questions: str) -> Tuple[str, str]:
    """构建答案解析的 prompt"""
    user_prompt = ANSWER_USER_PROMPT.format(
        knowledge_points=knowledge_points,
        questions=questions
    )
    return ANSWER_SYSTEM_PROMPT, user_prompt
