#!/usr/bin/env bash

set -euo pipefail

REPO="PIGU-PPPgu/harness-skill-v2"
INSTALL_DIR="${HOME}/.local/bin"
SKILL_DIR="${HOME}/.claude/skills"

echo "🚀 安装 Harness Engineering v2..."

# 创建安装目录
mkdir -p "$INSTALL_DIR"
mkdir -p "$SKILL_DIR"

# 下载 harness 可执行文件
echo "📥 下载 harness 可执行文件..."
curl -fsSL "https://raw.githubusercontent.com/${REPO}/main/harness" -o "${INSTALL_DIR}/harness"
chmod +x "${INSTALL_DIR}/harness"

# 下载 SKILL.md
echo "📥 下载 SKILL.md..."
curl -fsSL "https://raw.githubusercontent.com/${REPO}/main/SKILL.md" -o "${SKILL_DIR}/harness.md"

# 检查 PATH
if [[ ":$PATH:" != *":${INSTALL_DIR}:"* ]]; then
    echo ""
    echo "⚠️  请将以下内容添加到你的 shell 配置文件 (~/.bashrc 或 ~/.zshrc):"
    echo ""
    echo "    export PATH=\"\$PATH:${INSTALL_DIR}\""
    echo ""
fi

echo ""
echo "✅ 安装完成!"
echo ""
echo "使用方法:"
echo "  1. 初始化项目: harness init"
echo "  2. 创建 PRD: echo '需求文档' > .harness/prd/feature.md"
echo "  3. 启动智能体: harness swarm start"
echo ""
echo "更多信息: harness help"
