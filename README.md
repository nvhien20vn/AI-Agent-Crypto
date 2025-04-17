# Crypto Market Analysis AI Agent

A LangChain-based AI agent for analyzing cryptocurrency markets, with memory persistence and integrated tools.

## Features

### 1. Core Functionality
- Built with LangChain and LangGraph
- Three-node graph architecture: START → LLM → END
- Integrated memory in LangGraph for contextual conversations
- JSON-based conversation history storage

### 2. Available Tools

The agent comes with three powerful crypto-analysis tools:

1. **crypto_price**
   - Get real-time cryptocurrency prices
   - Input: Coin symbol (e.g., 'BTC' or 'ETH')
   - Example: "What's the current price of BTC?"

2. **crypto_news**
   - Fetch latest cryptocurrency news
   - Input: Optional coin name for specific news
   - Example: "Show me the latest Bitcoin news"

3. **web_search**
   - Search for crypto-related information online
   - Input: Search query
   - Example: "Search for cryptocurrency mining impact"

### 3. Memory System

The agent includes a robust memory system that:
- Persists conversation history in JSON format
- Stores all types of messages (Human, AI, Function calls)
- Maintains timestamp information
- Allows loading of recent conversations
- Supports future memory analysis and pattern recognition

## Usage

1. Start the agent:
```bash
python main.py
```

2. The agent will display available tools and wait for your input
3. Type your questions or commands
4. Use 'quit', 'exit', or 'bye' to end the conversation

## Memory Storage

Conversations are stored in `memory_history.json` with the following structure:

```json
{
  "conversations": [
    {
      "timestamp": "2024-04-17T17:14:00",
      "messages": [
        {
          "type": "HumanMessage",
          "content": "What's the price of Bitcoin?",
          "timestamp": "2024-04-17T17:14:00"
        },
        {
          "type": "AIMessage",
          "content": "I'll check the current Bitcoin price for you.",
          "timestamp": "2024-04-17T17:14:01",
          "tool_calls": [...]
        },
        {
          "type": "FunctionMessage",
          "content": "BTC/USD: $63,245.00",
          "timestamp": "2024-04-17T17:14:02",
          "name": "crypto_price",
          "tool_call_id": "call_123"
        }
      ]
    }
  ]
}
```

## Future Extensions

The system is designed for easy extension with additional features:
- Add new tool_calling functions
- Implement advanced memory analysis
- Add more data sources and APIs
- Extend conversation context loading
