#!/bin/bash

# ============================================================
# EduGuide-QuestionGen 项目初始化脚本
# ============================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# 日志函数
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[⚠]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }
log_step() { echo -e "${CYAN}→${NC} $1"; }

# 显示标题
echo ""
echo -e "${BOLD}╔════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║   EduGuide-QuestionGen 项目初始化         ║${NC}"
echo -e "${BOLD}╚════════════════════════════════════════════╝${NC}"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

log_info "工作目录: $SCRIPT_DIR"
echo ""

# 检查 Python
log_step "检查 Python..."
if ! command -v python3 &> /dev/null; then
    log_error "未安装 Python3，请先安装 Python 3.8+"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
log_success "Python 版本: $PYTHON_VERSION"

# 检查 pip
log_step "检查 pip..."
if ! command -v pip3 &> /dev/null; then
    log_error "未安装 pip3"
    exit 1
fi
PIP_VERSION=$(pip3 --version)
log_success "pip 版本: $PIP_VERSION"

echo ""
log_info "开始创建项目结构..."
echo ""

# 创建目录结构
log_step "创建目录结构..."
mkdir -p agents services workflow prompts utils output

log_success "目录结构创建完成"

# 检查 .env 文件
if [ ! -f ".env" ]; then
    log_warning ".env 文件不存在，从模板创建..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        log_success "已创建 .env 文件，请修改其中的 API Key"
    else
        log_warning ".env.example 也不存在，请手动创建 .env"
    fi
else
    log_success ".env 文件已存在"
fi

# 安装依赖
log_step "安装 Python 依赖..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    log_success "依赖安装完成"
else
    log_warning "requirements.txt 不存在，跳过依赖安装"
fi

# 初始化 Git（如果尚未初始化）
if [ ! -d ".git" ]; then
    log_step "初始化 Git 仓库..."
    git init
    log_success "Git 仓库初始化完成"
fi

# 创建 .gitignore（如果不存在）
if [ ! -f ".gitignore" ]; then
    log_step "创建 .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/

# 环境变量
.env

# 输出文件
output/*.json

# 日志
logs/
*.log

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# 操作系统
.DS_Store
Thumbs.db

# 临时文件
tmp/
temp/
*.tmp
EOF
    log_success ".gitignore 创建完成"
fi

# 更新 progress.txt
log_step "更新进度日志..."
if [ -f "progress.txt" ]; then
    cat >> progress.txt << EOF

---

### $(date '+%Y-%m-%d %H:%M:%S') - 项目初始化
- **任务**: 运行 init.sh 脚本
- **状态**: ✅ 完成
- **执行者**: init.sh
- **操作**:
  - 检查 Python 环境
  - 创建目录结构
  - 安装依赖
  - 初始化 Git 仓库
- **下一步**: 领取 T001 任务开始开发
EOF
    log_success "进度日志已更新"
fi

echo ""
log_success "================================"
log_success "  项目初始化完成！"
log_success "================================"
echo ""
log_info "下一步："
echo "  1. 配置 .env 文件中的 DEEPSEEK_API_KEY"
echo "  2. 领取 T001 任务开始开发"
echo "  3. 运行 ./run_glm.sh <次数> 启动自动化开发流程"
echo ""
