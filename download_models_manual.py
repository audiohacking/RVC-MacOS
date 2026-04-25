#!/usr/bin/env python3
"""手动下载 RVC 模型 - 使用国内镜像源"""
import os
import requests
from pathlib import Path

# 使用镜像源
MIRROR_URL = "https://hf-mirror.com"

# 模型下载链接
models = {
    # Hubert
    "assets/hubert/hubert_base.pt": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/hubert/hubert_base.pt",
    
    # RMVPE
    "assets/rmvpe/rmvpe.pt": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/rmvpe/rmvpe.pt",
    "assets/rmvpe/rmvpe.onnx": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/rmvpe/rmvpe.onnx",
    
    # 预训练模型 v1
    "assets/pretrained/D32k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained/D32k.pth",
    "assets/pretrained/D40k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained/D40k.pth",
    "assets/pretrained/D48k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained/D48k.pth",
    "assets/pretrained/G32k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained/G32k.pth",
    "assets/pretrained/G40k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained/G40k.pth",
    "assets/pretrained/G48k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained/G48k.pth",
    "assets/pretrained/f0D32k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained/f0D32k.pth",
    "assets/pretrained/f0D40k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained/f0D40k.pth",
    "assets/pretrained/f0D48k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained/f0D48k.pth",
    "assets/pretrained/f0G32k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained/f0G32k.pth",
    "assets/pretrained/f0G40k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained/f0G40k.pth",
    "assets/pretrained/f0G48k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained/f0G48k.pth",
    
    # 预训练模型 v2
    "assets/pretrained_v2/D32k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained_v2/D32k.pth",
    "assets/pretrained_v2/D40k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained_v2/D40k.pth",
    "assets/pretrained_v2/D48k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained_v2/D48k.pth",
    "assets/pretrained_v2/G32k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained_v2/G32k.pth",
    "assets/pretrained_v2/G40k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained_v2/G40k.pth",
    "assets/pretrained_v2/G48k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained_v2/G48k.pth",
    "assets/pretrained_v2/f0D32k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained_v2/f0D32k.pth",
    "assets/pretrained_v2/f0D40k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained_v2/f0D40k.pth",
    "assets/pretrained_v2/f0D48k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained_v2/f0D48k.pth",
    "assets/pretrained_v2/f0G32k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained_v2/f0G32k.pth",
    "assets/pretrained_v2/f0G40k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained_v2/f0G40k.pth",
    "assets/pretrained_v2/f0G48k.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/pretrained_v2/f0G48k.pth",
    
    # UVR5 权重
    "assets/uvr5_weights/HP2_all_vocals.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/uvr5_weights/HP2_all_vocals.pth",
    "assets/uvr5_weights/HP3_all_vocals.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/uvr5_weights/HP3_all_vocals.pth",
    "assets/uvr5_weights/HP5-主旋律人声 vocals+ 其他 instrumentals.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/uvr5_weights/HP5-%E4%B8%BB%E6%97%8B%E5%BE%8B%E4%BA%BA%E5%A3%B0vocals+%E5%85%B6%E4%BB%96instrumentals.pth",
    "assets/uvr5_weights/HP5_only_main_vocal.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/uvr5_weights/HP5_only_main_vocal.pth",
    "assets/uvr5_weights/VR-DeEchoAggressive.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/uvr5_weights/VR-DeEchoAggressive.pth",
    "assets/uvr5_weights/VR-DeEchoDeReverb.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/uvr5_weights/VR-DeEchoDeReverb.pth",
    "assets/uvr5_weights/VR-DeEchoNormal.pth": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/uvr5_weights/VR-DeEchoNormal.pth",
    "assets/uvr5_weights/onnx_dereverb_By_FoxJoy/vocals.onnx": f"{MIRROR_URL}/fumiama/RVC-Pretrained-Models/resolve/main/uvr5_weights/onnx_dereverb_By_FoxJoy/vocals.onnx",
}

def download_file(url, dest_path):
    """下载文件并显示进度"""
    print(f"下载：{dest_path}")
    
    # 创建目录
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # 如果文件已存在，跳过
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
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r  进度：{percent:.1f}%", end='', flush=True)
        
        print(f"\r  ✓ 下载完成")
        return True
        
    except Exception as e:
        print(f"\n  ✗ 下载失败：{e}")
        return False

def main():
    base_dir = Path(__file__).parent
    os.chdir(base_dir)
    
    print("=" * 60)
    print("RVC 模型手动下载工具 (使用镜像源)")
    print("=" * 60)
    print()
    
    success_count = 0
    fail_count = 0
    
    for dest, url in models.items():
        if download_file(url, dest):
            success_count += 1
        else:
            fail_count += 1
    
    print()
    print("=" * 60)
    print(f"下载完成！成功：{success_count}, 失败：{fail_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()
