"""
Assembly Agent - Multimedia Content Creation
Handles image generation, audio synthesis, and content packaging
"""

from .base_agent import BaseAgent
from typing import Dict, Any
import random
import requests
import base64
import io

class AssemblyAgent(BaseAgent):
    """Agent specialized in multimedia assembly"""

    def generate_image(self, prompt: str, style: str = "realistic", **kwargs) -> Dict[str, Any]:
        """Generate image based on text prompt"""

        # Get Stable Diffusion configuration
        sd_key = self.get_api_key('stable_diffusion')
        model_config = self.get_model_config('image')

        if sd_key:
            return self._generate_with_stable_diffusion(prompt, style, sd_key, model_config)
        else:
            return self._generate_placeholder_image(prompt, style)

    def _generate_with_stable_diffusion(self, prompt: str, style: str, api_key: str, model_config: Dict) -> Dict[str, Any]:
        """Generate image using Stable Diffusion API"""

        # Enhance prompt based on style
        enhanced_prompt = self._enhance_image_prompt(prompt, style)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "text_prompts": [
                {
                    "text": enhanced_prompt,
                    "weight": 1
                },
                {
                    "text": "nsfw, explicit, underage, violence",
                    "weight": -1
                }
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": model_config.get("steps", 20)
        }

        try:
            response = requests.post(
                "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                headers=headers,
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()

                # Get the first generated image
                image_data = result["artifacts"][0]
                image_base64 = image_data["base64"]

                # In a real implementation, you'd save this to storage
                # For now, we'll create a placeholder URL
                image_url = f"data:image/png;base64,{image_base64[:50]}..."

                return {
                    "image_url": image_url,
                    "prompt": enhanced_prompt,
                    "style": style,
                    "dimensions": "1024x1024",
                    "seed": image_data.get("seed"),
                    "model_used": "stable-diffusion-xl",
                    "status": "generated"
                }
            else:
                return {
                    "image_url": "",
                    "error": f"Stable Diffusion API error: {response.status_code}",
                    "status": "failed"
                }

        except Exception as e:
            self.logger.error(f"Error calling Stable Diffusion API: {str(e)}")
            return self._generate_placeholder_image(prompt, style)

    def _generate_placeholder_image(self, prompt: str, style: str) -> Dict[str, Any]:
        """Placeholder implementation for demo purposes"""

        # Generate a deterministic "image URL" based on prompt
        image_id = hash(prompt) % 10000
        image_url = f"https://picsum.photos/1024/1024?random={image_id}"

        return {
            "image_url": image_url,
            "prompt": prompt,
            "style": style,
            "dimensions": "1024x1024",
            "model_used": "placeholder",
            "status": "generated"
        }

    def _enhance_image_prompt(self, prompt: str, style: str) -> str:
        """Enhance image prompt based on style"""

        style_enhancements = {
            "realistic": "photorealistic, high detail, 8k",
            "anime": "anime style, vibrant colors, expressive characters",
            "fantasy": "fantasy art, epic, detailed, magical atmosphere",
            "sci-fi": "sci-fi concept art, futuristic, sleek design",
            "erotic": "tasteful erotic art, sensual, intimate"
        }

        enhancement = style_enhancements.get(style, style_enhancements["realistic"])
        return f"{prompt}, {enhancement}"

    def synthesize_audio(self, text: str, voice: str = "alloy", **kwargs) -> Dict[str, Any]:
        """Synthesize audio from text (TTS)"""

        openai_key = self.get_api_key('openai')
        model_config = self.get_model_config('tts')

        if openai_key and openai_key.startswith('sk-'):
            return self._synthesize_with_openai(text, voice, openai_key, model_config)
        else:
            return self._synthesize_placeholder(text, voice)

    def _synthesize_with_openai(self, text: str, voice: str, api_key: str, model_config: Dict) -> Dict[str, Any]:
        """Synthesize audio using OpenAI TTS API"""

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model_config.get("model", "tts-1"),
            "input": text,
            "voice": voice,
            "response_format": "mp3"
        }

        try:
            response = requests.post(
                "https://api.openai.com/v1/audio/speech",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                # In a real implementation, save to storage and return URL
                # For now, return a placeholder with partial base64 data
                audio_base64 = base64.b64encode(response.content).decode('utf-8')
                audio_url = f"data:audio/mp3;base64,{audio_base64[:50]}..."

                return {
                    "audio_url": audio_url,
                    "text_length": len(text),
                    "voice": voice,
                    "format": "mp3",
                    "model_used": payload["model"],
                    "status": "synthesized"
                }
            else:
                return {
                    "audio_url": "",
                    "error": f"OpenAI TTS API error: {response.status_code}",
                    "status": "failed"
                }

        except Exception as e:
            self.logger.error(f"Error calling OpenAI TTS API: {str(e)}")
            return self._synthesize_placeholder(text, voice)

    def _synthesize_placeholder(self, text: str, voice: str) -> Dict[str, Any]:
        """Placeholder for audio synthesis"""

        audio_url = f"placeholder_audio_{hash(text) % 1000}.mp3"

        return {
            "audio_url": audio_url,
            "text_length": len(text),
            "voice": voice,
            "format": "mp3",
            "model_used": "placeholder",
            "status": "synthesized"
        }

    def package_content(self, narrative: str, image_url: str, audio_url: str, **kwargs) -> Dict[str, Any]:
        """Package content into a structured format"""

        # This is a simplified packaging example
        packaged_data = {
            "title": kwargs.get("title", "Untitled Content"),
            "narrative_text": narrative,
            "visual_element": image_url,
            "audio_element": audio_url,
            "metadata": {
                "style": kwargs.get("style", "unknown"),
                "topic": kwargs.get("topic", "unknown"),
                "creation_date": "YYYY-MM-DD" # Placeholder
            }
        }

        result = {
            "packaged_content": packaged_data,
            "content_elements": ["narrative", "image", "audio"],
            "package_format": "json",
            "status": "packaged"
        }

        self.log_action("package_content", {"elements_count": 3}, result)
        return result

    def add_watermark(self, image_url: str, watermark_text: str = "WagonX", **kwargs) -> Dict[str, Any]:
        """Add watermark to image (conceptual)"""

        # Placeholder: in reality, this would involve image processing
        watermarked_image_url = f"{image_url}?watermark={watermark_text.replace(' ', '_')}"

        result = {
            "watermarked_image_url": watermarked_image_url,
            "original_image_url": image_url,
            "watermark_text": watermark_text,
            "status": "watermarked"
        }

        self.log_action("add_watermark", {"text": watermark_text}, result)
        return result
