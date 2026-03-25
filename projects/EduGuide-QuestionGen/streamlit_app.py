# streamlit_app.py - Streamlit 前端界面（支持多 API 提供商）
import streamlit as st
import json
import os
from datetime import datetime
from workflow.openclaw_flow import OpenClawFlow
from utils.logger import get_logger
from utils.formatters import format_knowledge_output, format_questions_output
from config.api_config import APIProvider, get_config_manager, ProviderConfig
from services.unified_client import create_client

logger = get_logger(__name__)

def read_uploaded_file(uploaded_file):
    """读取上传的文件内容"""
    try:
        if uploaded_file.name.endswith('.txt'):
            content = uploaded_file.read().decode('utf-8')
            return content
        
        elif uploaded_file.name.endswith('.pdf'):
            try:
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
            except ImportError:
                st.error("❌ PDF 支持未安装，请运行: pip install PyPDF2")
                return None
        
        elif uploaded_file.name.endswith('.docx'):
            try:
                import docx
                doc = docx.Document(uploaded_file)
                text = "\n".join([para.text for para in doc.paragraphs])
                return text
            except ImportError:
                st.error("❌ Word 支持未安装，请运行: pip install python-docx")
                return None
        
        elif uploaded_file.name.endswith('.pptx'):
            try:
                from pptx import Presentation
                prs = Presentation(uploaded_file)
                text = ""
                for slide_num, slide in enumerate(prs.slides, 1):
                    text += f"\n=== 幻灯片 {slide_num} ===\n"
                    for shape in slide.shapes:
                        if hasattr(shape, "text") and shape.text.strip():
                            text += shape.text + "\n"
                return text
            except ImportError:
                st.error("❌ PowerPoint 支持未安装，请运行: pip install python-pptx")
                return None
        
        else:
            st.error(f"❌ 不支持的文件格式: {uploaded_file.name}")
            return None
    
    except Exception as e:
        st.error(f"❌ 读取文件失败: {e}")
        return None

