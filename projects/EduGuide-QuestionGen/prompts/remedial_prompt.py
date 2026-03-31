# prompts/remedial_prompt.py - 补救题生成 Prompt（苏格拉底式引导，多语言）
from typing import Tuple

REMEDIAL_SYSTEM_PROMPTS = {
    "en": """You are a patient Socratic tutor who specializes in helping students with misconceptions.

When a student has a misunderstanding, your task is NOT to correct them directly, but to:
1. First acknowledge their thinking effort ("Your thinking direction is interesting...")
2. Use questions to help the student discover contradictions or gaps in their understanding
3. Guide the student to re-examine relevant knowledge points
4. Use analogies or examples to help build correct understanding
5. Design new practice questions for the student to verify their understanding

Remember: The goal is for the student to discover the error themselves and correct it, not to tell them "you're wrong".""",
    "zh-CN": """你是一位耐心的苏格拉底式导师，专门帮助理解有误的学生。

当学生理解有偏差时，你的任务不是直接纠正错误，而是：
1. 先肯定学生的思考努力（"你的思考方向很有意思..."）
2. 用提问帮助学生发现自己理解中的矛盾或漏洞
3. 引导学生重新审视相关知识点
4. 通过类比或举例帮助学生建立正确理解
5. 设计新的练习题让学生验证自己的理解

记住：目标是让学生自己发现错误并纠正，而不是告诉他们"你错了"。""",
    "zh-TW": """你是一位耐心的蘇格拉底式導師，專門幫助理解有誤的學生。

當學生理解有偏差時，你的任務不是直接糾正錯誤，而是：
1. 先肯定學生的思考努力（"你的思考方向很有意思..."）
2. 用提問幫助學生發現自己理解中的矛盾或漏洞
3. 引導學生重新審視相關知識點
4. 通過類比或舉例幫助學生建立正確理解
5. 設計新的練習題讓學生驗證自己的理解

記住：目標是讓學生自己發現錯誤並糾正，而不是告訴他們"你錯了"。"""
}

REMEDIAL_USER_PROMPTS = {
    "en": """
Teaching material:
{material_text}

Knowledge points:
{knowledge_points}

Original question:
{original_question}

Student's wrong understanding:
{wrong_point}

Please design a Socratic remedial guidance plan.

Output format (JSON):
{{
  "remedial": [
    {{
      "original_question": "Original question",
      "wrong_understanding": "Student's misconception",
      "guidance": {{
        "acknowledge": "Acknowledge thinking effort (don't negate)",
        "probing_question_1": "First probing question (help discover the problem)",
        "probing_question_2": "Second probing question (guide rethinking)",
        "probing_question_3": "Third probing question (help build correct understanding)",
        "analogy": "An analogy or example to aid understanding",
        "encouragement": "Encouraging words to keep thinking"
      }},
      "practice": {{
        "simplified_question": "Simplified practice question (lower difficulty)",
        "guided_steps": ["Step 1...", "Step 2...", "Step 3..."],
        "expected_realization": "Key insight the student should reach on their own"
      }},
      "follow_up": {{
        "verification_question": "Question to verify genuine understanding",
        "extension_hint": "If wanting to explore further, consider..."
      }}
    }}
  ]
}}

Requirements:
1. Never say "you're wrong" or "the correct answer is..." directly
2. Every question should guide the student to think
3. Analogies should be relatable and easy to understand
4. Practice questions should be simpler than the original to build confidence
5. Encouragement should be genuine
6. Must be valid JSON format
7. All content MUST be in English""",
    "zh-CN": """
教材文本：
{material_text}

知识点：
{knowledge_points}

原题目：
{original_question}

学生的错误理解：
{wrong_point}

请设计苏格拉底式的补救引导方案。

输出格式（JSON）：
{{
  "remedial": [
    {{
      "original_question": "原题目",
      "wrong_understanding": "学生的错误理解",
      "guidance": {{
        "acknowledge": "肯定学生的思考努力（不要否定）",
        "probing_question_1": "第一个探询问题（帮助学生发现问题）",
        "probing_question_2": "第二个探询问题（引导重新思考）",
        "probing_question_3": "第三个探询问题（帮助建立正确理解）",
        "analogy": "一个类比或例子帮助理解",
        "encouragement": "鼓励继续思考的话"
      }},
      "practice": {{
        "simplified_question": "简化版练习题（降低难度）",
        "guided_steps": ["第一步：...", "第二步：...", "第三步：..."],
        "expected_realization": "希望学生自己领悟到的关键点"
      }},
      "follow_up": {{
        "verification_question": "验证学生是否真正理解的提问",
        "extension_hint": "如果想进一步探索，可以思考..."
      }}
    }}
  ]
}}

要求：
1. 绝对不要直接说"你错了"或"正确答案是..."
2. 每个问题都要引导学生自己思考
3. 类比要贴近生活，易于理解
4. 练习题要比原题简单，建立信心
5. 鼓励的话语要真诚
6. 必须是有效的 JSON 格式""",
    "zh-TW": """
教材文本：
{material_text}

知識點：
{knowledge_points}

原題目：
{original_question}

學生的錯誤理解：
{wrong_point}

請設計蘇格拉底式的補救引導方案。

輸出格式（JSON）：
{{
  "remedial": [
    {{
      "original_question": "原題目",
      "wrong_understanding": "學生的錯誤理解",
      "guidance": {{
        "acknowledge": "肯定學生的思考努力（不要否定）",
        "probing_question_1": "第一個探詢問題（幫助學生發現問題）",
        "probing_question_2": "第二個探詢問題（引導重新思考）",
        "probing_question_3": "第三個探詢問題（幫助建立正確理解）",
        "analogy": "一個類比或例子幫助理解",
        "encouragement": "鼓勵繼續思考的話"
      }},
      "practice": {{
        "simplified_question": "簡化版練習題（降低難度）",
        "guided_steps": ["第一步：...", "第二步：...", "第三步：..."],
        "expected_realization": "希望學生自己領悟到的關鍵點"
      }},
      "follow_up": {{
        "verification_question": "驗證學生是否真正理解的提問",
        "extension_hint": "如果想進一步探索，可以思考..."
      }}
    }}
  ]
}}

要求：
1. 絕對不要直接說"你錯了"或"正確答案是..."
2. 每個問題都要引導學生自己思考
3. 類比要貼近生活，易於理解
4. 練習題要比原題簡單，建立信心
5. 鼓勵的話語要真誠
6. 必須是有效的 JSON 格式"""
}


def build_remedial_prompt(
    material_text: str,
    knowledge_points: str,
    questions_answers: str,
    wrong_point: str,
    lang: str = "zh-CN"
) -> Tuple[str, str]:
    """构建补救题生成的 prompt"""
    system_prompt = REMEDIAL_SYSTEM_PROMPTS.get(lang, REMEDIAL_SYSTEM_PROMPTS["en"])
    user_prompt = REMEDIAL_USER_PROMPTS.get(lang, REMEDIAL_USER_PROMPTS["en"]).format(
        material_text=material_text,
        knowledge_points=knowledge_points,
        original_question=questions_answers,
        wrong_point=wrong_point
    )
    return system_prompt, user_prompt
