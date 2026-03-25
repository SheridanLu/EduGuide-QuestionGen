# streamlit_app.py - 带多语言支持的主应用
import streamlit as st
import json
import os
from datetime import datetime

# 多语言配置
LANGUAGES = {
    "en": "🇺🇸 English",
    "zh-CN": "🇨🇳 简体中文", 
    "zh-TW": "🇹🇼 繁體中文"
}

TRANSLATIONS = {
    "en": {
        "app_title": "🎓 EduGuide",
        "app_subtitle": "Smart Question Generation · Socratic Guidance",
        "nav_home": "🏠 Home",
        "nav_settings": "⚙️ Settings",
        "language": "🌐 Language",
        "input_material": "📖 Input Material",
        "upload_file": "📁 Upload File",
        "upload_hint": "Supports: .txt, .pdf, .docx, .pptx",
        "or_input": "Or input text:",
        "placeholder": "Paste or enter material here...",
        "word_count": "Words",
        "error_point": "Simulate Student Error (Optional)",
        "error_placeholder": "e.g., confused stemming with lemmatization",
        "current_api": "Current API",
        "generate": "🚀 Start Generation",
        "tab_knowledge": "💡 Knowledge",
        "tab_questions": "📝 Questions",
        "tab_guidance": "📚 Guidance",
        "tab_remedial": "🤝 Remedial",
        "extracted": "Extracted {} knowledge points",
        "basic": "🟢 Basic",
        "intermediate": "🟡 Intermediate",
        "advanced": "🔴 Advanced",
        "click_expand": "💡 Click to expand",
        "step": "Step",
        "hints": "💡 Hints",
        "key_points": "🔑 Key Points",
        "api_title": "⚙️ API Settings",
        "api_subtitle": "Configure API providers",
        "select_provider": "📡 Select Provider",
        "configure": "🔑 Configure {}",
        "api_key": "API Key",
        "base_url": "Base URL",
        "select_model": "Select Model",
        "save": "💾 Save",
        "test": "🧪 Test",
        "saved": "✅ Saved!",
        "success": "✅ Success!",
        "input_required": "❌ Please input material",
        "generating": "Generating...",
        "complete": "✅ Complete!",
        "configure_first": "⚠️ Configure API first",
        "file_read": "✅ Read: {}",
    },
    "zh-CN": {
        "app_title": "🎓 EduGuide",
        "app_subtitle": "智能出题系统 · 苏格拉底式引导",
        "nav_home": "🏠 主页",
        "nav_settings": "⚙️ 设置",
        "language": "🌐 语言",
        "input_material": "📖 输入教材内容",
        "upload_file": "📁 上传文件",
        "upload_hint": "支持: .txt, .pdf, .docx, .pptx",
        "or_input": "或输入文本:",
        "placeholder": "在此粘贴或输入教材内容...",
        "word_count": "字数",
        "error_point": "模拟学生错误（可选）",
        "error_placeholder": "例如：混淆了词干提取和词形还原",
        "current_api": "当前 API",
        "generate": "🚀 开始生成",
        "tab_knowledge": "💡 知识点",
        "tab_questions": "📝 题目",
        "tab_guidance": "📚 引导",
        "tab_remedial": "🤝 补救",
        "extracted": "提取了 {} 个知识点",
        "basic": "🟢 基础题",
        "intermediate": "🟡 中级题",
        "advanced": "🔴 高级题",
        "click_expand": "💡 点击展开",
        "step": "步骤",
        "hints": "💡 提示",
        "key_points": "🔑 关键点",
        "api_title": "⚙️ API 设置",
        "api_subtitle": "配置 API 提供商",
        "select_provider": "📡 选择提供商",
        "configure": "🔑 配置 {}",
        "api_key": "API Key",
        "base_url": "Base URL",
        "select_model": "选择模型",
        "save": "💾 保存",
        "test": "🧪 测试",
        "saved": "✅ 已保存！",
        "success": "✅ 成功！",
        "input_required": "❌ 请输入教材内容",
        "generating": "生成中...",
        "complete": "✅ 生成完成！",
        "configure_first": "⚠️ 请先配置 API",
        "file_read": "✅ 已读取: {}",
    },
    "zh-TW": {
        "app_title": "🎓 EduGuide",
        "app_subtitle": "智慧出題系統 · 蘇格拉底式引導",
        "nav_home": "🏠 首頁",
        "nav_settings": "⚙️ 設定",
        "language": "🌐 語言",
        "input_material": "📖 輸入教材內容",
        "upload_file": "📁 上傳檔案",
        "upload_hint": "支援: .txt, .pdf, .docx, .pptx",
        "or_input": "或輸入文字:",
        "placeholder": "在此貼上或輸入教材內容...",
        "word_count": "字數",
        "error_point": "模擬學生錯誤（可選）",
        "error_placeholder": "例如：混淆了詞幹提取和詞形還原",
        "current_api": "當前 API",
        "generate": "🚀 開始生成",
        "tab_knowledge": "💡 知識點",
        "tab_questions": "📝 題目",
        "tab_guidance": "📚 引導",
        "tab_remedial": "🤝 補救",
        "extracted": "提取了 {} 個知識點",
        "basic": "🟢 基礎題",
        "intermediate": "🟡 中級題",
        "advanced": "🔴 高級題",
        "click_expand": "💡 點擊展開",
        "step": "步驟",
        "hints": "💡 提示",
        "key_points": "🔑 關鍵點",
        "api_title": "⚙️ API 設定",
        "api_subtitle": "配置 API 提供商",
        "select_provider": "📡 選擇提供商",
        "configure": "🔑 配置 {}",
        "api_key": "API Key",
        "base_url": "Base URL",
        "select_model": "選擇模型",
        "save": "💾 儲存",
        "test": "🧪 測試",
        "saved": "✅ 已儲存！",
        "success": "✅ 成功！",
        "input_required": "❌ 請輸入教材內容",
        "generating": "生成中...",
        "complete": "✅ 生成完成！",
        "configure_first": "⚠️ 請先配置 API",
        "file_read": "✅ 已讀取: {}",
    }
}

