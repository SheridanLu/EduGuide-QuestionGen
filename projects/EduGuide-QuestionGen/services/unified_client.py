# services/unified_client.py - 统一的 API 客户端
import httpx
import json
import re
import time
from typing import Dict, Any, Optional
from config.api_config import APIProvider, get_config_manager, ProviderConfig
from utils.logger import get_logger

logger = get_logger(__name__)

class UnifiedAPIClient:
    """统一的 API 客户端，支持多个提供商"""
    
    def __init__(self, provider_config: Optional[ProviderConfig] = None):
        self.config_manager = get_config_manager()
        self.config = provider_config or self.config_manager.get_current_config()
        self.max_retries = 3
        self.timeout = 60
        self._client = None
        self._init_client()
    
    def _init_client(self):
        """初始化 HTTP 客户端"""
        self._client = httpx.Client(
            timeout=self.timeout,
            headers=self._get_headers()
        )
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        if not self.config.api_key:
            raise ValueError("API Key 未配置")
        
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
    
    def call(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """调用 API
        
        Args:
            system_prompt: 模型角色设定
            user_prompt: 用户输入
        
        Returns:
            模型返回的解析结果
        """
        for attempt in range(self.max_retries):
            try:
                payload = self._build_payload(system_prompt, user_prompt)
                
                logger.info(f"调用 API: {self.config.base_url}/chat/completions")
                
                response = self._client.post(
                    f"{self.config.base_url}/chat/completions",
                    json=payload,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info("API 调用成功")
                    return self._parse_response(result)
                else:
                    error_msg = f"API 调用失败: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    if attempt < self.max_retries - 1:
                        logger.warning(f"第 {attempt + 1} 次失败，等待 2 秒...")
                        time.sleep(2)
                        continue
                    
                    raise Exception(f"API 调用失败，已达到最大重试次数: {self.max_retries}")
            
            except httpx.ReadTimeout as e:
                logger.error(f"读取超时: {e}")
                if attempt < self.max_retries - 1:
                    logger.warning(f"第 {attempt + 1} 次超时，等待 3 秒后重试...")
                    time.sleep(3)
                    continue
                raise
            except httpx.ConnectTimeout as e:
                logger.error(f"连接超时: {e}")
                if attempt < self.max_retries - 1:
                    logger.warning(f"第 {attempt + 1} 次连接超时，等待 3 秒后重试...")
                    time.sleep(3)
                    continue
                raise
            except httpx.RequestError as e:
                logger.error(f"请求错误: {e}")
                raise
            except Exception as e:
                logger.error(f"未知错误: {e}")
                raise
    
    def _build_payload(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """构建请求负载"""
        return {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
    
    def _parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """解析响应"""
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        if not content:
            return {"error": "响应内容为空"}
        
        # 尝试提取 JSON
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
            except Exception:
                logger.error(f"无法解析为 JSON: {cleaned[:200]}...")
                raise ValueError(f"无法解析模型输出: {cleaned[:200]}")
    
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
            except Exception:
                logger.error(f"无法解析为 JSON: {cleaned[:200]}...")
                raise ValueError(f"无法解析模型输出: {cleaned[:200]}")


# 工厂函数：根据提供商类型创建客户端
def create_client(provider: Optional[APIProvider] = None) -> UnifiedAPIClient:
    """创建 API 客户端"""
    config_manager = get_config_manager()
    
    if provider:
        config = config_manager.providers.get(provider)
        if not config:
            raise ValueError(f"不支持的提供商: {provider}")
    else:
        config = config_manager.get_current_config()
    
    if not config.api_key:
        raise ValueError(f"提供商 {config.name} 未配置 API Key")
    
    return UnifiedAPIClient(config)