def show_settings_page():
    """显示设置页面"""
    st.title("⚙️ API 设置")
    st.markdown("配置和管理 API 提供商")
    
    config_manager = get_config_manager()
    
    # 获取所有提供商
    providers = config_manager.get_all_providers()
    
    # 当前提供商
    current_provider = config_manager.current_provider
    
    # 提供商选择
    st.subheader("📡 选择 API 提供商")
    
    provider_options = {
        p['id']: f"{p['name']} {'✅' if p['configured'] else '⚠️ 未配置'}" 
        for p in providers
    }
    
    selected_provider = st.selectbox(
        "选择要使用的 API 提供商",
        options=list(provider_options.keys()),
        index=list(provider_options.keys()).index(current_provider.value),
        format_func=lambda x: provider_options[x]
    )
    
    # 显示当前提供商信息
    selected_enum = APIProvider(selected_provider)
    config = config_manager.providers.get(selected_enum)
    
    st.markdown("---")
    
    # 配置表单
    st.subheader(f"🔑 配置 {config.name}")
    
    with st.form("api_config_form"):
        # API Key
        api_key = st.text_input(
            "API Key",
            value=config.api_key,
            type="password",
            help=f"输入 {config.name} 的 API Key"
        )
        
        # Base URL
        if selected_enum == APIProvider.CUSTOM:
            base_url = st.text_input(
                "API Base URL",
                value=config.base_url,
                help="自定义 API 的 Base URL"
            )
        else:
            base_url = st.text_input(
                "API Base URL",
                value=config.base_url,
                disabled=True,
                help=f"{config.name} 的默认 API URL"
            )
        
        # 模型选择
        available_models = {
            APIProvider.ZHIPU: ["glm-4-flash", "glm-4", "glm-4-plus", "glm-4-air"],
            APIProvider.DEEPSEEK: ["deepseek-chat", "deepseek-coder"],
            APIProvider.OPENAI: ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o"],
            APIProvider.CLAUDE: ["claude-3-haiku-20240307", "claude-3-sonnet-20240229", "claude-3-opus-20240229"],
            APIProvider.QWEN: ["qwen-turbo", "qwen-plus", "qwen-max"],
            APIProvider.OLLAMA: ["llama2", "llama3", "mistral", "codellama", "qwen2"],
            APIProvider.CUSTOM: [config.model]
        }
        
        models = available_models.get(selected_enum, [config.model])
        
        selected_model = st.selectbox(
            "选择模型",
            options=models,
            index=models.index(config.model) if config.model in models else 0
        )
        
        # 自定义模型输入
        if selected_enum == APIProvider.CUSTOM:
            custom_model = st.text_input(
                "自定义模型名称",
                value=config.model,
                help="输入自定义模型的名称"
            )
            selected_model = custom_model
        
        # 提交按钮
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            submitted = st.form_submit_button("💾 保存配置", type="primary")
        
        with col2:
            test_clicked = st.form_submit_button("🧪 测试连接")
    
    # 处理表单提交
    if submitted:
        # 更新配置
        new_config = ProviderConfig(
            name=config.name,
            api_key=api_key,
            base_url=base_url,
            model=selected_model,
            enabled=True
        )
        
        config_manager.update_provider_config(selected_enum, new_config)
        config_manager.set_current_provider(selected_enum)
        
        st.success(f"✅ {config.name} 配置已保存！")
        st.rerun()
    
    if test_clicked:
        if not api_key:
            st.error("❌ 请先输入 API Key")
        else:
            with st.spinner("正在测试连接..."):
                try:
                    # 临时创建配置进行测试
                    test_config = ProviderConfig(
                        name=config.name,
                        api_key=api_key,
                        base_url=base_url,
                        model=selected_model,
                        enabled=True
                    )
                    
                    from services.unified_client import UnifiedAPIClient
                    client = UnifiedAPIClient(test_config)
                    
                    # 发送测试请求
                    result = client.call(
                        system_prompt="你是一个助手",
                        user_prompt="请回复'测试成功'"
                    )
                    
                    st.success(f"✅ 连接成功！模型响应正常")
                    st.json(result)
                    
                except Exception as e:
                    st.error(f"❌ 连接失败: {e}")
    
    # 显示所有提供商状态
    st.markdown("---")
    st.subheader("📊 所有提供商状态")
    
    for provider_data in providers:
        with st.expander(f"{provider_data['name']} {'✅' if provider_data['configured'] else '⚠️'}"):
            st.write(f"**已配置**: {'是' if provider_data['configured'] else '否'}")
            st.write(f"**可用模型**: {', '.join(provider_data['models'])}")

