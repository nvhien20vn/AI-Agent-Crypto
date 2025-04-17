from typing import Dict
from src.agent import create_agent, AgentState
from src.memory_manager import MemoryManager
from langchain_core.messages import HumanMessage, BaseMessage
from settings.config import LLM_CONF

# Tool Documentation
TOOL_DOCUMENTATION = """
Available Crypto Analysis Tools:
1. crypto_price: Get real-time cryptocurrency prices
   - Input: Coin symbol (e.g., 'BTC' or 'ETH')
   - Example: "What's the current price of BTC?"

2. crypto_news: Get latest cryptocurrency news
   - Input: Optional coin name for specific news
   - Example: "Show me the latest Bitcoin news"

3. web_search: Search for crypto-related information
   - Input: Search query
   - Example: "Search for cryptocurrency mining impact"
"""

# Define initial state creation here
def create_initial_state(initial_message: str = None) -> Dict:
    """Create the initial state for the agent."""
    user_message = initial_message or "Analyze the crypto market."
    # Ensure the state matches the AgentState structure used in the graph
    return {"messages": [HumanMessage(content=user_message)]}

def main():
    # Create the agent and memory manager
    agent = create_agent(LLM_CONF["openai"])
    memory_manager = MemoryManager()

    # Initial message or prompt
    print("Starting Crypto Market Analysis AI...")
    print("\nℹ️  Tool Information:")
    print(TOOL_DOCUMENTATION)
    initial_input = input("You: (Press Enter for default 'Analyze the crypto market.') ")
    state = create_initial_state(initial_input or None)

    try:
        # Run the agent conversation loop
        while True:
            # Invoke the agent with the current state
            # The agent graph will append messages internally
            # For invoke, the final state is returned
            # If using stream, you'd iterate through events
            print("AI is thinking...")
            final_state = agent.invoke(state)

            # Get the latest AI message
            ai_message = final_state["messages"][-1]
            print("\nAI:", ai_message.content)

            # Check if the conversation should end (optional, based on AI response or user input)
            # if "goodbye" in ai_message.content.lower():
            #    break
            
            # Get next user input
            user_input = input("\nYou: ")
            if user_input.lower() in ['quit', 'exit', 'bye']:
                break

            # Save conversation to JSON file after each interaction
            memory_manager.save_conversation(final_state["messages"])
            
            # Update state with conversation history
            state = {"messages": final_state["messages"] + [HumanMessage(content=user_input)]}
            
    except KeyboardInterrupt:
        print("\nExiting...")
    
    print("\nThank you for using the Crypto Market Analysis AI!")

if __name__ == "__main__":
    main()
