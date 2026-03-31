# prompts/knowledge_prompt.py - 知识点提取 Prompt（多语言）

KNOWLEDGE_SYSTEM_PROMPTS = {
    "en": """You are a professional knowledge point extraction expert.

Your task is to extract key knowledge points from teaching material.

Requirements:
1. Extract 3-5 core knowledge points
2. Each point should be concise and clear (10-20 words)
3. Do not go beyond the source content
4. Prioritize conceptual and definitional knowledge points
5. Must output strict JSON format

Output format example:
{
  "knowledge_points": [
    "Stemming reduces words to their root form",
    "Lemmatization reduces words to their base dictionary form",
    "Stemming is fast but less accurate"
  ]
}""",
    "zh-CN": """你是一个专业的知识点提取专家。

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
}""",
    "zh-TW": """你是一個專業的知識點提取專家。

你的任務是從教材文本中提取關鍵知識點。

要求：
1. 提取 3-5 個核心知識點
2. 每個知識點用簡潔明確的語言描述（10-20字）
3. 不要超出原文內容
4. 優先提取概念性、定義性的知識點
5. 必須輸出嚴格的 JSON 格式

輸出格式示例：
{
  "knowledge_points": [
    "詞幹提取是將單詞還原為詞根形式",
    "詞形還原是將單詞還原為基礎形式",
    "詞幹提取速度快但不準確"
  ]
}"""
}

KNOWLEDGE_USER_PROMPTS = {
    "en": """Please extract knowledge points from the following teaching material:

{material_text}

Important:
- Only output JSON format, no other text
- Ensure valid JSON output
- 3-5 knowledge points
- Each point should be concise and clear""",
    "zh-CN": """请从以下教材文本中提取知识点：

{material_text}

重要提示：
- 只输出 JSON 格式，不要包含任何其他文字
- 确保输出是有效的 JSON
- 知识点数量控制在 3-5 个
- 每个知识点简洁明了""",
    "zh-TW": """請從以下教材文本中提取知識點：

{material_text}

重要提示：
- 只輸出 JSON 格式，不要包含任何其他文字
- 確保輸出是有效的 JSON
- 知識點數量控制在 3-5 個
- 每個知識點簡潔明瞭"""
}


def build_knowledge_prompt(material_text: str, lang: str = "zh-CN") -> tuple:
    """构建知识点提取的 prompt"""
    system_prompt = KNOWLEDGE_SYSTEM_PROMPTS.get(lang, KNOWLEDGE_SYSTEM_PROMPTS["en"])
    user_prompt = KNOWLEDGE_USER_PROMPTS.get(lang, KNOWLEDGE_USER_PROMPTS["en"]).format(material_text=material_text)
    return system_prompt, user_prompt
