"""
Test suite for ReAct Agent

This module tests the ReAct Agent implementation including
LLM integration, tool execution, and conversation management.
"""

import unittest
import json
import sys
import os

# Add the parent directory to the path to import inference modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.react_agent import ReActAgent


class TestReActAgent(unittest.TestCase):
    """Test cases for ReAct Agent."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        import os
        if not os.getenv('GLM_API_KEY'):
            # Skip all tests if API key is not available
            self.skipTest("GLM_API_KEY not set, skipping all ReAct Agent tests")
        self.agent = ReActAgent()
    
    def test_agent_initialization(self):
        """Test that the agent initializes correctly."""
        self.assertIsNotNone(self.agent.client)
        self.assertEqual(self.agent.model, "glm-4.5-air")
        self.assertIn('search', self.agent.tools)
        self.assertIn('google_scholar', self.agent.tools)
        self.assertIn('visit', self.agent.tools)
        self.assertEqual(self.agent.llm_calls, 0)
        self.assertEqual(len(self.agent.messages), 0)
    
    def test_get_tools_signatures(self):
        """Test tools signature generation."""
        signatures = self.agent._get_tools_signatures()
        self.assertIn('<tools>', signatures)
        self.assertIn('</tools>', signatures)
        self.assertIn('search', signatures)
        self.assertIn('google_scholar', signatures)
        self.assertIn('visit', signatures)
        self.assertIn('"type": "function"', signatures)
    
    def test_create_system_prompt(self):
        """Test system prompt creation."""
        prompt = self.agent._create_system_prompt()
        self.assertIn('comprehensive research agent', prompt)
        self.assertIn('<tools>', prompt)
        self.assertIn('</tools>', prompt)
        self.assertIn('Tool Call Format:', prompt)
        self.assertIn('<answer>', prompt)
        self.assertIn('</answer>', prompt)
    
    def test_detect_tool_calls(self):
        """Test tool call detection in LLM responses."""
        # Test valid tool call
        response_with_tool = '''I need to search for information about Python.
{"name": "search", "arguments": {"query": "Python programming tutorial"}}'''
        
        tool_calls = self.agent._detect_tool_calls(response_with_tool)
        self.assertEqual(len(tool_calls), 1)
        self.assertEqual(tool_calls[0]['name'], 'search')
        self.assertEqual(tool_calls[0]['arguments']['query'], 'Python programming tutorial')
        
        # Test multiple tool calls
        response_with_multiple = '''Let me search for both web and academic sources.
{"name": "search", "arguments": {"query": "machine learning"}}
{"name": "google_scholar", "arguments": {"query": "deep learning research papers"}}'''
        
        tool_calls = self.agent._detect_tool_calls(response_with_multiple)
        self.assertEqual(len(tool_calls), 2)
        
        # Test no tool calls
        response_no_tools = "I don't need to search for anything right now."
        tool_calls = self.agent._detect_tool_calls(response_no_tools)
        self.assertEqual(len(tool_calls), 0)
    
    def test_execute_tool(self):
        """Test tool execution."""
        # Test valid tool
        result = self.agent._execute_tool('search', {'query': 'Python'})
        self.assertIsInstance(result, str)
        self.assertIn('search', result.lower())
        
        # Test invalid tool
        result = self.agent._execute_tool('invalid_tool', {})
        self.assertIn('not found', result)
    
    def test_should_exit(self):
        """Test exit condition detection."""
        # Test with answer tags
        self.assertTrue(self.agent._should_exit("Here is my <answer>final answer</answer>"))
        
        # Test without answer tags
        self.assertFalse(self.agent._should_exit("I need to search for more information"))
        
        # Test incomplete answer tags
        self.assertFalse(self.agent._should_exit("Here is my <answer>incomplete answer"))
    
    def test_estimate_tokens(self):
        """Test token estimation."""
        text = "This is a test text with some content."
        tokens = self.agent._estimate_tokens(text)
        self.assertIsInstance(tokens, int)
        self.assertGreater(tokens, 0)
        self.assertLess(tokens, len(text))  # Tokens should be less than characters
    
    def test_llm_call(self):
        """Test LLM API call with real API."""
        print("\n🔍 Testing real LLM API call...")
        
        # Check if API key is available
        import os
        if not os.getenv('GLM_API_KEY'):
            self.skipTest("GLM_API_KEY not set, skipping real API test")
        
        try:
            messages = [{"role": "user", "content": "What is 2+2? Just answer with the number."}]
            response = self.agent._llm_call(messages)
            
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)
            self.assertEqual(self.agent.llm_calls, 1)
            print(f"✓ Real LLM API call successful: {response[:100]}...")
            
        except Exception as e:
            self.fail(f"Real LLM API call failed: {e}")
    
    def test_reset(self):
        """Test agent reset functionality."""
        # Set some state
        self.agent.llm_calls = 5
        self.agent.messages = [{"role": "user", "content": "test"}]
        
        # Reset
        self.agent.reset()
        
        # Check state is cleared
        self.assertEqual(self.agent.llm_calls, 0)
        self.assertEqual(len(self.agent.messages), 0)
    
    def test_conversation_history(self):
        """Test conversation history retrieval."""
        self.agent.messages = [
            {"role": "system", "content": "System message"},
            {"role": "user", "content": "User message"},
            {"role": "assistant", "content": "Assistant message"}
        ]
        
        history = self.agent.get_conversation_history()
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]["role"], "system")
        self.assertEqual(history[1]["role"], "user")
        self.assertEqual(history[2]["role"], "assistant")
    
    def test_research_basic_flow(self):
        """Test basic research flow with real APIs."""
        print("\n🔍 Testing real research flow...")
        
        # Check if API keys are available
        import os
        if not os.getenv('GLM_API_KEY'):
            self.skipTest("GLM_API_KEY not set, skipping real API test")
        
        try:
            # Use a simple question that should have straightforward answers
            simple_question = "What is the capital of France?"
            print(f"📝 Research question: {simple_question}")
            
            # Run research with real APIs
            result = self.agent.research(simple_question)
            
            # Verify result contains relevant information
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 50)  # Should have substantial content
            
            # Should contain answer-related words (not exact match due to LLM variability)
            result_lower = result.lower()
            self.assertTrue(
                "paris" in result_lower or 
                "france" in result_lower or
                "capital" in result_lower,
                f"Result should contain information about France's capital. Got: {result_lower[:200]}..."
            )
            
            self.assertGreater(self.agent.llm_calls, 0)
            print(f"✓ Real research flow successful. LLM calls: {self.agent.llm_calls}")
            print(f"📋 Result preview: {result[:200]}...")
            
        except Exception as e:
            self.fail(f"Real research flow failed: {e}")
    
    def test_truncate_messages_if_needed(self):
        """Test message truncation when context limit is approached."""
        # Create many messages to simulate context overflow
        self.agent.messages = [{"role": "system", "content": "System"}]
        
        # Add many long messages
        for i in range(50):
            self.agent.messages.append({
                "role": "user" if i % 2 == 0 else "assistant",
                "content": "A" * 1000  # Long message
            })
        
        original_count = len(self.agent.messages)
        self.agent._truncate_messages_if_needed()
        
        # Should have fewer messages after truncation
        self.assertLess(len(self.agent.messages), original_count)
        # Should still have system message
        self.assertEqual(self.agent.messages[0]["role"], "system")


def run_react_agent_tests():
    """Run all ReAct Agent tests."""
    print("🧪 ReAct Agent 测试开始")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestReActAgent)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ 所有 ReAct Agent 测试通过!")
    else:
        print(f"❌ 测试失败: {len(result.failures)} 失败, {len(result.errors)} 错误")
        for test, error in result.failures + result.errors:
            print(f"   - {test}: {error}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_react_agent_tests()
