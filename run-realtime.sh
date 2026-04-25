#!/bin/bash
# 启动 RVC 实时变声 GUI

set -fa

# 使用 python3
PYTHON_CMD=python3

# 检查虚拟环境
venv_path=".venv"

if [[ ! -d "${venv_path}" ]]; then
  echo "错误：虚拟环境不存在！"
  echo "请先运行：./run.sh"
  exit 1
fi

echo "激活虚拟环境..."
source "${venv_path}/bin/activate"

# 启动实时变声 GUI
echo "============================================================"
echo "启动 RVC 实时变声 GUI..."
echo "============================================================"
echo ""
echo "📝 使用说明："
echo "1. 选择模型文件 (.pth)"
echo "2. 选择索引文件 (.index)"
echo "3. 选择输入/输出设备"
echo "4. 调整变声参数"
echo "5. 点击'开始变声'"
echo ""
echo "⚠️ 注意事项："
echo "- 需要麦克风输入"
echo "- 会有一定的延迟（约 100-300ms）"
echo "- Mac M4 使用 MPS 加速"
echo ""
echo "============================================================"

$PYTHON_CMD gui.py
