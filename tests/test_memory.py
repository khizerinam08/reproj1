"""
Tests for the conversation memory module.
"""
import os
import sys
import unittest
import tempfile

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.memory.conversation import ConversationMemory


class TestConversationMemory(unittest.TestCase):
    """Test cases for the ConversationMemory class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.memory = ConversationMemory()
        
    def test_add_messages(self):
        """Test adding different types of messages."""
        self.memory.add_system_message("You are a helpful assistant.")
        self.memory.add_user_message("Hello, how are you?")
        self.memory.add_ai_message("I'm doing well, thank you for asking!")
        
        messages = self.memory.get_messages()
        self.assertEqual(len(messages), 3)
        self.assertEqual(messages[0].type, "system")
        self.assertEqual(messages[1].type, "human")
        self.assertEqual(messages[2].type, "ai")
        
    def test_formatted_prompt(self):
        """Test generating a formatted prompt from messages."""
        self.memory.add_system_message("You are a helpful assistant.")
        self.memory.add_user_message("Hello, how are you?")
        self.memory.add_ai_message("I'm doing well, thank you for asking!")
        
        # With system messages
        prompt_with_system = self.memory.get_formatted_prompt(include_system_messages=True)
        self.assertIn("System: You are a helpful assistant.", prompt_with_system)
        self.assertIn("User: Hello, how are you?", prompt_with_system)
        
        # Without system messages
        prompt_without_system = self.memory.get_formatted_prompt(include_system_messages=False)
        self.assertNotIn("System:", prompt_without_system)
        self.assertIn("User: Hello, how are you?", prompt_without_system)
        
    def test_save_and_load(self):
        """Test saving and loading conversations."""
        self.memory.add_system_message("You are a helpful assistant.")
        self.memory.add_user_message("Hello, how are you?")
        self.memory.add_ai_message("I'm doing well, thank you for asking!")
        
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(delete=False, suffix='.yml') as temp_file:
            temp_path = temp_file.name
            
        try:
            # Save conversation
            success = self.memory.save_conversation(temp_path)
            self.assertTrue(success)
            
            # Create a new memory instance and load the conversation
            new_memory = ConversationMemory()
            success = new_memory.load_conversation(temp_path)
            self.assertTrue(success)
            
            # Verify loaded messages
            messages = new_memory.get_messages()
            self.assertEqual(len(messages), 3)
            self.assertEqual(messages[0].type, "system")
            self.assertEqual(messages[0].content, "You are a helpful assistant.")
            self.assertEqual(messages[1].type, "human")
            self.assertEqual(messages[2].type, "ai")
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    def test_memory_limit(self):
        """Test that memory limits are enforced."""
        # Create memory with a small token limit
        limited_memory = ConversationMemory(max_token_limit=20)
        
        # Add a system message
        limited_memory.add_system_message("System instruction")
        
        # Add user and AI messages
        limited_memory.add_user_message("First user message")
        limited_memory.add_ai_message("First AI response")
        limited_memory.add_user_message("Second user message with more text")
        
        # This should have triggered truncation
        messages = limited_memory.get_messages()
        
        # System message should always be preserved
        self.assertIn("System instruction", messages[0].content)
        
        # There should be fewer than or equal to 4 messages due to truncation
        self.assertLessEqual(len(messages), 4)


if __name__ == "__main__":
    unittest.main() 