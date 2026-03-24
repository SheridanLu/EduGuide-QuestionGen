#!/bin/bash

# ============================================================
# EduGuide-QuestionGen GLM Agent 循环运行脚本
# 用法: ./run_glm.sh <循环次数>
# 示例: ./run_glm.sh 10  # 运行10次开发流程
# ============================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# 日志函数
log_info() { echo -e "${BLUE}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"; }
log_warning() { echo -e "${YELLOW}[⚠]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"; }
log_error() { echo -e "${RED}[✗]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"; }
log_section() {
    echo ""
    echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════${NC}"
}

# 显示帮助
show_usage() {
    cat << EOF
用法: $0 <循环次数> [选项]

参数:
  循环次数    Agent 执行的次数 (1-100)

选项:
  --dry-run       只生成提示词，不实际运行
  --no-delay      运行之间不等待
  --help          显示帮助

示例:
  $0 1              # 运行 1 次
  $0 10             # 运行 10 次
  $0 5 --dry-run    # 模拟运行 5 次

EOF
    exit 0
}

# 检查参数
if [ -z "$1" ]; then
    log_error "缺少参数：循环次数"
    echo "用法: $0 <循环次数>"
    echo "示例: $0 10  # 运行10次开发流程"
    exit 1
fi

# 解析参数
ITERATIONS=0
DRY_RUN=false
NO_DELAY=false

while [ $# -gt 0 ]; do
    case "$1" in
        --help|-h) show_usage ;;
        --dry-run) DRY_RUN=true; shift ;;
        --no-delay) NO_DELAY=true; shift ;;
        [0-9]*) ITERATIONS=$1; shift ;;
        *) log_error "未知选项: $1"; show_usage ;;
    esac
done

# 验证参数是数字
if ! [[ "$ITERATIONS" =~ ^[0-9]+$ ]] || [ "$ITERATIONS" -lt 1 ]; then
    log_error "参数必须是大于0的数字: $ITERATIONS"
    exit 1
fi

# 工作目录
WORK_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$WORK_DIR"

# 显示启动信息
echo ""
echo -e "${BOLD}╔════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║   EduGuide-QuestionGen GLM Agent Runner   ║${NC}"
echo -e "${BOLD}╚════════════════════════════════════════════╝${NC}"
echo ""

log_info "工作目录: $WORK_DIR"
log_info "计划运行次数: ${BOLD}$ITERATIONS${NC}"
log_info "Dry Run 模式: $DRY_RUN"
log_info "开始时间: $(date '+%Y-%m-%d %H:%M:%S')"

# 检查必要文件
if [ ! -f "task.json" ]; then
    log_error "task.json 不存在！"
    exit 1
fi

if [ ! -f "CLAUDE.md" ]; then
    log_error "CLAUDE.md 不存在！"
    exit 1
fi

# 创建日志目录
LOG_DIR="$WORK_DIR/logs"
mkdir -p "$LOG_DIR"

