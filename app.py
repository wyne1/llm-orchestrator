import uuid
from fastapi import FastAPI, Request, HTTPException,Response
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn
from adapters.openai_adapter import OpenAIChatAdapter
from adapters.anthropic_adapter import AnthropicChatAdapter
from adapters.gemini_adapter import GeminiChatAdapter
from factory.llm_factory import LLMChatFactory
from conversation.conversation_manager import ConversationManager
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
factory = LLMChatFactory()
conversation_manager = ConversationManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with the specific origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register adapters with the factory
factory.register_adapter("openai", lambda: OpenAIChatAdapter())
factory.register_adapter("anthropic", lambda: AnthropicChatAdapter())
factory.register_adapter("gemini", lambda: GeminiChatAdapter())


@app.post('/chat')
async def chat(request: Request):
    data = await request.json()
    company_name = data.get("company_name", "openai")
    user_message = data["user_message"]
    stream = data.get("stream", False)
    model_name = data.get("model_name", "gpt-4")  # Default to a specific model if not provided
    
    # Check for session token
    session_id = data.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())  # Generate a new session token if not provided

    print("Session ID:", session_id)
    print("Conversation History")
    # Retrieve conversation history
    conversation_history = conversation_manager.get_conversation(session_id)
    # Add user message to history
    conversation_manager.add_message(session_id, 'user', user_message)
    # Get the adapter]
    print("Getting Adapter")
    adapter = factory.get_adapter(company_name)
    adapter.set_model_name(model_name)
    
    if stream:
        def generate():
            response = adapter.chat(conversation_history, stream=True)
            print("API RESPONSE: ", response)
            compiled_message = ''
            for chunk in response:
                if chunk.dict()['choices'][0]['finish_reason'] == 'stop':
                    print("Stream Ended")
                    break
                chunk_dict = chunk.dict()
                if 'content' in chunk_dict['choices'][0]['delta']:
                    content = chunk_dict['choices'][0]['delta']['content']
                    if content:
                        compiled_message += content + ' '  # Append content and space for separation
                        yield content
            # conversation_manager.add_message(session_id, 'assistant', compiled_message.strip())  # Strip trailing space
            
        # return StreamingResponse(generate(), media_type="application/x-ndjson")
        return StreamingResponse(generate(), media_type="text/event-stream")
        # return Response(content=generate(), media_type='text/plain')

    else:
        response_message = adapter.chat(conversation_history)
        conversation_manager.add_message(session_id, 'assistant', response_message)
        resp = {"message": response_message, "session_id": session_id}
        
        return JSONResponse(content=resp, status_code=200)

@app.post('/clear')
async def clear(request: Request):
    data = await request.json()
    session_id = data['session_id']
    
    # Clear the conversation history
    conversation_manager.clear_conversation(session_id)
    
    return {"status": "cleared"}


if __name__ == "__main__":
    uvicorn.run("app:app",host="0.0.0.0", port=5000, reload=False, workers=3, log_level="info")