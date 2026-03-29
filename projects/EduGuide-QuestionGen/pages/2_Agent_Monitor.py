# pages/2_Agent_Monitor.py - Agent监控可视化
import streamlit as st
import json
import os
import time
from datetime import datetime

# ========== 多语言 ==========
T = {
    "en": {
        "title": "Agent Monitor",
        "subtitle": "Real-time visualization of multi-agent collaboration",
        "refresh": "Refresh Status",
        "clear": "Clear",
        "input": "Input", "output": "Output",
        "no_logs": "No logs yet. Generate questions first, then refresh.",
        "no_data": "No data yet.",
        "download": "Download",
        "points": "points",
        "questions": "questions",
        "guidance": "guidance",
        "remedial": "remedial items",
        "workflow": "Agent Workflow",
        "status": "Status",
        "data_view": "Output Data",
        "how_to": "How to Use",
        "how_to_text": "1. Generate questions on the main page\n2. Come back here and click Refresh\n3. Watch agents process in sequence",
        "knowledge": "Knowledge", "question_tab": "Questions",
        "answer_tab": "Guidance", "remedial_tab": "Remedial",
        "processing": "Processing...",
        "extracted": "Extracted",
        "generated": "Generated",
        "created": "Created",
        "waiting_input": "Waiting for input",
        "no_errors": "No student errors",
        "from": "from",
        "for": "for",
        "each": "each",
    },
    "zh-CN": {
        "title": "Agent 监控",
        "subtitle": "多Agent协作实时可视化",
        "refresh": "刷新状态",
        "clear": "清空",
        "input": "输入", "output": "输出",
        "no_logs": "暂无日志。请先在主页生成题目，然后刷新。",
        "no_data": "暂无数据。",
        "download": "下载",
        "points": "个知识点",
        "questions": "道题目",
        "guidance": "条引导",
        "remedial": "条补救",
        "workflow": "Agent 工作流",
        "status": "状态",
        "data_view": "输出数据",
        "how_to": "使用说明",
        "how_to_text": "1. 在主页生成题目\n2. 回到此页面点击刷新\n3. 观察 Agent 依次处理",
        "knowledge": "知识点", "question_tab": "题目",
        "answer_tab": "引导", "remedial_tab": "补救",
        "processing": "处理中...",
        "extracted": "提取了",
        "generated": "生成了",
        "created": "创建了",
        "waiting_input": "等待输入",
        "no_errors": "未检测到学生错误",
        "from": "从",
        "for": "为",
        "each": "每道",
    },
    "zh-TW": {
        "title": "Agent 監控",
        "subtitle": "多Agent協作即時視覺化",
        "refresh": "重新整理狀態",
        "clear": "清空",
        "input": "輸入", "output": "輸出",
        "no_logs": "暫無日誌。請先在主頁生成題目，然後重新整理。",
        "no_data": "暫無資料。",
        "download": "下載",
        "points": "個知識點",
        "questions": "道題目",
        "guidance": "條引導",
        "remedial": "條補救",
        "workflow": "Agent 工作流",
        "status": "狀態",
        "data_view": "輸出資料",
        "how_to": "使用說明",
        "how_to_text": "1. 在主頁生成題目\n2. 回到此頁面點擊重新整理\n3. 觀察 Agent 依序處理",
        "knowledge": "知識點", "question_tab": "題目",
        "answer_tab": "引導", "remedial_tab": "補救",
        "processing": "處理中...",
        "extracted": "提取了",
        "generated": "生成了",
        "created": "建立了",
        "waiting_input": "等待輸入",
        "no_errors": "未偵測到學生錯誤",
        "from": "從",
        "for": "為",
        "each": "每道",
    }
}

def t(key, lang="en"):
    return T.get(lang, T["en"]).get(key, key)

# ========== 配置 ==========
st.set_page_config(page_title="Agent Monitor - EduGuide", page_icon="🔍", layout="wide")

lang = st.session_state.get('lang', 'en')

