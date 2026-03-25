# agents/remedial_agent.py - 补救题生成 Agent
import json
import os
from typing import Dict, Any
from services.unified_client import UnifiedAPIClient as DeepSeekClient
from prompts.remedial_prompt import build_remedial_prompt
from utils.logger import get_logger

logger = get_logger(__name__)

class RemedialAgent:
    """补救题生成 Agent"""
    
    def __init__(self):
        self.client = DeepSeekClient()
        self.name = "RemedialAgent"
    
    def run(self, material_text: str, knowledge_points: str, questions_answers: str, wrong_point: str) -> Dict[str, Any]:
        """执行补救题生成任务
        
        Args:
            material_text: 教材文本
            knowledge_points: 知识点
            questions_answers: 题目和答案
            wrong_point: 错误知识点
        
        Returns:
            补救题数据
        """
        logger.info(f"[{self.name}] 开始执行补救题生成任务...")
        logger.info(f"[{self.name}] 错误知识点: {wrong_point}")
        
        # 构建 prompt
        system_prompt, user_prompt = build_remedial_prompt(
            material_text=material_text,
            knowledge_points=knowledge_points,
            questions_answers=questions_answers,
            wrong_point=wrong_point
        )
        
        # 调用 API
        try:
            response = self.client.call_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
            
            logger.info(f"[{self.name}] API 调用成功")
            
            # 验证结果
            if "remedial" not in response:
                logger.warning(f"[{self.name}] 响应格式异常，尝试修复...")
                # 尝试修复
                if "questions" in response:
                    response = {"remedial": response["questions"]}
            
            return response
            
        except Exception as e:
            logger.error(f"[{self.name}] 任务执行失败: {e}")
            raise
    
    def run_with_files(self, material_path: str, knowledge_path: str, questions_path: str, 
                      answers_path: str, wrong_point: str, output_path: str) -> Dict[str, Any]:
        """使用文件系统运行"""
        # 读取输入
        with open(material_path, 'r', encoding='utf-8') as f:
            material_text = f.read()
        
        with open(knowledge_path, 'r', encoding='utf-8') as f:
            knowledge_data = json.load(f)
            knowledge_points = json.dumps(knowledge_data.get("knowledge_points", []), ensure_ascii=False)
        
        with open(questions_path, 'r', encoding='utf-8') as f:
            questions_data = json.load(f)
        
        with open(answers_path, 'r', encoding='utf-8') as f:
            answers_data = json.load(f)
        
        # 合并题目和答案
        questions_answers = {
            "questions": questions_data,
            "answers": answers_data
        }
        questions_answers_str = json.dumps(questions_answers, ensure_ascii=False, indent=2)
        
        # 执行
        result = self.run(material_text, knowledge_points, questions_answers_str, wrong_point)
        
        # 保存输出
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        logger.info(f"[{self.name}] 结果已保存到 {output_path}")
        return result
