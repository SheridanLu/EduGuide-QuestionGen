#!/usr/bin/env python3
# test_workflow.py - 工作流测试脚本
import json
import os
from workflow.openclaw_flow import OpenClawFlow
from utils.logger import get_logger

logger = get_logger(__name__)

def test_workflow():
    """测试完整工作流"""
    logger.info("=" * 60)
    logger.info("  EduGuide 工作流测试")
    logger.info("=" * 60)
    
    # 测试教材文本
    sample_material = """
自然语言处理（Natural Language Processing, NLP）是人工智能的一个分支领域，
主要研究如何让计算机理解和处理人类语言。

## 1. 词干提取（Stemming）
词干提取是自然语言处理中的一个基础任务。它的目标是将单词还原为其词根形式。
例如：
- running → run
- runs → run
- ran → run

## 2. 词形还原（Lemmatization）
词形还原是将单词还原为其词典中的基础形式（词元）。
与词干提取不同，词形还原会考虑单词的词性和语义。
例如：
- better → good
- running → run（作为动词）

## 3. 两者的区别
- 词干提取：基于规则的粗略截断，速度快但可能不准确
- 词形还原：基于词典和词性分析，更准确但速度较慢
"""
    
    # 初始化工作流
    logger.info("初始化工作流...")
    flow = OpenClawFlow()
    
    # 运行工作流（不生成补救题）
    logger.info("运行工作流...")
    try:
        result = flow.run(
            material_text=sample_material,
            wrong_point=None  # 不生成补救题
        )
        
        logger.info("=" * 60)
        logger.info("工作流执行成功！")
        logger.info("=" * 60)
        
        # 显示结果
        final_results = flow.get_final_results()
        
        if final_results.get("knowledge"):
            logger.info("\n知识点提取结果:")
            logger.info(json.dumps(final_results["knowledge"], ensure_ascii=False, indent=2))
        
        if final_results.get("questions"):
            logger.info("\n题目生成结果:")
            logger.info(json.dumps(final_results["questions"], ensure_ascii=False, indent=2))
        
        if final_results.get("answers"):
            logger.info("\n答案解析结果:")
            logger.info(json.dumps(final_results["answers"], ensure_ascii=False, indent=2))
        
        return True
        
    except Exception as e:
        logger.error(f"工作流执行失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_workflow()
    exit(0 if success else 1)
