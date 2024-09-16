import uuid
from flask import Flask, request, jsonify, Response
import sys
sys.path.append('.')
from adapters.openai_adapter import OpenAIChatAdapter
# from adapters.anthropic_adapter import AnthropicChatAdapter
from adapters.gemini_adapter import GeminiChatAdapter
from factory.llm_factory import LLMChatFactory
from conversation.conversation_manager import ConversationManager

app = Flask(__name__)
factory = LLMChatFactory()
conversation_manager = ConversationManager()

# Register adapters with the factory
factory.register_adapter("openai", lambda: OpenAIChatAdapter())
# factory.register_adapter("anthropic", lambda: AnthropicChatAdapter())
factory.register_adapter("gemini", lambda: GeminiChatAdapter())

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    company_name = data.get("company_name", "openai")
    user_message = data["user_message"]
    stream = data.get("stream", False)
    model_name = data.get("model_name", "gpt-4")  # Default to a specific model if not provided
    
    # Check for session token
    session_id = data.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())  # Generate a new session token if not provided

    # Retrieve conversation history
    conversation_history = conversation_manager.get_conversation(session_id)
    # Add user message to history
    conversation_manager.add_message(session_id, 'user', user_message)
    # Get the adapter
    adapter = factory.get_adapter(company_name)
    adapter.set_model_name(model_name)
    
    if stream:
        def generate():
            response = adapter.chat(conversation_history, stream=True)
            compiled_message = ''
            for chunk in response:
                chunk_dict = chunk.dict()
                if 'content' in chunk_dict['choices'][0]['delta']:
                    content = chunk_dict['choices'][0]['delta']['content']
                    if content:
                        compiled_message += content + ''  # Append content and space for separation
            conversation_manager.add_message(session_id, 'assistant', compiled_message.strip())  # Strip trailing space
            yield compiled_message

        return Response(generate(), content_type='text/plain')

    else:
        response_message = adapter.chat(conversation_history)
        conversation_manager.add_message(session_id, 'assistant', response_message)
        
        return jsonify({"response": response_message, "session_id": session_id})

@app.route('/clear', methods=['POST'])
def clear():
    data = request.json
    session_id = data['session_id']
    
    # Clear the conversation history
    conversation_manager.clear_conversation(session_id)
    
    return jsonify({"status": "cleared"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)