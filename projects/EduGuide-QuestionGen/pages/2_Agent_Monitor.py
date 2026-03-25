# pages/🔍_Agent_Monitor.py - Agent交互监控页面
import streamlit as st
import json
import os
import time
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="Agent Monitor - EduGuide",
    page_icon="🔍",
    layout="wide"
)

# 自定义CSS
st.markdown("""
<style>
.agent-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border-left: 4px solid #667eea;
}
.agent-active {
    border-left-color: #4caf50;
    animation: pulse 2s infinite;
}
.agent-complete {
    border-left-color: #4caf50;
}
.agent-waiting {
    border-left-color: #999;
}
.agent-error {
    border-left-color: #f44336;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}
.log-entry {
    padding: 0.5rem;
    margin: 0.25rem 0;
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.9rem;
}
.log-info { background: #e3f2fd; color: #1976d2; }
.log-success { background: #e8f5e9; color: #388e3c; }
.log-warning { background: #fff3e0; color: #f57c00; }
.log-error { background: #ffebee; color: #d32f2f; }
.timestamp {
    color: #999;
    font-size: 0.8rem;
    margin-right: 0.5rem;
}
.data-box {
    background: #f5f5f5;
    border-radius: 8px;
    padding: 1rem;
    font-family: monospace;
    font-size: 0.85rem;
    max-height: 300px;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)

# 标题
st.title("🔍 Agent Interaction Monitor")
st.markdown("**Real-time visualization of multi-agent collaboration**")
st.markdown("---")

# Agent配置
AGENTS = [
    {
        "id": "knowledge",
        "name": "📚 Knowledge Agent",
        "description": "Extracts key concepts from teaching materials",
        "input": "Raw text / Uploaded file",
        "output": "output/knowledge.json",
        "color": "#2196f3"
    },
    {
        "id": "question",
        "name": "📝 Question Agent",
        "description": "Generates tiered questions (Basic/Intermediate/Advanced)",
        "input": "output/knowledge.json",
        "output": "output/questions.json",
        "color": "#ff9800"
    },
    {
        "id": "answer",
        "name": "🎯 Answer Agent",
        "description": "Creates Socratic-style step-by-step guidance",
        "input": "output/questions.json",
        "output": "output/answers.json",
        "color": "#4caf50"
    },
    {
        "id": "remedial",
        "name": "🤝 Remedial Agent",
        "description": "Generates remedial questions for student errors",
        "input": "Student error + question context",
        "output": "output/remedial.json",
        "color": "#9c27b0"
    }
]

# 初始化session state
if 'logs' not in st.session_state:
    st.session_state.logs = []

if 'agent_status' not in st.session_state:
    st.session_state.agent_status = {agent['id']: 'waiting' for agent in AGENTS}

# 功能：读取文件内容
def read_json_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# 功能：添加日志
def add_log(agent_id, message, level='info'):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append({
        'timestamp': timestamp,
        'agent': agent_id,
        'message': message,
        'level': level
    })

# 功能：模拟Agent运行
def simulate_agent_run():
    # 清空日志
    st.session_state.logs = []
    st.session_state.agent_status = {agent['id']: 'waiting' for agent in AGENTS}
    
    # 检查文件是否存在
    has_knowledge = os.path.exists('output/knowledge.json')
    has_questions = os.path.exists('output/questions.json')
    has_answers = os.path.exists('output/answers.json')
    has_remedial = os.path.exists('output/remedial.json')
    
    # Agent 1: Knowledge
    st.session_state.agent_status['knowledge'] = 'active'
    add_log('knowledge', 'Started processing teaching material...', 'info')
    time.sleep(0.5)
    
    if has_knowledge:
        st.session_state.agent_status['knowledge'] = 'complete'
        data = read_json_file('output/knowledge.json')
        count = len(data.get('knowledge_points', []))
        add_log('knowledge', f'✅ Extracted {count} knowledge points', 'success')
    else:
        st.session_state.agent_status['knowledge'] = 'waiting'
        add_log('knowledge', '⏳ Waiting for input...', 'warning')
    
    # Agent 2: Question
    if st.session_state.agent_status['knowledge'] == 'complete':
        st.session_state.agent_status['question'] = 'active'
        add_log('question', 'Generating questions from knowledge points...', 'info')
        time.sleep(0.5)
        
        if has_questions:
            st.session_state.agent_status['question'] = 'complete'
            data = read_json_file('output/questions.json')
            total = sum(len(data.get(level, [])) for level in ['basic', 'intermediate', 'advanced'])
            add_log('question', f'✅ Generated {total} questions (3 levels)', 'success')
        else:
            st.session_state.agent_status['question'] = 'waiting'
    
    # Agent 3: Answer
    if st.session_state.agent_status['question'] == 'complete':
        st.session_state.agent_status['answer'] = 'active'
        add_log('answer', 'Creating Socratic guidance for each question...', 'info')
        time.sleep(0.5)
        
        if has_answers:
            st.session_state.agent_status['answer'] = 'complete'
            data = read_json_file('output/answers.json')
            total = sum(len(data.get(level, [])) for level in ['basic', 'intermediate', 'advanced'])
            add_log('answer', f'✅ Created guidance for {total} questions', 'success')
        else:
            st.session_state.agent_status['answer'] = 'waiting'
    
    # Agent 4: Remedial (conditional)
    if has_remedial:
        st.session_state.agent_status['remedial'] = 'active'
        add_log('remedial', 'Generating remedial questions...', 'info')
        time.sleep(0.5)
        
        data = read_json_file('output/remedial.json')
        count = len(data.get('remedial', []))
        st.session_state.agent_status['remedial'] = 'complete'
        add_log('remedial', f'✅ Generated {count} remedial guidance', 'success')
    else:
        add_log('remedial', '⏳ No student errors detected', 'info')

# 主界面
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Agent Status")
    
    # Agent卡片
    for agent in AGENTS:
        status = st.session_state.agent_status[agent['id']]
        status_emoji = {
            'waiting': '⏳',
            'active': '🔄',
            'complete': '✅',
            'error': '❌'
        }[status]
        
        status_class = f"agent-{status}"
        
        st.markdown(f"""
        <div class="agent-card {status_class}">
            <h3>{status_emoji} {agent['name']}</h3>
            <p>{agent['description']}</p>
            <div style="margin-top: 0.5rem;">
                <strong>Input:</strong> <code>{agent['input']}</code><br>
                <strong>Output:</strong> <code>{agent['output']}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 控制按钮
    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 Refresh Status", type="primary", use_container_width=True):
            simulate_agent_run()
            st.rerun()
    with col_b:
        if st.button("🗑️ Clear Logs", use_container_width=True):
            st.session_state.logs = []
            st.rerun()

with col2:
    st.subheader("📜 Interaction Log")
    
    # 日志显示
    log_container = st.container()
    with log_container:
        if st.session_state.logs:
            for log in reversed(st.session_state.logs[-20:]):  # 最近20条
                level_class = f"log-{log['level']}"
                st.markdown(f"""
                <div class="log-entry {level_class}">
                    <span class="timestamp">[{log['timestamp']}]</span>
                    <strong>{log['agent'].upper()}</strong>: {log['message']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No logs yet. Click 'Refresh Status' to simulate agent interaction.")

# 数据查看
st.markdown("---")
st.subheader("📁 Output Data")

tab1, tab2, tab3, tab4 = st.tabs(["Knowledge", "Questions", "Guidance", "Remedial"])

with tab1:
    data = read_json_file('output/knowledge.json')
    if data:
        st.json(data)
        st.download_button(
            "Download JSON",
            json.dumps(data, indent=2, ensure_ascii=False),
            "knowledge.json",
            "application/json"
        )
    else:
        st.info("No knowledge data yet.")

with tab2:
    data = read_json_file('output/questions.json')
    if data:
        st.json(data)
        st.download_button(
            "Download JSON",
            json.dumps(data, indent=2, ensure_ascii=False),
            "questions.json",
            "application/json"
        )
    else:
        st.info("No question data yet.")

with tab3:
    data = read_json_file('output/answers.json')
    if data:
        st.json(data)
        st.download_button(
            "Download JSON",
            json.dumps(data, indent=2, ensure_ascii=False),
            "answers.json",
            "application/json"
        )
    else:
        st.info("No guidance data yet.")

with tab4:
    data = read_json_file('output/remedial.json')
    if data:
        st.json(data)
        st.download_button(
            "Download JSON",
            json.dumps(data, indent=2, ensure_ascii=False),
            "remedial.json",
            "application/json"
        )
    else:
        st.info("No remedial data yet.")

# 使用说明
st.markdown("---")
with st.expander("ℹ️ How to Use This Monitor"):
    st.markdown("""
    **Purpose:**
    This page visualizes the multi-agent collaboration in real-time.
    
    **How it works:**
    1. Generate questions on the main page first
    2. Come back here and click "Refresh Status"
    3. Watch the agents process in sequence
    4. View the output JSON files
    
    **For Demo:**
    - Open this page during presentation
    - Generate questions on main page
    - Click "Refresh Status" to show agent interaction
    - Explain each agent's role while showing the logs
    
    **Agent Workflow:**
    ```
    Knowledge Agent → Question Agent → Answer Agent → Remedial Agent
         ↓                  ↓                ↓               ↓
    knowledge.json → questions.json → answers.json → remedial.json
    ```
    """)
