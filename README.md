# LLM Orchestrator

LLM Orchestrator is a Python project that provides a unified interface for interacting with various Large Language Models (LLMs) such as OpenAI's GPT, Anthropic's Claude, and Google's Gemini. This project aims to simplify the process of integrating and switching between different LLM providers in your applications.

## Features

- Unified API for multiple LLM providers
- Support for OpenAI, Anthropic, and Google Gemini
- Easy to extend for additional LLM providers
- Conversation history management
- Configurable API key management

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/wyne1/llm-orchestrator.git
   cd llm-orchestrator
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Copy `config/config.example.py` to `config/config.py`
2. Replace the placeholder values in `config/config.py` with your actual API keys

Alternatively, you can use environment variables:

1. Copy `.env.example` to `.env`
2. Replace the placeholder values in `.env` with your actual API keys

## Usage

Here's a basic example of how to use the LLM Adapters:
```
from adapters import OpenAIAdapter, AnthropicAdapter, GeminiAdapter 
```

Choose your preferred adapter
```
adapter = OpenAIAdapter() # or AnthropicAdapter() or GeminiAdapter()
```

Start a conversation
```
response = adapter.chat("Hello, how are you?")
print(response)
```
Continue the conversation
```
response = adapter.chat("Tell me a joke")
print(response)
```


## Project Structure

- `adapters/`: Contains the adapter classes for each LLM provider
  - `base_adapter.py`: Base class for all adapters
  - `openai_adapter.py`: Adapter for OpenAI's GPT
  - `anthropic_adapter.py`: Adapter for Anthropic's Claude
  - `gemini_adapter.py`: Adapter for Google's Gemini
- `config/`: Configuration files
- `app.py`: Main application file
- `testing.ipynb`: Jupyter notebook for testing adapters

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Acknowledgments

- OpenAI for their GPT models
- Anthropic for Claude
- Google for Gemini

## Disclaimer

This project is not officially affiliated with or endorsed by OpenAI, Anthropic, or Google. Please ensure you comply with each provider's terms of service when using their APIs.