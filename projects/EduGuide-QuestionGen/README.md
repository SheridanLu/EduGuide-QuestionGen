# EduGuide-QuestionGen

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Workflow-orange.svg)](https://github.com/openclaw)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red.svg)](https://streamlit.io/)
[![Version](https://img.shields.io/badge/Version-1.1.0-green.svg)](https://github.com/SheridanLu/EduGuide-QuestionGen/releases)

</div>

基于 **OpenClaw** 的智能出题系统，**支持多家 API 提供商**

## ✨ 功能特性

- 🎯 **知识点提取** - 自动从教材文本中提取核心知识点
- 📚 **分层出题** - 生成 basic/intermediate/advanced 三层难度题目
- 💡 **答案解析** - 为每道题目生成详细答案和解析
- 🔄 **补救题生成** - 针对学生错误生成个性化练习
- 🤖 **多 Agent 协作** - 基于 OpenClaw 的多 Agent 工作流
- 🎨 **友好界面** - Streamlit 提供的交互式界面
- 🔌 **多 API 支持** - 支持 6+ 家 API 提供商

## 🔌 支持的 API 提供商

| 提供商 | 模型 | 说明 |
|--------|------|------|
| **智谱 GLM** | glm-4-flash, glm-4, glm-4-plus | 推荐，性价比高 |
| **DeepSeek** | deepseek-chat, deepseek-coder | 代码能力强 |
| **OpenAI** | gpt-3.5-turbo, gpt-4, gpt-4o | 行业标准 |
| **Claude** | claude-3-haiku, claude-3-sonnet, claude-3-opus | 长文本处理 |
| **通义千问** | qwen-turbo, qwen-plus, qwen-max | 阿里云 |
| **Ollama** | llama2, llama3, mistral, codellama | 本地运行 |
| **自定义** | 任意模型 | 自定义 API |

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

### 3. 启动应用

```bash
streamlit run streamlit_app.py
```

### 4. 配置 API

1. 打开浏览器访问 `http://localhost:8501`
2. 点击左侧 **⚙️ API 设置**
3. 选择 API 提供商
4. 输入 API Key
5. 点击 **💾 保存配置**

### 5. 开始使用

1. 回到主页
2. 上传教材文件或直接输入文本
3. 点击 **🚀 开始生成**
4. 查看生成的知识点、题目、答案

## 📁 项目结构

```
EduGuide-QuestionGen/
├── agents/                  # Agent 实现
│   ├── knowledge_agent.py  # 知识点提取
│   ├── question_agent.py   # 分层出题
│   ├── answer_agent.py     # 答案解析
│   └── remedial_agent.py   # 补救题生成
├── services/                # 服务层
│   ├── unified_client.py   # 统一 API 客户端
│   └── glm_client.py       # GLM 客户端
├── workflow/                # 工作流
│   └── openclaw_flow.py    # OpenClaw 工作流
├── prompts/                 # Prompt 模板
├── utils/                   # 工具函数
├── config/                  # 配置文件
│   ├── api_config.py       # API 配置管理
│   └── api_settings.json   # API 设置（不提交）
├── output/                  # 输出结果
├── streamlit_app.py         # Streamlit 前端
└── README.md
```

## 🔧 配置说明

### 方式1: 界面配置（推荐）

在 Streamlit 界面的 **⚙️ API 设置** 页面配置。

### 方式2: 手动配置

复制配置模板：

```bash
cp config/api_settings.json.example config/api_settings.json
```

编辑 `config/api_settings.json`：

```json
{
  "providers": {
    "zhipu": {
      "name": "智谱 GLM",
      "api_key": "your_api_key_here",
      "base_url": "https://open.bigmodel.cn/api/paas/v4",
      "model": "glm-4-flash",
      "enabled": true
    }
  },
  "current_provider": "zhipu"
}
```

## 📝 API Key 获取方式

### 智谱 GLM
1. 访问 [智谱开放平台](https://open.bigmodel.cn/)
2. 注册并登录
3. 在 [API Keys](https://open.bigmodel.cn/user-center/api-keys) 页面创建

### DeepSeek
1. 访问 [DeepSeek](https://www.deepseek.com/)
2. 注册并登录
3. 在 API 设置中创建 Key

### OpenAI
1. 访问 [OpenAI](https://platform.openai.com/)
2. 注册并登录
3. 在 API Keys 页面创建

### 通义千问
1. 访问 [阿里云 DashScope](https://dashscope.aliyun.com/)
2. 开通服务
3. 获取 API Key

## 🎯 使用示例

### 输入教材文本

```
自然语言处理（NLP）是人工智能的一个分支领域...

## 1. 词干提取
词干提取是...
```

### 查看结果

系统会自动生成：

**知识点**:
- 词干提取是将单词还原为词根形式
- 词形还原是将单词还原为基础形式
- 两者在速度和准确性上有差异

**分层题目**:
- Basic: 什么是词干提取？
- Intermediate: 词干提取和词形还原有什么区别？
- Advanced: 在哪些任务中词形还原更适合？

## 🧪 测试

```bash
# 运行模拟测试（无需 API Key）
python test_workflow_mock.py

# 运行完整测试（需要 API Key）
python main.py
```

## 📊 版本历史

### v1.1.0 (2026-03-25)
- ✅ 添加多 API 提供商支持
- ✅ Streamlit 设置页面
- ✅ 实时切换 API
- ✅ 测试连接功能

### v1.0.0 (2026-03-25)
- ✅ 基础功能实现
- ✅ 智谱 GLM 支持
- ✅ 文件上传功能

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

<div align="center">
Made with ❤️ by AI Agent (全能大龙虾) 🦞
</div>
