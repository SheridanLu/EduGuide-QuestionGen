# services/glm_client.py - 智谱 GLM API 调用客户端
import httpx
import json
import re
import time
from typing import Dict, Any, Optional
from config import API_KEY, API_BASE_URL, API_MODEL
from utils.logger import get_logger
from utils.formatters import clean_json_response

logger = get_logger(__name__)


class GLMClient:
    """智谱 GLM API 客户端"""
    
    def __init__(self, max_retries: int = 3, timeout: int = 30):
        self.max_retries = max_retries
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
    
    def call(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        调用智谱 GLM API
        
        Args:
            system_prompt: 模型角色设定
            user_prompt: 用户输入
        
        Returns:
            模型返回的解析结果
        """
        for attempt in range(self.max_retries):
            try:
                payload = {
                    "model": API_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 2000
                }
                
                logger.info(f"调用 GLM API: {API_BASE_URL}/chat/completions")
                
                response = httpx.post(
                    f"{API_BASE_URL}/chat/completions",
                    json=payload,
                    headers=self.headers,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info("GLM API 调用成功")
                    return clean_json_response(result)
                else:
                    error_msg = f"API 调用失败: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    if attempt < self.max_retries - 1:
                        logger.warning(f"第 {attempt + 1} 次失败，等待 2 秒...")
                        time.sleep(2)
                        continue
                    
                    raise Exception(f"API 调用失败，已达到最大重试次数: {self.max_retries}")
            
            except httpx.Timeout as e:
                logger.error(f"请求超时: {e}")
                raise
            except httpx.RequestError as e:
                logger.error(f"请求错误: {e}")
                raise
            except Exception as e:
                logger.error(f"未知错误: {e}")
                raise
    
    def call_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """强制返回 JSON 格式"""
        response = self.call(system_prompt, user_prompt)
        
        # 如果已经是字典且包含数据，直接返回
        if isinstance(response, dict) and 'error' not in response:
            return response
        
        # 获取内容字符串
        if isinstance(response, dict):
            content = response.get('raw_content', str(response))
        else:
            content = str(response)
        
        # 尝试提取 ```json ... ``` 中的内容
        json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1).strip()
        else:
            # 尝试提取 ```... ``` 中的内容
            cleaned = content.strip()
            if cleaned.startswith('```'):
                cleaned = cleaned[3:]
            if cleaned.endswith('```'):
                cleaned = cleaned[:-3]
            json_str = cleaned
        
        try:
            result = json.loads(json_str)
            logger.info("成功解析 JSON")
            return result
        except json.JSONDecodeError as e:
            logger.warning(f"JSON 解析失败: {e}")
            # 尝试修复常见的 JSON 格式问题
            cleaned = json_str.strip()
            if cleaned.startswith('{'):
                cleaned = cleaned[1:]
            if cleaned.endswith('}'):
                cleaned = cleaned[:-1]
            
            try:
                result = json.loads(cleaned)
                logger.info("修复后成功解析 JSON")
                return result
            except:
                logger.error(f"无法解析为 JSON: {cleaned[:200]}...")
                raise ValueError(f"无法解析模型输出: {cleaned[:200]}")


# 向后兼容：保留 DeepSeekClient 别名
DeepSeekClient = GLMClient
