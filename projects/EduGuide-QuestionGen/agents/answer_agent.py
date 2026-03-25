# agents/answer_agent.py - 答案解析 Agent
import json
import os
from typing import Dict, Any
from services.unified_client import UnifiedAPIClient as DeepSeekClient
from prompts.answer_prompt import build_answer_prompt
from utils.logger import get_logger

logger = get_logger(__name__)

class AnswerAgent:
    """答案解析 Agent"""
    
    def __init__(self):
        self.client = DeepSeekClient()
        self.name = "AnswerAgent"
    
    def run(self, material_text: str, knowledge_points: str, questions: Dict[str, Any]) -> Dict[str, Any]:
        """执行答案解析任务
        
        Args:
            material_text: 教材文本
            knowledge_points: 知识点列表
            questions: 题目数据
        
        Returns:
            答案和解析数据
        """
        logger.info(f"[{self.name}] 开始执行答案解析任务...")
        
        # 处理知识点格式
        if isinstance(knowledge_points, str):
            try:
                kp_data = json.loads(knowledge_points)
                if isinstance(kp_data, dict):
                    knowledge_points = json.dumps(kp_data.get("knowledge_points", []), ensure_ascii=False)
            except Exception:
                pass
        
        # 将题目转为字符串
        questions_str = json.dumps(questions, ensure_ascii=False, indent=2)
        
        # 构建 prompt
        system_prompt, user_prompt = build_answer_prompt(knowledge_points, questions_str)
        
        # 调用 API
        try:
            response = self.client.call_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
            
            logger.info(f"[{self.name}] API 调用成功")
            return response
            
        except Exception as e:
            logger.error(f"[{self.name}] 任务执行失败: {e}")
            raise
    
    def run_with_files(self, material_path: str, knowledge_path: str, questions_path: str, output_path: str) -> Dict[str, Any]:
        """使用文件系统运行"""
        try:
            # 读取输入
            with open(material_path, 'r', encoding='utf-8') as f:
                material_text = f.read()
            
            with open(knowledge_path, 'r', encoding='utf-8') as f:
                knowledge_data = json.load(f)
                knowledge_points = json.dumps(knowledge_data.get("knowledge_points", []), ensure_ascii=False)
            
            with open(questions_path, 'r', encoding='utf-8') as f:
                questions = json.load(f)
            
            # 执行
            result = self.run(material_text, knowledge_points, questions)
            
            # 保存输出
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            logger.info(f"[{self.name}] 结果已保存到 {output_path}")
            return result
        except Exception as e:
            logger.error(f"[{self.name}] run_with_files 失败: {e}")
            raise
