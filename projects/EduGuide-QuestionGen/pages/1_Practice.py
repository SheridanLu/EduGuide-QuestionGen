# pages/1_Practice.py - 交互式解题页面（多语言版）
import streamlit as st
import json
import os
from typing import Dict, Any, List

# 多语言配置
T = {
    "en": {
        "page_title": "🎯 Interactive Practice - EduGuide",
        "subtitle": "**Step-by-step guidance to find answers yourself**",
        "no_data": "⚠️ No question data. Please generate questions first.",
        "steps_text": "Steps",
        "progress": "Progress",
        "total": "Total Questions",
        "completed": "Completed",
        "completion_rate": "Completion Rate",
        "basic": "🟢 Basic",
        "intermediate": "🟡 Intermediate",
        "advanced": "🔴 Advanced",
        "question_label": "Question",
        "your_thought": "Your Thought",
        "placeholder": "Enter your thinking or answer here...",
        "submit": "✅ Submit",
        "need_hint": "💡 Need a Hint?",
        "view_key_points": "🔑 Key Points",
        "hint_title": "💡 Hint",
        "key_points_title": "🔑 Key Points",
        "all_steps": "🎉 Great! You've completed all steps!",
        "answer_review": "📝 Your Answer Review",
        "step": "Step",
        "complete": "Complete This Question",
        "retry": "🔄 Retry",
        "too_short": "⚠️ Answer is too short, can you elaborate?",
        "enter_answer": "❌ Please enter your answer first",
        "correct": "✅ Good! Continue to next step.",
        "try_again": "⚠️ Not quite. Try again.",
        "back": "← Back",
        "think_first": "*Please think first, then continue*",
        "key_concept_hint": "Think about the key concepts in the question.",
        "completed_msg": "🎉 Congratulations! You've completed this question!",
        "start_practice": "🎯 Start Practice",
        "no_data_steps": "**Steps:**\n1. Return to Home\n2. Upload file or input text\n3. Click 'Start Generation'\n4. Return to this page",
        "step_guide": "💡 Practice step-by-step with verification",
        "generate_first": "⚠️ No question data. Please generate questions on the main page first.",
        "slide_label": "Slide",
        "your_answer_label": "Your Answer",
        "question_label": "Q",
        "verifying": "Verifying...",
        "incorrect": "Not quite right.",
        "incorrect_detail": "Your answer doesn't fully address the question. Think about it again or try the hint.",
        "retry_step": "🔄 Try Again",
        "correct_detail": "Great job! Your understanding is correct.",
        "attempt": "Attempt",
        "max_attempts": "Max attempts reached. Showing key points.",
        "error_analysis": "Error Analysis",
        "guidance": "Guidance",
        "try_again_after": "Try again after reviewing the guidance above.",
    },
    "zh-CN": {
        "page_title": "🎯 解题练习 - EduGuide",
        "subtitle": "**一步步引导，自己得出答案**",
        "no_data": "⚠️ 暂无题目数据。请先在主页生成题目。",
        "steps_text": "步骤",
        "progress": "进度",
        "total": "总题目数",
        "completed": "已完成",
        "completion_rate": "完成率",
        "basic": "🟢 基础题",
        "intermediate": "🟡 中级题",
        "advanced": "🔴 高级题",
        "question_label": "题目",
        "your_thought": "你的思考",
        "placeholder": "在这里输入你的思考过程或答案...",
        "submit": "✅ 提交",
        "need_hint": "💡 需要提示吗？",
        "view_key_points": "🔑 查看关键点",
        "hint_title": "💡 提示",
        "key_points_title": "🔑 关键点",
        "all_steps": "🎉 太棒了！你已经完成了所有步骤！",
        "answer_review": "📝 你的答案回顾",
        "step": "步骤",
        "complete": "完成此题",
        "retry": "🔄 重新练习",
        "too_short": "⚠️ 答案太简短了，能再详细一点吗？",
        "enter_answer": "❌ 请先输入你的答案",
        "correct": "✅ 很好！继续下一步。",
        "try_again": "⚠️ 不太对，再试一次。",
        "back": "← 返回",
        "think_first": "*请先自己思考，再继续*",
        "key_concept_hint": "想想题目中的关键词和它们之间的关系。",
        "completed_msg": "🎉 恭喜！你已经完成了这道题！",
        "start_practice": "🎯 开始解题",
        "no_data_steps": "**步骤：**\n1. 返回主页\n2. 上传文件或输入文本\n3. 点击'开始生成'\n4. 生成完成后返回此页面",
        "step_guide": "💡 一步步练习，验证每个答案",
        "generate_first": "⚠️ 暂无题目数据。请先在主页生成题目。",
        "slide_label": "幻灯片",
        "your_answer_label": "你的答案",
        "question_label": "Q",
        "verifying": "验证中...",
        "incorrect": "答案不太对哦。",
        "incorrect_detail": "你的答案没有完全回答这个问题，再想想看，或者试试提示。",
        "retry_step": "🔄 再试一次",
        "correct_detail": "很好！你的理解是正确的。",
        "attempt": "第",
        "max_attempts": "已达最大尝试次数，显示关键点。",
        "error_analysis": "错因分析",
        "guidance": "引导提示",
        "try_again_after": "看完引导后，再试一次吧！",
    },
    "zh-TW": {
        "page_title": "🎯 解題練習 - EduGuide",
        "subtitle": "**一步步引導，自己得出答案**",
        "no_data": "⚠️ 暫無題目資料。請先在主頁生成題目。",
        "steps_text": "步驟",
        "progress": "進度",
        "total": "總題目數",
        "completed": "已完成",
        "completion_rate": "完成率",
        "basic": "🟢 基礎題",
        "intermediate": "🟡 中級題",
        "advanced": "🔴 高級題",
        "question_label": "題目",
        "your_thought": "你的思考",
        "placeholder": "在這裡輸入你的思考過程或答案...",
        "submit": "✅ 提交",
        "need_hint": "💡 需要提示嗎？",
        "view_key_points": "🔑 查看關鍵點",
        "hint_title": "💡 提示",
        "key_points_title": "🔑 關鍵點",
        "all_steps": "🎉 太棒了！你已經完成了所有步驟！",
        "answer_review": "📝 你的答案回顧",
        "step": "步驟",
        "complete": "完成此題",
        "retry": "🔄 重新練習",
        "too_short": "⚠️ 答案太簡短了，能再詳細一點嗎？",
        "enter_answer": "❌ 請先輸入你的答案",
        "correct": "✅ 很好！繼續下一步。",
        "try_again": "⚠️ 不太對，再試一次。",
        "back": "← 返回",
        "think_first": "*請先自己思考，再繼續*",
        "key_concept_hint": "想想題目中的關鍵詞和它們之間的關係。",
        "completed_msg": "🎉 恭喜！你已經完成了這道題！",
        "start_practice": "🎯 開始解題",
        "no_data_steps": "**步驟：**\n1. 返回首頁\n2. 上傳檔案或輸入文字\n3. 點擊'開始生成'\n4. 生成完成後返回此頁面",
        "step_guide": "💡 一步步練習，驗證每個答案",
        "generate_first": "⚠️ 暫無題目資料。請先在主頁生成題目。",
        "slide_label": "投影片",
        "your_answer_label": "你的答案",
        "question_label": "Q",
        "verifying": "驗證中...",
        "incorrect": "答案不太對哦。",
        "incorrect_detail": "你的答案沒有完全回答這個問題，再想想看，或者試試提示。",
        "retry_step": "🔄 再試一次",
        "correct_detail": "很好！你的理解是正確的。",
        "attempt": "第",
        "max_attempts": "已達最大嘗試次數，顯示關鍵點。",
        "error_analysis": "錯因分析",
        "guidance": "引導提示",
        "try_again_after": "看完引導後，再試一次吧！",
    }
}

