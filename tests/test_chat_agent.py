"""
Test suite for ChatAgent

This module tests the ChatAgent functionality including conversation management,
research detection, and tool integration.
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path to import inference modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.chat_agent import ChatAgent


class TestChatAgentBasic(unittest.TestCase):
    """Basic test cases for ChatAgent class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Mock environment variable
        with patch.dict(os.environ, {'GLM_API_KEY': 'test_key'}):
            # Create chat agent with mocked dependencies
            with patch('inference.chat_agent.OpenAI') as mock_openai, \
                 patch('inference.chat_agent.ResearchTool') as mock_research_tool_class:

                # Mock OpenAI client
                mock_client = Mock()
                mock_response = Mock()
                mock_response.choices = [Mock()]
                mock_response.choices[0].message.content = "Test response"
                mock_client.chat.completions.create.return_value = mock_response
                mock_openai.return_value = mock_client

                # Mock ResearchTool
                mock_research_tool = Mock()
                mock_research_tool.call.return_value = "Research result here"
                mock_research_tool.get_research_stats.return_value = {"llm_calls": 1}
                mock_research_tool_class.return_value = mock_research_tool

                self.chat_agent = ChatAgent()
                self.mock_client = mock_client
                self.mock_research_tool = mock_research_tool

    def test_initialization(self):
        """Test ChatAgent initialization."""
        self.assertIsNotNone(self.chat_agent.client)
        self.assertIsNotNone(self.chat_agent.research_tool)
        self.assertEqual(len(self.chat_agent.messages), 0)
        self.assertFalse(self.chat_agent.is_research_mode)
        self.assertIsNone(self.chat_agent.pending_research_result)

    def test_system_prompt_creation(self):
        """Test system prompt creation."""
        prompt = self.chat_agent.system_prompt
        self.assertIn("helpful AI assistant", prompt)
        self.assertIn("research capabilities", prompt)
        self.assertIn("conversation", prompt.lower())

    def test_research_request_detection(self):
        """Test detection of research requests."""
        # Research requests
        research_requests = [
            "research quantum computing",
            "tell me about AI",
            "what is machine learning",
            "investigate climate change",
            "find information about renewable energy",
            "latest developments in blockchain"
        ]

        for request in research_requests:
            with self.subTest(request=request):
                self.assertTrue(self.chat_agent._is_research_request(request))

        # Non-research requests
        non_research_requests = [
            "hello how are you",
            "what's the weather",
            "tell me a joke",
            "good morning",
            "how are you doing"
        ]

        for request in non_research_requests:
            with self.subTest(request=request):
                self.assertFalse(self.chat_agent._is_research_request(request))

    def test_clarification_needed_detection(self):
        """Test detection of questions needing clarification."""
        # Questions needing clarification
        unclear_questions = [
            "tell me about AI",
            "what is ML",
            "research it",
            "information about tech",
            "quantum",
            "ai"
        ]

        for question in unclear_questions:
            with self.subTest(question=question):
                self.assertTrue(self.chat_agent._should_ask_for_clarification(question))

        # Specific questions not needing clarification
        specific_questions = [
            "What are the latest applications of artificial intelligence in healthcare in 2024?",
            "How does quantum computing work and what are its practical applications?",
            "Research the ethical implications of AI in hiring processes for large corporations"
        ]

        for question in specific_questions:
            with self.subTest(question=question):
                self.assertFalse(self.chat_agent._should_ask_for_clarification(question))

    def test_tool_call_detection(self):
        """Test detection of tool calls in LLM responses."""
        # Valid tool call
        tool_call_response = '{"name": "research", "arguments": {"research_quest": "test query"}}'
        tool_calls = self.chat_agent._detect_tool_calls(tool_call_response)
        self.assertEqual(len(tool_calls), 1)
        self.assertEqual(tool_calls[0]['name'], 'research')
        self.assertEqual(tool_calls[0]['arguments']['research_quest'], 'test query')

        # No tool call
        normal_response = "This is a normal response without any tool calls."
        tool_calls = self.chat_agent._detect_tool_calls(normal_response)
        self.assertEqual(len(tool_calls), 0)

        # Invalid JSON
        invalid_response = '{"name": "research", "arguments": {"research_quest": "test query"'  # Missing closing brace
        tool_calls = self.chat_agent._detect_tool_calls(invalid_response)
        self.assertEqual(len(tool_calls), 0)

    def test_research_tool_execution(self):
        """Test execution of research tool."""
        result = self.chat_agent._execute_research_tool("test query")
        self.mock_research_tool.call.assert_called_once_with({"research_quest": "test query"})
        self.assertEqual(result, "Research result here")

    def test_clarification_questions_generation(self):
        """Test generation of clarification questions."""
        clarification = self.chat_agent._generate_clarification_questions("AI")
        self.assertIn("help clarify", clarification.lower())
        self.assertIn("specific focus", clarification.lower())
        self.assertIn("time range", clarification.lower())

    def test_research_result_formatting(self):
        """Test formatting of research results for chat."""
        research_result = """📋 Research Report: Test Question
==========================================================================
📊 Research Statistics:
• LLM Calls: 3

Test content here
==================================================
🔍 Research completed using ReActAgent methodology"""

        formatted = self.chat_agent._format_research_result_for_chat(research_result)
        self.assertIn("📊 **Research Results**", formatted)
        self.assertIn("Test content here", formatted)
        self.assertNotIn("📋 Research Report:", formatted)  # Header should be removed

    def test_normal_conversation(self):
        """Test normal conversation flow."""
        # Mock LLM response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Hello! How can I help you today?"
        self.mock_client.chat.completions.create.return_value = mock_response

        user_message = "Hello, how are you?"
        response = self.chat_agent.chat(user_message)

        # Verify response
        self.assertEqual(response, "Hello! How can I help you today?")
        self.assertEqual(len(self.chat_agent.messages), 2)  # User + Assistant
        self.assertEqual(self.chat_agent.messages[0]["role"], "user")
        self.assertEqual(self.chat_agent.messages[0]["content"], user_message)
        self.assertEqual(self.chat_agent.messages[1]["role"], "assistant")

    def test_research_conversation_with_tool_call(self):
        """Test conversation with research tool call."""
        # Mock LLM response with tool call
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '{"name": "research", "arguments": {"research_quest": "What is quantum computing?"}}'
        self.mock_client.chat.completions.create.return_value = mock_response

        user_message = "research quantum computing applications and current developments in 2024"
        response = self.chat_agent.chat(user_message)

        # Verify research tool was called
        self.mock_research_tool.call.assert_called_once_with({"research_quest": "What is quantum computing?"})

        # Verify pending research result is set
        self.assertIsNotNone(self.chat_agent.pending_research_result)
        self.assertIn("Conducting Research", response)

    def test_pending_research_result_delivery(self):
        """Test delivery of pending research results."""
        # Set up pending research result
        self.chat_agent.pending_research_result = "📊 **Research Results**\n\nHere's the research result..."

        # Get next response
        response = self.chat_agent.chat("any message")

        # Should return pending result and clear it
        self.assertEqual(response, "📊 **Research Results**\n\nHere's the research result...")
        self.assertIsNone(self.chat_agent.pending_research_result)

    def test_conversation_history_management(self):
        """Test conversation history management."""
        # Add some messages
        self.chat_agent.messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]

        history = self.chat_agent.get_conversation_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["content"], "Hello")
        self.assertEqual(history[1]["content"], "Hi there!")

    def test_conversation_reset(self):
        """Test conversation reset functionality."""
        # Set up some state
        self.chat_agent.messages = [{"role": "user", "content": "test"}]
        self.chat_agent.is_research_mode = True
        self.chat_agent.pending_research_result = "pending"

        # Reset
        self.chat_agent.reset_conversation()

        # Verify state is cleared
        self.assertEqual(len(self.chat_agent.messages), 0)
        self.assertFalse(self.chat_agent.is_research_mode)
        self.assertIsNone(self.chat_agent.pending_research_result)

    def test_stats_collection(self):
        """Test statistics collection."""
        # Set up some state
        self.chat_agent.messages = [{"role": "user"}, {"role": "assistant"}]

        stats = self.chat_agent.get_stats()
        self.assertEqual(stats["conversation_length"], 2)
        self.assertFalse(stats["is_research_mode"])
        self.assertFalse(stats["has_pending_research"])
        self.assertIn("research_stats", stats)

    def test_error_handling_in_chat(self):
        """Test error handling in chat method."""
        # Mock LLM to raise exception
        self.mock_client.chat.completions.create.side_effect = Exception("API Error")

        user_message = "Hello"
        response = self.chat_agent.chat(user_message)

        # Should handle error gracefully
        self.assertIn("encountered an error", response)
        self.assertIn("API Error", response)

    def test_empty_message_handling(self):
        """Test handling of empty messages."""
        # Should not add empty messages to conversation
        initial_length = len(self.chat_agent.messages)
        self.chat_agent.chat("")  # Empty string
        self.chat_agent.chat("   ")  # Whitespace only

        # No messages should be added
        self.assertEqual(len(self.chat_agent.messages), initial_length)


class TestChatAgentIntegration(unittest.TestCase):
    """Integration tests for ChatAgent (requires API keys)."""

    @unittest.skipUnless(os.getenv('GLM_API_KEY'), "GLM_API_KEY required for integration test")
    def test_integration_with_real_api(self):
        """Test ChatAgent with real API (if GLM_API_KEY is available)."""
        try:
            agent = ChatAgent()

            # Test basic conversation
            response = agent.chat("Hello, can you help me?")
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)

            # Test conversation history
            history = agent.get_conversation_history()
            self.assertGreaterEqual(len(history), 2)  # At least user + assistant

            # Test stats
            stats = agent.get_stats()
            self.assertIn("conversation_length", stats)
            self.assertGreater(stats["conversation_length"], 0)

        except Exception as e:
            self.fail(f"Integration test failed: {str(e)}")


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)