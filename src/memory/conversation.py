"""
Memory management for the LLM chatbot using LangChain.
Provides functionality to store, retrieve, and manage conversation history.
"""
from typing import List
import os
import yaml
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage

class ConversationMemory:
    """
    Manages conversation history for the chatbot using LangChain memory classes.
    """
    
    def __init__(self, max_token_limit: int = 4000):
        """
        Initialize the conversation memory.
        
        Args:
            max_token_limit: Maximum number of tokens to keep in memory
        """
        self.messages = []
        self.max_token_limit = max_token_limit
        
    def add_user_message(self, message: str) -> None:
        """
        Add a user message to the conversation history.
        
        Args:
            message: The user's message
        """
        self.messages.append(HumanMessage(content=message))
        self._check_memory_limit()
        
    def add_ai_message(self, message: str) -> None:
        """
        Add an AI message to the conversation history.
        
        Args:
            message: The AI's message
        """
        self.messages.append(AIMessage(content=message))
        self._check_memory_limit()
        
    def add_system_message(self, message: str) -> None:
        """
        Add a system message to the conversation history.
        
        Args:
            message: The system message
        """
        self.messages.append(SystemMessage(content=message))
        # No need to check memory limit for system messages as they're typically few and important
        
    def get_messages(self) -> List[BaseMessage]:
        """
        Get all messages in the conversation history.
        
        Returns:
            List of message objects
        """
        return self.messages
        
    def clear(self) -> None:
        """
        Clear the conversation history.
        """
        self.messages = []
        
    def _estimate_token_count(self, text: str) -> int:
        """
        Estimate the number of tokens in text using a simple heuristic.
        
        Args:
            text: Input text
            
        Returns:
            Estimated token count
        """
        # A simple approximation: 4 characters per token on average
        return len(text) // 4
        
    def _check_memory_limit(self) -> None:
        """
        Check if the conversation history exceeds the token limit and truncate if necessary.
        """
        # Skip if no messages or just a few
        if len(self.messages) <= 3:
            return
            
        # Estimate total tokens
        total_tokens = sum(self._estimate_token_count(msg.content) for msg in self.messages)
        
        # If under the limit, nothing to do
        if total_tokens <= self.max_token_limit:
            return
            
        # First, keep all system messages
        system_messages = [msg for msg in self.messages if msg.type == "system"]
        
        # Then get user and AI messages, keeping pairs together
        conversation_messages = [msg for msg in self.messages if msg.type != "system"]
        
        # Keep truncating from the oldest messages until we're under the limit
        while conversation_messages and total_tokens > self.max_token_limit:
            # Remove the oldest message
            oldest_msg = conversation_messages.pop(0)
            total_tokens -= self._estimate_token_count(oldest_msg.content)
            
            # If next message is also from the same exchange, remove it too to maintain pairs
            if conversation_messages and oldest_msg.type != conversation_messages[0].type:
                next_msg = conversation_messages.pop(0)
                total_tokens -= self._estimate_token_count(next_msg.content)
        
        # Combine system messages and remaining conversation messages
        self.messages = system_messages + conversation_messages
        
    def get_formatted_prompt(self, include_system_messages: bool = True) -> str:
        """
        Format conversation history into a prompt string for the LLM.
        
        Args:
            include_system_messages: Whether to include system messages in the prompt
            
        Returns:
            Formatted prompt string
        """
        formatted_messages = []
        
        for message in self.messages:
            if message.type == "system":
                if include_system_messages:
                    formatted_messages.append(f"System: {message.content}")
            elif message.type == "human":
                formatted_messages.append(f"User: {message.content}")
            elif message.type == "ai":
                formatted_messages.append(f"Assistant: {message.content}")
        
        return "\n".join(formatted_messages)
        
    def save_conversation(self, file_path: str) -> bool:
        """
        Save the conversation history to a file.
        
        Args:
            file_path: Path to save the conversation
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Convert messages to a serializable format
            serialized_messages = []
            for msg in self.messages:
                serialized_messages.append({
                    'type': msg.type,
                    'content': msg.content
                })
            
            # Save to file
            with open(file_path, 'w', encoding='utf-8') as file:
                yaml.dump({'messages': serialized_messages}, file, default_flow_style=False)
                
            return True
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False
            
    def load_conversation(self, file_path: str) -> bool:
        """
        Load conversation history from a file.
        
        Args:
            file_path: Path to the conversation file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                return False
                
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                
            if not data or 'messages' not in data:
                return False
                
            # Clear current messages
            self.clear()
            
            # Load messages
            for msg_data in data['messages']:
                msg_type = msg_data.get('type')
                content = msg_data.get('content')
                
                if msg_type == 'human':
                    self.add_user_message(content)
                elif msg_type == 'ai':
                    self.add_ai_message(content)
                elif msg_type == 'system':
                    self.add_system_message(content)
                    
            return True
        except Exception as e:
            print(f"Error loading conversation: {e}")
            return False 