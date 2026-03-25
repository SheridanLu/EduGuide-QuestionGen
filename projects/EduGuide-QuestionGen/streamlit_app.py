# streamlit_app.py - Streamlit 前端界面（支持文件上传）
import streamlit as st
import json
import os
from datetime import datetime
from workflow.openclaw_flow import OpenClawFlow
from utils.logger import get_logger
from utils.formatters import format_knowledge_output, format_questions_output

logger = get_logger(__name__)

def read_uploaded_file(uploaded_file):
    """读取上传的文件内容"""
    try:
        if uploaded_file.name.endswith('.txt'):
            # 读取 txt 文件
            content = uploaded_file.read().decode('utf-8')
            return content
        
        elif uploaded_file.name.endswith('.pdf'):
            # 读取 PDF 文件（需要 PyPDF2）
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
            # 读取 Word 文件（需要 python-docx）
            try:
                import docx
                doc = docx.Document(uploaded_file)
                text = "\n".join([para.text for para in doc.paragraphs])
                return text
            except ImportError:
                st.error("❌ Word 支持未安装，请运行: pip install python-docx")
                return None
        
        else:
            st.error(f"❌ 不支持的文件格式: {uploaded_file.name}")
            return None
    
    except Exception as e:
        st.error(f"❌ 读取文件失败: {e}")
        return None

def main():
    st.set_page_config(
        page_title="EduGuide 智能出题系统",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 EduGuide 智能出题系统")
    st.markdown("基于 **OpenClaw + 智谱 GLM** 的多 Agent 协作出题系统")
    
    # 初始化会话状态
    if 'workflow_result' not in st.session_state:
        st.session_state['workflow_result'] = None
    
    if 'material_text' not in st.session_state:
        st.session_state['material_text'] = ""
    
    # 侧边栏
    with st.sidebar:
        st.header("⚙️ 配置")
        st.info("✅ 智谱 GLM API 已配置")
        
        if st.button("🔄 重置"):
            st.session_state.clear()
            st.rerun()
    
    # 主界面
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📖 输入教材文本")
        
        # 文件上传区域
        st.markdown("**方式1: 上传文件**")
        uploaded_file = st.file_uploader(
            "上传教材文件",
            type=['txt', 'pdf', 'docx'],
            help="支持格式: .txt, .pdf, .docx"
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
                
                # 美化显示
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
                        st.markdown("")  # 空行
            else:
                st.info("暂无数据")
        
        with tab3:
            st.subheader("答案与解析")
            answers_path = "output/answers.json"
            if os.path.exists(answers_path):
                with open(answers_path, 'r', encoding='utf-8') as f:
                    answers = json.load(f)
                
                # 美化显示
                for level in ["basic", "intermediate", "advanced"]:
                    if level in answers:
                        level_names = {
                            "basic": "🟢 基础题答案",
                            "intermediate": "🟡 中级题答案",
                            "advanced": "🔴 高级题答案"
                        }
                        st.markdown(f"### {level_names.get(level, level.upper())}")
                        
                        for item in answers[level]:
                            if isinstance(item, dict):
                                with st.expander(f"**Q:** {item.get('question', 'N/A')}"):
                                    st.markdown(f"**答案:** {item.get('answer', 'N/A')}")
                                    st.markdown(f"**解析:** {item.get('explanation', 'N/A')}")
                        st.markdown("")
            else:
                st.info("暂无数据")
        
        with tab4:
            st.subheader("补救练习")
            remedial_path = "output/remedial.json"
            if os.path.exists(remedial_path):
                with open(remedial_path, 'r', encoding='utf-8') as f:
                    remedial = json.load(f)
                
                remedial_items = remedial.get("remedial", [])
                if remedial_items:
                    for i, item in enumerate(remedial_items, 1):
                        with st.expander(f"补救题 {i}"):
                            st.markdown(f"**原题:** {item.get('original_question', 'N/A')}")
                            st.markdown(f"**错误点:** {item.get('wrong_point', 'N/A')}")
                            st.markdown(f"**补救题:** {item.get('remedial_question', 'N/A')}")
                            st.markdown(f"**解析:** {item.get('explanation', 'N/A')}")
                else:
                    st.json(remedial)
            else:
                st.info("暂无补救题（未指定错误知识点）")


if __name__ == "__main__":
    main()
