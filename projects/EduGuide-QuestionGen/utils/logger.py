# utils/logger.py - 日志工具
import logging
import sys
from datetime import datetime
from typing import Optional, Dict, Any

from config import DEBUG_MODE

class Logger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.name = name
        
        # 设置日志级别
        if DEBUG_MODE:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        
        # 添加控制台处理器
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            f'{asctime} - {name} - {levelname} - {message}'
        ))
        self.logger.addHandler(handler)
    
    def info(self, message: str, data: Optional[Dict] = None):
        extra = {"data": data} if data else {}
        self.logger.info(message, extra=extra)
    
    def warning(self, message: str, data: Optional[Dict] = None):
        extra = {"data": data} if data else {}
        self.logger.warning(message, extra=extra)
    
    def error(self, message: str, data: Optional[Dict] = None):
        extra = {"data": data} if data else {}
        self.logger.error(message, extra=extra)
    
    def debug(self, message: str, data: Optional[Dict] = None):
        if DEBUG_MODE:
            extra = {"data": data} if data else {}
            self.logger.debug(message, extra=extra)


def get_logger(name: str) -> Logger:
    return Logger(name)
