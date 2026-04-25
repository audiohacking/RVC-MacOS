#!/usr/bin/env python3
"""下载真实的 RVC 推理模型"""

import requests
from pathlib import Path

print("=" * 60)
print("下载 RVC 推理模型")
print("=" * 60)

weights_dir = Path("assets/weights")
weights_dir.mkdir(exist_ok=True)

# 从 RVC 官方示例模型下载
# 这是一个完整的推理模型，包含所有必需的权重
models = [
    {
        "name": "ljq.pth",  # 刘嘉杰模型（RVC 官方示例）
        "url": "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/checkpoints/ljq.pth",
        "mirror_url": "https://hf-mirror.com/lj1995/VoiceConversionWebUI/resolve/main/checkpoints/ljq.pth"
    }
]

for model in models:
    dest = weights_dir / model["name"]
    
    if dest.exists():
        print(f"\n✓ {model['name']} 已存在，跳过")
        continue
    
    # 尝试从镜像源下载
    url = model.get("mirror_url", model["url"])
    print(f"\n下载：{model['name']}")
    print(f"URL: {url}")
    
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
