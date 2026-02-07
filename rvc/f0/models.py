import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import os


def get_rmvpe(model_path, device, is_half=True):
    try:
        # First try to load as a JIT model
        try:
            model = torch.jit.load(model_path, map_location=device)
            model.eval()
            if is_half:
                model = model.half()
            model = model.to(device)
            return model
        except Exception as jit_e:
            print(f"JIT loading failed: {jit_e}")
        
        # If JIT loading fails, this model format is not yet supported
        raise NotImplementedError(
            "The current RMVPE model format is not yet supported in this implementation. "
            "The system will fall back to an alternative F0 estimation method (FCPE)."
        )
        
    except Exception as e:
        raise RuntimeError(f"Failed to load RMVPE model: {str(e)}")
