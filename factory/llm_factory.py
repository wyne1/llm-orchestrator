from adapters.base_adapter import LLMChatAdapter
from typing import Type, Callable

class LLMChatFactory:
    def __init__(self):
        self.adapters = {}

    def register_adapter(self, model_name: str, adapter_creator: Callable[[], LLMChatAdapter]):
        self.adapters[model_name] = adapter_creator

    def get_adapter(self, model_name: str) -> LLMChatAdapter:
        if model_name in self.adapters:
            return self.adapters[model_name]()
        else:
            raise ValueError(f"No adapter registered for model: {model_name}")