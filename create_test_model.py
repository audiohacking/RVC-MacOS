#!/usr/bin/env python3
"""
创建一个简单的测试模型用于 RVC 推理
这个脚本会创建一个最小可用的模型结构
"""

import torch
from collections import OrderedDict
from pathlib import Path

print("=" * 60)
print("创建测试用 RVC 推理模型")
print("=" * 60)

# 创建模型目录
model_dir = Path("assets/weights/test_voice")
model_dir.mkdir(exist_ok=True)

# 创建一个模拟的 RVC 模型检查点
# 注意：这只是一个测试模型，不能用于实际的语音转换
# 实际使用需要训练真实的模型

print("\n创建模型文件...")

# 模拟模型配置
config = [
    1,  # spec_channels
    256,  # inter_channels
    192,  # hidden_channels
    2,  # filter_channels
    3,  # n_heads
    2,  # n_layers
    6,  # kernel_size
    1,  # p_dropout
    16000,  # sample_rate
    40,  # hop_length
    512,  # n_fft
    0,  # pitch_guidance
    256,  # encoder_dim (v2)
    1,  # use_f0
]

# 创建一个空的权重字典（仅用于测试）
weight = OrderedDict()
weight["emb_g.weight"] = torch.randn(1, 256)  # n_spk=1

# 创建检查点
cpt = OrderedDict()
cpt["config"] = config
cpt["f0"] = 1
cpt["version"] = "v2"
cpt["weight"] = weight

# 保存模型
model_path = model_dir / "test_voice.pth"
torch.save(cpt, model_path)

size_mb = model_path.stat().st_size / 1024 / 1024
print(f"✓ 模型已保存：{model_path}")
print(f"  大小：{size_mb:.2f} MB")

print("\n" + "=" * 60)
print("注意：")
print("这是一个测试模型，仅用于验证 Web UI 功能")
print("不能用于实际的语音转换")
print("\n要使用真实的语音转换，需要：")
print("1. 训练自己的模型，或")
print("2. 下载他人训练好的完整模型")
print("=" * 60)

print("\n模型目录结构：")
import subprocess
subprocess.run(['find', 'assets/weights/', '-type', 'f'])
