# This tests running hordelib standalone, as an external caller would use it.
# Call with: python -m test.run_img2img_inpaint
# You need all the deps in whatever environment you are running this.
import os

import hordelib

hordelib.initialise()

from PIL import Image

from hordelib.horde import HordeLib
from hordelib.shared_model_manager import SharedModelManager

generate = HordeLib()
SharedModelManager.loadModelManagers(diffusers=True)
SharedModelManager.manager.load("stable_diffusion_inpainting")

data = {
    "sampler_name": "euler",
    "cfg_scale": 8,
    "denoising_strength": 0.72,
    "seed": 836913938046008,
    "height": 512,
    "width": 512,
    "karras": False,
    "tiling": False,
    "hires_fix": False,
    "clip_skip": 1,
    "control_type": "canny",
    "image_is_control": False,
    "return_control_map": False,
    "prompt": "a dinosaur",
    "ddim_steps": 20,
    "n_iter": 1,
    "model": "stable_diffusion_inpainting",
    "source_image": Image.open("images/test_inpaint.png"),
    "source_processing": "inpainting",
}
pil_image = generate.basic_inference(data)
pil_image.save("images/test_run_inpainting.png")