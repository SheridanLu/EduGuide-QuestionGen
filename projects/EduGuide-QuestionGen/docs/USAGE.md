# 使用指南

## 目录

1. [环境准备](#环境准备)
2. [快速开始](#快速开始)
3. [详细使用说明](#详细使用说明)
4. [常见问题](#常见问题)
5. [高级功能](#高级功能)

## 环境准备

### 系统要求

- Python 3.8 或更高版本
- pip 包管理器
- DeepSeek API Key

### 安装步骤

1. **克隆项目**

```bash
git clone https://github.com/SheridanLu/EduGuide-QuestionGen.git
cd EduGuide-QuestionGen
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

3. **配置 API Key**

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
nano .env
```

在 `.env` 文件中填入你的 DeepSeek API Key：

```
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
```

## 快速开始

### 方式 1: 命令行运行

```bash
python main.py
```

这将运行一个示例工作流，输出结果保存在 `output/` 目录。

### 方式 2: Streamlit 界面

```bash
streamlit run streamlit_app.py
```

然后在浏览器中打开 `http://localhost:8501`。

## 详细使用说明

### 1. 输入教材文本

在 Streamlit 界面的输入框中粘贴你的教材文本。例如：

```
自然语言处理（NLP）是人工智能的一个分支领域...

## 1. 词干提取
词干提取是...
```

### 2. 模拟学生错误（可选）

如果你想生成补救题，可以在"错误知识点"输入框中填入学生的错误理解。例如：

```
混淆了词干提取和词形还原
```

### 3. 运行工作流

点击"开始生成"按钮，系统将自动：

1. 提取知识点
2. 生成分层题目
3. 生成答案和解析
4. (如果指定错误) 生成补救题

### 4. 查看结果

结果将显示在界面的不同标签页中：

- **知识点** - 提取的核心知识点
- **题目** - 三层难度的题目
- **答案** - 每道题的答案和解析
- **补救题** - 针对错误的练习题

## 常见问题

### Q1: 如何获取 DeepSeek API Key？

1. 访问 [DeepSeek 官网](https://www.deepseek.com/)
2. 注册账号并登录
3. 在 API 管理页面创建 API Key
4. 复制 API Key 到 `.env` 文件

### Q2: 为什么提示 JSON 解析失败？

可能原因：
- 模型返回的格式不规范
- 网络问题导致响应不完整

解决方案：
- 查看日志文件了解详情
- 系统会自动尝试修复格式问题
- 如果持续失败，请检查网络连接

### Q3: 如何自定义 Prompt？

每个 Agent 的 Prompt 模板位于 `prompts/` 目录：

```
prompts/
├── knowledge_prompt.py
├── question_prompt.py
├── answer_prompt.py
└── remedial_prompt.py
```

你可以编辑这些文件来自定义 Prompt。

### Q4: 输出结果保存在哪里？

所有输出结果保存在 `output/` 目录：

```
output/
├── knowledge.json    # 知识点
├── questions.json    # 题目
├── answers.json      # 答案
└── remedial.json     # 补救题
```

## 高级功能

### 1. 自定义 Agent

你可以创建自己的 Agent：

```python
from agents.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.name = "MyCustomAgent"
    
    def run(self, input_data):
        # 你的逻辑
        return result
```

### 2. 批量处理

创建一个脚本批量处理多个教材：

```python
from workflow.openclaw_flow import OpenClawFlow

flow = OpenClawFlow()

materials = ["教材1", "教材2", "教材3"]

for i, material in enumerate(materials):
    print(f"处理第 {i+1} 个教材...")
    result = flow.run(material)
    print(f"完成！结果保存在 output/ 目录")
```

### 3. 导出结果

将结果导出为 Markdown 文件：

```python
import json

# 读取结果
with open('output/knowledge.json', 'r') as f:
    knowledge = json.load(f)

# 生成 Markdown
markdown = "# 知识点\n\n"
for point in knowledge['knowledge_points']:
    markdown += f"- {point}\n"

# 保存
with open('export.md', 'w') as f:
    f.write(markdown)
```

### 4. 使用 GLM Agent 自动开发

如果你想使用 OpenClaw 的 GLM Agent 继续开发：

```bash
# 初始化项目
./init.sh

# 运行 5 次开发流程
./run_glm.sh 5
```

GLM Agent 会自动：
1. 读取 `task.json` 领取任务
2. 开发实现
3. 测试验证
4. 更新文档
5. 提交代码

## 联系方式

如有问题，请提交 Issue 或 Pull Request。

---

*此文档由 AI Agent (全能大龙虾) 自动生成*
