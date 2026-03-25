# streamlit_app.py - 美观完整版
import streamlit as st
import json
import os

# ========== 多语言配置 ==========
LANGUAGES = {"en": "🇺🇸 EN", "zh-CN": "🇨🇳 中文", "zh-TW": "🇹🇼 繁體"}

T = {
    "en": {
        "title": "EduGuide", "subtitle": "Intelligent Question Generation",
        "upload": "Upload Material", "upload_hint": "Drag & drop or click",
        "input": "Or paste text...", "words": "words",
        "error": "Student error (optional)", "error_hint": "e.g., confused X with Y",
        "generate": "Generate", "generating": "Generating...", "done": "Done!",
        "knowledge": "Knowledge", "questions": "Questions", "remedial": "Remedial",
        "basic": "Basic", "intermediate": "Intermediate", "advanced": "Advanced",
        "api": "API Settings", "provider": "Provider", "key": "API Key", "model": "Model",
        "save": "Save", "saved": "Saved!", "language": "Language",
        "start": "🎯 Start", "step": "Step", "answer": "Your Answer",
        "submit": "Submit", "hint": "Hint", "correct": "Correct!", "retry": "Try again",
        "complete": "Complete", "progress": "Progress", "back": "Back",
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
        "start": "🎯 开始解题", "step": "步骤", "answer": "你的答案",
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
        "start": "🎯 開始解題", "step": "步驟", "answer": "你的答案",
        "submit": "提交", "hint": "提示", "correct": "正確！", "retry": "再試一次",
        "complete": "完成", "progress": "進度", "back": "返回",
        "current_api": "當前 API",
    }
}

def t(key, lang="en"):
    return T.get(lang, T["en"]).get(key, key)

# ========== 页面配置 ==========
st.set_page_config(page_title="EduGuide", page_icon="🎓", layout="wide", initial_sidebar_state="auto")

