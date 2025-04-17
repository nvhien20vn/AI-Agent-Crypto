# nvhien-example1/src/agent.py
from typing import Dict, List, TypedDict, Annotated, Sequence, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from langgraph.prebuilt.tool_executor import ToolExecutor, ToolInvocation # Import ToolInvocation
from langgraph.graph.message import add_messages
# from langgraph.checkpoint.sqlite import SqliteSaver # Example checkpoint saver - Removed as it caused ModuleNotFoundError and is unused
from .search import get_crypto_tools

# Keep AgentState simple for add_messages
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def create_agent(llm_config: dict) -> StateGraph:
    """Create the crypto market analysis agent using standard LangGraph patterns."""
    config = llm_config.copy()
    provider = config.pop('provider', None)
    model_name = config.pop('model_name', 'gpt-4o') # Default or from config
    config.pop('model', None)  # Remove 'model' if present to avoid duplicate argument
    llm = ChatOpenAI(model=model_name, **config) # Pass remaining config

    tools = get_crypto_tools()
    tool_executor = ToolExecutor(tools)

    # Bind tools to the LLM so it knows when to call them
    llm_with_tools = llm.bind_tools(tools)

    # Agent node: invokes LLM with tools. Output is an AIMessage potentially containing tool_calls.
    def agent_node(state: AgentState):
        print("---AGENT NODE---")
        messages = state["messages"]
        response = llm_with_tools.invoke(messages)
        # Append the response to existing messages
        return {"messages": messages + [response]}

    def tools_node(state: AgentState) -> Dict[str, List]:
        print("---TOOLS NODE---")
        messages = state.get("messages", [])
        if not messages:
            return {"messages": []}

        last_message = messages[-1]
        if not isinstance(last_message, AIMessage) or not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
            print("No tool calls found or last message is not AIMessage with tool_calls.")
            return {"messages": []}

        tool_calls = last_message.tool_calls
        print(f"Tool calls: {tool_calls}")

        tool_results = []
        for tool_call in tool_calls:
            print(f"Executing tool: {tool_call['name']} with args: {tool_call['args']}")
            tool_name = tool_call.get('name', '')
            tool_id = tool_call.get('id', '')
            tool_args = tool_call.get('args', {})

            try:
                # Convert tool call to expected format
                tool_input = tool_call["args"]["__arg1"] if "__arg1" in tool_call["args"] else ""
                
                # Get the actual tool from our tools list
                tool = next((t for t in tools if t.name == tool_name), None)
                if not tool:
                    raise ValueError(f"Tool {tool_name} not found")
                    
                # Call the tool's function directly
                output = tool.func(tool_input)
                print(f"Tool output: {output}")
                
                # Create function message for tool result
                tool_results.append(
                    ToolMessage(
                        tool_call_id=tool_id,
                        content=str(output),
                        name=tool_name
                    )
                )
            except Exception as e:
                print(f"Error executing tool {tool_name}: {e}")
                tool_results.append(
                    ToolMessage(
                        tool_call_id=tool_id,
                        content=f"Error executing tool {tool_name}: {str(e)}",
                        name=tool_name
                    )
                )

        # Append tool results to existing messages
        return {"messages": messages + tool_results}

    # Conditional edge logic
    def should_continue(state: AgentState) -> str:
        messages = state.get("messages", [])
        if not messages:
            return "__end__"
            
        last_message = messages[-1]
        
        # If the last message is an AIMessage with tool calls and no tool results yet
        if isinstance(last_message, AIMessage) and hasattr(last_message, "tool_calls") and last_message.tool_calls:
            # Check if we already have tool results for all tool calls
            tool_call_ids = {tc["id"] for tc in last_message.tool_calls}
            tool_results = [m for m in messages if isinstance(m, ToolMessage)]
            result_ids = {tr.tool_call_id for tr in tool_results}
            
            # If there are any tool calls without results, route to tools
            if not tool_call_ids.issubset(result_ids):
                print("Routing to tools")
                return "tools"
                
        # Otherwise, end the execution
        print("Routing to end")
        return "__end__"

    # Define the graph
    workflow = StateGraph(AgentState)

    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tools_node)

    workflow.set_entry_point("agent")

    # Conditional edge from agent
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "__end__": "__end__",
        }
    )

    # After tools are executed, return to the agent to process results
    workflow.add_edge("tools", "agent")

    # Compile the graph (add memory for multi-turn conversations)
    # memory = SqliteSaver.from_conn_string(":memory:") # Example in-memory checkpointing
    # graph = workflow.compile(checkpointer=memory)
    graph = workflow.compile() # Compile without memory first for simplicity

    return graph

# --- Potential changes needed in main.py ---
# Ensure create_initial_state uses HumanMessage and matches the simplified AgentState

# Example of how create_initial_state might look in main.py:
# from langchain_core.messages import HumanMessage
# def create_initial_state(initial_message: str = None) -> Dict:
#     user_message = initial_message or "Analyze the crypto market."
#     return {"messages": [HumanMessage(content=user_message)]}