# 获取任务统计
get_task_stats() {
    python3 << 'PYEOF'
import json
try:
    with open('task.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    tasks = data.get('tasks', [])
    total = len(tasks)
    completed = sum(1 for t in tasks if t.get('status') == 'completed')
    pending = sum(1 for t in tasks if t.get('status') == 'pending')
    in_progress = sum(1 for t in tasks if t.get('status') == 'in_progress')
    blocked = sum(1 for t in tasks if t.get('status') == 'blocked')
    print(f"📊 总计: {total} | ✅ 完成: {completed} | 🔄 进行中: {in_progress} | ⏳ 待处理: {pending} | 🚫 阻塞: {blocked}")
except Exception as e:
    print(f"读取任务失败: {e}")
PYEOF
}

# 获取下一个待处理任务
get_next_task() {
    python3 << 'PYEOF'
import json
try:
    with open('task.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    tasks = data.get('tasks', [])
    pending = [t for t in tasks if t.get('status') == 'pending']
    if pending:
        # 按优先级排序
        pending.sort(key=lambda x: x.get('priority', 999))
        task = pending[0]
        print(f"{task['id']}|{task['title']}|{task['category']}")
    else:
        print("NO_TASKS")
except Exception as e:
    print(f"ERROR:{e}")
PYEOF
}

# 更新任务状态为进行中
mark_task_in_progress() {
    local task_id=$1
    python3 << PYEOF
import json
from datetime import datetime
try:
    with open('task.json', 'r+', encoding='utf-8') as f:
        data = json.load(f)
        for task in data['tasks']:
            if task['id'] == '$task_id':
                task['status'] = 'in_progress'
                task['started_at'] = datetime.now().isoformat()
                break
        # 更新统计
        total = len(data['tasks'])
        completed = sum(1 for t in data['tasks'] if t.get('status') == 'completed')
        pending = sum(1 for t in data['tasks'] if t.get('status') == 'pending')
        in_progress = sum(1 for t in data['tasks'] if t.get('status') == 'in_progress')
        blocked = sum(1 for t in data['tasks'] if t.get('status') == 'blocked')
        data['statistics'] = {
            'total': total,
            'pending': pending,
            'in_progress': in_progress,
            'completed': completed,
            'blocked': blocked
        }
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()
    print("任务 $task_id 已标记为进行中")
except Exception as e:
    print(f"更新失败: {e}")
PYEOF
}

# 显示初始状态
log_section "初始任务状态"
log_info "$(get_task_stats)"

# 统计变量
SUCCESS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0

# 主循环
for i in $(seq 1 $ITERATIONS); do
    log_section "第 ${BOLD}${i}/${ITERATIONS}${NC} 次迭代"
    
    # 获取下一个任务
    TASK_INFO=$(get_next_task)
    
    if [[ "$TASK_INFO" == "NO_TASKS" ]] || [[ "$TASK_INFO" == ERROR:* ]]; then
        log_success "🎉 没有待处理任务了！"
        SKIP_COUNT=$((SKIP_COUNT + 1))
        break
    fi
    
    TASK_ID=$(echo "$TASK_INFO" | cut -d'|' -f1)
    TASK_TITLE=$(echo "$TASK_INFO" | cut -d'|' -f2)
    TASK_CATEGORY=$(echo "$TASK_INFO" | cut -d'|' -f3)
    
    log_info "📋 领取任务: ${BOLD}$TASK_ID${NC} - $TASK_TITLE"
    log_info "📂 分类: $TASK_CATEGORY"
    
    # 生成日志文件名
    LOG_FILE="$LOG_DIR/iteration_${i}_${TASK_ID}_$(date '+%Y%m%d_%H%M%S').log"
    log_info "📝 日志文件: $LOG_FILE"
    
    if [ "$DRY_RUN" = "true" ]; then
        log_warning "[DRY-RUN] 模拟运行，不实际执行"
        
        # 生成提示词
        cat << PROMPT_EOF
════════════════════════════════════════════════════════════
请将以下内容发送给 GLM Agent 执行：
════════════════════════════════════════════════════════════

你是 EduGuide-QuestionGen 项目的开发 Agent。

请严格按照 CLAUDE.md 中的工作流程执行任务 $TASK_ID: $TASK_TITLE

工作步骤：
1. 读取 CLAUDE.md 了解工作规范
2. 读取 task.json 找到任务 $TASK_ID 的详细信息
3. 读取 progress.txt 了解项目进展
4. 按照任务的 steps 逐步实现
5. 测试验证
6. 更新 progress.txt 记录工作内容
7. 更新 task.json 标记任务完成
8. Git 提交代码

注意：
- 一次只处理一个任务
- 遇到困难及时在 progress.txt 中记录并标记任务为 blocked
- 完成后更新任务状态为 completed

请开始工作！

════════════════════════════════════════════════════════════
PROMPT_EOF
        
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        continue
    fi
    
    # 标记任务为进行中
    mark_task_in_progress "$TASK_ID"
    
    # 记录开始时间
    START_TIME=$(date +%s)
    
    log_info "🚀 开始调用 GLM Agent..."
    
    # 构建提示词
    PROMPT="你是 EduGuide-QuestionGen 项目的开发 Agent。

请严格按照 CLAUDE.md 中的工作流程执行任务 $TASK_ID: $TASK_TITLE

工作步骤：
1. 读取 CLAUDE.md 了解工作规范
2. 读取 task.json 找到任务 $TASK_ID 的详细信息
3. 读取 progress.txt 了解项目进展
4. 按照任务的 steps 逐步实现
5. 测试验证
6. 更新 progress.txt 记录工作内容
7. 更新 task.json 标记任务完成
8. Git 提交代码

注意：
- 一次只处理一个任务
- 遇到困难及时在 progress.txt 中记录并标记任务为 blocked
- 完成后更新任务状态为 completed

请开始工作！"

    # 调用 GLM（通过 openclaw）
    if command -v openclaw &> /dev/null; then
        log_info "使用 openclaw 命令调用..."
        echo "$PROMPT" | openclaw chat --model glm-5 2>&1 | tee "$LOG_FILE"
        EXIT_CODE=${PIPESTATUS[1]}
    else
        log_error "未找到 openclaw 命令"
        log_info "请确保已安装并配置好 OpenClaw CLI"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        continue
    fi
    
    # 记录结束时间
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    
    # 检查执行结果
    if [ $EXIT_CODE -eq 0 ]; then
        log_success "第 $i 次迭代完成！耗时: ${DURATION}秒"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    else
        log_error "第 $i 次迭代失败！退出码: $EXIT_CODE, 耗时: ${DURATION}秒"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
    
    # 显示当前状态
    log_info "当前状态: $(get_task_stats)"
    
    # 显示 Git 状态
    if [ -d ".git" ]; then
        log_info "Git 状态:"
        git status --short 2>/dev/null || log_warning "无法获取 Git 状态"
    fi
    
    # 如果不是最后一次，等待一段时间
    if [ "$NO_DELAY" = "false" ] && [ $i -lt $ITERATIONS ]; then
        WAIT_TIME=3
        log_info "等待 ${WAIT_TIME} 秒后继续..."
        sleep $WAIT_TIME
    fi
done

# 最终报告
log_section "执行完成报告"
log_info "总迭代次数: $ITERATIONS"
log_success "成功次数: $SUCCESS_COUNT"
log_error "失败次数: $FAIL_COUNT"
log_warning "跳过次数: $SKIP_COUNT"
log_info "结束时间: $(date '+%Y-%m-%d %H:%M:%S')"

# 最终任务统计
log_section "最终任务状态"
log_info "$(get_task_stats)"

log_section "脚本结束"

# 返回退出码
if [ $FAIL_COUNT -gt 0 ]; then
    exit 1
else
    exit 0
fi
