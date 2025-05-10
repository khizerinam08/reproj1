"""
Integration tests for the LLM chatbot components.
"""
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.memory.conversation import ConversationMemory
from src.llm.ollama_client import OllamaClient


class TestIntegration(unittest.TestCase):
    """Integration test cases for the chatbot components."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create memory component
        self.memory = ConversationMemory()
        
        # Mock the Ollama client to avoid actual API calls during testing
        self.ollama_client = MagicMock(spec=OllamaClient)
        self.ollama_client.generate_response.return_value = "This is a mock response."
        
    def test_memory_and_llm_integration(self):
        """Test that memory and LLM components can work together."""
        # Add messages to memory
        self.memory.add_system_message("You are a helpful assistant.")
        self.memory.add_user_message("Hello, how are you?")
        
        # Generate a prompt from memory
        prompt = self.memory.get_formatted_prompt()
        
        # Verify prompt format
        self.assertIn("System: You are a helpful assistant.", prompt)
        self.assertIn("User: Hello, how are you?", prompt)
        
        # Send prompt to LLM
        response = self.ollama_client.generate_response(prompt)
        
        # Verify response is received
        self.assertEqual(response, "This is a mock response.")
        
        # Add AI response to memory
        self.memory.add_ai_message(response)
        
        # Verify memory now contains the AI response
        messages = self.memory.get_messages()
        self.assertEqual(len(messages), 3)
        self.assertEqual(messages[2].content, "This is a mock response.")
        
    def test_conversation_flow(self):
        """Test a full conversation flow with memory integration."""
        # Start with system message
        self.memory.add_system_message("You are a helpful assistant.")
        
        # First user turn
        self.memory.add_user_message("What's the weather like?")
        prompt1 = self.memory.get_formatted_prompt()
        response1 = self.ollama_client.generate_response(prompt1)
        self.memory.add_ai_message(response1)
        
        # Second user turn
        self.memory.add_user_message("How about tomorrow?")
        prompt2 = self.memory.get_formatted_prompt()
        
        # Verify that prompt2 contains the first exchange
        self.assertIn("User: What's the weather like?", prompt2)
        self.assertIn("Assistant: This is a mock response.", prompt2)
        self.assertIn("User: How about tomorrow?", prompt2)


if __name__ == "__main__":
    unittest.main() 