def t(key, lang="en", *args):
    """翻译函数"""
    text = TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
    if args:
        return text.format(*args)
    return text

# 页面配置
st.set_page_config(
    page_title="EduGuide",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
.main { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
#MainMenu, footer, header {visibility: hidden;}
.card {
    background: white;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    margin: 20px 0;
}
.main-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 10px;
}
.subtitle {
    text-align: center;
    color: #666;
    font-size: 1.2rem;
    margin-bottom: 30px;
}
.stButton > button {
    width: 100%;
    border-radius: 50px;
    height: 50px;
    font-weight: 600;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    color: white;
}
.question-card {
    background: white;
    border-radius: 15px;
    padding: 25px;
    margin: 15px 0;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    border-left: 5px solid #667eea;
}
</style>
""", unsafe_allow_html=True)

# 初始化
if 'lang' not in st.session_state:
    st.session_state.lang = "en"
if 'material_text' not in st.session_state:
    st.session_state.material_text = ""
if 'workflow_result' not in st.session_state:
    st.session_state.workflow_result = None

lang = st.session_state.lang

# 侧边栏
with st.sidebar:
    st.markdown(f"# {t('app_title', lang)}")
    
    # 语言选择
    st.markdown(f"### {t('language', lang)}")
    selected_lang = st.selectbox(
        "",
        options=list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x],
        index=list(LANGUAGES.keys()).index(lang),
        label_visibility="collapsed"
    )
    if selected_lang != lang:
        st.session_state.lang = selected_lang
        st.rerun()
    
    st.markdown("---")
    
    # 导航
    page = st.radio(
        "",
        [t("nav_home", lang), t("nav_settings", lang)],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # 当前API
    try:
        from config.api_config import get_config_manager
        config_manager = get_config_manager()
        current_config = config_manager.get_current_config()
        st.markdown(f"**{t('current_api', lang)}**  \n{current_config.name}")
    except:
        pass

# 主页
if page == t("nav_home", lang):
    st.markdown(f'<h1 class="main-title">{t("app_title", lang)}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">{t("app_subtitle", lang)}</p>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.markdown(f"### {t('input_material', lang)}")
        
        # 文件上传
        st.markdown(f"**{t('upload_file', lang)}**  \n{t('upload_hint', lang)}")
        uploaded_file = st.file_uploader("", type=['txt', 'pdf', 'docx', 'pptx'], label_visibility="collapsed")
        
        if uploaded_file:
            # 读取文件逻辑
            try:
                if uploaded_file.name.endswith('.txt'):
                    content = uploaded_file.read().decode('utf-8')
                elif uploaded_file.name.endswith('.pdf'):
                    import PyPDF2
                    pdf = PyPDF2.PdfReader(uploaded_file)
                    content = "\n".join([p.extract_text() for p in pdf.pages])
                elif uploaded_file.name.endswith('.docx'):
                    import docx
                    doc = docx.Document(uploaded_file)
                    content = "\n".join([p.text for p in doc.paragraphs])
                elif uploaded_file.name.endswith('.pptx'):
                    from pptx import Presentation
                    prs = Presentation(uploaded_file)
                    content = ""
                    for i, slide in enumerate(prs.slides, 1):
                        content += f"\n=== {t('slide', lang)} {i} ===\n"
                        for shape in slide.shapes:
                            if hasattr(shape, "text"):
                                content += shape.text + "\n"
                st.session_state.material_text = content
                st.success(t("file_read", lang, uploaded_file.name))
            except Exception as e:
                st.error(f"Error: {e}")
        
        st.markdown(f"**{t('or_input', lang)}**")
        material_text = st.text_area(
            "",
            height=250,
            value=st.session_state.material_text,
            placeholder=t("placeholder", lang),
            label_visibility="collapsed"
        )
        if material_text:
            st.session_state.material_text = material_text
    
    with col_right:
        st.markdown(f"### {t('settings', lang)}")
        
        if material_text:
            st.metric(t("word_count", lang), len(material_text))
        
        st.markdown(f"**{t('error_point', lang)}**")
        wrong_point = st.text_input("", placeholder=t("error_placeholder", lang), label_visibility="collapsed")
        
        st.markdown("---")
        generate = st.button(t("generate", lang), type="primary")
    
    # 生成逻辑
    if generate:
        if not material_text:
            st.warning(t("input_required", lang))
        else:
            with st.spinner(t("generating", lang)):
                try:
                    from workflow.openclaw_flow import OpenClawFlow
                    flow = OpenClawFlow()
                    result = flow.run(material_text, wrong_point if wrong_point else None)
                    st.session_state.workflow_result = result
                    st.success(t("complete", lang))
                except Exception as e:
                    st.error(f"Error: {e}")

# 设置页
elif page == t("nav_settings", lang):
    st.markdown(f'<h1 class="main-title">{t("api_title", lang)}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">{t("api_subtitle", lang)}</p>', unsafe_allow_html=True)
    
    try:
        from config.api_config import get_config_manager, APIProvider, ProviderConfig
        
        config_manager = get_config_manager()
        providers = config_manager.get_all_providers()
        current = config_manager.current_provider
        
        st.markdown(f"### {t('select_provider', lang)}")
        provider_options = {p['id']: f"{p['name']} {'✅' if p['configured'] else '⚠️'}" for p in providers}
        
        selected = st.selectbox(
            "",
            options=list(provider_options.keys()),
            index=list(provider_options.keys()).index(current.value),
            format_func=lambda x: provider_options[x],
            label_visibility="collapsed"
        )
        
        selected_enum = APIProvider(selected)
        config = config_manager.providers.get(selected_enum)
        
        st.markdown(f"### {t('configure', lang, config.name)}")
        
        col1, col2 = st.columns(2)
        with col1:
            api_key = st.text_input(t('api_key', lang), value=config.api_key, type="password")
        with col2:
            base_url = st.text_input(t('base_url', lang), value=config.base_url, disabled=(selected_enum.value != "custom"))
        
        # 模型选择
        models_map = {
            APIProvider.ZHIPU: ["glm-4-plus", "glm-4-flash", "glm-4-air"],
            APIProvider.DEEPSEEK: ["deepseek-chat", "deepseek-reasoner"],
            APIProvider.OPENAI: ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        }
        models = models_map.get(selected_enum, [config.model])
        model = st.selectbox(t('select_model', lang), models)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(t('save', lang), type="primary"):
                new_config = ProviderConfig(
                    name=config.name,
                    api_key=api_key,
                    base_url=base_url,
                    model=model,
                    enabled=True
                )
                config_manager.update_provider_config(selected_enum, new_config)
                config_manager.set_current_provider(selected_enum)
                st.success(t('saved', lang))
        
        with col2:
            if st.button(t('test', lang)):
                if not api_key:
                    st.warning(t('enter_key', lang))
                else:
                    st.success(t('success', lang))
    
    except Exception as e:
        st.warning(t('configure_first', lang))
        st.code(f"Error: {e}")
