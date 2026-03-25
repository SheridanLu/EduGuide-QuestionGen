#!/bin/bash

# ============================================================
# 配置智谱 GLM API Key 脚本
# ============================================================

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${BOLD}╔════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║   配置智谱 GLM API Key                ║${NC}"
echo -e "${BOLD}╚════════════════════════════════════════════╝${NC}"
echo ""

# 检查 .env 文件是否存在
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️ .env 文件不存在，从模板创建...${NC}"
    cp .env.example .env
fi

# 提示用户输入 API Key
echo -e "${CYAN}请输入你的智谱 GLM API Key:${NC}"
echo -e "${CYAN}(可以从 https://open.bigmodel.cn/ 获取)${NC}"
echo ""
read -p "API Key: " API_KEY

if [ -z "$API_KEY" ]; then
    echo ""
    echo -e "${YELLOW}⚠️ API Key 不能为空${NC}"
    exit 1
fi

# 更新 .env 文件
sed -i "s|your_glm_api_key_here|$API_KEY|g" .env

echo ""
echo -e "${GREEN}✅ API Key 已配置完成！${NC}"
echo ""
echo -e "${CYAN}下一步:${NC}"
echo "  1. 运行测试: python test_workflow_mock.py"
echo "  2. 启动界面: streamlit run streamlit_app.py"
echo ""
