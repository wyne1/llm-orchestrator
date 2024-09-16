import openai
from .base_adapter import LLMChatAdapter
import json

# class GPT4ChatAdapter(LLMChatAdapter):
#     def __init__(self, api_key: str):
#         super().__init__(api_key)

#     def chat(self, messages: list, **kwargs):
#         openai.api_key = self.api_key
#         response = openai.chat.completions.create(
#             model="gpt-4",
#             messages=messages,
#             **kwargs
#         )

#         response = json.loads(response.model_dump_json())
#         print(response)
#         return response['choices'][0]['message']['content']
#         # return response.choices[0].message['content']

class GPTChatAdapter(LLMChatAdapter):
    def __init__(self, api_key: str):
        super().__init__(api_key)

    def chat(self, messages: list, stream: bool = False, **kwargs):
        openai.api_key = self.api_key
        
        if stream:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=messages,
                stream=True,
                **kwargs
            )
            # response = json.loads(response.model_dump_json())
            return response  # Return the stream generator
        else:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=messages,
                **kwargs
            )
            return response.choices[0].message['content']
        

