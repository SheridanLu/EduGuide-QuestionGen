# streamlit_app.py - 美观简约版 v4.0
import streamlit as st
import json
import os

# ========== 多语言 ==========
LANGUAGES = {"en": "🇺🇸 EN", "zh-CN": "🇨🇳 中文", "zh-TW": "🇹🇼 繁體"}

T = {
    "en": {
        "title": "EduGuide", "subtitle": "AI-Powered Question Generation",
        "upload": "Upload Material", "upload_hint": "Drag & drop or click to upload",
        "input": "Or paste text...", "words": "words",
        "error": "Student error (optional)", "error_hint": "e.g., confused X with Y",
        "generate": "Generate", "generating": "Generating...", "done": "Done!",
        "knowledge": "Knowledge", "questions": "Questions", "remedial": "Remedial",
        "basic": "Basic", "intermediate": "Intermediate", "advanced": "Advanced",
        "api": "Settings", "provider": "Provider", "key": "API Key", "model": "Model",
        "save": "Save", "saved": "Saved!", "language": "Language",
        "start": "Start Practice", "step": "Step", "answer": "Your Answer",
        "submit": "Submit", "hint": "Hint", "correct": "Correct!",
        "retry": "Try again", "complete": "Complete",
        "progress": "Progress", "back": "Back",
        "current_api": "Current API",
    },
    "zh-CN": {
        "title": "EduGuide", "subtitle": "智能出题系统",
        "upload": "上传教材", "upload_hint": "拖拽或点击上传",
        "input": "或粘贴文本...", "words": "字",
        "error": "学生错误（可选）", "error_hint": "例如：混淆了A和B",
        "generate": "生成题目", "generating": "生成中...", "done": "完成！",
        "knowledge": "知识点", "questions": "题目", "remedial": "补救",
        "basic": "基础", "intermediate": "中级", "advanced": "高级",
        "api": "API 设置", "provider": "提供商", "key": "密钥", "model": "模型",
        "save": "保存", "saved": "已保存！", "language": "语言",
        "start": "开始解题", "step": "步骤", "answer": "你的答案",
        "submit": "提交", "hint": "提示", "correct": "正确！", "retry": "再试一次",
        "complete": "完成", "progress": "进度", "back": "返回",
        "current_api": "当前 API",
    },
    "zh-TW": {
        "title": "EduGuide", "subtitle": "智慧出題系統",
        "upload": "上傳教材", "upload_hint": "拖曳或點擊上傳",
        "input": "或貼上文字...", "words": "字",
        "error": "學生錯誤（可選）", "error_hint": "例如：混淆了A和B",
        "generate": "生成題目", "generating": "生成中...", "done": "完成！",
        "knowledge": "知識點", "questions": "題目", "remedial": "補救",
        "basic": "基礎", "intermediate": "中級", "advanced": "高級",
        "api": "API 設定", "provider": "提供商", "key": "金鑰", "model": "模型",
        "save": "儲存", "saved": "已儲存！", "language": "語言",
        "start": "開始解題", "step": "步驟", "answer": "你的答案",
        "submit": "提交", "hint": "提示", "correct": "正確！", "retry": "再試一次",
        "complete": "完成", "progress": "進度", "back": "返回",
        "current_api": "當前 API",
    }
}

def t(key, lang="en"):
    return T.get(lang, T["en"]).get(key, key)

# ========== 配置 ==========
st.set_page_config(page_title="EduGuide", page_icon="🎓", layout="wide", initial_sidebar_state="auto")

