import google.generativeai as genai
# from google.generativeai.types import 
from google.generativeai.types import StrictContentType
from .base_adapter import LLMChatAdapter
from config.config import GEMINI_API_KEY  # Ensure the Gemini API key is in the config file

class GeminiChatAdapter(LLMChatAdapter):
    def __init__(self, model_name: str = "gemini-pro"):
        super().__init__(model_name)
        # genai.api_key = GEMINI_API_KEY
        self.model_name = 'gemini-pro'
        genai.configure(api_key=GEMINI_API_KEY)
        self.chat_session = None

    def start_chat(self, history=None):
        model = genai.GenerativeModel(self.model_name)
        self.chat_session = model.start_chat(history=history)

    def _format_history(self, history):
        if not history:
            return []
        formatted_history = []
        for message in history:
            formatted_message = self._format_message(message)
            formatted_history.append(formatted_message)
        # return {"history": formatted_history}
        return formatted_history

    def _format_message(self, message):
        role = message.get('role')
        content = message.get('content')
        parts = [{"text": content}]
        if role == 'assistant':
            role = 'model'
        return {"role": role, "parts": parts}
    
    def chat(self, messages: list, stream: bool = False, **kwargs):
        print("In Chat:", messages)
        if self.chat_session is None:
            formatted_messages = self._format_history(history=messages)
            self.start_chat(history=formatted_messages)
        
        if stream:
            response = self.chat_session.send_message(messages[-1]['content'], stream=True, **kwargs)
            return response  # Return the stream generator
        else:
            response = self.chat_session.send_message(messages[-1]['content'], **kwargs)
            return response.text
        
    


