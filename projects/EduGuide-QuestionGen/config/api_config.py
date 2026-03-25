# config/api_config.py - API 配置管理
import os
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum

class APIProvider(Enum):
    """支持的 API 提供商"""
    ZHIPU = "zhipu"          # 智谱 GLM
    DEEPSEEK = "deepseek"    # DeepSeek
    OPENAI = "openai"        # OpenAI
    CLAUDE = "claude"        # Claude (Anthropic)
    QWEN = "qwen"            # 通义千问
    OLLAMA = "ollama"        # Ollama (本地)
    CUSTOM = "custom"        # 自定义

@dataclass
class ProviderConfig:
    """API 提供商配置"""
    name: str
    api_key: str = ""
    base_url: str = ""
    model: str = ""
    enabled: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProviderConfig':
        return cls(**data)

# 默认配置
DEFAULT_PROVIDERS = {
    APIProvider.ZHIPU: ProviderConfig(
        name="智谱 GLM",
        api_key="",
        base_url="https://open.bigmodel.cn/api/paas/v4",
        model="glm-4-flash",
        enabled=True
    ),
    APIProvider.DEEPSEEK: ProviderConfig(
        name="DeepSeek",
        api_key="",
        base_url="https://api.deepseek.com/v1",
        model="deepseek-chat",
        enabled=False
    ),
    APIProvider.OPENAI: ProviderConfig(
        name="OpenAI",
        api_key="",
        base_url="https://api.openai.com/v1",
        model="gpt-3.5-turbo",
        enabled=False
    ),
    APIProvider.CLAUDE: ProviderConfig(
        name="Claude (Anthropic)",
        api_key="",
        base_url="https://api.anthropic.com/v1",
        model="claude-3-haiku-20240307",
        enabled=False
    ),
    APIProvider.QWEN: ProviderConfig(
        name="通义千问",
        api_key="",
        base_url="https://dashscope.aliyuncs.com/api/v1",
        model="qwen-turbo",
        enabled=False
    ),
    APIProvider.OLLAMA: ProviderConfig(
        name="Ollama (本地)",
        api_key="",
        base_url="http://localhost:11434/v1",
        model="llama2",
        enabled=False
    ),
    APIProvider.CUSTOM: ProviderConfig(
        name="自定义 API",
        api_key="",
        base_url="",
        model="",
        enabled=False
    ),
}

# 可选模型列表
AVAILABLE_MODELS = {
    APIProvider.ZHIPU: [
        "glm-4-flash (推荐，快速)",
        "glm-4 (标准)",
        "glm-4-plus (高级)",
        "glm-4-air (经济)",
    ],
    APIProvider.DEEPSEEK: [
        "deepseek-chat (推荐)",
        "deepseek-coder (代码)",
    ],
    APIProvider.OPENAI: [
        "gpt-3.5-turbo (经济)",
        "gpt-4 (标准)",
        "gpt-4-turbo (快速)",
        "gpt-4o (最新)",
    ],
    APIProvider.CLAUDE: [
        "claude-3-haiku-20240307 (快速)",
        "claude-3-sonnet-20240229 (标准)",
        "claude-3-opus-20240229 (高级)",
    ],
    APIProvider.QWEN: [
        "qwen-turbo (快速)",
        "qwen-plus (标准)",
        "qwen-max (高级)",
    ],
    APIProvider.OLLAMA: [
        "llama2",
        "llama3",
        "mistral",
        "codellama",
        "qwen2",
    ],
    APIProvider.CUSTOM: [
        "自定义模型"
    ],
}

class APIConfigManager:
    """API 配置管理器"""
    
    def __init__(self, config_file: str = "config/api_settings.json"):
        self.config_file = config_file
        self.providers: Dict[APIProvider, ProviderConfig] = {}
        self.current_provider: APIProvider = APIProvider.ZHIPU
        self.load_config()
    
    def load_config(self):
        """加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 加载提供商配置
                for provider_str, config_data in data.get('providers', {}).items():
                    provider = APIProvider(provider_str)
                    self.providers[provider] = ProviderConfig.from_dict(config_data)
                
                # 加载当前提供商
                current = data.get('current_provider')
                if current:
                    self.current_provider = APIProvider(current)
                    
            except Exception as e:
                print(f"加载配置失败: {e}")
                self._init_default_config()
        else:
            self._init_default_config()
    
    def _init_default_config(self):
        """初始化默认配置"""
        self.providers = DEFAULT_PROVIDERS.copy()
        self.current_provider = APIProvider.ZHIPU
    
    def save_config(self):
        """保存配置"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        
        data = {
            'providers': {
                provider.value: config.to_dict() 
                for provider, config in self.providers.items()
            },
            'current_provider': self.current_provider.value
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_current_config(self) -> ProviderConfig:
        """获取当前提供商配置"""
        return self.providers.get(self.current_provider, DEFAULT_PROVIDERS[self.current_provider])
    
    def set_current_provider(self, provider: APIProvider):
        """设置当前提供商"""
        self.current_provider = provider
        self.save_config()
    
    def update_provider_config(self, provider: APIProvider, config: ProviderConfig):
        """更新提供商配置"""
        self.providers[provider] = config
        self.save_config()
    
    def get_all_providers(self) -> List[Dict[str, Any]]:
        """获取所有提供商列表"""
        return [
            {
                'id': provider.value,
                'name': config.name,
                'enabled': config.enabled,
                'configured': bool(config.api_key),
                'models': AVAILABLE_MODELS.get(provider, [])
            }
            for provider, config in self.providers.items()
        ]
    
    def is_configured(self, provider: APIProvider) -> bool:
        """检查提供商是否已配置"""
        config = self.providers.get(provider)
        return config is not None and bool(config.api_key)

# 全局配置管理器实例
_config_manager: Optional[APIConfigManager] = None

def get_config_manager() -> APIConfigManager:
    """获取配置管理器实例"""
    global _config_manager
    if _config_manager is None:
        _config_manager = APIConfigManager()
    return _config_manager
