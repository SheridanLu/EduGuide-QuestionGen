# config.py - 配置文件
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# 调试模式
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

