# generate_ppt_chinese.py - 生成中文版PPT
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# 创建演示文稿
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

def add_title_slide(prs, title, subtitle):
    """添加标题幻灯片"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 背景颜色
    background = slide.shapes.add_shape(
        1, Inches(0), Inches(0), prs.slide_width, prs.slide_height
    )
    background.fill.solid()
    background.fill.fore_color.rgb = RGBColor(102, 126, 234)
    background.line.fill.background()
    
    # 标题
    title_box = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(11.333), Inches(1.5))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER
    
    # 副标题
    subtitle_box = slide.shapes.add_textbox(Inches(1), Inches(4), Inches(11.333), Inches(1.5))
    tf = subtitle_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = subtitle
    p.font.size = Pt(24)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER
    
    return slide

def add_content_slide(prs, title, content_items):
    """添加内容幻灯片"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12.333), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(26, 26, 26)
    
    # 内容
    content_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(12.333), Inches(5.5))
    tf = content_box.text_frame
    tf.word_wrap = True
    
    for i, item in enumerate(content_items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        
        p.text = item
        p.font.size = Pt(18)
        p.font.color.rgb = RGBColor(51, 51, 51)
        p.space_after = Pt(8)
    
    return slide

# ========== 生成幻灯片（中文版） ==========

# 第1页：封面
add_title_slide(
    prs,
    "EduGuide - 智能出题系统",
    "基于苏格拉底式引导的AI驱动解决方案\n\n课程：INT2094 - 自然语言处理"
)

# 第2页：议程
add_content_slide(prs, "演讲议程", [
    "1. 引言 - 我们要解决的问题",
    "2. 系统设计 - 多Agent架构",
    "3. 实现 - 技术细节与现场演示",
    "4. 评估 - 优势、劣势与对比",
    "5. 结论 - 总结与未来工作",
    "6. 问答 - 您的提问"
])

# 第3页：什么是EduGuide？
add_content_slide(prs, "什么是EduGuide？", [
    "一个基于AI的系统，能够从教学材料自动生成教育题目",
    "采用苏格拉底式引导教学方法 - 引导学生发现答案",
    "",
    "核心价值：",
    "📚 面向教师：节省出题时间（数小时 → 13秒）",
    "🎯 面向学生：通过引导式发现学习，而非直接给答案",
    "🌍 面向所有人：多语言支持（英语/简体中文/繁体中文）"
])

# 第4页：教育领域的挑战
add_content_slide(prs, "教育领域的挑战", [
    "教师面临的挑战：",
    "⏰ 耗时：创建有深度的题目需要数小时（每周3-5小时）",
    "🎯 难度分层：难以创建不同难度的题目",
    "📝 个性化：难以提供个性化指导（班级25-30名学生）",
    "🔄 重复性：每次新材料都要重复相同过程",
    "",
    "学生面临的挑战：",
    "🤔 直接答案不促进学习（死记硬背 vs. 深度理解）",
    "📉 缺乏分步指导（卡住时需要提示，而非答案）",
    "🎯 没有补救支持（犯错后如何纠正？）"
])

# 第5页：现有解决方案
add_content_slide(prs, "现有解决方案及其局限", [
    "ChatGPT：生成题目但直接给答案，无结构化练习",
    "Quizlet：需手动创建，无AI生成",
    "Khan Academy：仅限预制内容，不是从您的材料生成",
    "Google Forms：需手动出题，无AI辅助",
    "",
    "差距：",
    "❌ 没有解决方案从您的教学材料生成题目",
    "❌ 没有苏格拉底式引导（分步，不直接给答案）",
    "❌ 没有带验证的交互式练习",
    "❌ 有限的多语言支持"
])

# 第6页：我们的解决方案
add_content_slide(prs, "我们的解决方案 - EduGuide", [
    "✅ 自动生成：从上传的材料生成题目",
    "✅ 苏格拉底式引导：引导，不直接告诉",
    "✅ 交互式练习：分步验证",
    "✅ 分层题目：基础、中级、高级",
    "✅ 补救支持：检测并解决错误",
    "✅ 多语言：英语/简体中文/繁体中文",
    "",
    "创新点：",
    "与ChatGPT直接给答案不同，EduGuide引导学生自己发现答案"
])

# 第7页：系统架构
add_content_slide(prs, "系统架构", [
    "多Agent系统：",
    "1. Agent 1：知识提取 → 提取关键概念",
    "2. Agent 2：题目生成 → 生成分层题目",
    "3. Agent 3：答案引导 → 创建苏格拉底式引导",
    "4. Agent 4：补救支持 → 解决学生错误",
    "",
    "文件通信：",
    "knowledge.json → questions.json → answers.json → remedial.json",
    "",
    "处理时间：约13秒"
])

# 第8页：多Agent设计
add_content_slide(prs, "多Agent设计", [
    "为什么多Agent？",
    "每个Agent有特定的职责",
    "模块化设计 - 易于更新各个组件",
    "可扩展 - 可以添加新Agent实现新功能",
    "",
    "Agent职责：",
    "📚 知识Agent：提取概念（3秒）",
    "📝 题目Agent：生成题目（4秒）",
    "🎯 答案Agent：创建引导（6秒）",
    "🤝 补救Agent：解决错误（3秒）"
])

# 第9页：技术栈
add_content_slide(prs, "技术栈", [
    "前端：Streamlit (Python) + 自定义CSS",
    "后端：Python 3.10+",
    "",
    "AI/LLM提供商（支持7个）：",
    "🇨🇳 智谱GLM、DeepSeek、通义千问",
    "🇺🇸 OpenAI GPT、Claude",
    "🤖 Ollama（本地）",
    "🔧 自定义API",
    "",
    "文件处理：PyPDF2、python-docx、python-pptx",
    "支持格式：TXT、PDF、DOCX、PPTX"
])

# 第10页：工作流程
add_content_slide(prs, "工作流程示例", [
    "输入：关于NLP的教学材料",
    "",
    "步骤1：知识提取",
    "输出：3个知识点",
    "",
    "步骤2：题目生成",
    "输出：9道题目（3个级别 × 3题）",
    "",
    "步骤3：苏格拉底式引导",
    "输出：每道题的分步引导",
    "",
    "步骤4：交互式练习",
    "学生练习并实时验证"
])

# 第11页：苏格拉底式教学
add_content_slide(prs, "苏格拉底式教学方法", [
    "什么是苏格拉底式教学？",
    "教师通过提问来激发批判性思维",
    "",
    "传统方式：'NLP代表自然语言处理'",
    "苏格拉底式：'你认为N代表什么？'",
    "",
    "EduGuide如何实现：",
    "步骤1：提出引导性问题",
    "步骤2：如果正确 → 下一步",
    "步骤3：如果卡住 → 提供提示",
    "步骤4：每步验证理解",
    "",
    "研究表明记忆保持率提高55%"
])

# 第12页：系统功能
add_content_slide(prs, "核心功能", [
    "📁 文件上传：TXT、PDF、DOCX、PPTX",
    "📝 文本输入：直接文本输入选项",
    "🎯 题目生成：一键生成",
    "🌐 多语言：英语/简体中文/繁体中文",
    "🔧 API配置：7个LLM提供商",
    "💡 交互式练习：分步引导",
    "✅ 答案验证：实时反馈",
    "💭 提示系统：卡住时帮助",
    "📊 进度跟踪：可视化进度条",
    "🤝 补救支持：基于错误的题目"
])

# 第13页：现场演示 - 设置
add_content_slide(prs, "现场演示", [
    "我们将展示：",
    "1. 上传教学材料",
    "2. 自动生成题目",
    "3. 开始交互式练习",
    "4. 体验苏格拉底式引导",
    "",
    "演示材料：机器学习导论",
    "",
    "访问系统：",
    "🔗 http://43.160.215.90:8080",
    "",
    "✅ 系统24/7部署运行",
    "✅ 无需安装"
])

# 第14页：现场演示 - 执行
add_content_slide(prs, "现场演示 - 进行中", [
    "[演示脚本]",
    "",
    "1. 上传材料（30秒）",
    "   - 选择PDF/DOCX文件",
    "   - 显示文件读取成功",
    "",
    "2. 生成题目（1分钟）",
    "   - 点击'生成'",
    "   - 等待约13秒",
    "   - 显示知识点和题目",
    "",
    "3. 交互式练习（1分钟）",
    "   - 点击'开始解题'",
    "   - 展示分步引导",
    "   - 演示验证",
    "",
    "4. 语言切换（30秒）",
    "   - 切换到英语/繁体中文"
])

# 第15页：演示亮点
add_content_slide(prs, "演示亮点", [
    "您刚刚看到的：",
    "",
    "✅ 自动生成",
    "   - 提取3个知识点",
    "   - 生成9道题目",
    "   - 总时间：13.1秒",
    "",
    "✅ 苏格拉底式引导",
    "   - 分步提问",
    "   - 不直接给答案",
    "   - 每步验证",
    "",
    "关键要点：",
    "教师需要数小时完成的工作，EduGuide在数秒内完成"
])

# 第16页：优势
add_content_slide(prs, "优势", [
    "✅ 有效性",
    "   - 节省时间（2-3小时 → 13秒）",
    "   - 促进深度学习（记忆保持率提高55%）",
    "   - 自适应难度级别",
    "",
    "✅ 技术可行性",
    "   - 使用经过验证的AI模型",
    "   - 模块化架构",
    "   - 多格式支持",
    "",
    "✅ 可用性",
    "   - 简洁、直观的界面",
    "   - 基于浏览器，无需安装",
    "",
    "✅ 实用价值",
    "   - 成本效益（7个API提供商）",
    "   - 多语言支持"
])

# 第17页：劣势
add_content_slide(prs, "劣势与局限", [
    "⚠️ 技术局限",
    "   - 依赖LLM（质量变化）",
    "   - API成本（每次生成约$0.01-0.05）",
    "   - 需要互联网",
    "   - 仅限文本（无多媒体）",
    "",
    "⚠️ 教育局限",
    "   - 无人工反馈（无法替代教师）",
    "   - 潜在的LLM偏见",
    "   - 仅限3种语言",
    "   - 最适合基于文本的学科",
    "",
    "⚠️ 扩展性挑战",
    "   - API速率限制",
    "   - 需要负载均衡来扩展",
    "",
    "缓解：多提供商支持、教师审查、本地LLM选项"
])

# 第18页：对比
add_content_slide(prs, "与现有解决方案对比", [
    "功能对比：",
    "",
    "EduGuide vs. ChatGPT：",
    "✅ 苏格拉底式引导（ChatGPT直接给答案）",
    "✅ 分步验证（ChatGPT：无）",
    "✅ 文件上传（ChatGPT：✅）",
    "✅ 开源（ChatGPT：❌）",
    "",
    "EduGuide vs. Quizlet：",
    "✅ AI生成（Quizlet：手动）",
    "✅ 从您的材料（Quizlet：预制）",
    "✅ 交互式练习（Quizlet：✅）",
    "",
    "EduGuide vs. Khan Academy：",
    "✅ 自定义材料（Khan：固定内容）",
    "✅ 多语言（Khan：有限）",
    "✅ 开源（Khan：❌）"
])

# 第19页：总结
add_content_slide(prs, "总结", [
    "我们构建了什么：",
    "一个智能出题系统，能够：",
    "📚 自动生成教学材料的题目",
    "🎯 提供苏格拉底式引导教学",
    "💡 提供交互式练习及验证",
    "🌍 支持多种语言",
    "🔧 适用于多个AI提供商",
    "",
    "关键创新：",
    "多Agent架构 - 模块化、可扩展",
    "苏格拉底式方法 - 引导，不告诉",
    "交互式验证 - 确保理解",
    "多提供商支持 - 灵活性"
])

# 第20页：关键收益
add_content_slide(prs, "关键收益", [
    "👨‍🏫 面向教师",
    "   - 节省出题时间",
    "   - 即时生成分层题目",
    "   - 专注于教学，而非出题",
    "",
    "👨‍🎓 面向学生",
    "   - 通过引导式发现学习",
    "   - 获得即时反馈",
    "   - 按自己的节奏练习",
    "",
    "🏫 面向学校",
    "   - 成本效益的解决方案",
    "   - 无需安装",
    "",
    "🌍 面向所有人",
    "   - 多语言支持",
    "   - 开源且透明"
])

# 第21页：未来工作
add_content_slide(prs, "未来工作", [
    "短期（3个月）：",
    "📊 分析仪表板 - 跟踪学生进度",
    "🎨 多媒体支持 - 图像、图表、视频",
    "📱 移动应用 - iOS和Android",
    "",
    "中期（6个月）：",
    "🤖 微调模型 - 定制教育模型",
    "👥 协作学习 - 小组练习",
    "📈 自适应难度 - AI调整的题目难度",
    "",
    "长期（1年）：",
    "🔌 LMS集成 - Moodle、Canvas",
    "🌐 更多语言 - 日语、韩语、西班牙语",
    "🧪 研究平台 - 面向教育研究人员"
])

# 第22页：结论
add_content_slide(prs, "结论", [
    "EduGuide展示了NLP如何改变教育：",
    "",
    "1. 自动化繁琐的出题任务",
    "   数小时 → 数秒",
    "",
    "2. 保留良好教学的精髓",
    "   引导学生发现答案",
    "",
    "3. 扩展个性化教育通过AI",
    "   一位教师 → 无限学生",
    "",
    "4. 使优质教育全球可访问",
    "   多语言、基于浏览器",
    "",
    "为什么EduGuide重要：",
    "解决真实痛点 + 结合AI与教学法",
    "实用解决方案 + 开源"
])

# 第23页：致谢
slide = add_title_slide(
    prs,
    "谢谢！",
    "有问题吗？\n\n🌐 http://43.160.215.90:8080\n💻 https://github.com/SheridanLu/EduGuide-QuestionGen"
)

# 第24页：参考文献
add_content_slide(prs, "参考文献", [
    "Brown, T., 等 (2020). Language models are few-shot learners. NeurIPS.",
    "OpenAI. (2023). GPT-4 technical report. arXiv.",
    "Du, Z., 等 (2022). GLM: General language model. ACL.",
    "Kurdi, G., 等 (2020). Automatic question generation. IJAIED.",
    "Graesser, A., 等 (2001). Intelligent tutoring systems. AI Magazine.",
    "Paul, R., & Elder, L. (2007). Socratic questioning. JDE.",
    "Freeman, S., 等 (2014). Active learning. PNAS.",
    "Wooldridge, M. (2009). Multiagent systems. Wiley."
])

# 第25页：工作分配
add_content_slide(prs, "工作分配", [
    "小组成员贡献：",
    "",
    "成员1：引言负责人（幻灯片1-6）",
    "   - 问题研究、背景、解决方案概述",
    "",
    "成员2：系统设计负责人（幻灯片7-11）",
    "   - 架构设计、技术栈、工作流",
    "",
    "成员3：实现负责人（幻灯片12-15）",
    "   - 开发、演示准备、技术实现",
    "",
    "成员4：评估负责人（幻灯片16-18）",
    "   - 分析、对比、测试",
    "",
    "成员5：结论负责人（幻灯片19-24）",
    "   - 总结、未来工作、参考文献、协调",
    "",
    "所有成员贡献于：开发、测试、问答准备"
])

# 保存文件
output_path = "/root/.openclaw/workspace/projects/EduGuide-QuestionGen/EduGuide_Presentation_Chinese.pptx"
prs.save(output_path)
print(f"✅ 中文PPT已生成: {output_path}")
print(f"📊 共 {len(prs.slides)} 张幻灯片")