# ========== CSS ==========
st.markdown("""<style>
/* Agent 状态卡片 */
.agent-node {
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.agent-node::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
}
.node-waiting {
    background: #fafbfc;
    border: 1px solid #f0f0f0;
}
.node-waiting::before { background: #ccc; }
.node-active {
    background: #f0f9ff;
    border: 1.5px solid #93c5fd;
    box-shadow: 0 4px 16px rgba(59, 130, 246, 0.1);
}
.node-active::before { background: #3b82f6; }
.node-complete {
    background: #f0fdf4;
    border: 1.5px solid #86efac;
}
.node-complete::before { background: #22c55e; }
.node-error {
    background: #fef2f2;
    border: 1.5px solid #fca5a5;
}
.node-error::before { background: #ef4444; }

.agent-icon {
    font-size: 2rem;
    margin-bottom: 8px;
}
.agent-name {
    font-size: 0.95rem;
    font-weight: 700;
    color: #111;
    margin-bottom: 4px;
}
.agent-desc {
    font-size: 0.78rem;
    color: #888;
    line-height: 1.4;
    margin-bottom: 12px;
}
.agent-stat {
    font-size: 0.82rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 100px;
    display: inline-block;
}
.stat-complete { background: #dcfce7; color: #166534; }
.stat-waiting { background: #f3f4f6; color: #6b7280; }
.stat-active { background: #dbeafe; color: #1e40af; }

/* 连接箭头 */
.flow-arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    color: #d0d0d0;
    font-size: 1.5rem;
    padding: 0 4px;
}
.flow-arrow.active { color: #6366f1; }

/* 日志 */
.log-line {
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 0.85rem;
    margin: 4px 0;
    display: flex;
    align-items: flex-start;
    gap: 8px;
    line-height: 1.5;
}
.log-info { background: #f0f9ff; color: #1e40af; }
.log-success { background: #f0fdf4; color: #166534; }
.log-warning { background: #fffbeb; color: #92400e; }
.log-error { background: #fef2f2; color: #991b1b; }
.log-time {
    font-size: 0.75rem;
    color: #aaa;
    white-space: nowrap;
    margin-top: 2px;
}

/* 数据JSON */
.data-card {
    background: #fafbfc;
    border: 1px solid #f0f0f0;
    border-radius: 12px;
    padding: 16px;
    font-family: "SF Mono", "Fira Code", monospace;
    font-size: 0.82rem;
    max-height: 400px;
    overflow-y: auto;
    line-height: 1.6;
    white-space: pre-wrap;
    word-break: break-all;
}

/* Section */
.section-title {
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #aaa;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

# ========== Agent 配置 ==========
AGENTS = [
    {"id": "knowledge", "icon": "📚", "name": {"en": "Knowledge Agent", "zh-CN": "知识Agent", "zh-TW": "知識Agent"},
     "desc": {"en": "Extract key concepts", "zh-CN": "提取核心概念", "zh-TW": "提取核心概念"},
     "output": "output/knowledge.json"},
    {"id": "question", "icon": "📝", "name": {"en": "Question Agent", "zh-CN": "题目Agent", "zh-TW": "題目Agent"},
     "desc": {"en": "Generate tiered questions", "zh-CN": "生成分级题目", "zh-TW": "生成分級題目"},
     "output": "output/questions.json"},
    {"id": "answer", "icon": "🎯", "name": {"en": "Answer Agent", "zh-CN": "引导Agent", "zh-TW": "引導Agent"},
     "desc": {"en": "Socratic step-by-step guidance", "zh-CN": "苏格拉底式引导", "zh-TW": "蘇格拉底式引導"},
     "output": "output/answers.json"},
    {"id": "remedial", "icon": "🤝", "name": {"en": "Remedial Agent", "zh-CN": "补救Agent", "zh-TW": "補救Agent"},
     "desc": {"en": "Remedial for student errors", "zh-CN": "学生错误补救", "zh-TW": "學生錯誤補救"},
     "output": "output/remedial.json"},
]

# ========== 初始化 ==========
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'agent_status' not in st.session_state:
    st.session_state.agent_status = {a['id']: 'waiting' for a in AGENTS}
if 'agent_stats' not in st.session_state:
    st.session_state.agent_stats = {}

# ========== 工具函数 ==========
def read_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def add_log(agent_id, msg, level='info'):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append({'ts': ts, 'agent': agent_id, 'msg': msg, 'level': level})

def refresh_status():
    st.session_state.logs = []
    st.session_state.agent_status = {a['id']: 'waiting' for a in AGENTS}
    st.session_state.agent_stats = {}

    files = {
        'knowledge': 'output/knowledge.json',
        'question': 'output/questions.json',
        'answer': 'output/answers.json',
        'remedial': 'output/remedial.json',
    }

    # Knowledge
    st.session_state.agent_status['knowledge'] = 'active'
    add_log('knowledge', f'{t("processing", lang)}...', 'info')
    time.sleep(0.3)
    d = read_json(files['knowledge'])
    if d:
        n = len(d.get('knowledge_points', []))
        st.session_state.agent_status['knowledge'] = 'complete'
        st.session_state.agent_stats['knowledge'] = f"{n} {t('points', lang)}"
        add_log('knowledge', f'✅ {t("extracted", lang)} {n} {t("points", lang)}', 'success')
    else:
        st.session_state.agent_stats['knowledge'] = ""
        add_log('knowledge', f'⏳ {t("waiting_input", lang)}', 'warning')

    # Question
    if st.session_state.agent_status['knowledge'] == 'complete':
        st.session_state.agent_status['question'] = 'active'
        add_log('question', f'{t("processing", lang)}...', 'info')
        time.sleep(0.3)
        d = read_json(files['question'])
        if d:
            n = sum(len(d.get(l, [])) for l in ['basic', 'intermediate', 'advanced'])
            st.session_state.agent_status['question'] = 'complete'
            st.session_state.agent_stats['question'] = f"{n} {t('questions', lang)}"
            add_log('question', f'✅ {t("generated", lang)} {n} {t("questions", lang)}', 'success')
        else:
            add_log('question', '⏳ ...', 'warning')

    # Answer
    if st.session_state.agent_status['question'] == 'complete':
        st.session_state.agent_status['answer'] = 'active'
        add_log('answer', f'{t("processing", lang)}...', 'info')
        time.sleep(0.3)
        d = read_json(files['answer'])
        if d:
            n = sum(len(d.get(l, [])) for l in ['basic', 'intermediate', 'advanced'])
            st.session_state.agent_status['answer'] = 'complete'
            st.session_state.agent_stats['answer'] = f"{n} {t('guidance', lang)}"
            add_log('answer', f'✅ {t("created", lang)} {n} {t("guidance", lang)}', 'success')
        else:
            add_log('answer', '⏳ ...', 'warning')

    # Remedial
    d = read_json(files['remedial'])
    if d:
        st.session_state.agent_status['remedial'] = 'active'
        add_log('remedial', f'{t("processing", lang)}...', 'info')
        time.sleep(0.3)
        n = len(d.get('remedial', []))
        st.session_state.agent_status['remedial'] = 'complete'
        st.session_state.agent_stats['remedial'] = f"{n} {t('remedial', lang)}"
        add_log('remedial', f'✅ {t("generated", lang)} {n} {t("remedial", lang)}', 'success')
    else:
        st.session_state.agent_stats['remedial'] = ""
        add_log('remedial', f'ℹ️ {t("no_errors", lang)}', 'info')

# ========== 页面内容 ==========
st.markdown(f'<div class="section-title">{t("workflow", lang).upper()}</div>', unsafe_allow_html=True)

# 工作流可视化 - 4个Agent + 箭头
cols = st.columns([3, 0.5, 3, 0.5, 3, 0.5, 3])
for i, agent in enumerate(AGENTS):
    with cols[i * 2]:
        status = st.session_state.agent_status[agent['id']]
        name = agent['name'].get(lang, agent['name']['en'])
        desc = agent['desc'].get(lang, agent['desc']['en'])
        stat = st.session_state.agent_stats.get(agent['id'], '')
        stat_cls = f"stat-{status}"

        st.markdown(f"""
        <div class="agent-node node-{status}">
            <div class="agent-icon">{agent['icon']}</div>
            <div class="agent-name">{name}</div>
            <div class="agent-desc">{desc}</div>
            {'<div class="agent-stat ' + stat_cls + '">' + stat + '</div>' if stat else ''}
        </div>
        """, unsafe_allow_html=True)

    # 箭头（不在最后一个后面画）
    if i < len(AGENTS) - 1:
        next_status = st.session_state.agent_status[AGENTS[i + 1]['id']]
        arrow_cls = "active" if status == 'complete' and next_status in ('complete', 'active') else ""
        with cols[i * 2 + 1]:
            st.markdown(f'<div class="flow-arrow {arrow_cls}" style="margin-top:30px">→</div>', unsafe_allow_html=True)

# 刷新按钮
col_r, col_c = st.columns([1, 5])
with col_r:
    if st.button(f"🔄 {t('refresh', lang)}", type="primary", use_container_width=True):
        refresh_status()
        st.rerun()
with col_c:
    if st.button(f"🗑️ {t('clear', lang)}", use_container_width=True):
        st.session_state.logs = []
        st.session_state.agent_status = {a['id']: 'waiting' for a in AGENTS}
        st.session_state.agent_stats = {}
        st.rerun()

# ========== 日志 ==========
st.markdown('<div class="section-title">LOG</div>', unsafe_allow_html=True)

if st.session_state.logs:
    for log in reversed(st.session_state.logs[-15:]):
        st.markdown(f"""
        <div class="log-line log-{log['level']}">
            <span class="log-time">[{log['ts']}]</span>
            <span><strong>{log['agent'].upper()}</strong>: {log['msg']}</span>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info(t('no_logs', lang))

# ========== 数据查看 ==========
st.markdown('<div class="section-title">OUTPUT DATA</div>', unsafe_allow_html=True)

files = [
    ("output/knowledge.json", t('knowledge', lang)),
    ("output/questions.json", t('question_tab', lang)),
    ("output/answers.json", t('answer_tab', lang)),
    ("output/remedial.json", t('remedial_tab', lang)),
]

t1, t2, t3, t4 = st.tabs([f"📚 {files[0][1]}", f"📝 {files[1][1]}", f"🎯 {files[2][1]}", f"🤝 {files[3][1]}"])

for tab, (filepath, label) in zip([t1, t2, t3, t4], files):
    with tab:
        data = read_json(filepath)
        if data:
            st.markdown(f'<div class="data-card">{json.dumps(data, indent=2, ensure_ascii=False)}</div>', unsafe_allow_html=True)
            st.download_button(
                f"📥 {t('download', lang)} {os.path.basename(filepath)}",
                json.dumps(data, indent=2, ensure_ascii=False),
                os.path.basename(filepath),
                "application/json"
            )
        else:
            st.info(t('no_data', lang))

# ========== 使用说明 ==========
with st.expander(f"ℹ️ {t('how_to', lang)}"):
    st.markdown(t('how_to_text', lang))
