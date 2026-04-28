#!/usr/bin/env python3
"""使用镜像源下载 MDX-Net 模型"""
import os
import requests
from pathlib import Path
from huggingface_hub import hf_hub_download

print("=" * 60)
print("使用镜像源下载 MDX-Net 模型")
print("=" * 60)
print()

# 模型信息
models = [
    {
        "name": "model_bs_roformer_ep_317_sdr_12.9755.pth",
        "description": "最佳质量模型（推荐）",
        "size": "~200MB"
    },
    {
        "name": "UVR-MDX-NET-Main.pth",
        "description": "平衡质量和速度",
        "size": "~150MB"
    }
]

print("📦 将下载以下模型：")
print()
for model in models:
    print(f"  • {model['name']}")
    print(f"    说明：{model['description']}")
    print(f"    大小：{model['size']}")
    print()

print("⚠️  使用镜像源：hf-mirror.com")
print("📁 保存位置：assets/uvr5_weights/")
print()

# 尝试使用镜像源下载
base_url = "https://hf-mirror.com"
repo_id = "lj1995/VoiceConversionWebUI"
output_dir = Path("/Volumes/Jason/rvc/RVC-MacOS/assets/uvr5_weights")

os.makedirs(output_dir, exist_ok=True)

success_count = 0
fail_count = 0

for model in models:
    model_name = model["name"]
    print(f"开始下载：{model_name}")
    
    # 检查是否已存在
    dest_path = output_dir / model_name
    if dest_path.exists() and dest_path.stat().st_size > 1000000:  # 大于 1MB 才算有效
        print(f"  ✓ 文件已存在，跳过")
        success_count += 1
        print()
        continue
    
    try:
        # 方法 1：使用 huggingface_hub 配合镜像
        print(f"  尝试从镜像源下载...")
        
        # 构建镜像源 URL
        download_url = f"{base_url}/{repo_id}/resolve/main/uvr5_weights/{model_name}"
        
        # 使用 requests 下载
        response = requests.get(download_url, stream=True, timeout=300)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f'\r  进度：{percent:.1f}%', end='', flush=True)
        
        print(f'\r  ✓ 下载完成')
        
        # 验证文件大小
        actual_size = dest_path.stat().st_size
        print(f"  文件大小：{actual_size / 1024 / 1024:.1f} MB")
        
        if actual_size > 1000000:  # 大于 1MB
            print(f"  ✅ 下载成功")
            success_count += 1
        else:
            print(f"  ❌ 文件太小，可能下载失败")
            dest_path.unlink()  # 删除无效文件
            fail_count += 1
            
    except Exception as e:
        print(f"\n  ❌ 下载失败：{e}")
        if dest_path.exists():
            dest_path.unlink()
        fail_count += 1
    
    print()

print("=" * 60)
print("下载完成！")
print(f"✅ 成功：{success_count} 个")
print(f"❌ 失败：{fail_count} 个")
print("=" * 60)
print()

if success_count > 0:
    print("💡 使用提示：")
    print("  1. 刷新 Web UI 页面")
    print("  2. 进入 UVR5 页面")
    print("  3. 在下拉菜单中选择新下载的模型")
    print("  4. 享受无噪音的高质量分离！")
    print()