def t(key: str, lang: str = "en") -> str:
    return T.get(lang, T.get("en", {})).get(key, key)

def init_session_state():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'completed_questions' not in st.session_state:
        st.session_state.completed_questions = set()
    if 'show_hints' not in st.session_state:
        st.session_state.show_hints = {}
    if 'step_attempts' not in st.session_state:
        st.session_state.step_attempts = {}

def verify_answer_with_ai(question_text, step_prompt, user_answer, key_points, lang):
    """调用AI验证学生答案是否正确，答错时分析错因并给出引导"""
    try:
        import httpx
        from config.api_config import get_config_manager
        cfg = get_config_manager().get_current_config()
        
        if not cfg.api_key:
            return False, t('incorrect_detail', lang), ""
        
        prompt_map = {
            "en": "You are an educator verifying a student's answer. Be strict but fair.\n\n",
            "zh-CN": "你是一位严格但公正的教育者，正在验证学生的答案。\n\n",
            "zh-TW": "你是一位嚴格但公正的教育者，正在驗證學生的答案。\n\n",
        }
        
        prompt = prompt_map.get(lang, prompt_map["en"])
        prompt += f"Question context: {question_text}\n\n"
        prompt += f"Current step asks: {step_prompt}\n\n"
        if key_points:
            prompt += f"Expected key points:\n" + "\n".join(f"- {kp}" for kp in key_points) + "\n\n"
        prompt += f"Student's answer: {user_answer}\n\n"
        prompt += "Respond in JSON format only:\n"
        prompt += '{\n'
        prompt += '  "correct": true or false,\n'
        prompt += '  "feedback": "brief feedback",\n'
        prompt += '  "error_analysis": "if wrong: analyze WHY the student got it wrong - what misconception or gap led to this answer",\n'
        prompt += '  "guidance": "if wrong: a guiding question or hint to help the student think in the right direction"\n'
        prompt += '}'
        
        headers = {
            "Authorization": f"Bearer {cfg.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": cfg.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 300
        }
        
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(
                f"{cfg.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"].strip()
            
            # 解析JSON
            import re
            json_match = re.search(r'\{[^}]+\}', content)
            if json_match:
                result = json.loads(json_match.group())
                is_correct = result.get("correct", False)
                feedback = result.get("feedback", "")
                error_analysis = result.get("error_analysis", "") if not is_correct else ""
                guidance = result.get("guidance", "") if not is_correct else ""
                return is_correct, feedback, error_analysis, guidance
            return False, t('incorrect_detail', lang), "", ""
            
    except Exception as e:
        # AI验证失败时，用关键词匹配作为fallback
        if key_points:
            matched = sum(1 for kp in key_points if kp.lower() in user_answer.lower())
            if matched >= len(key_points) * 0.5:
                return True, t('correct_detail', lang), "", ""
        return False, f"Error: {e}", "", ""

