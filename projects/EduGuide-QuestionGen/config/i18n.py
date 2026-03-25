# config/i18n.py - 多语言支持
from typing import Dict, Any

# 语言定义
LANGUAGES = {
    "en": "English",
    "zh-CN": "简体中文",
    "zh-TW": "繁體中文"
}

# 翻译文本
TRANSLATIONS = {
    "en": {
        # 标题和导航
        "app_title": "EduGuide",
        "app_subtitle": "Smart Question Generation System · Socratic Guidance",
        "nav_home": "🏠 Home",
        "nav_settings": "⚙️ API Settings",
        "nav_practice": "🎯 Practice",
        
        # 主页
        "input_material": "📖 Input Material",
        "upload_file": "📁 Upload Material File",
        "upload_hint": "Supports .txt, .pdf, .docx, .pptx",
        "or_direct_input": "Or input text directly:",
        "text_placeholder": "Paste or enter material content here...",
        "settings": "⚙️ Settings",
        "simulate_error": "Simulate Student Error (Optional)",
        "error_placeholder": "e.g., confused stemming with lemmatization",
        "current_api": "Current API",
        "generate_button": "🚀 Start Generation",
        
        # 统计
        "word_count": "Word Count",
        "configured": "Configured",
        "not_configured": "Not Configured",
        
        # 结果标签
        "tab_knowledge": "💡 Knowledge",
        "tab_questions": "📝 Questions",
        "tab_guidance": "📚 Guidance",
        "tab_remedial": "🤝 Remedial",
        
        # 知识点
        "extracted_points": "Extracted {} knowledge points",
        
        # 题目
        "basic_questions": "🟢 Basic",
        "intermediate_questions": "🟡 Intermediate",
        "advanced_questions": "🔴 Advanced",
        
        # 引导
        "guidance_info": "💡 Click on a question to expand guidance steps",
        "step": "Step",
        "view_hints": "💡 View Hints",
        "hint": "Hint",
        "key_points": "🔑 Key Points",
        "common_mistakes": "⚠️ Common Mistakes",
        
        # 补救
        "remedial_info": "💡 When you have a misunderstanding, here you'll find Socratic guidance",
        "remedial_guidance": "Remedial Guidance",
        "probing_questions": "🤔 Let's Think Together",
        "think_first": "*Please think first, then continue*",
        "need_analogy": "🎭 Need an analogy?",
        "analogy": "Analogy",
        "try_practice": "📝 Try This Simplified Practice",
        "practice_question": "Question",
        "need_guidance": "💡 Need guidance steps?",
        "verify_understanding": "✅ Verify Your Understanding",
        "verification_question": "Verification Question",
        "extension_hint": "Extension Thought",
        
        # 设置页面
        "api_settings": "API Settings",
        "settings_subtitle": "Configure and manage API providers",
        "select_provider": "📡 Select API Provider",
        "configure": "🔑 Configure {}",
        "api_key": "API Key",
        "base_url": "API Base URL",
        "select_model": "Select Model",
        "save_config": "💾 Save Configuration",
        "test_connection": "🧪 Test Connection",
        "config_saved": "✅ Configuration saved!",
        "connection_success": "✅ Connection successful!",
        "connection_failed": "❌ Connection failed: {}",
        "enter_api_key": "❌ Please enter API Key first",
        "testing": "Testing...",
        
        # 提供商状态
        "all_providers": "📊 All Providers Status",
        "configured_status": "Configured",
        "not_configured_status": "Not Configured",
        "available_models": "Available Models",
        
        # 消息
        "material_required": "❌ Please input material content",
        "generating": "Generating, please wait...",
        "generation_complete": "✅ Generation complete!",
        "generation_failed": "❌ Generation failed: {}",
        "configure_api_first": "⚠️ Please configure API Key first",
        "steps": "Step 1: Return to Home | Step 2: Upload file or input text | Step 3: Click 'Start Generation' | Step 4: Return here after generation",
        "no_questions": "⚠️ No question data available. Please generate questions first.",
        
        # 文件上传
        "file_read_success": "✅ File read: {}",
        "unsupported_format": "❌ Unsupported file format: {}",
        "file_read_failed": "❌ Failed to read file: {}",
        "slide": "Slide",
        
        # 侧边栏
        "sidebar_title": "🎓 EduGuide",
        "current_api_label": "**Current API**",
        
        # 交互式练习
        "practice_title": "🎯 Interactive Practice",
        "practice_subtitle": "**Step-by-step guidance to find answers yourself**",
        "total_questions": "Total Questions",
        "completed": "Completed",
        "completion_rate": "Completion Rate",
        "your_answer": "Your Answer",
        "answer_placeholder": "Write your thoughts or answer here...",
        "submit_answer": "✅ Submit Answer",
        "need_hint": "💡 Need a Hint?",
        "view_key_points": "🔑 View Key Points",
        "complete_question": "✅ Complete This Question",
        "all_steps_complete": "🎉 Great! You've completed all steps!",
        "your_answers": "📝 Your Answer Review",
        "answer_too_short": "⚠️ Answer is too short, can you elaborate?",
        "please_enter_answer": "❌ Please enter your answer first",
    },
    
    "zh-CN": {
        # 标题和导航
        "app_title": "EduGuide",
        "app_subtitle": "智能出题系统 · 苏格拉底式引导教学",
        "nav_home": "🏠 主页",
        "nav_settings": "⚙️ API 设置",
        "nav_practice": "🎯 解题练习",
        
        # 主页
        "input_material": "📖 输入教材内容",
        "upload_file": "📁 上传教材文件",
        "upload_hint": "支持 .txt, .pdf, .docx, .pptx",
        "or_direct_input": "或直接输入文本：",
        "text_placeholder": "在此粘贴或输入教材内容...",
        "settings": "⚙️ 设置",
        "simulate_error": "模拟学生错误（可选）",
        "error_placeholder": "例如：混淆了词干提取和词形还原",
        "current_api": "当前 API",
        "generate_button": "🚀 开始生成",
        
        # 统计
        "word_count": "字数",
        "configured": "已配置",
        "not_configured": "未配置",
        
        # 结果标签
        "tab_knowledge": "💡 知识点",
        "tab_questions": "📝 题目",
        "tab_guidance": "📚 引导",
        "tab_remedial": "🤝 补救",
        
        # 知识点
        "extracted_points": "提取了 {} 个知识点",
        
        # 题目
        "basic_questions": "🟢 基础题",
        "intermediate_questions": "🟡 中级题",
        "advanced_questions": "🔴 高级题",
        
        # 引导
        "guidance_info": "💡 点击题目展开引导步骤",
        "step": "步骤",
        "view_hints": "💡 查看提示",
        "hint": "提示",
        "key_points": "🔑 关键点",
        "common_mistakes": "⚠️ 常见错误",
        
        # 补救
        "remedial_info": "💡 当你理解有偏差时，这里会提供苏格拉底式的引导",
        "remedial_guidance": "补救引导",
        "probing_questions": "🤔 让我们一起思考",
        "think_first": "*请先自己思考，再继续*",
        "need_analogy": "🎭 需要一个类比吗？",
        "analogy": "类比",
        "try_practice": "📝 试试这个简化练习",
        "practice_question": "题目",
        "need_guidance": "💡 需要引导步骤吗？",
        "verify_understanding": "✅ 验证你的理解",
        "verification_question": "验证问题",
        "extension_hint": "延伸思考",
        
        # 设置页面
        "api_settings": "API 设置",
        "settings_subtitle": "配置和管理 API 提供商",
        "select_provider": "📡 选择 API 提供商",
        "configure": "🔑 配置 {}",
        "api_key": "API Key",
        "base_url": "API Base URL",
        "select_model": "选择模型",
        "save_config": "💾 保存配置",
        "test_connection": "🧪 测试连接",
        "config_saved": "✅ 配置已保存！",
        "connection_success": "✅ 连接成功！",
        "connection_failed": "❌ 连接失败: {}",
        "enter_api_key": "❌ 请先输入 API Key",
        "testing": "测试中...",
        
        # 提供商状态
        "all_providers": "📊 所有提供商状态",
        "configured_status": "已配置",
        "not_configured_status": "未配置",
        "available_models": "可用模型",
        
        # 消息
        "material_required": "❌ 请输入教材内容",
        "generating": "正在生成中，请稍候...",
        "generation_complete": "✅ 生成完成！",
        "generation_failed": "❌ 生成失败: {}",
        "configure_api_first": "⚠️ 请先配置 API Key",
        "steps": "**步骤：** 1. 返回主页 | 2. 上传文件或输入文本 | 3. 点击'开始生成' | 4. 生成完成后返回此页面",
        "no_questions": "⚠️ 暂无题目数据。请先在主页生成题目。",
        
        # 文件上传
        "file_read_success": "✅ 已读取: {}",
        "unsupported_format": "❌ 不支持的文件格式: {}",
        "file_read_failed": "❌ 读取文件失败: {}",
        "slide": "幻灯片",
        
        # 侧边栏
        "sidebar_title": "🎓 EduGuide",
        "current_api_label": "**当前 API**",
        
        # 交互式练习
        "practice_title": "🎯 交互式解题练习",
        "practice_subtitle": "**一步步引导，自己得出答案**",
        "total_questions": "总题目数",
        "completed": "已完成",
        "completion_rate": "完成率",
        "your_answer": "你的答案",
        "answer_placeholder": "在这里输入你的思考过程或答案...",
        "submit_answer": "✅ 提交答案",
        "need_hint": "💡 需要提示吗？",
        "view_key_points": "🔑 查看关键点",
        "complete_question": "✅ 完成此题",
        "all_steps_complete": "🎉 太棒了！你已经完成了所有步骤！",
        "your_answers": "📝 你的答案回顾",
        "answer_too_short": "⚠️ 答案太简短了，能再详细一点吗？",
        "please_enter_answer": "❌ 请先输入你的答案",
    },
    
    "zh-TW": {
        # 標題和導航
        "app_title": "EduGuide",
        "app_subtitle": "智慧出題系統 · 蘇格拉底式引導教學",
        "nav_home": "🏠 首頁",
        "nav_settings": "⚙️ API 設定",
        "nav_practice": "🎯 解題練習",
        
        # 主頁
        "input_material": "📖 輸入教材內容",
        "upload_file": "📁 上傳教材檔案",
        "upload_hint": "支援 .txt, .pdf, .docx, .pptx",
        "or_direct_input": "或直接輸入文字：",
        "text_placeholder": "在此貼上或輸入教材內容...",
        "settings": "⚙️ 設定",
        "simulate_error": "模擬學生錯誤（可選）",
        "error_placeholder": "例如：混淆了詞幹提取和詞形還原",
        "current_api": "當前 API",
        "generate_button": "🚀 開始生成",
        
        # 統計
        "word_count": "字數",
        "configured": "已配置",
        "not_configured": "未配置",
        
        # 結果標籤
        "tab_knowledge": "💡 知識點",
        "tab_questions": "📝 題目",
        "tab_guidance": "📚 引導",
        "tab_remedial": "🤝 補救",
        
        # 知識點
        "extracted_points": "提取了 {} 個知識點",
        
        # 題目
        "basic_questions": "🟢 基礎題",
        "intermediate_questions": "🟡 中級題",
        "advanced_questions": "🔴 高級題",
        
        # 引導
        "guidance_info": "💡 點擊題目展開引導步驟",
        "step": "步驟",
        "view_hints": "💡 查看提示",
        "hint": "提示",
        "key_points": "🔑 關鍵點",
        "common_mistakes": "⚠️ 常見錯誤",
        
        # 補救
        "remedial_info": "💡 當你理解有偏差時，這裡會提供蘇格拉底式的引導",
        "remedial_guidance": "補救引導",
        "probing_questions": "🤔 讓我們一起思考",
        "think_first": "*請先自己思考，再繼續*",
        "need_analogy": "🎭 需要一個類比嗎？",
        "analogy": "類比",
        "try_practice": "📝 試試這個簡化練習",
        "practice_question": "題目",
        "need_guidance": "💡 需要引導步驟嗎？",
        "verify_understanding": "✅ 驗證你的理解",
        "verification_question": "驗證問題",
        "extension_hint": "延伸思考",
        
        # 設定頁面
        "api_settings": "API 設定",
        "settings_subtitle": "配置和管理 API 提供商",
        "select_provider": "📡 選擇 API 提供商",
        "configure": "🔑 配置 {}",
        "api_key": "API Key",
        "base_url": "API Base URL",
        "select_model": "選擇模型",
        "save_config": "💾 儲存配置",
        "test_connection": "🧪 測試連線",
        "config_saved": "✅ 配置已儲存！",
        "connection_success": "✅ 連線成功！",
        "connection_failed": "❌ 連線失敗: {}",
        "enter_api_key": "❌ 請先輸入 API Key",
        "testing": "測試中...",
        
        # 提供商狀態
        "all_providers": "📊 所有提供商狀態",
        "configured_status": "已配置",
        "not_configured_status": "未配置",
        "available_models": "可用模型",
        
        # 訊息
        "material_required": "❌ 請輸入教材內容",
        "generating": "正在生成中，請稍候...",
        "generation_complete": "✅ 生成完成！",
        "generation_failed": "❌ 生成失敗: {}",
        "configure_api_first": "⚠️ 請先配置 API Key",
        "steps": "**步驟：** 1. 返回首頁 | 2. 上傳檔案或輸入文字 | 3. 點擊'開始生成' | 4. 生成完成後返回此頁面",
        "no_questions": "⚠️ 暫無題目資料。請先在首頁生成題目。",
        
        # 檔案上傳
        "file_read_success": "✅ 已讀取: {}",
        "unsupported_format": "❌ 不支援的檔案格式: {}",
        "file_read_failed": "❌ 讀取檔案失敗: {}",
        "slide": "投影片",
        
        # 側邊欄
        "sidebar_title": "🎓 EduGuide",
        "current_api_label": "**當前 API**",
        
        # 交互式練習
        "practice_title": "🎯 交互式解題練習",
        "practice_subtitle": "**一步步引導，自己得出答案**",
        "total_questions": "總題目數",
        "completed": "已完成",
        "completion_rate": "完成率",
        "your_answer": "你的答案",
        "answer_placeholder": "在這裡輸入你的思考過程或答案...",
        "submit_answer": "✅ 提交答案",
        "need_hint": "💡 需要提示嗎？",
        "view_key_points": "🔑 查看關鍵點",
        "complete_question": "✅ 完成此題",
        "all_steps_complete": "🎉 太棒了！你已經完成了所有步驟！",
        "your_answers": "📝 你的答案回顧",
        "answer_too_short": "⚠️ 答案太簡短了，能再詳細一點嗎？",
        "please_enter_answer": "❌ 請先輸入你的答案",
    }
}

class I18n:
    """多语言管理器"""
    
    def __init__(self, default_lang: str = "en"):
        self.current_lang = default_lang
    
    def set_language(self, lang: str):
        """设置当前语言"""
        if lang in LANGUAGES:
            self.current_lang = lang
    
    def get(self, key: str, *args) -> str:
        """获取翻译文本"""
        translations = TRANSLATIONS.get(self.current_lang, TRANSLATIONS["en"])
        text = translations.get(key, key)
        
        if args:
            return text.format(*args)
        return text
    
    def t(self, key: str, *args) -> str:
        """get 方法的别名"""
        return self.get(key, *args)
    
    def get_current_language(self) -> str:
        """获取当前语言"""
        return self.current_lang
    
    def get_language_name(self, lang: str = None) -> str:
        """获取语言名称"""
        lang = lang or self.current_lang
        return LANGUAGES.get(lang, lang)
    
    def get_available_languages(self) -> Dict[str, str]:
        """获取所有可用语言"""
        return LANGUAGES.copy()

# 全局实例
_i18n = I18n("en")

def get_i18n() -> I18n:
    """获取多语言管理器实例"""
    return _i18n

def t(key: str, *args) -> str:
    """快捷翻译函数"""
    return _i18n.t(key, *args)
