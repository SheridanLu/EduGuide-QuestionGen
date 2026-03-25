# pages/🎯_解题练习.py - 交互式解题页面
import streamlit as st
import json
import os
from typing import Dict, Any, List

def init_session_state():
    """初始化会话状态"""
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

def load_questions() -> Dict[str, Any]:
    """加载题目数据"""
    questions_path = "output/questions.json"
    answers_path = "output/answers.json"
    
    data = {
        'basic': [],
        'intermediate': [],
        'advanced': []
    }
    
    if os.path.exists(questions_path):
        with open(questions_path, 'r', encoding='utf-8') as f:
            questions = json.load(f)
            data.update(questions)
    
    if os.path.exists(answers_path):
        with open(answers_path, 'r', encoding='utf-8') as f:
            answers = json.load(f)
            # 将引导信息合并到题目中
            for level in ['basic', 'intermediate', 'advanced']:
                if level in answers:
                    for i, answer in enumerate(answers[level]):
                        if i < len(data.get(level, [])):
                            if isinstance(data[level][i], dict):
                                data[level][i]['guidance'] = answer.get('guidance', {})
                            else:
                                data[level][i] = {
                                    'question': data[level][i],
                                    'guidance': answer.get('guidance', {})
                                }
    
    return data

def check_answer(user_answer: str, expected_keywords: List[str]) -> tuple:
    """检查答案（基于关键词匹配）"""
    user_answer = user_answer.strip().lower()
    
    # 简单的关键词匹配
    matched = sum(1 for keyword in expected_keywords if keyword.lower() in user_answer)
    
    if matched >= len(expected_keywords) * 0.7:  # 匹配70%以上
        return True, "✅ 很好！你的答案抓住了关键点。"
    elif matched >= len(expected_keywords) * 0.4:  # 匹配40%以上
        return False, "⚠️ 你接近了，但还差一点点。再想想？"
    else:
        return False, "❌ 似乎不太对。让我们重新思考这个问题。"

def render_question_card(question_data: Dict, level: str, index: int):
    """渲染单个题目的卡片"""
    question_id = f"{level}_{index}"
    question_text = question_data.get('question', question_data) if isinstance(question_data, dict) else question_data
    guidance = question_data.get('guidance', {}) if isinstance(question_data, dict) else {}
    
    # 检查是否已完成
    is_completed = question_id in st.session_state.completed_questions
    
    with st.expander(
        f"{'✅' if is_completed else '📝'} {level.upper()} - 题目 {index + 1}",
        expanded=(st.session_state.current_question == question_id)
    ):
        st.markdown(f"### 📋 题目")
        st.info(f"**{question_text}**")
        
        if is_completed:
            st.success("🎉 恭喜！你已经完成了这道题！")
            if st.button(f"🔄 重新练习", key=f"retry_{question_id}"):
                st.session_state.completed_questions.discard(question_id)
                st.session_state.current_step = 0
                st.session_state.user_answers.pop(question_id, None)
                st.rerun()
        else:
            # 开始练习按钮
            if st.session_state.current_question != question_id:
                if st.button(f"🚀 开始解题", key=f"start_{question_id}", type="primary"):
                    st.session_state.current_question = question_id
                    st.session_state.current_step = 0
                    st.session_state.user_answers[question_id] = []
                    st.rerun()
            else:
                render_interactive_steps(question_id, question_text, guidance)