def load_questions():
    questions_path = "output/questions.json"
    answers_path = "output/answers.json"
    
    data = {'basic': [], 'intermediate': [], 'advanced': []}
    
    if os.path.exists(questions_path):
        with open(questions_path, 'r', encoding='utf-8') as f:
            data.update(json.load(f))
    
    if os.path.exists(answers_path):
        with open(answers_path, 'r', encoding='utf-8') as f:
            answers = json.load(f)
            for level in ['basic', 'intermediate', 'advanced']:
                if level in answers:
                    for i, answer in enumerate(answers[level]):
                        if i < len(data.get(level, [])):
                            if isinstance(data[level][i], dict):
                                data[level][i]['guidance'] = answer.get('guidance', {})
                            else:
                                data[level][i] = {'question': data[level][i], 'guidance': answer.get('guidance', {})}
    
    return data

def render_question_card(question_data, level, index, lang):
    question_id = f"{level}_{index}"
    question_text = question_data.get('question', question_data) if isinstance(question_data, dict) else question_data
    guidance = question_data.get('guidance', {}) if isinstance(question_data, dict) else {}
    is_completed = question_id in st.session_state.completed_questions
    
    with st.expander(
        f"{'✅' if is_completed else '📝'} {t(level, lang)} - {t('question_label', lang)} {index + 1}",
        expanded=(st.session_state.current_question == question_id)
    ):
        st.markdown(f"### {t('question_label', lang)}")
        st.info(f"**{question_text}**")
        
        if is_completed:
            st.success(t('completed_msg', lang))
            if st.button(f"{t('retry', lang)}", key=f"retry_{question_id}"):
                st.session_state.completed_questions.discard(question_id)
                st.session_state.current_step = 0
                st.session_state.user_answers.pop(question_id, None)
                st.rerun()
        else:
            if st.session_state.current_question != question_id:
                if st.button(f"{t('start_practice', lang)}", key=f"start_{question_id}", type="primary"):
                    st.session_state.current_question = question_id
                    st.session_state.current_step = 0
                    st.session_state.user_answers[question_id] = []
                    st.rerun()
            else:
                render_interactive_steps(question_id, question_text, guidance, lang)

