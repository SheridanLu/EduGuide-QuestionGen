#!/usr/bin/env python3
# test_workflow_mock.py - 模拟测试工作流（无需 API Key）
import json
import os
import sys

# 测试模块导入
def test_imports():
    """测试所有模块是否可以正确导入"""
    print("=" * 60)
    print("测试模块导入...")
    print("=" * 60)
    
    try:
        from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL
        print("✅ config.py 导入成功")
        
        from services.deepseek_client import DeepSeekClient
        print("✅ deepseek_client.py 导入成功")
        
        from agents.knowledge_agent import KnowledgeAgent
        print("✅ knowledge_agent.py 导入成功")
        
        from agents.question_agent import QuestionAgent
        print("✅ question_agent.py 导入成功")
        
        from agents.answer_agent import AnswerAgent
        print("✅ answer_agent.py 导入成功")
        
        from agents.remedial_agent import RemedialAgent
        print("✅ remedial_agent.py 导入成功")
        
        from workflow.openclaw_flow import OpenClawFlow
        print("✅ openclaw_flow.py 导入成功")
        
        from utils.logger import get_logger
        print("✅ logger.py 导入成功")
        
        from utils.formatters import clean_json_response
        print("✅ formatters.py 导入成功")
        
        print("\n✅ 所有模块导入成功！\n")
        return True
    except Exception as e:
        print(f"\n❌ 模块导入失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


# 测试 Prompt 模板
def test_prompts():
    """测试 Prompt 模板"""
    print("=" * 60)
    print("测试 Prompt 模板...")
    print("=" * 60)
    
    try:
        from prompts.knowledge_prompt import build_knowledge_prompt
        from prompts.question_prompt import build_question_prompt
        from prompts.answer_prompt import build_answer_prompt
        from prompts.remedial_prompt import build_remedial_prompt
        
        # 测试知识点提取 prompt
        system_prompt, user_prompt = build_knowledge_prompt("测试教材")
        assert len(system_prompt) > 0
        assert len(user_prompt) > 0
        print("✅ knowledge_prompt 测试通过")
        
        # 测试分层出题 prompt
        system_prompt, user_prompt = build_question_prompt("测试教材", "知识点1\n知识点2")
        assert len(system_prompt) > 0
        assert len(user_prompt) > 0
        print("✅ question_prompt 测试通过")
        
        # 测试答案解析 prompt
        system_prompt, user_prompt = build_answer_prompt("知识点", "题目")
        assert len(system_prompt) > 0
        assert len(user_prompt) > 0
        print("✅ answer_prompt 测试通过")
        
        # 测试补救题 prompt
        system_prompt, user_prompt = build_remedial_prompt("教材", "知识点", "题目答案", "错误点")
        assert len(system_prompt) > 0
        assert len(user_prompt) > 0
        print("✅ remedial_prompt 测试通过")
        
        print("\n✅ 所有 Prompt 模板测试通过！\n")
        return True
    except Exception as e:
        print(f"\n❌ Prompt 模板测试失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


# 测试 Agent 初始化
def test_agents():
    """测试 Agent 初始化"""
    print("=" * 60)
    print("测试 Agent 初始化...")
    print("=" * 60)
    
    try:
        from agents.knowledge_agent import KnowledgeAgent
        from agents.question_agent import QuestionAgent
        from agents.answer_agent import AnswerAgent
        from agents.remedial_agent import RemedialAgent
        
        knowledge_agent = KnowledgeAgent()
        print(f"✅ {knowledge_agent.name} 初始化成功")
        
        question_agent = QuestionAgent()
        print(f"✅ {question_agent.name} 初始化成功")
        
        answer_agent = AnswerAgent()
        print(f"✅ {answer_agent.name} 初始化成功")
        
        remedial_agent = RemedialAgent()
        print(f"✅ {remedial_agent.name} 初始化成功")
        
        print("\n✅ 所有 Agent 初始化成功！\n")
        return True
    except Exception as e:
        print(f"\n❌ Agent 初始化失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


# 测试工作流初始化
def test_workflow():
    """测试工作流初始化"""
    print("=" * 60)
    print("测试工作流初始化...")
    print("=" * 60)
    
    try:
        from workflow.openclaw_flow import OpenClawFlow
        
        flow = OpenClawFlow()
        print("✅ OpenClawFlow 初始化成功")
        
        # 检查输出目录
        assert os.path.exists(flow.output_dir)
        print(f"✅ 输出目录创建成功: {flow.output_dir}")
        
        # 检查 Agent 是否正确初始化
        assert flow.knowledge_agent is not None
        assert flow.question_agent is not None
        assert flow.answer_agent is not None
        assert flow.remedial_agent is not None
        print("✅ 所有 Agent 已正确关联")
        
        print("\n✅ 工作流初始化成功！\n")
        return True
    except Exception as e:
        print(f"\n❌ 工作流初始化失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


# 测试 JSON 处理
def test_json_processing():
    """测试 JSON 处理"""
    print("=" * 60)
    print("测试 JSON 处理...")
    print("=" * 60)
    
    try:
        from utils.formatters import clean_json_response
        
        # 测试正常的 JSON 响应
        test_response = {
            "choices": [{
                "message": {
                    "content": '{"knowledge_points": ["点1", "点2"]}'
                }
            }]
        }
        result = clean_json_response(test_response)
        assert "knowledge_points" in result
        print("✅ 正常 JSON 解析测试通过")
        
        # 测试带 markdown 的 JSON 响应
        test_response = {
            "choices": [{
                "message": {
                    "content": '```json\n{"knowledge_points": ["点1", "点2"]}\n```'
                }
            }]
        }
        result = clean_json_response(test_response)
        print("✅ Markdown JSON 解析测试通过")
        
        print("\n✅ JSON 处理测试通过！\n")
        return True
    except Exception as e:
        print(f"\n❌ JSON 处理测试失败: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("  EduGuide-QuestionGen 测试套件")
    print("=" * 60 + "\n")
    
    tests = [
        ("模块导入", test_imports),
        ("Prompt 模板", test_prompts),
        ("Agent 初始化", test_agents),
        ("工作流初始化", test_workflow),
        ("JSON 处理", test_json_processing),
    ]
    
    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))
    
    # 显示总结
    print("\n" + "=" * 60)
    print("  测试总结")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, result in results if result)
    failed = total - passed
    
    print(f"\n总计: {total} | 通过: {passed} | 失败: {failed}")
    
    if failed == 0:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print(f"\n⚠️  {failed} 个测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
