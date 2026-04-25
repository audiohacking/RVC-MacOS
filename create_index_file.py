#!/usr/bin/env python3
"""
为测试模型创建一个空的 index 文件
index 文件用于检索增强，是可选的
"""

from pathlib import Path

print("=" * 60)
print("创建 Index 文件")
print("=" * 60)

# 创建空的 index 文件
index_path = Path("assets/weights/test_voice/test_voice.index")

# 创建一个非常小的空 index 文件（仅用于占位）
# 实际的 index 文件需要通过训练生成
index_path.write_bytes(b"")

print(f"\n✓ 已创建：{index_path}")
print("  大小：0 bytes (空文件)")
print("\n说明：")
print("- Index 文件是可选的，用于提高音色相似度")
print("- 没有 index 文件也可以正常使用")
print("- 如果要生成真实的 index 文件，需要训练模型")

print("\n" + "=" * 60)
