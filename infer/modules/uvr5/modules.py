import os
import traceback
import logging

logger = logging.getLogger(__name__)

from infer.lib.audio import resample_audio, get_audio_properties
import torch

from configs import Config
from infer.modules.uvr5.mdxnet import MDXNetDereverb
from infer.modules.uvr5.vr import AudioPre

config = Config()


def uvr(model_name, inp_root, save_root_vocal, paths, save_root_ins, agg, format0):
    infos = []
    try:
        # Check if UVR5 models are available
        if model_name is None or model_name == "" or "Please download UVR5 models" in str(model_name):
            yield "❌ Error: No UVR5 model selected. Please download UVR5 models first.\n\nUVR5 models are required for vocal/accompaniment separation. Without these models, this feature cannot function.\n\nTo download UVR5 models, you would typically need to run the model download script or manually place the model files in the assets/uvr5_weights directory."
            return
        
        inp_root = inp_root.strip(" ").strip('"').strip("\n").strip('"').strip(" ")
        save_root_vocal = (
            save_root_vocal.strip(" ").strip('"').strip("\n").strip('"').strip(" ")
        )
        save_root_ins = (
            save_root_ins.strip(" ").strip('"').strip("\n").strip('"').strip(" ")
        )
        if model_name == "onnx_dereverb_By_FoxJoy":
            pre_fun = MDXNetDereverb(15, config.device)
        else:
            # Check if model_name is valid
            if model_name is None or model_name == "":
                raise ValueError("UVR5 model name is required but not provided.")
            
            # Use default uvr5_weights path if environment variable is not set
            weight_uvr5_root = os.getenv("weight_uvr5_root")
            if weight_uvr5_root is None:
                weight_uvr5_root = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "assets", "uvr5_weights")
            
            model_path = os.path.join(weight_uvr5_root, model_name + ".pth")
            
            # Check if the model file exists
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"UVR5 model not found: {model_path}. Please download the required UVR5 models.")
            
            pre_fun = AudioPre(
                agg=int(agg),
                model_path=model_path,
                device=config.device,
                is_half=config.is_half,
            )
        if inp_root != "":
            paths = [os.path.join(inp_root, name) for name in os.listdir(inp_root)]
        else:
            paths = [path.name for path in paths]
        for path in paths:
            inp_path = os.path.join(inp_root, path)
            need_reformat = 1
            done = 0
            try:
                channels, rate = get_audio_properties(inp_path)

                # Check the audio stream's properties
                if channels == 2 and rate == 44100:
                    pre_fun._path_audio_(
                        inp_path, save_root_ins, save_root_vocal, format0
                    )
                    need_reformat = 0
                    done = 1
            except Exception as e:
                need_reformat = 1
                logger.warning(f"Exception {e} occured. Will reformat")
            if need_reformat == 1:
                tmp_path = "%s/%s.reformatted.wav" % (
                    os.path.join(os.environ["TEMP"]),
                    os.path.basename(inp_path),
                )
                resample_audio(inp_path, tmp_path, "pcm_s16le", "s16", 44100, "stereo")
                try:  # Remove the original file
                    os.remove(inp_path)
                except Exception as e:
                    print(f"Failed to remove the original file: {e}")
                inp_path = tmp_path
            try:
                if done == 0:
                    pre_fun._path_audio_(
                        inp_path, save_root_ins, save_root_vocal, format0
                    )
                infos.append("%s->Success" % (os.path.basename(inp_path)))
                yield "\n".join(infos)
            except:
                infos.append(
                    "%s->%s" % (os.path.basename(inp_path), traceback.format_exc())
                )
                yield "\n".join(infos)
    except:
        infos.append(traceback.format_exc())
        yield "\n".join(infos)
    finally:
        try:
            # Only cleanup if pre_fun was actually created
            if 'pre_fun' in locals():
                if model_name == "onnx_dereverb_By_FoxJoy":
                    del pre_fun.pred.model
                    del pre_fun.pred.model_
                else:
                    del pre_fun.model
                    del pre_fun
        except:
            traceback.print_exc()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            logger.info("Executed torch.cuda.empty_cache()")
        elif torch.backends.mps.is_available():
            torch.mps.empty_cache()
            logger.info("Executed torch.mps.empty_cache()")
    yield "\n".join(infos)
