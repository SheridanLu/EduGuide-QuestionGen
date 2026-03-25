# streamlit_app.py - 简洁优雅版界面
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
    /* 隐藏默认元素 */
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    
    /* 主容器 */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 800px;
    }
    
    /* 标题 */
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
    
    /* 上传区域 */
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
    
    /* 输入框 */
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
    
    /* 按钮 */
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
    
    .stButton button:active {
        transform: translateY(0);
    }
    
    /* 卡片 */
    .card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #eee;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    /* 标签页 */
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
    
    /* 选择框 */
    .stSelectbox, .stTextInput {
        margin-bottom: 1rem;
    }
    
    /* 侧边栏 */
    [data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #eee;
    }
    
    [data-testid="stSidebar"] .block-container {
        padding: 2rem 1.5rem;
    }
    
    /* 统计数字 */
    .stat {
        text-align: center;
        padding: 1rem;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a1a;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* 题目卡片 */
    .question-card {
        padding: 1.25rem;
        border-left: 3px solid #4a90e2;
        background: #f8f9fa;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    /* 分隔线 */
    .divider {
        height: 1px;
        background: #eee;
        margin: 2rem 0;
    }
    
    /* 小字提示 */
    .hint {
        font-size: 0.85rem;
        color: #999;
    }
    
    /* 成功消息 */
    .success-msg {
        background: #e8f5e9;
        color: #2e7d32;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
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

lang = st.session_state.lang

# ========== 侧边栏 ==========
with st.sidebar:
    st.markdown(f"### ⚙️ {t('api', lang)}")
    
    # 语言选择
    st.markdown(f"**{t('lang', lang)}**")
    new_lang = st.selectbox("", list(LANGUAGES.keys()), 
                           format_func=lambda x: LANGUAGES[x],
                           index=list(LANGUAGES.keys()).index(lang),
                           label_visibility="collapsed")
    if new_lang != lang:
        st.session_state.lang = new_lang
        st.rerun()
    
    st.markdown("---")
    
    # API 配置
    try:
        from config.api_config import get_config_manager, APIProvider, ProviderConfig
        cm = get_config_manager()
        current = cm.current_provider
        
        providers = cm.get_all_providers()
        options = {p['id']: p['name'] for p in providers}
        
        st.markdown(f"**{t('provider', lang)}**")
        selected = st.selectbox("", list(options.keys()),
                               format_func=lambda x: options[x],
                               index=list(options.keys()).index(current.value),
                               label_visibility="collapsed")
        
        config = cm.providers.get(APIProvider(selected))
        
        st.markdown(f"**{t('key', lang)}**")
        key = st.text_input("", value=config.api_key, type="password", label_visibility="collapsed")
        
        st.markdown(f"**{t('model', lang)}**")
        model = st.text_input("", value=config.model, label_visibility="collapsed")
        
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

# 文本输入
text = st.text_area(
    t('input', lang),
    value=st.session_state.text,
    height=200,
    label_visibility="collapsed"
)
if text:
    st.session_state.text = text
    st.markdown(f'<div class="hint">{len(text)} {t("words", lang)}</div>', unsafe_allow_html=True)

# 错误点
st.markdown("---")
error = st.text_input(
    t('error', lang),
    placeholder=t('error_hint', lang),
    label_visibility="collapsed"
)

# 生成按钮
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

# 结果展示
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
    
    # 引导
    with tab3:
        ap = "output/answers.json"
        if os.path.exists(ap):
            with open(ap, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for level in ["basic", "intermediate", "advanced"]:
                if level in data:
                    for i, item in enumerate(data[level], 1):
                        if isinstance(item, dict):
                            with st.expander(f"Q{i}: {item.get('question', '')[:50]}..."):
                                g = item.get('guidance', {})
                                for step in ['step1', 'step2', 'step3']:
                                    if step in g:
                                        st.markdown(f"**{step.upper()}:** {g[step]}")
    
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
