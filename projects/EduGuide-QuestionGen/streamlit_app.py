# streamlit_app.py - 美化版前端界面
import streamlit as st
import json
import os
from datetime import datetime
from workflow.openclaw_flow import OpenClawFlow
from utils.logger import get_logger
from config.api_config import APIProvider, get_config_manager, ProviderConfig

logger = get_logger(__name__)

# 页面配置
st.set_page_config(
    page_title="EduGuide - 智能出题系统",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS 样式
def load_custom_css():
    st.markdown("""
    <style>
    /* 全局样式 */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 隐藏 Streamlit 默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 卡片样式 */
    .card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    /* 标题样式 */
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
    
    /* 按钮样式 */
    .stButton > button {
        width: 100%;
        border-radius: 50px;
        height: 50px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* 上传区域样式 */
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        background: #f8f9ff;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: #764ba2;
        background: #f0f2ff;
    }
    
    /* 文本区域样式 */
    .stTextArea > textarea {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        padding: 15px;
        font-size: 1rem;
    }
    
    .stTextArea > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* 指标卡片 */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #667eea;
    }
    
    .metric-label {
        color: #999;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
    }
    
    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 15px 30px;
        font-weight: 600;
        background: #f0f0f0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* 成功/错误消息 */
    .success-message {
        background: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .error-message {
        background: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    /* 信息卡片 */
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    
    /* 加载动画 */
    .loading {
        text-align: center;
        padding: 40px;
    }
    
    /* 题目卡片 */
    .question-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border-left: 5px solid #667eea;
    }
    
    /* 答案卡片 */
    .answer-card {
        background: #f8f9ff;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }
    
    /* 进度条 */
    .progress-bar {
        height: 8px;
        background: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transition: width 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

def show_home_page():
    """主页"""
    # 标题
    st.markdown('<h1 class="main-title">🎓 EduGuide</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">智能出题系统 · 苏格拉底式引导教学</p>', unsafe_allow_html=True)
    
    # 检查 API 配置
    config_manager = get_config_manager()
    current_config = config_manager.get_current_config()
    
    if not current_config.api_key:
        st.warning("⚠️ 请先配置 API Key")
        st.markdown("**步骤：** 左侧导航 → ⚙️ API 设置")
        return
    
    # 主内容区
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.markdown("### 📖 输入教材内容")
        
        # 文件上传
        st.markdown("""
        <div class="upload-area">
            <h4>📁 上传教材文件</h4>
            <p>支持 .txt, .pdf, .docx, .pptx</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "",
            type=['txt', 'pdf', 'docx', 'pptx'],
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            file_content = read_uploaded_file(uploaded_file)
            if file_content:
                st.success(f"✅ 已读取: {uploaded_file.name}")
                st.session_state['material_text'] = file_content
        
        # 文本输入
        st.markdown("**或直接输入文本：**")
        material_text = st.text_area(
            "",
            height=250,
            value=st.session_state.get('material_text', ''),
            placeholder="在此粘贴或输入教材内容...",
            label_visibility="collapsed"
        )
        
        if material_text:
            st.session_state['material_text'] = material_text
    
    with col_right:
        st.markdown("### ⚙️ 设置")
        
        # 字数统计
        if material_text:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(material_text)}</div>
                <div class="metric-label">字数</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 错误知识点
        st.markdown("**模拟学生错误（可选）**")
        wrong_point = st.text_input(
            "",
            placeholder="例如：混淆了词干提取和词形还原",
            label_visibility="collapsed"
        )
        
        # 当前 API
        st.markdown(f"""
        <div class="info-card">
            <strong>当前 API</strong><br>
            {current_config.name}<br>
            <small>{current_config.model}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # 生成按钮
        st.markdown("---")
        generate = st.button("🚀 开始生成", type="primary")
    
    # 执行生成
    if generate:
        if not material_text:
            st.error("❌ 请输入教材内容")
        else:
            with st.spinner("正在生成中，请稍候..."):
                try:
                    flow = OpenClawFlow()
                    result = flow.run(
                        material_text=material_text,
                        wrong_point=wrong_point if wrong_point else None
                    )
                    st.session_state['workflow_result'] = result
                    st.success("✅ 生成完成！")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ 生成失败: {e}")
    
    # 显示结果
    if st.session_state.get('workflow_result'):
        show_results()

def show_results():
    """显示生成结果"""
    st.markdown("---")
    st.markdown('<h2 class="main-title">📋 生成结果</h2>', unsafe_allow_html=True)
    
    # 标签页
    tab1, tab2, tab3, tab4 = st.tabs([
        "💡 知识点",
        "📝 题目",
        "🎯 引导",
        "🤝 补救"
    ])
    
    with tab1:
        show_knowledge()
    
    with tab2:
        show_questions()
    
    with tab3:
        show_guidance()
    
    with tab4:
        show_remedial()

def show_knowledge():
    """显示知识点"""
    knowledge_path = "output/knowledge.json"
    if os.path.exists(knowledge_path):
        with open(knowledge_path, 'r', encoding='utf-8') as f:
            knowledge = json.load(f)
        
        points = knowledge.get("knowledge_points", [])
        if points:
            st.markdown(f"**提取了 {len(points)} 个知识点**")
            
            for i, point in enumerate(points, 1):
                st.markdown(f"""
                <div class="question-card">
                    <strong>{i}.</strong> {point}
                </div>
                """, unsafe_allow_html=True)

def show_questions():
    """显示题目"""
    questions_path = "output/questions.json"
    if os.path.exists(questions_path):
        with open(questions_path, 'r', encoding='utf-8') as f:
            questions = json.load(f)
        
        levels = {
            "basic": ("🟢 基础题", "#28a745"),
            "intermediate": ("🟡 中级题", "#ffc107"),
            "advanced": ("🔴 高级题", "#dc3545")
        }
        
        for level, (title, color) in levels.items():
            if level in questions:
                st.markdown(f"### {title}")
                
                for i, q in enumerate(questions[level], 1):
                    st.markdown(f"""
                    <div class="question-card" style="border-left-color: {color};">
                        <strong>Q{i}:</strong> {q}
                    </div>
                    """, unsafe_allow_html=True)

def show_guidance():
    """显示引导"""
    answers_path = "output/answers.json"
    if os.path.exists(answers_path):
        with open(answers_path, 'r', encoding='utf-8') as f:
            answers = json.load(f)
        
        st.info("💡 点击题目展开引导步骤")
        
        for level in ["basic", "intermediate", "advanced"]:
            if level in answers:
                level_names = {
                    "basic": "🟢 基础题",
                    "intermediate": "🟡 中级题",
                    "advanced": "🔴 高级题"
                }
                
                st.markdown(f"### {level_names[level]}")
                
                for i, item in enumerate(answers[level], 1):
                    if isinstance(item, dict):
                        question = item.get('question', 'N/A')
                        guidance = item.get('guidance', {})
                        
                        with st.expander(f"**题目 {i}:** {question[:50]}..."):
                            # 引导步骤
                            for step_key in ['step1', 'step2', 'step3']:
                                if step_key in guidance:
                                    st.markdown(f"**{step_key.upper()}:** {guidance[step_key]}")
                            
                            # 提示
                            if 'hints' in guidance:
                                with st.expander("💡 查看提示"):
                                    for hint in guidance['hints']:
                                        st.markdown(f"- {hint}")

def show_remedial():
    """显示补救"""
    remedial_path = "output/remedial.json"
    if os.path.exists(remedial_path):
        with open(remedial_path, 'r', encoding='utf-8') as f:
            remedial = json.load(f)
        
        items = remedial.get("remedial", [])
        if items:
            for i, item in enumerate(items, 1):
                with st.expander(f"补救引导 {i}"):
                    guidance = item.get('guidance', {})
                    
                    if 'acknowledge' in guidance:
                        st.success(guidance['acknowledge'])
                    
                    for q_key in ['probing_question_1', 'probing_question_2', 'probing_question_3']:
                        if q_key in guidance:
                            st.markdown(f"**{guidance[q_key]}**")
        else:
            st.info("暂无补救题（未指定错误知识点）")

def read_uploaded_file(uploaded_file):
    """读取上传的文件"""
    try:
        if uploaded_file.name.endswith('.txt'):
            return uploaded_file.read().decode('utf-8')
        
        elif uploaded_file.name.endswith('.pdf'):
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        
        elif uploaded_file.name.endswith('.docx'):
            import docx
            doc = docx.Document(uploaded_file)
            return "\n".join([para.text for para in doc.paragraphs])
        
        elif uploaded_file.name.endswith('.pptx'):
            from pptx import Presentation
            prs = Presentation(uploaded_file)
            text = ""
            for slide_num, slide in enumerate(prs.slides, 1):
                text += f"\n=== 幻灯片 {slide_num} ===\n"
                for shape in slide.shapes:
                    if hasattr(shape, "text") and shape.text.strip():
                        text += shape.text + "\n"
            return text
        
        else:
            st.error(f"❌ 不支持的文件格式: {uploaded_file.name}")
            return None
    
    except Exception as e:
        st.error(f"❌ 读取文件失败: {e}")
        return None

def show_settings_page():
    """设置页面"""
    st.markdown('<h1 class="main-title">⚙️ API 设置</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">配置和管理 API 提供商</p>', unsafe_allow_html=True)
    
    config_manager = get_config_manager()
    providers = config_manager.get_all_providers()
    current_provider = config_manager.current_provider
    
    # 提供商选择
    st.markdown("### 📡 选择 API 提供商")
    
    provider_options = {
        p['id']: f"{p['name']} {'✅' if p['configured'] else '⚠️'}" 
        for p in providers
    }
    
    selected_provider = st.selectbox(
        "选择要使用的 API 提供商",
        options=list(provider_options.keys()),
        index=list(provider_options.keys()).index(current_provider.value),
        format_func=lambda x: provider_options[x]
    )
    
    selected_enum = APIProvider(selected_provider)
    config = config_manager.providers.get(selected_enum)
    
    st.markdown("---")
    
    # 配置表单
    st.markdown(f"### 🔑 配置 {config.name}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        api_key = st.text_input(
            "API Key",
            value=config.api_key,
            type="password"
        )
    
    with col2:
        if selected_enum == APIProvider.CUSTOM:
            base_url = st.text_input("API Base URL", value=config.base_url)
        else:
            base_url = st.text_input("API Base URL", value=config.base_url, disabled=True)
    
    # 模型选择
    available_models = {
        APIProvider.ZHIPU: ["glm-4-plus", "glm-4-flash", "glm-4-air", "glm-4-long"],
        APIProvider.DEEPSEEK: ["deepseek-chat", "deepseek-reasoner"],
        APIProvider.OPENAI: ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        APIProvider.CLAUDE: ["claude-3-5-sonnet", "claude-3-opus"],
        APIProvider.QWEN: ["qwen-max", "qwen-plus", "qwen-turbo"],
        APIProvider.OLLAMA: ["llama3", "mistral", "qwen2"],
        APIProvider.CUSTOM: [config.model]
    }
    
    models = available_models.get(selected_enum, [config.model])
    
    selected_model = st.selectbox(
        "选择模型",
        options=models,
        index=models.index(config.model) if config.model in models else 0
    )
    
    # 按钮
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("💾 保存配置", type="primary"):
            new_config = ProviderConfig(
                name=config.name,
                api_key=api_key,
                base_url=base_url,
                model=selected_model,
                enabled=True
            )
            config_manager.update_provider_config(selected_enum, new_config)
            config_manager.set_current_provider(selected_enum)
            st.success("✅ 配置已保存！")
            st.rerun()
    
    with col2:
        if st.button("🧪 测试连接"):
            if not api_key:
                st.error("❌ 请先输入 API Key")
            else:
                with st.spinner("测试中..."):
                    try:
                        from services.unified_client import UnifiedAPIClient
                        test_config = ProviderConfig(
                            name=config.name,
                            api_key=api_key,
                            base_url=base_url,
                            model=selected_model,
                            enabled=True
                        )
                        client = UnifiedAPIClient(test_config)
                        result = client.call("你是一个助手", "回复'测试成功'")
                        st.success("✅ 连接成功！")
                    except Exception as e:
                        st.error(f"❌ 连接失败: {e}")

def main():
    load_custom_css()
    
    # 初始化会话状态
    if 'workflow_result' not in st.session_state:
        st.session_state['workflow_result'] = None
    if 'material_text' not in st.session_state:
        st.session_state['material_text'] = ""
    
    # 侧边栏
    with st.sidebar:
        st.markdown("# 🎓 EduGuide")
        st.markdown("---")
        
        page = st.radio(
            "导航",
            ["🏠 主页", "⚙️ API 设置"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # 显示当前 API
        try:
            config_manager = get_config_manager()
            current_config = config_manager.get_current_config()
            st.markdown(f"""
            **当前 API**  
            {current_config.name}  
            <small>{current_config.model}</small>
            """, unsafe_allow_html=True)
        except:
            pass
    
    # 根据选择显示页面
    if page == "⚙️ API 设置":
        show_settings_page()
    else:
        show_home_page()

if __name__ == "__main__":
    main()
