# streamlit_app.py - Streamlit 前端界面
import streamlit as st
import json
from datetime import datetime
from workflow.openclaw_flow import OpenClawFlow
from utils.logger import get_logger
from utils.formatters import format_knowledge_output, format_questions_output

logger = get_logger(__name__)

def main():
    st.set_page_config(
        page_title="EduGuide 智能出题系统",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 EduGuide 智能出题系统")
    st.markdown("基于 OpenClaw + DeepSeek 的多 Agent 协作出题系统")
    
    # 初始化会话状态
    if 'workflow_result' not in st.session_state:
        st.session_state['workflow_result'] = None
    
    # 侧边栏
    with st.sidebar:
        st.header("⚙️ 配置")
        st.info("项目已初始化完成")
        
        if st.button("🔄 重置"):
            st.session_state.clear()
            st.rerun()
    
    # 主界面
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📖 输入教材文本")
        material_text = st.text_area(
            "教材内容",
            height=300,
            placeholder="请输入教材文本..."
        )
        
        st.subheader("❌ 错误知识点（可选）")
        wrong_point = st.text_input(
            "模拟学生错误",
            placeholder="例如：混淆了词干提取和词形还原"
        )
    
    with col2:
        st.subheader("📊 执行状态")
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
                        st.markdown(f"### {level.upper()}")
                        for i, q in enumerate(questions[level], 1):
                            st.markdown(f"{i}. {q}")
            else:
                st.info("暂无数据")
        
        with tab3:
            st.subheader("答案与解析")
            answers_path = "output/answers.json"
            if os.path.exists(answers_path):
                with open(answers_path, 'r', encoding='utf-8') as f:
                    answers = json.load(f)
                st.json(answers)
            else:
                st.info("暂无数据")
        
        with tab4:
            st.subheader("补救练习")
            remedial_path = "output/remedial.json"
            if os.path.exists(remedial_path):
                with open(remedial_path, 'r', encoding='utf-8') as f:
                    remedial = json.load(f)
                st.json(remedial)
            else:
                st.info("暂无补救题（未指定错误知识点）")


if __name__ == "__main__":
    import os
    main()