def render_interactive_steps(question_id: str, question_text: str, guidance: Dict):
    """渲染交互式解题步骤"""
    steps = [
        guidance.get('step1', '让我们先理解这道题在问什么'),
        guidance.get('step2', '现在思考相关的知识点'),
        guidance.get('step3', '建立你的答案逻辑')
    ]
    
    hints = guidance.get('hints', [])
    key_points = guidance.get('key_points', [])
    
    # 进度条
    progress = st.session_state.current_step / len(steps)
    st.progress(progress)
    st.markdown(f"**进度:** {st.session_state.current_step}/{len(steps)} 步")
    
    # 当前步骤
    if st.session_state.current_step < len(steps):
        current_step_text = steps[st.session_state.current_step]
        
        st.markdown("---")
        st.markdown(f"### 💭 步骤 {st.session_state.current_step + 1}")
        st.markdown(f"**{current_step_text}**")
        
        # 用户输入区域
        st.markdown("#### ✍️ 你的思考")
        user_input = st.text_area(
            "写下你的想法或答案",
            key=f"input_{question_id}_{st.session_state.current_step}",
            height=100,
            placeholder="在这里输入你的思考过程或答案..."
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("✅ 提交答案", type="primary", key=f"submit_{question_id}_{st.session_state.current_step}"):
                if user_input.strip():
                    # 保存答案
                    if question_id not in st.session_state.user_answers:
                        st.session_state.user_answers[question_id] = []
                    st.session_state.user_answers[question_id].append(user_input)
                    
                    # 简单验证（这里可以接入AI验证）
                    if len(user_input) > 10:  # 简单检查：答案长度
                        st.success("✅ 很好！继续下一步。")
                        st.session_state.current_step += 1
                        st.rerun()
                    else:
                        st.warning("⚠️ 答案太简短了，能再详细一点吗？")
                else:
                    st.error("❌ 请先输入你的答案")
        
        with col2:
            # 提示按钮
            hint_key = f"hint_{question_id}_{st.session_state.current_step}"
            if hint_key not in st.session_state.show_hints:
                st.session_state.show_hints[hint_key] = False
            
            if st.button("💡 需要提示", key=f"hint_btn_{question_id}_{st.session_state.current_step}"):
                st.session_state.show_hints[hint_key] = not st.session_state.show_hints[hint_key]
                st.rerun()
        
        # 显示提示
        if st.session_state.show_hints.get(hint_key, False):
            st.markdown("---")
            st.markdown("#### 💡 提示")
            hint_index = min(st.session_state.current_step, len(hints) - 1)
            if hint_index >= 0 and hint_index < len(hints):
                st.info(hints[hint_index])
            else:
                st.info("想想题目中的关键词和它们之间的关系。")
        
        # 显示关键点（可展开）
        with st.expander("🔑 查看关键点"):
            for point in key_points:
                st.markdown(f"- {point}")
    
    else:
        # 完成所有步骤
        st.markdown("---")
        st.success("🎉 太棒了！你已经完成了所有步骤！")
        
        # 显示完整答案回顾
        st.markdown("### 📝 你的答案回顾")
        for i, answer in enumerate(st.session_state.user_answers.get(question_id, []), 1):
            st.markdown(f"**步骤 {i}:** {answer}")
        
        # 标记为完成
        if st.button("✅ 完成此题", type="primary", key=f"complete_{question_id}"):
            st.session_state.completed_questions.add(question_id)
            st.session_state.current_question = None
            st.session_state.current_step = 0
            st.rerun()

def main():
    st.set_page_config(
        page_title="🎯 解题练习 - EduGuide",
        page_icon="🎯",
        layout="wide"
    )
    
    init_session_state()
    
    st.title("🎯 交互式解题练习")
    st.markdown("**一步步引导，自己得出答案**")
    
    # 加载题目
    questions_data = load_questions()
    
    if not any(questions_data.values()):
        st.warning("⚠️ 暂无题目数据。请先在主页生成题目。")
        st.markdown("**步骤：**")
        st.markdown("1. 返回主页")
        st.markdown("2. 上传教材文件或输入文本")
        st.markdown("3. 点击 '🚀 开始生成'")
        st.markdown("4. 等待生成完成后，返回此页面")
        return
    
    # 统计信息
    total_questions = sum(len(questions_data[level]) for level in ['basic', 'intermediate', 'advanced'])
    completed = len(st.session_state.completed_questions)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("总题目数", total_questions)
    with col2:
        st.metric("已完成", completed)
    with col3:
        st.metric("完成率", f"{completed/total_questions*100:.1f}%" if total_questions > 0 else "0%")
    
    st.markdown("---")
    
    # 题目列表
    tab1, tab2, tab3 = st.tabs(["🟢 基础题", "🟡 中级题", "🔴 高级题"])
    
    with tab1:
        st.subheader("基础题")
        for i, question in enumerate(questions_data.get('basic', [])):
            render_question_card(question, 'basic', i)
    
    with tab2:
        st.subheader("中级题")
        for i, question in enumerate(questions_data.get('intermediate', [])):
            render_question_card(question, 'intermediate', i)
    
    with tab3:
        st.subheader("高级题")
        for i, question in enumerate(questions_data.get('advanced', [])):
            render_question_card(question, 'advanced', i)

if __name__ == "__main__":
    main()
