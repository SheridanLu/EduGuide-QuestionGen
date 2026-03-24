# EduGuide-QuestionGen

基于 OpenClaw + DeepSeek 的智能出题系统

## 项目简介

本项目是一个多 Agent 协作的智能出题系统，能够：

1. **输入教材文本** → 提取知识点
2. **生成分层题目** → basic / intermediate / advanced 三层难度
3. **生成答案与解析** → 为每道题提供详细解析
4. **生成补救题** → 针对错误知识点生成针对性练习

## 技术栈

- **Python 3.8+**
- **DeepSeek API** - 大模型调用
- **OpenClaw** - 工作流协调
- **Streamlit** - 前端界面

## 项目结构

```
EduGuide-QuestionGen/
├── agents/              # Agent 实现
│   ├── knowledge_agent.py
│   ├── question_agent.py
│   ├── answer_agent.py
│   └── remedial_agent.py
├── services/            # 服务层
│   ├── deepseek_client.py
│   └── parser.py
├── workflow/            # 工作流
│   └── openclaw_flow.py
├── prompts/             # Prompt 模板
│   ├── knowledge_prompt.py
│   ├── question_prompt.py
│   ├── answer_prompt.py
│   └── remedial_prompt.py
├── utils/               # 工具函数
│   ├── logger.py
│   └── formatters.py
├── output/              # 输出结果
├── main.py              # 主入口
├── streamlit_app.py     # Streamlit 前端
├── config.py            # 配置
├── task.json            # 任务清单
├── progress.txt         # 进度日志
├── CLAUDE.md            # Agent 工作指南
├── init.sh              # 初始化脚本
├── run_glm.sh           # GLM 运行脚本
└── requirements.txt     # 依赖列表
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

复制环境变量模板并填入你的 DeepSeek API Key：

```bash
cp .env.example .env
# 编辑 .env 文件，填入 DEEPSEEK_API_KEY
```

### 3. 运行项目

```bash
# 方式1: 直接运行主程序
python main.py

# 方式2: 启动 Streamlit 前端
streamlit run streamlit_app.py

# 方式3: 使用 GLM Agent 自动开发
./init.sh          # 初始化项目
./run_glm.sh 5     # 运行 5 次开发流程
```

## 工作流程

```
教材文本
    ↓
知识点提取 Agent
    ↓
分层出题 Agent
    ↓
答案解析 Agent
    ↓
补救题 Agent (条件执行)
    ↓
最终结果
```

## 输出示例

### 知识点
```json
{
  "knowledge_points": [
    "词干提取（Stemming）",
    "词形还原（Lemmatization）",
    "两者的区别"
  ]
}
```

### 题目
```json
{
  "basic": [
    "什么是词干提取？"
  ],
  "intermediate": [
    "词干提取和词形还原有什么区别？"
  ],
  "advanced": [
    "在哪些任务中词形还原更适合？为什么？"
  ]
}
```

## 开发任务

当前任务状态：

| 状态 | 任务数 |
|------|--------|
| ✅ 已完成 | 10 |
| ⏳ 待处理 | 2 |
| 🚫 阻塞中 | 0 |

详细任务列表请查看 `task.json`。

## 贡献

本项目采用 Long-running Agent 架构，支持多 Agent 协作开发。请参考 `CLAUDE.md` 了解工作规范。

## 许可证

MIT
