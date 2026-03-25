# streamlit_app.py - 简洁优雅版界面 + 交互式引导
import streamlit as st
import json
import os

# ========== 多语言配置 ==========
LANGUAGES = {
    "en": "🇺🇸 English",
    "zh-CN": "🇨🇳 简体中文",
    "zh-TW": "🇹🇼 繁體中文"
}

T = {
    "en": {
        "title": "EduGuide",
        "subtitle": "Intelligent Question Generation",
        "upload": "Upload Material",
        "upload_hint": "Drag & drop or click to upload",
        "input": "Or paste text here...",
        "words": "words",
        "error": "Student misunderstanding (optional)",
        "error_hint": "e.g., confused X with Y",
        "generate": "Generate Questions",
        "generating": "Generating...",
        "done": "Done!",
        "knowledge": "Knowledge Points",
        "questions": "Questions",
        "guidance": "Guidance",
        "remedial": "Remedial",
        "basic": "Basic",
        "intermediate": "Intermediate",
        "advanced": "Advanced",
        "api": "API Settings",
        "provider": "Provider",
        "key": "API Key",
        "model": "Model",
        "save": "Save",
        "saved": "Saved",
        "lang": "Language",
        "start_practice": "🎯 Start Practice",
        "interactive": "Interactive Practice",
        "step": "Step",
        "your_answer": "Your Answer",
        "submit": "Submit",
        "hint": "Hint",
        "correct": "Correct!",
        "try_again": "Try again",
        "next_step": "Next Step",
        "complete": "Complete",
        "progress": "Progress",
        "expand": "Click to expand",
        "practice_hint": "💡 Practice step-by-step with verification",
    },
    "zh-CN": {
        "title": "EduGuide",
        "subtitle": "智能出题系统",
        "upload": "上传教材",
        "upload_hint": "拖拽或点击上传文件",
        "input": "或在此粘贴文本...",
        "words": "字",
        "error": "学生常见错误（可选）",
        "error_hint": "例如：混淆了A和B",
        "generate": "生成题目",
        "generating": "生成中...",
        "done": "完成！",
        "knowledge": "知识点",
        "questions": "题目",
        "guidance": "引导",
        "remedial": "补救",
        "basic": "基础",
        "intermediate": "中级",
        "advanced": "高级",
        "api": "API 设置",
        "provider": "提供商",
        "key": "API 密钥",
        "model": "模型",
        "save": "保存",
        "saved": "已保存",
        "lang": "语言",
        "start_practice": "🎯 开始练习",
        "interactive": "交互式练习",
        "step": "步骤",
        "your_answer": "你的答案",
        "submit": "提交",
        "hint": "提示",
        "correct": "正确！",
        "try_again": "再试一次",
        "next_step": "下一步",
        "complete": "完成",
        "progress": "进度",
        "expand": "点击展开",
        "practice_hint": "💡 一步步练习，验证每个答案",
    },
    "zh-TW": {
        "title": "EduGuide",
        "subtitle": "智慧出題系統",
        "upload": "上傳教材",
        "upload_hint": "拖曳或點擊上傳檔案",
        "input": "或在此貼上文字...",
        "words": "字",
        "error": "學生常見錯誤（可選）",
        "error_hint": "例如：混淆了A和B",
        "generate": "生成題目",
        "generating": "生成中...",
        "done": "完成！",
        "knowledge": "知識點",
        "questions": "題目",
        "guidance": "引導",
        "remedial": "補救",
        "basic": "基礎",
        "intermediate": "中級",
        "advanced": "高級",
        "api": "API 設定",
        "provider": "提供商",
        "key": "API 金鑰",
        "model": "模型",
        "save": "儲存",
        "saved": "已儲存",
        "lang": "語言",
        "start_practice": "🎯 開始練習",
        "interactive": "交互式練習",
        "step": "步驟",
        "your_answer": "你的答案",
        "submit": "提交",
        "hint": "提示",
        "correct": "正確！",
        "try_again": "再試一次",
        "next_step": "下一步",
        "complete": "完成",
        "progress": "進度",
        "expand": "點擊展開",
        "practice_hint": "💡 一步步練習，驗證每個答案",
    }
}

