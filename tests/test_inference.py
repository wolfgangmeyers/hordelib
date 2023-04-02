# test_inference.py
import pytest
from hordelib.comfy import Comfy
from PIL import Image


class TestInference:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.comfy = Comfy()
        yield
        self.comfy = None

    def test_unknown_pipeline(self):
        result = self.comfy.run_pipeline("non-existent-pipeline", {})
        assert result is None

    def test_stable_diffusion_pipeline(self):
        params = {
            "sampler.seed": 12345,
            "sampler.cfg": 7.5,
            "sampler.scheduler": "karras",
            "sampler.sampler_name": "dpmpp_2m",
            "sampler.steps": 25,
            "prompt.text": "a closeup photo of a confused dog",
            "negative_prompt.text": "cat, black and white, deformed",
            "model_loader.ckpt_name": "model.ckpt",
            "empty_latent_image.width": 768,
            "empty_latent_image.height": 768,
        }
        images = self.comfy.run_image_pipeline("stable_diffusion", params)

        image = Image.open(images[0]["imagedata"])
        image.save("pipeline_stable_diffusion.png")

    def test_stable_diffusion_hires_fix_pipeline(self):
        params = {
            "sampler.seed": 12345,
            "sampler.cfg": 7.5,
            "sampler.scheduler": "normal",
            "sampler.sampler_name": "dpmpp_sde",
            "sampler.steps": 12,
            "prompt.text": (
                "(masterpiece) HDR victorian portrait painting of (girl), "
                "blonde hair, mountain nature, blue sky"
            ),
            "negative_prompt.text": "bad hands, text, watermark",
            "model_loader.ckpt_name": "model.ckpt",
            "empty_latent_image.width": 768,
            "empty_latent_image.height": 768,
            "latent_upscale.width": 1216,
            "latent_upscale.height": 1216,
            "latent_upscale.crop": "disabled",
            "latent_upscale.upscale_method": "nearest-exact",
            "upscale_sampler.seed": 45678,
            "upscale_sampler.steps": 15,
            "upscale_sampler.cfg": 8.0,
            "upscale_sampler.sampler_name": "dpmpp_2m",
            "upscale_sampler.scheduler": "simple",
            "upscale_sampler.denoise": 0.5,
        }
        images = self.comfy.run_image_pipeline("stable_diffusion_hires_fix", params)

        image = Image.open(images[0]["imagedata"])
        image.save("pipeline_stable_diffusion_hires_fix.png")
