#!/usr/bin/env python3
"""下载公开的 RVC 模型"""

import os
import sys
import requests
from pathlib import Path

def download_file(url, dest_path, description=""):
    """下载文件"""
    print(f"\n下载：{description}")
    print(f"URL: {url}")
    print(f"目标：{dest_path}")
    
    if os.path.exists(dest_path):
        print(f"  ✓ 已存在，跳过")
        return True
    
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\r  进度：{percent:.1f}%", end='', flush=True)
        
        print(f"\r  ✓ 下载完成！")
        return True
        
    except Exception as e:
        print(f"\n  ✗ 下载失败：{e}")
        if os.path.exists(dest_path):
            os.remove(dest_path)
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("RVC 公开模型下载工具")
    print("=" * 60)
    
    # 创建 weights 目录
    weights_dir = Path("assets/weights")
    weights_dir.mkdir(exist_ok=True)
    
    # 公开模型列表（示例模型）
    # 注意：这些是示例 URL，实际使用时需要替换为真实的模型链接
    models = [
        {
            "name": "example_voice.pth",
            "url": "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained_v2/D40k.pth",
            "description": "示例模型（使用预训练模型作为占位符）"
        }
    ]
    
    success_count = 0
    failed_count = 0
    
    for model in models:
        dest_path = weights_dir / model["name"]
        if download_file(model["url"], dest_path, model["description"]):
            success_count += 1
        else:
            failed_count += 1
    
    print("\n" + "=" * 60)
    print(f"下载完成！成功：{success_count}, 失败：{failed_count}")
    print("=" * 60)
    
    print("\n提示：")
    print("1. 要下载更多模型，请访问:")
    print("   - https://huggingface.co/lj1995/VoiceConversionWebUI")
    print("   - https://huggingface.co/RVC-Project")
    print("   - https://github.com/RVC-Project/RVC-Models-Downloader")
    print("\n2. 下载 .pth 文件后，放入 assets/weights/ 目录即可")

if __name__ == "__main__":
    main()