def t(key, lang="en"):
    return T.get(lang, T["en"]).get(key, key)

# ========== 页面配置 ==========
st.set_page_config(
    page_title="EduGuide",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ========== 自定义CSS ==========
st.markdown("""
<style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 800px;
    }
    
    .title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        color: #1a1a1a;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }
    
    .upload-box {
        border: 2px dashed #d0d0d0;
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        background: #fafafa;
        transition: all 0.3s ease;
        margin-bottom: 2rem;
    }
    
    .upload-box:hover {
        border-color: #999;
        background: #f5f5f5;
    }
    
    .upload-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .upload-text {
        color: #666;
        font-size: 0.95rem;
    }
    
    .stTextArea textarea {
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        font-size: 0.95rem;
        min-height: 150px;
    }
    
    .stTextArea textarea:focus {
        border-color: #4a90e2;
        box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
    }
    
    .stButton button {
        width: 100%;
        border-radius: 12px;
        height: 54px;
        font-size: 1rem;
        font-weight: 600;
        background: #1a1a1a;
        border: none;
        color: white;
        transition: all 0.2s ease;
    }
    
    .stButton button:hover {
        background: #333;
        transform: translateY(-1px);
    }
    
    .card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #eee;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f5f5f5;
        border-radius: 12px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 12px 20px;
        font-weight: 500;
        background: transparent;
        color: #666;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: #1a1a1a;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #eee;
    }
    
    [data-testid="stSidebar"] .block-container {
        padding: 2rem 1.5rem;
    }
    
    .hint {
        font-size: 0.85rem;
        color: #999;
    }
    
    .question-card {
        padding: 1.25rem;
        border-left: 3px solid #4a90e2;
        background: #f8f9fa;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .practice-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    .practice-btn button {
        background: white !important;
        color: #667eea !important;
    }
    
    .step-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #4a90e2;
    }
    
    .step-active {
        background: #e3f2fd;
        border-left-color: #2196f3;
    }
    
    .step-complete {
        background: #e8f5e9;
        border-left-color: #4caf50;
    }
    
    .progress-bar {
        height: 8px;
        background: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #4a90e2 0%, #667eea 100%);
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# ========== 初始化 ==========
if 'lang' not in st.session_state:
    st.session_state.lang = "zh-CN"
if 'text' not in st.session_state:
    st.session_state.text = ""
if 'result' not in st.session_state:
    st.session_state.result = None
if 'practice_question' not in st.session_state:
    st.session_state.practice_question = None
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

lang = st.session_state.lang

# ========== 侧边栏 ==========
with st.sidebar:
    st.markdown(f"### ⚙️ {t('api', lang)}")
    
    new_lang = st.selectbox(
        f"**{t('lang', lang)}**",
        list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x],
        index=list(LANGUAGES.keys()).index(lang)
    )
    if new_lang != lang:
        st.session_state.lang = new_lang
        st.rerun()
    
    st.markdown("---")
    
    try:
        from config.api_config import get_config_manager, APIProvider, ProviderConfig
        cm = get_config_manager()
        current = cm.current_provider
        
        providers = cm.get_all_providers()
        options = {p['id']: p['name'] for p in providers}
        
        selected = st.selectbox(
            f"**{t('provider', lang)}**",
            list(options.keys()),
            format_func=lambda x: options[x],
            index=list(options.keys()).index(current.value)
        )
        
        config = cm.providers.get(APIProvider(selected))
        
        key = st.text_input(f"**{t('key', lang)}**", value=config.api_key, type="password")
        model = st.text_input(f"**{t('model', lang)}**", value=config.model)
        
        if st.button(t('save', lang), use_container_width=True):
            new_cfg = ProviderConfig(name=config.name, api_key=key, 
                                    base_url=config.base_url, model=model, enabled=True)
            cm.update_provider_config(APIProvider(selected), new_cfg)
            cm.set_current_provider(APIProvider(selected))
            st.success(t('saved', lang))
    except Exception as e:
        st.error(f"Error: {e}")

# ========== 主页 ==========
st.markdown(f'<div class="title">🎓 {t("title", lang)}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{t("subtitle", lang)}</div>', unsafe_allow_html=True)

# 上传区域
st.markdown(f"""
<div class="upload-box">
    <div class="upload-icon">📁</div>
    <div class="upload-text">{t('upload_hint', lang)}</div>
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader("", type=['txt', 'pdf', 'docx', 'pptx'], label_visibility="collapsed")

if uploaded:
    try:
        if uploaded.name.endswith('.txt'):
            content = uploaded.read().decode('utf-8')
        elif uploaded.name.endswith('.pdf'):
            import PyPDF2
            pdf = PyPDF2.PdfReader(uploaded)
            content = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
        elif uploaded.name.endswith('.docx'):
            import docx
            doc = docx.Document(uploaded)
            content = "\n".join([p.text for p in doc.paragraphs if p.text])
        elif uploaded.name.endswith('.pptx'):
            from pptx import Presentation
            prs = Presentation(uploaded)
            content = ""
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        content += shape.text + "\n"
        st.session_state.text = content
        st.success(f"✅ {uploaded.name}")
    except Exception as e:
        st.error(f"Error: {e}")

text = st.text_area(t('input', lang), value=st.session_state.text, height=200, label_visibility="collapsed")
if text:
    st.session_state.text = text
    st.markdown(f'<div class="hint">{len(text)} {t("words", lang)}</div>', unsafe_allow_html=True)

st.markdown("---")
error = st.text_input(t('error', lang), placeholder=t('error_hint', lang), label_visibility="collapsed")

st.markdown("")
if st.button(t('generate', lang), type="primary"):
    if not text:
        st.warning("Please input material" if lang == "en" else "请输入教材内容")
    else:
        with st.spinner(t('generating', lang)):
            try:
                from workflow.openclaw_flow import OpenClawFlow
                flow = OpenClawFlow()
                result = flow.run(text, error if error else None)
                st.session_state.result = result
                st.success(t('done', lang))
            except Exception as e:
                st.error(f"Error: {e}")

# ========== 结果展示（含交互式练习）==========
if st.session_state.result:
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        f"💡 {t('knowledge', lang)}",
        f"📝 {t('questions', lang)}",
        f"📚 {t('guidance', lang)}",
        f"🤝 {t('remedial', lang)}"
    ])
    
    # 知识点
    with tab1:
        kp = "output/knowledge.json"
        if os.path.exists(kp):
            with open(kp, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for i, p in enumerate(data.get("knowledge_points", []), 1):
                st.markdown(f"**{i}.** {p}")
    
    # 题目
    with tab2:
        qp = "output/questions.json"
        if os.path.exists(qp):
            with open(qp, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            levels = [
                ("basic", f"🟢 {t('basic', lang)}"),
                ("intermediate", f"🟡 {t('intermediate', lang)}"),
                ("advanced", f"🔴 {t('advanced', lang)}")
            ]
            
            for level, title in levels:
                if level in data:
                    st.markdown(f"### {title}")
                    for i, q in enumerate(data[level], 1):
                        st.markdown(f'<div class="question-card"><strong>Q{i}:</strong> {q}</div>', unsafe_allow_html=True)
    
    # 引导（含交互式练习）
    with tab3:
        ap = "output/answers.json"
        if os.path.exists(ap):
            with open(ap, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 交互式练习提示
            st.markdown(f"""
            <div class="practice-card">
                <h3>{t('interactive', lang)}</h3>
                <p>{t('practice_hint', lang)}</p>
            </div>
            """, unsafe_allow_html=True)
            
            for level in ["basic", "intermediate", "advanced"]:
                if level in data:
                    level_names = {
                        "basic": f"🟢 {t('basic', lang)}",
                        "intermediate": f"🟡 {t('intermediate', lang)}",
                        "advanced": f"🔴 {t('advanced', lang)}"
                    }
                    st.markdown(f"### {level_names[level]}")
                    
                    for i, item in enumerate(data[level], 1):
                        if isinstance(item, dict):
                            q_id = f"{level}_{i}"
                            question = item.get('question', '')
                            guidance = item.get('guidance', {})
                            
                            # 如果正在练习这道题
                            if st.session_state.practice_question == q_id:
                                steps = [
                                    guidance.get('step1', ''),
                                    guidance.get('step2', ''),
                                    guidance.get('step3', '')
                                ]
                                total_steps = len([s for s in steps if s])
                                current = st.session_state.current_step
                                
                                # 进度条
                                progress = current / total_steps if total_steps > 0 else 0
                                st.markdown(f"**{t('progress', lang)}: {current}/{total_steps}**")
                                st.progress(progress)
                                
                                st.markdown(f"**{question}**")
                                st.markdown("---")
                                
                                # 显示已完成的步骤
                                for idx in range(current):
                                    st.markdown(f"""
                                    <div class="step-card step-complete">
                                        <strong>✅ {t('step', lang)} {idx+1}:</strong><br>
                                        {steps[idx]}<br>
                                        <small>你的答案: {st.session_state.answers.get(f"{q_id}_{idx}", '')}</small>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                # 当前步骤
                                if current < total_steps:
                                    st.markdown(f"""
                                    <div class="step-card step-active">
                                        <strong>{t('step', lang)} {current+1}:</strong><br>
                                        {steps[current]}
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # 答案输入
                                    answer_key = f"{q_id}_{current}"
                                    user_answer = st.text_area(
                                        t('your_answer', lang),
                                        key=f"answer_{q_id}_{current}",
                                        height=100
                                    )
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        if st.button(f"✅ {t('submit', lang)}", key=f"submit_{q_id}_{current}"):
                                            if user_answer.strip():
                                                # 保存答案
                                                st.session_state.answers[answer_key] = user_answer
                                                # 进入下一步
                                                st.session_state.current_step += 1
                                                st.success(t('correct', lang))
                                                st.rerun()
                                            else:
                                                st.warning(t('try_again', lang))
                                    
                                    with col2:
                                        if st.button(f"💡 {t('hint', lang)}", key=f"hint_{q_id}_{current}"):
                                            hints = guidance.get('hints', [])
                                            if hints and current < len(hints):
                                                st.info(hints[current])
                                            else:
                                                st.info("Think about the key concepts in the question." if lang == "en" else "想想题目中的关键概念。")
                                
                                else:
                                    # 完成所有步骤
                                    st.success(f"🎉 {t('complete', lang)}!")
                                    if st.button(f"✅ {t('complete', lang)}", key=f"complete_{q_id}"):
                                        st.session_state.practice_question = None
                                        st.session_state.current_step = 0
                                        st.rerun()
                                
                                # 返回按钮
                                if st.button("← 返回", key=f"back_{q_id}"):
                                    st.session_state.practice_question = None
                                    st.session_state.current_step = 0
                                    st.rerun()
                            
                            else:
                                # 题目卡片（未开始练习）
                                with st.expander(f"**Q{i}:** {question[:60]}..."):
                                    st.markdown(f"**{question}**")
                                    st.markdown("")
                                    
                                    # 开始练习按钮
                                    if st.button(f"🎯 {t('start_practice', lang)}", key=f"start_{q_id}", type="primary"):
                                        st.session_state.practice_question = q_id
                                        st.session_state.current_step = 0
                                        st.rerun()
    
    # 补救
    with tab4:
        rp = "output/remedial.json"
        if os.path.exists(rp):
            with open(rp, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for i, item in enumerate(data.get("remedial", []), 1):
                g = item.get('guidance', {})
                for key in ['probing_question_1', 'probing_question_2', 'probing_question_3']:
                    if key in g:
                        st.markdown(f"**{key.replace('_', ' ').title()}:** {g[key]}")
