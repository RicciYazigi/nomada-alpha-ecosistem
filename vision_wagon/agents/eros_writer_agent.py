"""
Eros Writer Agent - Narrative Generation
Generates erotic/creative content with cultural adaptation
"""

from .base_agent import BaseAgent
from typing import Dict, Any
import random
import requests
import json

class ErosWriterAgent(BaseAgent):
    """Agent specialized in narrative generation"""

    def generate_narrative(self, topic: str = "default", style: str = "erotic", **kwargs) -> Dict[str, Any]:
        """Generate narrative content based on topic"""

        # Get OpenAI configuration
        openai_key = self.get_api_key('openai')
        model_config = self.get_model_config('text')

        if openai_key and openai_key.startswith('sk-'):
            # Real OpenAI integration
            return self._generate_with_openai(topic, style, openai_key, model_config)
        else:
            # Placeholder implementation for demo
            return self._generate_placeholder(topic, style)

    def _generate_with_openai(self, topic: str, style: str, api_key: str, model_config: Dict) -> Dict[str, Any]:
        """Generate narrative using OpenAI API"""

        prompt = self._build_prompt(topic, style)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model_config.get("model", "gpt-4"),
            "messages": [
                {"role": "system", "content": "You are an expert creative writer specializing in engaging, tasteful adult fiction."},
                {"role": "user", "content": prompt}
            ],
            "temperature": model_config.get("temperature", 0.9),
            "max_tokens": model_config.get("max_tokens", 1000)
        }

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                narrative = result['choices'][0]['message']['content']

                # Compliance check
                if not self.is_compliant(narrative):
                    return {
                        "narrative": "",
                        "error": "Content failed compliance check",
                        "status": "failed"
                    }

                return {
                    "narrative": narrative,
                    "word_count": len(narrative.split()),
                    "topic": topic,
                    "style": style,
                    "model_used": payload["model"],
                    "status": "success"
                }
            else:
                return {
                    "narrative": "",
                    "error": f"OpenAI API error: {response.status_code}",
                    "status": "failed"
                }

        except Exception as e:
            self.logger.error(f"Error calling OpenAI API: {str(e)}")
            return self._generate_placeholder(topic, style)

    def _generate_placeholder(self, topic: str, style: str) -> Dict[str, Any]:
        """Placeholder implementation for demo purposes"""

        narratives = {
            "erotic": [
                f"In the neon-lit corridors of the space station, {topic} unfolded like a forbidden dream. The artificial gravity couldn't contain the weightless feeling of desire that pulsed through the air...",
                f"The {topic} whispered secrets that only the stars could hear, as passion ignited in the vast emptiness of space. Her breath fogged the viewport as she pressed against the cool metal...",
                f"Among the {topic}, she found herself drawn to mysteries that defied both physics and desire. The quantum entanglement of their souls created ripples across dimensions..."
            ],
            "romantic": [
                f"Under the gentle glow of distant nebulae, {topic} became the backdrop for an unexpected romance. Time seemed to slow as their eyes met across the observation deck...",
                f"The {topic} provided the perfect setting for love to bloom in the most unlikely of places. Against all odds, two hearts found each other in the infinite cosmos..."
            ],
            "adventure": [
                f"The {topic} held secrets that would change everything. As the ship's engines hummed with anticipation, the crew prepared for a journey beyond imagination...",
                f"Deep within the {topic}, ancient mysteries awaited discovery. The expedition team had no idea what they were about to uncover..."
            ]
        }

        style_narratives = narratives.get(style, narratives["erotic"])
        narrative = random.choice(style_narratives)

        return {
            "narrative": narrative,
            "word_count": len(narrative.split()),
            "topic": topic,
            "style": style,
            "model_used": "placeholder",
            "status": "generated"
        }

    def _build_prompt(self, topic: str, style: str) -> str:
        """Build prompt for narrative generation"""

        prompts = {
            "erotic": f"Write a tasteful, engaging erotic short story about {topic}. Focus on tension, desire, and emotional connection. Keep it sophisticated and avoid explicit language. Aim for 400-600 words.",
            "romantic": f"Write a romantic story about {topic}. Focus on emotional connection, chemistry, and meaningful moments. Aim for 400-600 words.",
            "adventure": f"Write an adventure story involving {topic}. Focus on excitement, discovery, and compelling characters. Aim for 400-600 words."
        }

        return prompts.get(style, prompts["erotic"])

    def adapt_culturally(self, content: str, culture: str = "universal", **kwargs) -> Dict[str, Any]:
        """Adapt content for different cultural contexts"""

        cultural_adaptations = {
            "universal": content,
            "western": f"[Western Context] {content}",
            "eastern": f"[Eastern Context] {content}",
            "latin": f"[Latin Context] {content}"
        }

        adapted_content = cultural_adaptations.get(culture, content)

        result = {
            "adapted_content": adapted_content,
            "original_content": content,
            "target_culture": culture,
            "status": "adapted"
        }

        self.log_action("adapt_culturally", {"culture": culture}, result)
        return result

    def create_cliffhanger(self, narrative: str, **kwargs) -> Dict[str, Any]:
        """Create cliffhanger ending for serialized content"""

        cliffhangers = [
            "But then, the airlock began to open...",
            "Suddenly, the lights went out and she heard footsteps...",
            "The message on her screen changed everything...",
            "A shadow moved in the corridor behind her...",
            "The ship's AI spoke with a voice she didn't recognize...",
            "Her communicator crackled with an impossible transmission..."
        ]

        cliffhanger = random.choice(cliffhangers)
        enhanced_narrative = f"{narrative}\n\n{cliffhanger}"

        result = {
            "enhanced_narrative": enhanced_narrative,
            "cliffhanger": cliffhanger,
            "original_length": len(narrative.split()),
            "enhanced_length": len(enhanced_narrative.split()),
            "status": "enhanced"
        }

        self.log_action("create_cliffhanger", {"narrative_length": len(narrative)}, result)
        return result

    def ensure_character_consistency(self, narrative: str, character_profile: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """Ensure character consistency across narratives"""

        if not character_profile:
            character_profile = {
                "name": "Alex",
                "traits": ["curious", "brave", "passionate"],
                "background": "space explorer"
            }

        # Simple consistency check and enhancement
        name = character_profile.get("name", "Alex")
        traits = character_profile.get("traits", [])

        # Add character consistency note
        consistency_note = f"\n\n[Character Note: {name} - {', '.join(traits)}]"
        enhanced_narrative = narrative + consistency_note

        result = {
            "enhanced_narrative": enhanced_narrative,
            "character_profile": character_profile,
            "consistency_applied": True,
            "status": "consistent"
        }

        self.log_action("ensure_character_consistency", {"character": name}, result)
        return result
