# workflow/openclaw_flow.py - OpenClaw 工作流
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from agents.knowledge_agent import KnowledgeAgent
from agents.question_agent import QuestionAgent
from agents.answer_agent import AnswerAgent
from agents.remedial_agent import RemedialAgent
from utils.logger import get_logger

logger = get_logger(__name__)

class OpenClawFlow:
    """OpenClaw 工作流"""
    
    def __init__(self):
        self.knowledge_agent = KnowledgeAgent()
        self.question_agent = QuestionAgent()
        self.answer_agent = AnswerAgent()
        self.remedial_agent = RemedialAgent()
        self.output_dir = "output"
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.workflow_data = {
            "project": "EduGuide-QuestionGen",
            "created_at": datetime.now().isoformat(),
            "status": "initialized",
            "steps": []
        }
        
        logger.info("OpenClaw 工作流初始化完成")
    
    def run(self, material_text: str, wrong_point: Optional[str] = None) -> Dict[str, Any]:
        """运行完整工作流"""
        logger.info("=" * 50)
        logger.info("开始执行 OpenClaw 工作流")
        logger.info("=" * 50)
        
        # 保存教材文本
        material_path = os.path.join(self.output_dir, "material.txt")
        with open(material_path, 'w', encoding='utf-8') as f:
            f.write(material_text)
        
        try:
            # Step 1: 知识点提取
            logger.info("Step 1: 知识点提取...")
            knowledge_path = os.path.join(self.output_dir, "knowledge.json")
            knowledge_result = self.knowledge_agent.run_with_file(
                input_path=material_path,
                output_path=knowledge_path
            )
            self.workflow_data["steps"].append({
                "step": "knowledge_extraction",
                "status": "completed",
                "completed_at": datetime.now().isoformat()
            })
            
            # Step 2: 分层出题
            logger.info("Step 2: 分层出题...")
            questions_path = os.path.join(self.output_dir, "questions.json")
            questions_result = self.question_agent.run_with_files(
                material_path=material_path,
                knowledge_path=knowledge_path,
                output_path=questions_path
            )
            self.workflow_data["steps"].append({
                "step": "question_generation",
                "status": "completed",
                "completed_at": datetime.now().isoformat()
            })
            
            # Step 3: 答案解析
            logger.info("Step 3: 答案解析...")
            answers_path = os.path.join(self.output_dir, "answers.json")
            answers_result = self.answer_agent.run_with_files(
                material_path=material_path,
                knowledge_path=knowledge_path,
                questions_path=questions_path,
                output_path=answers_path
            )
            self.workflow_data["steps"].append({
                "step": "answer_generation",
                "status": "completed",
                "completed_at": datetime.now().isoformat()
            })
            
            # Step 4: 补救题生成（条件执行）
            if wrong_point:
                logger.info(f"Step 4: 补救题生成 (错误点: {wrong_point})...")
                remedial_path = os.path.join(self.output_dir, "remedial.json")
                remedial_result = self.remedial_agent.run_with_files(
                    material_path=material_path,
                    knowledge_path=knowledge_path,
                    questions_path=questions_path,
                    answers_path=answers_path,
                    wrong_point=wrong_point,
                    output_path=remedial_path
                )
                self.workflow_data["steps"].append({
                    "step": "remedial_generation",
                    "status": "completed",
                    "completed_at": datetime.now().isoformat()
                })
            else:
                logger.info("跳过补救题生成步骤")
            
            # 完成工作流
            self.workflow_data["status"] = "completed"
            self.workflow_data["completed_at"] = datetime.now().isoformat()
            
            logger.info("=" * 50)
            logger.info("工作流执行完成！")
            logger.info("=" * 50)
            
        except Exception as e:
            logger.error(f"工作流执行失败: {e}")
            self.workflow_data["status"] = "failed"
            self.workflow_data["error"] = str(e)
            raise
        
        return self.workflow_data
    
    def get_final_results(self) -> Dict[str, Any]:
        """获取最终结果"""
        result = {
            "knowledge": None,
            "questions": None,
            "answers": None,
            "remedial": None
        }
        
        files = {
            "knowledge": os.path.join(self.output_dir, "knowledge.json"),
            "questions": os.path.join(self.output_dir, "questions.json"),
            "answers": os.path.join(self.output_dir, "answers.json"),
            "remedial": os.path.join(self.output_dir, "remedial.json")
        }
        
        for key, path in files.items():
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        result[key] = json.load(f)
                except:
                    pass
        
        return result
