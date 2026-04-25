#!/usr/bin/env python3
"""下载 Whis RVC 推理模型"""

import requests
from pathlib import Path

print("=" * 60)
print("下载 Whis RVC 推理模型")
print("=" * 60)

# Whis 模型目录
whis_dir = Path("assets/weights/Whis")
whis_dir.mkdir(exist_ok=True)

# Whis 模型文件
models = [
    {
        "name": "Whis.pth",
        "url": "https://huggingface.co/datasets/IAHispano/WhisperRVC/resolve/main/Whis.pth",
        "mirror_url": "https://hf-mirror.com/datasets/IAHispano/WhisperRVC/resolve/main/Whis.pth"
    },
    {
        "name": "Whis.index",
        "url": "https://huggingface.co/datasets/IAHispano/WhisperRVC/resolve/main/Whis.index",
        "mirror_url": "https://hf-mirror.com/datasets/IAHispano/WhisperRVC/resolve/main/Whis.index"
    }
]

for model in models:
    dest = whis_dir / model["name"]
    
    if dest.exists():
        print(f"\n✓ {model['name']} 已存在，跳过")
        continue
    
    # 使用镜像源
    url = model.get("mirror_url", model["url"])
    print(f"\n下载：{model['name']}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, stream=True, timeout=300)
        response.raise_for_status()
        
        total = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(dest, 'wb') as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total > 0:
                    pct = (downloaded / total) * 100
                    print(f"进度：{pct:.1f}%", end='\r')
        
        size_mb = dest.stat().st_size / 1024 / 1024
        print(f"\n✓ 完成！大小：{size_mb:.2f} MB")
        
    except Exception as e:
        print(f"\n✗ 失败：{e}")
        if dest.exists():
            dest.unlink()

print("\n" + "=" * 60)
print("完成！")
print("=" * 60)

print("\n模型文件：")
import subprocess
subprocess.run(['ls', '-lh', 'assets/weights/Whis/'])
