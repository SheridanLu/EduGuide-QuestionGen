# main.py - 主入口
import json
import os
from workflow.openclaw_flow import OpenClawFlow
from utils.logger import get_logger

logger = get_logger(__name__)

def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("  EduGuide 智能出题系统")
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
    flow = OpenClawFlow()
    
    # 运行工作流
    try:
        result = flow.run(
            material_text=sample_material,
            wrong_point="词干提取和词形还原的区别"  # 可选：模拟错误知识点
        )
        
        # 显示结果
        logger.info("\n" + "=" * 60)
        logger.info("执行结果：")
        logger.info("=" * 60)
        
        final_results = flow.get_final_results()
        
        for key, value in final_results.items():
            if value:
                logger.info(f"\n{key.upper()}:")
                logger.info(json.dumps(value, ensure_ascii=False, indent=2))
        
        logger.info("\n" + "=" * 60)
        logger.info("工作流执行成功！")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"工作流执行失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
