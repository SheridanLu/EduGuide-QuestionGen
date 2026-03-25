# config/__init__.py - 配置文件
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API 配置（从环境变量读取，优先级低于 api_settings.json）
API_KEY = os.getenv("API_KEY", "")
API_BASE_URL = os.getenv("API_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
API_MODEL = os.getenv("API_MODEL", "glm-4-flash")

# 调试模式
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

# 如果没有通过环境变量配置，给出提示
if not API_KEY:
    print("⚠️ 提示: 请在 API 设置页面配置 API Key，或设置环境变量 API_KEY")