def main():
    st.set_page_config(
        page_title="EduGuide 智能出题系统",
        page_icon="📚",
        layout="wide"
    )
    
    # 侧边栏导航
    with st.sidebar:
        st.title("📚 EduGuide")
        st.markdown("智能出题系统")
        
        page = st.radio(
            "导航",
            ["🏠 主页", "⚙️ API 设置"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # 显示当前 API 提供商
        try:
            config_manager = get_config_manager()
            current_config = config_manager.get_current_config()
            st.info(f"**当前 API**: {current_config.name}")
            if current_config.api_key:
                st.success("✅ 已配置")
            else:
                st.warning("⚠️ 未配置 API Key")
        except:
            st.warning("⚠️ 请先配置 API")
    
    # 根据选择显示页面
    if page == "⚙️ API 设置":
        show_settings_page()
        return
    
    # 主页内容
    st.title("📚 EduGuide 智能出题系统")
    st.markdown("基于 **OpenClaw + 多 API 支持** 的智能出题系统")
    
    # 检查 API 配置
    config_manager = get_config_manager()
    current_config = config_manager.get_current_config()
    
    if not current_config.api_key:
        st.warning("⚠️ 当前 API 未配置，请先前往 **API 设置** 页面配置")
        return
    
    # 初始化会话状态
    if 'workflow_result' not in st.session_state:
        st.session_state['workflow_result'] = None
    
    if 'material_text' not in st.session_state:
        st.session_state['material_text'] = ""
    
    # 主界面
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📖 输入教材文本")
        
        # 文件上传区域
        st.markdown("**方式1: 上传文件**")
        uploaded_file = st.file_uploader(
            "上传教材文件",
            type=['txt', 'pdf', 'docx', 'pptx'],
            help="支持格式: .txt, .pdf, .docx, .pptx"
        )
        
        if uploaded_file is not None:
            file_content = read_uploaded_file(uploaded_file)
            if file_content:
                st.session_state['material_text'] = file_content
                st.success(f"✅ 已读取文件: {uploaded_file.name}")
        
        # 文本输入区域
        st.markdown("**方式2: 直接输入文本**")
        material_text = st.text_area(
            "教材内容",
            height=300,
            value=st.session_state.get('material_text', ''),
            placeholder="请输入教材文本，或上传文件自动填充..."
        )
        
        # 更新会话状态
        if material_text:
            st.session_state['material_text'] = material_text
        
        st.subheader("❌ 错误知识点（可选）")
        wrong_point = st.text_input(
            "模拟学生错误",
            placeholder="例如：混淆了词干提取和词形还原"
        )
    
    with col2:
        st.subheader("📊 执行状态")
        
        # 显示字符数统计
        if material_text:
            st.metric("教材字数", len(material_text))
        
        if st.button("🚀 开始生成", type="primary"):
            if not material_text:
                st.error("请输入教材文本！")
            else:
                with st.spinner("正在执行工作流..."):
                    try:
                        flow = OpenClawFlow()
                        result = flow.run(
                            material_text=material_text,
                            wrong_point=wrong_point if wrong_point else None
                        )
                        st.session_state['workflow_result'] = result
                        st.success("✅ 工作流执行完成！")
                    except Exception as e:
                        st.error(f"❌ 执行失败: {e}")
                        logger.error(f"工作流执行失败: {e}")
    
    # 显示结果
    if st.session_state['workflow_result']:
        st.markdown("---")
        st.header("📋 执行结果")
        
        result = st.session_state['workflow_result']
        
        # 创建标签页
        tab1, tab2, tab3, tab4 = st.tabs(["知识点", "题目", "答案", "补救题"])
        
        with tab1:
            st.subheader("提取的知识点")
            knowledge_path = "output/knowledge.json"
            if os.path.exists(knowledge_path):
                with open(knowledge_path, 'r', encoding='utf-8') as f:
                    knowledge = json.load(f)
                
                points = knowledge.get("knowledge_points", [])
                if points:
                    for i, point in enumerate(points, 1):
                        st.markdown(f"**{i}.** {point}")
                else:
                    st.json(knowledge)
            else:
                st.info("暂无数据")
        
        with tab2:
            st.subheader("分层题目")
            questions_path = "output/questions.json"
            if os.path.exists(questions_path):
                with open(questions_path, 'r', encoding='utf-8') as f:
                    questions = json.load(f)
                
                for level in ["basic", "intermediate", "advanced"]:
                    if level in questions:
                        level_names = {
                            "basic": "🟢 基础题",
                            "intermediate": "🟡 中级题",
                            "advanced": "🔴 高级题"
                        }
                        st.markdown(f"### {level_names.get(level, level.upper())}")
                        for i, q in enumerate(questions[level], 1):
                            st.markdown(f"**{i}.** {q}")
                        st.markdown("")
            else:
                st.info("暂无数据")
        
        with tab3:
            st.subheader("📚 苏格拉底式引导")
            st.info("💡 以下内容采用引导式教学，请跟随步骤自己思考，而不是直接看答案")
            answers_path = "output/answers.json"
            if os.path.exists(answers_path):
                with open(answers_path, 'r', encoding='utf-8') as f:
                    answers = json.load(f)
                
                for level in ["basic", "intermediate", "advanced"]:
                    if level in answers:
                        level_names = {
                            "basic": "🟢 基础题引导",
                            "intermediate": "🟡 中级题引导",
                            "advanced": "🔴 高级题引导"
                        }
                        st.markdown(f"### {level_names.get(level, level.upper())}")
                        
                        for idx, item in enumerate(answers[level], 1):
                            if isinstance(item, dict):
                                question = item.get('question', 'N/A')
                                guidance = item.get('guidance', {})
                                
                                with st.expander(f"**题目 {idx}:** {question}"):
                                    # 引导步骤
                                    st.markdown("#### 🎯 引导步骤")
                                    for step_key in ['step1', 'step2', 'step3']:
                                        if step_key in guidance:
                                            step_num = step_key[-1]
                                            st.markdown(f"**步骤 {step_num}:** {guidance[step_key]}")
                                    
                                    # 提示（可展开）
                                    if 'hints' in guidance:
                                        with st.expander("💡 需要提示吗？"):
                                            for i, hint in enumerate(guidance['hints'], 1):
                                                st.markdown(f"**提示 {i}:** {hint}")
                                    
                                    # 关键点
                                    if 'key_points' in guidance:
                                        st.markdown("#### 🔑 关键点")
                                        for point in guidance['key_points']:
                                            st.markdown(f"- {point}")
                                    
                                    # 常见错误
                                    if 'common_mistakes' in guidance:
                                        with st.expander("⚠️ 注意这些常见错误"):
                                            for mistake in guidance['common_mistakes']:
                                                st.markdown(f"- {mistake}")
                        st.markdown("")
            else:
                st.info("暂无数据")
        
        with tab4:
            st.subheader("🤝 补救引导")
            st.info("💡 当你理解有偏差时，这里会提供苏格拉底式的引导帮助你自己发现问题")
            remedial_path = "output/remedial.json"
            if os.path.exists(remedial_path):
                with open(remedial_path, 'r', encoding='utf-8') as f:
                    remedial = json.load(f)
                
                remedial_items = remedial.get("remedial", [])
                if remedial_items:
                    for i, item in enumerate(remedial_items, 1):
                        with st.expander(f"补救引导 {i}"):
                            st.markdown(f"**原题:** {item.get('original_question', 'N/A')}")
                            
                            guidance = item.get('guidance', {})
                            practice = item.get('practice', {})
                            follow_up = item.get('follow_up', {})
                            
                            # 肯定努力
                            if 'acknowledge' in guidance:
                                st.success(f"💬 {guidance['acknowledge']}")
                            
                            # 探询问题
                            st.markdown("#### 🤔 让我们一起思考")
                            for q_key in ['probing_question_1', 'probing_question_2', 'probing_question_3']:
                                if q_key in guidance:
                                    st.markdown(f"**{guidance[q_key]}**")
                                    st.markdown("*请先自己思考，再继续*")
                            
                            # 类比
                            if 'analogy' in guidance:
                                with st.expander("🎭 需要一个类比吗？"):
                                    st.markdown(f"**类比:** {guidance['analogy']}")
                            
                            # 鼓励
                            if 'encouragement' in guidance:
                                st.info(f"💪 {guidance['encouragement']}")
                            
                            # 练习
                            if practice:
                                st.markdown("#### 📝 试试这个简化练习")
                                st.markdown(f"**题目:** {practice.get('simplified_question', 'N/A')}")
                                if 'guided_steps' in practice:
                                    with st.expander("💡 需要引导步骤吗？"):
                                        for step in practice['guided_steps']:
                                            st.markdown(f"- {step}")
                            
                            # 跟进
                            if follow_up:
                                with st.expander("✅ 验证你的理解"):
                                    st.markdown(f"**验证问题:** {follow_up.get('verification_question', 'N/A')}")
                                    if 'extension_hint' in follow_up:
                                        st.markdown(f"**延伸思考:** {follow_up['extension_hint']}")
                else:
                    st.info("暂无补救题（未指定错误知识点）")
            else:
                st.info("暂无补救题（未指定错误知识点）")


if __name__ == "__main__":
    main()