# ========== CSS ==========
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden}
.main .block-container {padding: 2rem 3rem; max-width: 1200px}
.hero {text-align: center; padding: 3rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 24px; margin-bottom: 2rem; color: white}
.hero-title {font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem}
.hero-subtitle {font-size: 1.1rem; opacity: 0.9}
.card {background: white; border-radius: 16px; padding: 1.5rem; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin-bottom: 1rem}
.upload-area {border: 2px dashed #d0d0d0; border-radius: 12px; padding: 2.5rem; text-align: center; background: #fafafa; margin-bottom: 1rem}
.stButton button {border-radius: 12px; height: 48px; font-weight: 600; background: #667eea; color: white; border: none}
.stButton button:hover {background: #5a6fd6}
.question-card {background: #f8f9fa; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; border-left: 4px solid #667eea}
.step-card {background: #f8f9fa; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border-left: 4px solid #667eea}
.step-active {background: #e3f2fd; border-left-color: #2196f3}
.step-complete {background: #e8f5e9; border-left-color: #4caf50}
.api-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; padding: 1.5rem; color: white}
.stTabs [data-baseweb="tab"] {border-radius: 8px; padding: 10px 20px; font-weight: 500}
.stTabs [aria-selected="true"] {background: white; color: #667eea; box-shadow: 0 2px 8px rgba(0,0,0,0.08)}
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
c1, c2, c3 = st.columns([2, 1, 1])
with c1: st.markdown("### 🎓 EduGuide")
with c2:
    new_lang = st.selectbox("", list(LANGUAGES.keys()), format_func=lambda x: LANGUAGES[x],
                           index=list(LANGUAGES.keys()).index(lang), label_visibility="collapsed")
    if new_lang != lang:
        st.session_state.lang = new_lang
        st.rerun()
with c3:
    if st.button(f"⚙️ {t('api', lang)}", use_container_width=True):
        st.session_state.show_api = not st.session_state.show_api

# ========== API设置 ==========
if st.session_state.show_api:
    st.markdown("---")
    st.markdown(f"### ⚙️ {t('api', lang)}")
    try:
        from config.api_config import get_config_manager, APIProvider, ProviderConfig
        cm = get_config_manager()
        current = cm.current_provider
        providers = cm.get_all_providers()
        options = {p['id']: p['name'] for p in providers}
        
        c1, c2 = st.columns(2)
        with c1:
            selected = st.selectbox("", list(options.keys()), format_func=lambda x: options[x],
                                   index=list(options.keys()).index(current.value), label_visibility="collapsed")
            config = cm.providers.get(APIProvider(selected))
            key = st.text_input(t('key', lang), value=config.api_key, type="password")
        with c2:
            model = st.text_input(t('model', lang), value=config.model)
            if st.button(t('save', lang), type="primary", use_container_width=True):
                new_cfg = ProviderConfig(name=config.name, api_key=key, base_url=config.base_url, model=model, enabled=True)
                cm.update_provider_config(APIProvider(selected), new_cfg)
                cm.set_current_provider(APIProvider(selected))
                st.success(t('saved', lang))
    except Exception as e:
        st.error(f"Error: {e}")
    st.markdown("---")

# ========== 标题 ==========
st.markdown(f"""
<div class="hero">
    <div class="hero-title">🎓 {t('title', lang)}</div>
    <div class="hero-subtitle">{t('subtitle', lang)}</div>
</div>
""", unsafe_allow_html=True)

# ========== 主内容 ==========
c1, c2 = st.columns([3, 2])

with c1:
    st.markdown(f"""
    <div class="card">
        <div class="upload-area">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📁</div>
            <div>{t('upload_hint', lang)}</div>
        </div>
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
    
    text = st.text_area(t('input', lang), value=st.session_state.text, height=200, label_visibility="collapsed")
    if text:
        st.session_state.text = text
        st.markdown(f"<small>{len(text)} {t('words', lang)}</small>", unsafe_allow_html=True)
    
    st.markdown("---")
    error = st.text_input(t('error', lang), placeholder=t('error_hint', lang), label_visibility="collapsed")
    
    if st.button(t('generate', lang), type="primary"):
        if not text:
            st.warning("Please input" if lang == "en" else "请输入内容")
        else:
            with st.spinner(t('generating', lang)):
                try:
                    from workflow.openclaw_flow import OpenClawFlow
                    st.session_state.result = OpenClawFlow().run(text, error if error else None)
                    st.success(t('done', lang))
                except Exception as e:
                    st.error(f"Error: {e}")

with c2:
    try:
        from config.api_config import get_config_manager
        cfg = get_config_manager().get_current_config()
        st.markdown(f"""
        <div class="api-card">
            <strong>🔌 {t('current_api', lang)}</strong><br>
            {cfg.name}<br>
            <small>{cfg.model}</small>
        </div>
        """, unsafe_allow_html=True)
    except: pass

# ========== 结果 ==========
if st.session_state.result:
    st.markdown("---")
    
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
        st.progress(st.session_state.step / len(steps) if steps else 0)
        st.markdown(f"**{t('progress', lang)}: {st.session_state.step}/{len(steps)}**")
        
        for i in range(st.session_state.step):
            st.markdown(f"<div class='step-card step-complete'><strong>✅ {t('step', lang)} {i+1}:</strong> {steps[i]}<br><small>答案: {st.session_state.answers.get(f'{qid}_{i}', '')}</small></div>", unsafe_allow_html=True)
        
        if st.session_state.step < len(steps):
            st.markdown(f"<div class='step-card step-active'><strong>{t('step', lang)} {st.session_state.step+1}:</strong> {steps[st.session_state.step]}</div>", unsafe_allow_html=True)
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
                        st.warning(t('retry', lang))
            with c2:
                if st.button(f"💡 {t('hint', lang)}", use_container_width=True):
                    hints = guidance.get('hints', [])
                    st.info(hints[st.session_state.step] if st.session_state.step < len(hints) else "Think about key concepts.")
        else:
            st.success(f"🎉 {t('complete', lang)}!")
            if st.button(f"✅ {t('complete', lang)}"):
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
