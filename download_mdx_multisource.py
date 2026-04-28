#!/usr/bin/env python3
"""
MDX-Net 模型下载工具 - 多源尝试
支持：官方 Hugging Face、镜像源、备用仓库
"""
import os
import requests
from pathlib import Path

print("=" * 70)
print("MDX-Net 模型下载工具 - 多源自动尝试")
print("=" * 70)
print()

# 模型信息
models = {
    "model_bs_roformer_ep_317_sdr_12.9755.pth": {
        "description": "最佳质量模型（推荐）",
        "size": "~200MB"
    },
    "UVR-MDX-NET-Main.pth": {
        "description": "平衡质量和速度",
        "size": "~150MB"
    }
}

output_dir = Path("/Volumes/Jason/rvc/RVC-MacOS/assets/uvr5_weights")
os.makedirs(output_dir, exist_ok=True)

# 下载源列表（按优先级）
sources = [
    {
        "name": "Hugging Face 官方",
        "url_template": "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/uvr5_weights/{filename}"
    },
    {
        "name": "Hugging Face 镜像",
        "url_template": "https://hf-mirror.com/lj1995/VoiceConversionWebUI/resolve/main/uvr5_weights/{filename}"
    },
    {
        "name": "OpenXLab",
        "url_template": "https://code.openxlab.org.cn/api/v1/repos/openxlab/RVC/resolve/main/uvr5_weights/{filename}"
    }
]

def download_with_progress(url, dest_path, source_name):
    """带进度显示的下载"""
    try:
        print(f"  源：{source_name}")
        response = requests.get(url, stream=True, timeout=300)
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
            return True
        else:
            print(f"  ⚠️  文件太小，可能下载失败")
            dest_path.unlink()
            return False
            
    except Exception as e:
        print(f"\n  ✗ 下载失败：{e}")
        if dest_path.exists():
            dest_path.unlink()
        return False

print("📦 将下载以下模型：")
for name, info in models.items():
    print(f"  • {name}")
    print(f"    说明：{info['description']}")
    print(f"    大小：{info['size']}")
print()

print("🔍 尝试多个下载源...")
print()

success_count = 0
fail_count = 0

for model_name, info in models.items():
    print(f"开始下载：{model_name}")
    print(f"  说明：{info['description']}")
    
    # 检查是否已存在
    dest_path = output_dir / model_name
    if dest_path.exists() and dest_path.stat().st_size > 1000000:
        print(f"  ✓ 文件已存在，跳过")
        success_count += 1
        print()
        continue
    
    # 尝试所有源
    downloaded = False
    for source in sources:
        url = source["url_template"].format(filename=model_name)
        print()
        
        if download_with_progress(url, dest_path, source["name"]):
            downloaded = True
            success_count += 1
            break
    
    if not downloaded:
        print(f"\n  ❌ 所有源都下载失败")
        fail_count += 1
    
    print()

print("=" * 70)
print("下载完成！")
print(f"✅ 成功：{success_count} 个")
print(f"❌ 失败：{fail_count} 个")
print("=" * 70)
print()

if success_count > 0:
    print("💡 使用提示：")
    print("  1. 刷新 Web UI 页面 (Ctrl+R)")
    print("  2. 进入 UVR5 页面")
    print("  3. 在下拉菜单中选择新下载的模型")
    print("  4. 享受无噪音的高质量分离！")
    print()
else:
    print("❌ 所有模型下载失败")
    print()
    print("💡 建议：")
    print("  1. 检查网络连接")
    print("  2. 手动从 Hugging Face 下载：")
    print("     https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main/uvr5_weights")
    print("  3. 下载后放到：assets/uvr5_weights/")
    print()