# ========== CSS ==========
st.markdown("""<style>
/* === Reset Defaults === */
.css-1efxmp, .cm4xw3, .e8xn31, .edgvf1 { all: revert; }

/* === Typography === */
h1, h2, h3, h4, h5, h6, .stMarkdown, .stMarkdown p {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
    color: #1a1a1a;
}

/* === Layout === */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 900px;
}

/* === Top Bar === */
.top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    margin-bottom: 2rem;
    border-bottom: 1px solid #eee;
}

.top-bar-logo {
    font-size: 1.4rem;
    font-weight: 700;
    color: #1a1a1a;
    letter-spacing: -0.5px;
}

.top-bar-right {
    display: flex;
    gap: 0.75rem;
    align-items: center;
}

/* === Hero === */
.hero {
    text-align: center;
    padding: 4rem 2rem;
    background: #1a1a1a;
    border-radius: 24px;
    margin-bottom: 2rem;
    color: white;
}

.hero h1 {
    font-size: 3rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -1px;
}

.hero p {
    font-size: 1.1rem;
    color: rgba(255,255,255,0.75);
    margin: 0.5rem 0 0 0;
}

/* === Card === */
.card {
    background: white;
    border-radius: 20px;
    padding: 1.5rem 2rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    border: 1px solid #f0f0f0;
    margin-bottom: 1rem;
    transition: box-shadow 0.2s ease;
}

.card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

/* === Upload === */
.upload-box {
    border: 2px dashed #ddd;
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    background: #fafbfc;
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: 1.5rem;
}

.upload-box:hover {
    border-color: #bbb;
    background: #f0f0f8;
}

.upload-box .upload-icon {
    font-size: 2.5rem;
    margin-bottom: 0.75rem;
}

.upload-box .upload-text {
    color: #888;
    font-size: 0.95rem;
}

/* === Text Area === */
.stTextArea textarea {
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 1rem 1rem;
    font-size: 1rem;
    line-height: 1.6;
    resize: vertical;
    transition: border-color 0.2s;
}

.stTextArea textarea:focus {
    outline: none;
    border-color: #333;
}

/* === Select / Input === */
.stSelectbox > div > div, .stTextInput > div > div {
    font-size: 0.95rem;
}

.stSelectbox > div > div[data-baseweb="select"] {
    font-size: 0.95rem;
}

/* === Buttons === */
.stButton > button {
    border-radius: 12px;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.75rem 1.5rem;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}

/* Primary button */
.stButton > button[data-testid="stPrimary"] {
    background: #1a1a1a;
    color: white;
    border: none;
}

/* === Question Card === */
.question-card {
    background: #fafbfc;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.75rem;
    border-left: 3px solid #ddd;
    transition: all 0.2s ease;
}

.question-card:hover {
    border-left-color: #333;
}

/* === Step Card === */
.step-done {
    background: #f0fdf4;
    border-left: 3px solid #4caf50;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin: 0.75rem 0;
}

.step-current {
    background: #fff;
    border-left: 3px solid #333;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin: 0.75rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

/* === API Card === */
.api-card {
    background: #1a1a1a;
    border-radius: 16px;
    padding: 1.25rem 1.75rem;
    color: white;
}

.api-card .api-name {
    font-size: 0.95rem;
    font-weight: 600;
    opacity: 0.9;
}

.api-card .api-model {
    font-size: 0.85rem;
    opacity: 0.7;
    margin-top: 0.25rem;
}

/* === Tabs === */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: transparent;
    border-bottom: 2px solid #eee;
    margin-bottom: 1.5rem;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 0;
    padding: 12px 20px;
    font-weight: 500;
    background: transparent;
    color: #888;
    border-bottom: 2px solid transparent;
    transition: all 0.2s ease;
}

.stTabs [aria-selected="true"] {
    color: #1a1a1a;
    border-bottom: 2px solid #1a1a1a;
}

/* === Metrics === */
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #1a1a1a;
}

.metric-label {
    font-size: 0.8rem;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* === Misc === */
.stDivider {
    height: 1px;
    background: #eee;
    border: none;
    margin: 1.5rem 0;
}

.divider {
    height: 1px;
    background: #eee;
    border: none;
    margin: 1.5rem 0;
}

.small { font-size: 0.85rem; color: #aaa; }
.hide-label label { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ========== 初始化 ==========
if 'lang' not in st.session_state: st.session_state.lang = "zh-CN"
if 'text' not in st.session_state: st.session_state.text = ""
if 'result' not in st.session_state: st.session_state.result = None
if 'practice' not in st.session_state: st.session_state.practice = None
if 'step' not in st.session_state: st.session_state.step = 0
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'show_api' not in st.session_state: st.session_state.show_api = False

lang = st.session_state.lang

# ========== 顶部栏 ==========
st.markdown(f'<div class="top-bar"><div class="top-bar-logo">🎓 EduGuide</div><div class="top-bar-right"></div></div>', unsafe_allow_html=True)

# 语言选择
new_lang = st.selectbox(
    t('language', lang),
    list(LANGUAGES.keys()),
    format_func=lambda x: LANGUAGES[x],
    index=list(LANGUAGES.keys()).index(lang),
    label_visibility="collapsed"
)
if new_lang != lang:
    st.session_state.lang = new_lang
    st.rerun()

# API设置按钮
if st.button(f"⚙️ {t('api', lang)}", key="api_toggle"):
    st.session_state.show_api = not st.session_state.show_api

# ========== API设置面板 ==========
if st.session_state.show_api:
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
            index=list(options.keys()).index(current.value),
        )
        config = cm.providers.get(APIProvider(selected))
        
        col1, col2 = st.columns(2)
        with col1:
            key = st.text_input(f"**{t('key', lang)}**", value=config.api_key, type="password")
        with col2:
            model = st.text_input(f"**{t('model', lang)}**", value=config.model)
            if st.button(f"✅ {t('save', lang)}", type="primary"):
                new_cfg = ProviderConfig(name=config.name, api_key=key, base_url=config.base_url, model=model, enabled=True)
                cm.update_provider_config(APIProvider(selected), new_cfg)
                cm.set_current_provider(APIProvider(selected))
                st.success(t('saved', lang))
    except Exception as e:
        st.error(f"Error: {e}")
    st.markdown("---")

# ========== Hero ==========
st.markdown(f"""
<div class="hero">
    <h1>🎓 {t('title', lang)}</h1>
    <p>{t('subtitle', lang)}</p>
</div>
""", unsafe_allow_html=True)

# ========== 主内容 ==========
c1, c2 = st.columns([3, 2])

with c1:
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
                content = "\n".join([p.extract_text() for p in PyPDF2.PdfReader(uploaded).pages if p.extract_text()])
            elif uploaded.name.endswith('.docx'):
                import docx
                content = "\n".join([p.text for p in docx.Document(uploaded).paragraphs if p.text])
            elif uploaded.name.endswith('.pptx'):
                from pptx import Presentation
                content = ""
                for slide in Presentation(uploaded).slides:
                    for shape in slide.shapes:
                        if hasattr(shape, "text"): content += shape.text + "\n"
            st.session_state.text = content
            st.success(f"✅ {uploaded.name}")
        except Exception as e:
            st.error(f"Error: {e}")
    
    # 文本输入
    text = st.text_area(
        t('input', lang),
        value=st.session_state.text,
        height=220,
        placeholder=t('placeholder', lang),
        label_visibility="collapsed"
    )
    if text:
        st.session_state.text = text
        st.markdown(f"<div class='divider'></div><div class='small'>{len(text)} {t('words', lang)}</div>", unsafe_allow_html=True)

with c2:
    # API信息卡片
    try:
        from config.api_config import get_config_manager
        cfg = get_config_manager().get_current_config()
        st.markdown(f"""
        <div class="api-card">
            <div class="api-name">🔌 {t('current_api', lang)}</div>
            <div class="api-model">{cfg.model}</div>
        </div>
        """, unsafe_allow_html=True)
    except: pass
    
    # 错误点输入
    st.markdown(f"**{t('error', lang)}**")
    error = st.text_input(
        t('error_hint', lang),
        label_visibility="collapsed"
    )

# 生成按钮
st.markdown("<div class='divider'></div>")
st.button(f"🚀 {t('generate', lang)}", type="primary", use_container_width=True)

# ========== 结果 ==========
if st.session_state.result:
    st.markdown("<div class='divider'></div>")
    
    # 加载数据
    q_data, a_data = {}, {}
    if os.path.exists("output/questions.json"):
        with open("output/questions.json", 'r', encoding='utf-8') as f:
            q_data = json.load(f)
    if os.path.exists("output/answers.json"):
        with open("output/answers.json", 'r', encoding='utf-8') as f:
            a_data = json.load(f)
    
    # 练习模式
    if st.session_state.practice:
        qid = st.session_state.practice
        level, idx = qid.split('_')
        idx = int(idx)
        question = q_data.get(level, [])[idx]
        guidance = a_data.get(level, [])[idx].get('guidance', {}) if idx < len(a_data.get(level, [])) else {}
        steps = [guidance.get(f'step{i}', '') for i in range(1, 4)]
        steps = [s for s in steps if s]
        
        if st.button(f"← {t('back', lang)}"):
            st.session_state.practice = None
            st.session_state.step = 0
            st.rerun()
        
        st.markdown(f"### {question}")
        progress = st.session_state.step / len(steps) if steps else 0
        st.progress(progress)
        st.markdown(f"**{t('progress', lang)}: {st.session_state.step}/{len(steps)} {t('steps_text', lang)}**")
        
        for i in range(st.session_state.step):
            ans = st.session_state.answers.get(f"{qid}_{i}", '')
            st.markdown(f"<div class='step-done'><strong>✅ {t('step', lang)} {i+1}:</strong> {steps[i]}<br><small class='small'>答案: {ans}</small></div>", unsafe_allow_html=True)
        
        if st.session_state.step < len(steps):
            st.markdown(f"<div class='step-current'><strong>{t('step', lang)} {st.session_state.step+1}:</strong> {steps[st.session_state.step]}</div>", unsafe_allow_html=True)
            ans = st.text_area(t('answer', lang), key=f"ans_{qid}_{st.session_state.step}", height=100)
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"✅ {t('submit', lang)}", use_container_width=True):
                    if ans.strip():
                        st.session_state.answers[f"{qid}_{st.session_state.step}"] = ans
                        st.session_state.step += 1
                        st.success(t('correct', lang))
                        st.rerun()
                    else:
                        st.warning(t('enter_answer', lang))
            with c2:
                if st.button(f"💡 {t('hint', lang)}", use_container_width=True):
                    hints = guidance.get('hints', [])
                    st.info(hints[st.session_state.step] if st.session_state.step < len(hints) else "Think about key concepts.")
        
        else:
            st.success(t('complete', lang))
            if st.button(f"✅ {t('complete', lang)}", use_container_width=True):
                st.session_state.practice = None
                st.session_state.step = 0
                st.rerun()
    else:
        t1, t2, t3 = st.tabs([f"💡 {t('knowledge', lang)}", f"📝 {t('questions', lang)}", f"🤝 {t('remedial', lang)}"])
        
        with t1:
            if os.path.exists("output/knowledge.json"):
                with open("output/knowledge.json", 'r', encoding='utf-8') as f:
                    for i, p in enumerate(json.load(f).get("knowledge_points", []), 1):
                        st.markdown(f"**{i}.** {p}")
        
        with t2:
            for level, title in [("basic", f"🟢 {t('basic', lang)}"), ("intermediate", f"🟡 {t('intermediate', lang)}"), ("advanced", f"🔴 {t('advanced', lang)}")]:
                if level in q_data:
                    st.markdown(f"### {title}")
                    for i, q in enumerate(q_data[level], 1):
                        st.markdown(f"<div class='question-card'><strong>Q{i}:</strong> {q}</div>", unsafe_allow_html=True)
                        if st.button(t('start', lang), key=f"start_{level}_{i}", type="primary"):
                            st.session_state.practice = f"{level}_{i}"
                            st.session_state.step = 0
                            st.rerun()
        
        with t3:
            if os.path.exists("output/remedial.json"):
                with open("output/remedial.json", 'r', encoding='utf-8') as f:
                    for item in json.load(f).get("remedial", []):
                        g = item.get('guidance', {})
                        for k in ['probing_question_1', 'probing_question_2', 'probing_question_3']:
                            if k in g:
                                st.markdown(f"**{k.replace('_', ' ').title()}:** {g[k]}")
