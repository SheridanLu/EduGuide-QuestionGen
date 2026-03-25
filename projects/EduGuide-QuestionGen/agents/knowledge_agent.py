# agents/knowledge_agent.py - 知识点提取 Agent
import json
import os
from typing import Dict, Any
from services.glm_client import DeepSeekClient
from prompts.knowledge_prompt import build_knowledge_prompt
from utils.logger import get_logger

logger = get_logger(__name__)

class KnowledgeAgent:
    """知识点提取 Agent"""
    
    def __init__(self):
        self.client = DeepSeekClient()
        self.name = "KnowledgeAgent"
    
    def run(self, material_text: str) -> Dict[str, Any]:
        """
        运行知识点提取
        
        Args:
            material_text: 教材文本
        
        Returns:
            {"knowledge_points": [...]}
        """
        logger.info(f"[{self.name}] 开始执行知识点提取...")
        
        # 构建 prompt
        system_prompt, user_prompt = build_knowledge_prompt(material_text)
        
        # 调用 DeepSeek API
        response = self.client.call_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )
        
        # 验证结果
        if "knowledge_points" not in response:
            logger.warning(f"[{self.name}] 响应格式异常，尝试修复...")
            # 尝试修复
            if isinstance(response, dict):
                points = response.get("points", response.get("knowledge", []))
                if points:
                    response = {"knowledge_points": points}
        
        logger.info(f"[{self.name}] 知识点提取完成，共 {len(response.get('knowledge_points', []))} 个")
        return response
    
    def run_with_file(self, input_path: str, output_path: str) -> Dict[str, Any]:
        """
        使用文件系统运行
        
        Args:
            input_path: 输入文件路径（教材文本）
            output_path: 输出文件路径（知识点 JSON）
        """
        # 读取输入
        with open(input_path, 'r', encoding='utf-8') as f:
            material_text = f.read()
        
        # 执行
        result = self.run(material_text)
        
        # 保存输出
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        logger.info(f"[{self.name}] 结果已保存到 {output_path}")
        return result
    
    # 别名，保持一致性
    run_with_files = run_with_file