def render_interactive_steps(question_id, question_text, guidance, lang):
    steps = [
        guidance.get('step1', ''),
        guidance.get('step2', ''),
        guidance.get('step3', '')
    ]
    steps = [s for s in steps if s]
    hints = guidance.get('hints', [])
    
    if not steps:
        st.warning(t('generate_first', lang))
        return
    
    progress = st.session_state.current_step / len(steps)
    st.progress(progress)
    st.markdown(f"**{t('progress', lang)}:** {st.session_state.current_step}/{len(steps)} {t('steps_text', lang)}")
    
    # 已完成的步骤
    for step_idx in range(st.session_state.current_step):
        ans = st.session_state.user_answers.get(f"{question_id}_{step_idx}", '')
        st.markdown(
            f'<div style="background:#e8f5e9;color:#1a1a2e;border-left:4px solid #4caf50;border-radius:8px;padding:1rem;margin:0.5rem 0;">'
            f'<strong>✅ {t("step", lang)} {step_idx+1}:</strong><br>'
            f'{ans}'
            f'</div>', unsafe_allow_html=True
        )
    
    # 当前步骤
    if st.session_state.current_step < len(steps):
        st.markdown("---")
        st.markdown(f"### 💭 {t('step', lang)} {st.session_state.current_step + 1}")
        st.markdown(f"**{steps[st.session_state.current_step]}**")
        
        user_answer = st.text_area(
            t('your_thought', lang),
            key=f"input_{question_id}_{st.session_state.current_step}",
            height=100,
            placeholder=t('placeholder', lang)
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"✅ {t('submit', lang)}", key=f"submit_{question_id}_{st.session_state.current_step}", type="primary", use_container_width=True):
                if user_answer.strip():
                    with st.spinner(t('verifying', lang)):
                        key_points = guidance.get('key_points', [])
                        result = verify_answer_with_ai(
                            question_text,
                            steps[st.session_state.current_step],
                            user_answer,
                            key_points,
                            lang
                        )
                    
                    if len(result) == 4:
                        is_correct, feedback, error_analysis, guidance_text = result
                    else:
                        is_correct, feedback = result[0], result[1]
                        error_analysis, guidance_text = "", ""
                    
                    if is_correct:
                        if question_id not in st.session_state.user_answers:
                            st.session_state.user_answers[question_id] = []
                        st.session_state.user_answers[question_id].append(user_answer)
                        st.session_state.current_step += 1
                        st.success(f"✅ {feedback if feedback else t('correct_detail', lang)}")
                        st.rerun()
                    else:
                        # 显示错因分析和引导
                        st.error(f"❌ {feedback if feedback else t('incorrect', lang)}")
                        
                        if error_analysis:
                            st.markdown(f"**🔍 {t('error_analysis', lang)}**")
                            st.markdown(
                                f'<div style="background:#fff7ed;color:#1a1a2e;border-left:4px solid #f59e0b;border-radius:8px;padding:1rem;margin:0.5rem 0;">'
                                f'{error_analysis}'
                                f'</div>', unsafe_allow_html=True
                            )
                        
                        if guidance_text:
                            st.markdown(f"**💡 {t('guidance', lang)}**")
                            st.markdown(
                                f'<div style="background:#f0f9ff;color:#1a1a2e;border-left:4px solid #3b82f6;border-radius:8px;padding:1rem;margin:0.5rem 0;">'
                                f'{guidance_text}'
                                f'</div>', unsafe_allow_html=True
                            )
                        
                        st.info(f"🔄 {t('try_again_after', lang)}")
                else:
                    st.warning(t('enter_answer', lang))
        
        with col2:
            hint_key = f"hint_{question_id}_{st.session_state.current_step}"
            if hint_key not in st.session_state.show_hints:
                st.session_state.show_hints[hint_key] = False
            
            if st.button(f"💡 {t('need_hint', lang)}", key=f"hint_btn_{question_id}_{st.session_state.current_step}", use_container_width=True):
                st.session_state.show_hints[hint_key] = not st.session_state.show_hints[hint_key]
                st.rerun()
        
        if st.session_state.show_hints.get(hint_key, False):
            st.markdown("---")
            st.markdown(f"#### {t('hint_title', lang)}")
            hint_index = min(st.session_state.current_step, len(hints) - 1)
            if hint_index >= 0 and hint_index < len(hints):
                st.info(hints[hint_index])
            else:
                st.info(t('key_concept_hint', lang))
        
        with st.expander(t('view_key_points', lang)):
            for point in guidance.get('key_points', []):
                st.markdown(f"- {point}")
    
    else:
        st.markdown("---")
        st.success(t('all_steps', lang))
        st.markdown(f"### {t('answer_review', lang)}")
        for i, ans in enumerate(st.session_state.user_answers.get(question_id, []), 1):
            st.markdown(f"**{t('step', lang)} {i}:** {ans}")
        
        if st.button(f"✅ {t('complete', lang)}", type="primary", key=f"complete_{question_id}", use_container_width=True):
            st.session_state.completed_questions.add(question_id)
            st.session_state.current_question = None
            st.session_state.current_step = 0
            st.rerun()

