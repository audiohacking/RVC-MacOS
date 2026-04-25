#!/usr/bin/env python3
"""下载公开 RVC 模型"""

import requests
from pathlib import Path

print("=" * 60)
print("RVC 公开模型下载")
print("=" * 60)

weights_dir = Path("assets/weights")
weights_dir.mkdir(exist_ok=True)

# 下载测试模型（使用镜像源）
url = "https://hf-mirror.com/lj1995/VoiceConversionWebUI/resolve/main/pretrained_v2/D40k.pth"
dest = weights_dir / "test_model.pth"

print(f"\n下载测试模型...")
print(f"URL: {url}")

try:
    response = requests.get(url, stream=True, timeout=120)
    total = int(response.headers.get('content-length', 0))
    
    with open(dest, 'wb') as f:
        downloaded = 0
        for chunk in response.iter_content(8192):
            f.write(chunk)
            downloaded += len(chunk)
            if total > 0:
                pct = (downloaded / total) * 100
                print(f"进度：{pct:.1f}%", end='\r')
    
    size_mb = dest.stat().st_size / 1024 / 1024
    print(f"\n✓ 完成！大小：{size_mb:.2f} MB")
    print(f"文件：{dest}")
    
except Exception as e:
    print(f"\n✗ 失败：{e}")
    if dest.exists():
        dest.unlink()

print("\n" + "=" * 60)
