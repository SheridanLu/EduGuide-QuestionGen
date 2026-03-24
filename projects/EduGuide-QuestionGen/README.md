# EduGuide-QuestionGen

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-API-green.svg)](https://www.deepseek.com/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Workflow-orange.svg)](https://github.com/openclaw)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red.svg)](https://streamlit.io/)

</div>

基于 **OpenClaw + DeepSeek** 的智能出题系统

## ✨ 功能特性

- 🎯 **知识点提取** - 自动从教材文本中提取核心知识点
- 📚 **分层出题** - 生成 basic/intermediate/advanced 三层难度题目
- 💡 **答案解析** - 为每道题目生成详细答案和解析
- 🔄 **补救题生成** - 针对学生错误生成个性化练习
- 🤖 **多 Agent 协作** - 基于 OpenClaw 的多 Agent 工作流
- 🎨 **友好界面** - Streamlit 提供的交互式界面

## 🏗️ 技术架构

```
教材文本
    ↓
知识点提取 Agent (KnowledgeAgent)
    ↓
分层出题 Agent (QuestionAgent)
    ↓
答案解析 Agent (AnswerAgent)
    ↓
补救题 Agent (RemedialAgent) [条件执行]
    ↓
最终结果
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/SheridanLu/EduGuide-QuestionGen.git
cd EduGuide-QuestionGen
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

复制环境变量模板并填入你的 DeepSeek API Key：

```bash
cp .env.example .env
# 编辑 .env 文件，填入 DEEPSEEK_API_KEY
```

### 4. 运行项目

#### 方式 1: 命令行测试

```bash
python main.py
```

#### 方式 2: Streamlit 界面

```bash
streamlit run streamlit_app.py
```

#### 方式 3: 自动化开发（GLM Agent）

```bash
./init.sh          # 初始化项目
./run_glm.sh 5     # 运行 5 次开发流程
```

## 📁 项目结构

```
EduGuide-QuestionGen/
├── agents/                  # Agent 实现
│   ├── knowledge_agent.py  # 知识点提取
│   ├── question_agent.py   # 分层出题
│   ├── answer_agent.py     # 答案解析
│   └── remedial_agent.py   # 补救题生成
├── services/                # 服务层
│   └── deepseek_client.py  # DeepSeek API 封装
├── workflow/                # 工作流
│   └── openclaw_flow.py    # OpenClaw 工作流
├── prompts/                 # Prompt 模板
│   ├── knowledge_prompt.py
│   ├── question_prompt.py
│   ├── answer_prompt.py
│   └── remedial_prompt.py
├── utils/                   # 工具函数
│   ├── logger.py           # 日志工具
│   └── formatters.py       # 格式化工具
├── output/                  # 输出结果
├── main.py                  # 主入口
├── streamlit_app.py         # Streamlit 前端
├── test_workflow_mock.py    # 测试脚本
├── config.py                # 配置
├── task.json                # 任务清单
├── progress.txt             # 进度日志
├── CLAUDE.md                # Agent 工作指南
├── init.sh                  # 初始化脚本
├── run_glm.sh               # GLM 运行脚本
└── requirements.txt         # 依赖列表
```

## 📊 输出示例

### 知识点

```json
{
  "knowledge_points": [
    "词干提取（Stemming）",
    "词形还原（Lemmatization）",
    "两者的区别与应用场景"
  ]
}
```

### 分层题目

```json
{
  "basic": [
    "什么是词干提取？",
    "词干提取的目的是什么？"
  ],
  "intermediate": [
    "词干提取和词形还原有什么区别？",
    "在什么情况下应该使用词形还原而不是词干提取？"
  ],
  "advanced": [
    "请设计一个实验来比较词干提取和词形还原在信息检索任务中的效果差异。",
    "分析词干提取对搜索引擎性能的影响，并讨论其优缺点。"
  ]
}
```

### 答案与解析

```json
{
  "basic": [
    {
      "question": "什么是词干提取？",
      "answer": "词干提取是将单词还原为其词根形式的自然语言处理技术。",
      "explanation": "词干提取通过去除单词的前缀和后缀来提取词根，例如将 'running' 提取为 'run'。"
    }
  ]
}
```

## 🧪 测试

运行测试脚本：

```bash
python test_workflow_mock.py
```

测试覆盖：
- ✅ 模块导入测试
- ✅ Prompt 模板测试
- ✅ Agent 初始化测试
- ✅ 工作流初始化测试
- ✅ JSON 处理测试

## 📈 开发进度

当前任务状态：

| 状态 | 任务数 | 说明 |
|------|--------|------|
| ✅ 已完成 | 11 | 核心功能已完成 |
| ⏳ 进行中 | 1 | 文档优化 |
| 🚫 阻塞中 | 0 | - |

详细任务列表请查看 `task.json`。

## 🤝 贡献

本项目采用 **Long-running Agent** 架构，支持多 Agent 协作开发。

### 开发流程

1. 阅读 `CLAUDE.md` 了解工作规范
2. 从 `task.json` 领取任务
3. 开发实现
4. 更新 `progress.txt` 记录进度
5. 提交代码

### 使用 GLM Agent 自动开发

```bash
# 初始化项目
./init.sh

# 运行 N 次开发流程
./run_glm.sh 10
```

## 📝 注意事项

1. **API Key 安全** - 不要将 `.env` 文件提交到 Git
2. **输出目录** - `output/` 目录下的文件会被 `.gitignore` 忽略
3. **日志文件** - 查看 `logs/` 目录了解详细执行日志
4. **错误处理** - 如果遇到 JSON 解析错误，系统会自动尝试修复

## 🔧 故障排除

### 问题 1: 模块导入失败

```bash
# 确保在项目根目录
cd EduGuide-QuestionGen

# 重新安装依赖
pip install -r requirements.txt
```

### 问题 2: API 调用失败

检查 `.env` 文件中的 API Key 是否正确配置：

```bash
cat .env
```

### 问题 3: JSON 解析错误

查看日志文件了解详细信息：

```bash
tail -f logs/*.log
```

## 📄 许可证

MIT License

## 🙏 致谢

- [DeepSeek](https://www.deepseek.com/) - 提供强大的 AI 模型
- [OpenClaw](https://github.com/openclaw) - Agent 工作流框架
- [Streamlit](https://streamlit.io/) - 优秀的 Python 前端框架

---

<div align="center">
Made with ❤️ by AI Agent (全能大龙虾)
</div>
