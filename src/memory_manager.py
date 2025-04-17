import json
import os
from typing import List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, FunctionMessage
from datetime import datetime

class MemoryManager:
    def __init__(self, file_path: str = "memory_history.json"):
        self.file_path = file_path
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Create the JSON file if it doesn't exist."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump({"conversations": []}, f, indent=2)

    def serialize_message(self, message: BaseMessage) -> dict:
        """Convert a LangChain message to a serializable dict."""
        base = {
            "type": message.__class__.__name__,
            "content": message.content,
            "timestamp": datetime.now().isoformat()
        }
        
        # Handle special cases for different message types
        if isinstance(message, FunctionMessage):
            base["name"] = message.name
            base["tool_call_id"] = message.tool_call_id
        
        if hasattr(message, 'tool_calls') and message.tool_calls:
            base["tool_calls"] = message.tool_calls

        return base

    def deserialize_message(self, data: dict) -> BaseMessage:
        """Convert a serialized dict back to a LangChain message."""
        msg_type = data["type"]
        content = data["content"]
        
        if msg_type == "HumanMessage":
            return HumanMessage(content=content)
        elif msg_type == "AIMessage":
            msg = AIMessage(content=content)
            if "tool_calls" in data:
                msg.tool_calls = data["tool_calls"]
            return msg
        elif msg_type == "FunctionMessage":
            return FunctionMessage(
                content=content,
                name=data.get("name", ""),
                tool_call_id=data.get("tool_call_id", "")
            )
        else:
            raise ValueError(f"Unknown message type: {msg_type}")

    def save_conversation(self, messages: List[BaseMessage]):
        """Save the current conversation to the JSON file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {"conversations": []}

        # Convert messages to serializable format
        serialized_messages = [self.serialize_message(msg) for msg in messages]
        
        # Add as a new conversation
        data["conversations"].append({
            "timestamp": datetime.now().isoformat(),
            "messages": serialized_messages
        })

        # Write back to file
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_recent_conversations(self, limit: int = 5) -> List[List[BaseMessage]]:
        """Load the most recent conversations."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

        conversations = data.get("conversations", [])
        recent_convs = conversations[-limit:] if limit else conversations
        
        return [
            [self.deserialize_message(msg) for msg in conv["messages"]]
            for conv in recent_convs
        ]
