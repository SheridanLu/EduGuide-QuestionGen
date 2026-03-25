# config.py - 配置文件
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API 配置
API_KEY = os.getenv("API_KEY", "")
API_BASE_URL = os.getenv("API_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
API_MODEL = os.getenv("API_MODEL", "glm-4-flash")

# 调试模式
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

if not API_KEY:
    print("⚠️ 警告: API_KEY 未设置，请在 .env 文件中配置")
