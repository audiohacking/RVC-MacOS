#!/bin/bash
# 清理临时脚本和文件
# 用法：./cleanup_temp.sh

echo "============================================================"
echo "清理临时脚本和文件"
echo "============================================================"

cd "$(dirname "$0")"

# 计数器
deleted=0

# 删除临时下载脚本
echo ""
echo "清理临时下载脚本..."
for file in download_test_*.py download_temp_*.py download_backup_*.py; do
    if [ -f "$file" ]; then
        rm -f "$file"
        echo "  ✓ 删除：$file"
        ((deleted++))
    fi
done

# 删除临时创建脚本
echo ""
echo "清理临时创建脚本..."
for file in create_temp_*.py create_test_*.py; do
    if [ -f "$file" ]; then
        rm -f "$file"
        echo "  ✓ 删除：$file"
        ((deleted++))
    fi
done

# 删除临时测试脚本（非官方）
echo ""
echo "清理临时测试脚本..."
for file in test_*.py; do
    if [ -f "$file" ] && [ "$file" != "test_runner.py" ]; then
        rm -f "$file"
        echo "  ✓ 删除：$file"
        ((deleted++))
    fi
done

# 删除调试脚本
echo ""
echo "清理调试脚本..."
for file in debug_*.py fix_*.py; do
    if [ -f "$file" ]; then
        rm -f "$file"
        echo "  ✓ 删除：$file"
        ((deleted++))
    fi
done

# 删除其他临时文件
echo ""
echo "清理其他临时文件..."
for file in temp_*.py backup_*.py; do
    if [ -f "$file" ]; then
        rm -f "$file"
        echo "  ✓ 删除：$file"
        ((deleted++))
    fi
done

echo ""
echo "============================================================"
echo "清理完成！"
echo "共删除 $deleted 个文件"
echo "============================================================"
echo ""
echo "保留的核心脚本："
ls -1 *.py 2>/dev/null | grep -E "(download_models|web\.py|infer-web\.py|gui\.py|launcher\.py)" | sed 's/^/  ✓ /'
echo ""
