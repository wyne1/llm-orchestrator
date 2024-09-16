import openai
from .base_adapter import LLMChatAdapter
from config.config import OPENAI_API_KEY  # Ensure the OpenAI API key is in the config file
import json

class OpenAIChatAdapter(LLMChatAdapter):
    def __init__(self, model_name: str = "gpt-4"):
        super().__init__(model_name)
        self.api_key = OPENAI_API_KEY

    def chat(self, messages: list, stream: bool = False, **kwargs):
        openai.api_key = self.api_key
        
        if stream:
            response = openai.chat.completions.create(
                model=self.model_name,
                messages=messages,
                stream=True,
                **kwargs
            )
            return response  # Return the stream generator
        else:
            response = openai.chat.completions.create(
                model=self.model_name,
                messages=messages,
                **kwargs
            )

            response = json.loads(response.model_dump_json())
            print(f"response: {response}")
            return response['choices'][0]['message']['content']