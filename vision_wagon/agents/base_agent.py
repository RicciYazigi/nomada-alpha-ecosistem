"""
Base Agent Class for WagonX
All agents inherit from this base class
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
import logging
import os

class BaseAgent(ABC):
    """Base class for all WagonX agents"""

    def __init__(self, name: str, capabilities: List[str], config: Dict[str, Any]):
        self.name = name
        self.agent_id = name  # For compatibility
        self.capabilities = capabilities
        self.config = config
        self.logger = logging.getLogger(f"wagonx.{self.__class__.__name__}")

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name}, capabilities={self.capabilities})"

    def get_api_key(self, service: str) -> str:
        """Get API key for a service from config"""
        api_keys = self.config.get('api_keys', {})
        key = api_keys.get(service, '')

        # Also try environment variables as fallback
        if not key:
            env_key = f"{service.upper()}_API_KEY"
            key = os.getenv(env_key, '')

        return key

    def get_model_config(self, model_type: str) -> Dict[str, Any]:
        """Get model configuration for a specific type"""
        models = self.config.get('models', {})
        return models.get(model_type, {})

    def is_compliant(self, content: str) -> bool:
        """Basic compliance check - override in specific agents"""
        compliance = self.config.get('compliance', {})
        nsfw_config = compliance.get('nsfw', {})

        if not nsfw_config.get('enabled', False):
            return True

        # Basic content filtering
        filters = nsfw_config.get('content_filters', [])
        content_lower = content.lower()

        for filter_term in filters:
            if filter_term.lower() in content_lower:
                self.logger.warning(f"Content failed compliance check: {filter_term}")
                return False

        return True

    def log_action(self, action: str, inputs: Dict[str, Any], outputs: Dict[str, Any]):
        """Log agent action for monitoring"""
        self.logger.info(f"Action: {action}, Inputs: {list(inputs.keys())}, Status: {outputs.get('status', 'unknown')}")
