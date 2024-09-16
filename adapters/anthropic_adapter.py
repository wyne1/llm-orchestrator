import anthropic
from .base_adapter import LLMChatAdapter
from config.config import ANTHROPIC_API_KEY

class AnthropicChatAdapter(LLMChatAdapter):
    def __init__(self, model_name: str = "claude-3-5-sonnet-20240620"):
        super().__init__(model_name)
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def chat(self, messages: list, stream: bool = False, **kwargs):
        formatted_messages = self._format_history(messages)
        # formatted_messages += "\n\nAssistant:"
        max_tokens_to_sample = kwargs.get('max_tokens_to_sample', 100)  # Set a default value for max_tokens_to_sample
        
        print(f"Formatted Messages: {formatted_messages}")
        print(f"Messages: {messages}")

        if stream:
            return "not implemented"
        
        else:
            response = self.client.messages.create(
                model = self.model_name,
                messages = messages,
                max_tokens= 1024,
            )

            print(f"Claude Response: {response.content}")
            return response.content[0].text
        # if stream:

        #     message = self.client.messages.create(
        #         model="claude-3-5-sonnet-20240620",
        #         max_tokens=1024,
        #         messages=[
        #             {"role": "user", "content": "Hello, Claude"}
        #         ]
        #     )
            
        #     response = self.client.completions.create(
        #         model=self.model_name,
        #         prompt=formatted_messages,
        #         max_tokens_to_sample=max_tokens_to_sample,
        #         stream=True,
        #         **kwargs
        #     )
        #     return self._stream_response(response)
        # else:
        #     response = self.client.completions.create(
        #         model=self.model_name,
        #         prompt=formatted_messages,
        #         max_tokens_to_sample=max_tokens_to_sample,
        #         **kwargs
        #     )
        #     return response.completion

    def add_to_history(self, message_type: str, content: str):
        # This method can be used if you want to maintain additional internal state
        pass

    def _format_history(self, history):
        formatted_history = ""
        for message in history:
            role = message.get('role')
            content = message.get('content')
            if role == 'user':
                formatted_history += f"\n\nHuman: {content}"
            elif role == 'assistant':
                formatted_history += f"\n\nAssistant: {content}"
        return formatted_history.strip()

    def _stream_response(self, response):
        for chunk in response:
            if chunk.completion:
                yield chunk.completion

    def set_model_name(self, model_name: str):
        self.model_name = model_name