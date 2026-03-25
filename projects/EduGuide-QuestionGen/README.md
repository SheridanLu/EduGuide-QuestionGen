# EduGuide-QuestionGen

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![GLM](https://img.shields.io/badge/GLM-4-green.svg)](https://open.bigmodel.cn/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Workflow-orange.svg)](https://github.com/openclaw)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red.svg)](https://streamlit.io/)

</div>

基于 **OpenClaw + 智谱 GLM** 的智能出题系统

## ✨ 功能特性

- 🎯 **知识点提取** - 自动从教材文本中提取核心知识点
- 📚 **分层出题** - 生成 basic/intermediate/advanced 三层难度题目
- 💡 **答案解析** - 为每道题目生成详细答案和解析
- 🔄 **补救题生成** - 针对学生错误生成个性化练习
- 🤖 **多 Agent 协作** - 基于 OpenClaw 的多 Agent 工作流
- 🎨 **友好界面** - Streamlit 提供的交互式界面

## 🚀 快速开始

### 1. 获取智谱 API Key

1. 访问 [智谱开放平台](https://open.bigmodel.cn/)
2. 注册账号并登录
3. 在 [API 密钥管理](https://open.bigmodel.cn/user-center/api-keys) 页面创建 API Key
4. 复制 API Key

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
nano .env
```

在 `.env` 文件中填入你的智谱 API Key：

### 3. 安装依赖

```bash
pip install -r requirements.txt
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

## 📝 API 配置说明

### 智谱 API 配置

在 `.env` 文件中配置：

```bash
# 智谱 API Key（必填）
API_KEY=your_glm_api_key_here

# API 基础 URL（可选，默认为智谱 API）
API_BASE_URL=https://open.bigmodel.cn/api/paas/v4

# 模型名称（可选，默认为 glm-4-flash）
API_MODEL=glm-4-flash
```

### 可用模型

| 模型 | 说明 | 推荐场景 |
|------|------|--------|
| `glm-4-flash` | 速度快，成本低 | 日常测试、快速迭代 |
| `glm-4` | 效果更好、支持长文本 | 生产环境、复杂任务 |
| `glm-4-plus` | 最强效果 | 高质量要求场景 |

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

## 📁 项目结构

```
EduGuide-QuestionGen/
├── agents/              # Agent 实现
├── services/            # 服务层（GLM API 客户端）
├── workflow/            # 工作流
├── prompts/             # Prompt 模板
├── utils/               # 工具函数
├── output/              # 输出结果
├── main.py              # 主入口
├── streamlit_app.py     # Streamlit 前端
└── config.py            # 配置
```

## 🧪 测试

```bash
# 运行模拟测试（无需 API Key）
python test_workflow_mock.py

# 运行完整测试（需要 API Key）
python main.py
```

## 📊 开发进度

| 状态 | 任务数 |
|------|--------|
| ✅ 已完成 | 12 |
| ⏳ 待处理 | 0 |

## 🤝 贡献

本项目采用 Long-running Agent 架构，支持 GLM Agent 自动开发。

```bash
./init.sh          # 初始化项目
./run_glm.sh 5     # 运行 5 次开发流程
```

## 📄 许可证

MIT License

---

<div align="center">
Made with ❤️ by AI Agent (全能大龙虾) 🦞
Powered by 智谱 GLM
</div>
