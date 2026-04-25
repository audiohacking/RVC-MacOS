#!/usr/bin/env python3
"""下载 RVC 示例模型"""

import requests
from pathlib import Path

print("=" * 60)
print("下载 RVC 示例模型")
print("=" * 60)

# 创建模型目录
model_dir = Path("assets/weights/example_model")
model_dir.mkdir(exist_ok=True)

# 从 RVC 官方 HuggingFace Space 下载
# 使用正确的路径
urls = [
    {
        "name": "example_model.pth",
        # RVC 官方示例模型
        "url": "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained_v2/G40k.pth",
        "mirror": "https://hf-mirror.com/lj1995/VoiceConversionWebUI/resolve/main/pretrained_v2/G40k.pth"
    }
]

for item in urls:
    dest = model_dir / item["name"]
    url = item.get("mirror", item["url"])
    
    print(f"\n下载：{item['name']}")
    
    if dest.exists():
        print("  ✓ 已存在，跳过")
        continue
    
    try:
        response = requests.get(url, stream=True, timeout=180)
        response.raise_for_status()
        
        total = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(dest, 'wb') as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total > 0:
                    pct = (downloaded / total) * 100
                    print(f"  进度：{pct:.1f}%", end='\r')
        
        size_mb = dest.stat().st_size / 1024 / 1024
        print(f"  ✓ 完成！大小：{size_mb:.2f} MB")
        
    except Exception as e:
        print(f"  ✗ 失败：{e}")
        if dest.exists():
            dest.unlink()

print("\n" + "=" * 60)
print("模型目录结构：")
import subprocess
subprocess.run(['find', 'assets/weights/', '-type', 'f'])
print("=" * 60)