def main():
    # 获取当前语言（从主页session_state继承）
    lang = st.session_state.get('lang', 'zh-CN')
    
    st.set_page_config(
        page_title=t('page_title', lang),
        page_icon="🎯",
        layout="wide"
    )
    
    init_session_state()
    
    st.title(f"🎯 {t('subtitle', lang)}")
    
    questions_data = load_questions()
    
    if not any(questions_data.values()):
        st.warning(t('no_data', lang))
        st.markdown(t('no_data_steps', lang))
        return
    
    total_questions = sum(len(questions_data[level]) for level in ['basic', 'intermediate', 'advanced'])
    completed = len(st.session_state.completed_questions)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t('total', lang), total_questions)
    with col2:
        st.metric(t('completed', lang), completed)
    with col3:
        st.metric(t('completion_rate', lang), f"{completed/total_questions*100:.1f}%" if total_questions > 0 else "0%")
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs([
        f"{t('basic', lang)}",
        f"{t('intermediate', lang)}",
        f"{t('advanced', lang)}"
    ])
    
    with tab1:
        for i, question in enumerate(questions_data.get('basic', [])):
            render_question_card(question, 'basic', i, lang)
    
    with tab2:
        for i, question in enumerate(questions_data.get('intermediate', [])):
            render_question_card(question, 'intermediate', i, lang)
    
    with tab3:
        for i, question in enumerate(questions_data.get('advanced', [])):
            render_question_card(question, 'advanced', i, lang)

if __name__ == "__main__":
    main()
