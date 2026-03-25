# agents/question_agent.py - 分层出题 Agent
import json
import os
from typing import Dict, Any
from services.unified_client import UnifiedAPIClient as DeepSeekClient
from prompts.question_prompt import build_question_prompt
from utils.logger import get_logger

logger = get_logger(__name__)

class QuestionAgent:
    """分层出题 Agent"""
    
    def __init__(self):
        self.client = DeepSeekClient()
        self.name = "QuestionAgent"
    
    def run(self, material_text: str, knowledge_points: str) -> Dict[str, Any]:
        """执行分层出题任务
        
        Args:
            material_text: 教材文本
            knowledge_points: 知识点列表（JSON 字符串或列表）
        
        Returns:
            生成的题目数据
        """
        logger.info(f"[{self.name}] 开始执行分层出题任务...")
        
        # 处理知识点格式
        if isinstance(knowledge_points, str):
            try:
                kp_data = json.loads(knowledge_points)
                if isinstance(kp_data, dict):
                    knowledge_points = json.dumps(kp_data.get("knowledge_points", []), ensure_ascii=False)
            except Exception:
                pass
        
        # 构建 prompt
        system_prompt, user_prompt = build_question_prompt(material_text, knowledge_points)
        
        # 调用 API
        try:
            response = self.client.call_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
            
            logger.info(f"[{self.name}] API 调用成功")
            
            # 验证结果
            if "basic" not in response and "intermediate" not in response and "advanced" not in response:
                logger.warning(f"[{self.name}] 响应格式异常，尝试修复...")
                # 尝试修复
                if "questions" in response:
                    response = response["questions"]
            
            return response
            
        except Exception as e:
            logger.error(f"[{self.name}] 任务执行失败: {e}")
            raise
    
    def run_with_files(self, material_path: str, knowledge_path: str, output_path: str) -> Dict[str, Any]:
        """使用文件系统运行"""
        try:
            # 读取输入
            with open(material_path, 'r', encoding='utf-8') as f:
                material_text = f.read()
            
            with open(knowledge_path, 'r', encoding='utf-8') as f:
                knowledge_data = json.load(f)
                knowledge_points = json.dumps(knowledge_data.get("knowledge_points", []), ensure_ascii=False)
            
            # 执行
            result = self.run(material_text, knowledge_points)
            
            # 保存输出
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            logger.info(f"[{self.name}] 结果已保存到 {output_path}")
            return result
        except Exception as e:
            logger.error(f"[{self.name}] run_with_files 失败: {e}")
            raise
