"""
Test suite for ResearchTool

This module tests the ResearchTool functionality including
tool initialization, parameter parsing, and research execution.
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path to import inference modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.research_tool import ResearchTool


class TestResearchTool(unittest.TestCase):
    """Test cases for ResearchTool class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create tool with mocked ReActAgent to avoid API key requirement
        with patch('inference.research_tool.ReActAgent') as mock_react_agent_class:
            mock_react_agent = Mock()
            mock_react_agent.research.return_value = "Mock research result"
            mock_react_agent.llm_calls = 0
            mock_react_agent.messages = []
            mock_react_agent.tools = {}
            mock_react_agent.reset = Mock()
            mock_react_agent_class.return_value = mock_react_agent
            self.research_tool = ResearchTool()

    def test_tool_attributes(self):
        """Test that tool has required attributes."""
        self.assertEqual(self.research_tool.name, 'research')
        self.assertIsInstance(self.research_tool.description, str)
        self.assertIn('research', self.research_tool.description.lower())
        self.assertIsInstance(self.research_tool.parameters, dict)

    def test_parameters_schema(self):
        """Test that parameters schema is valid."""
        schema = self.research_tool.parameters

        # Check basic schema structure
        self.assertEqual(schema['type'], 'object')
        self.assertIn('properties', schema)
        self.assertIn('required', schema)

        # Check research_quest property
        self.assertIn('research_quest', schema['properties'])
        quest_prop = schema['properties']['research_quest']
        self.assertEqual(quest_prop['type'], 'string')
        self.assertEqual(quest_prop['minLength'], 5)
        self.assertEqual(quest_prop['maxLength'], 500)

        # Check required fields
        self.assertIn('research_quest', schema['required'])

    @patch('inference.research_tool.ReActAgent')
    def test_initialization_with_react_agent(self, mock_react_agent_class):
        """Test tool initialization with mocked ReActAgent."""
        mock_react_agent = Mock()
        mock_react_agent_class.return_value = mock_react_agent

        # Create new tool instance
        tool = ResearchTool()

        # Verify ReActAgent was initialized
        mock_react_agent_class.assert_called_once()
        self.assertEqual(tool.react_agent, mock_react_agent)

    @patch('inference.research_tool.ReActAgent')
    def test_initialization_failure(self, mock_react_agent_class):
        """Test tool initialization when ReActAgent fails."""
        mock_react_agent_class.side_effect = Exception("Failed to initialize")

        # Create tool instance
        tool = ResearchTool()

        # Should handle failure gracefully
        self.assertIsNone(tool.react_agent)

    @patch('inference.research_tool.ReActAgent')
    def test_call_with_dict_params(self, mock_react_agent_class):
        """Test tool call with dictionary parameters."""
        mock_react_agent = Mock()
        mock_react_agent.research.return_value = "Research result here"
        mock_react_agent_class.return_value = mock_react_agent

        tool = ResearchTool()
        result = tool.call({"research_quest": "test query"})

        # Verify ReActAgent.research was called
        mock_react_agent.research.assert_called_once_with("test query")
        self.assertIn("Research Report: test query", result)

    @patch('inference.research_tool.ReActAgent')
    def test_call_with_string_params(self, mock_react_agent_class):
        """Test tool call with string parameters."""
        mock_react_agent = Mock()
        mock_react_agent.research.return_value = "Research result here"
        mock_react_agent_class.return_value = mock_react_agent

        tool = ResearchTool()
        result = tool.call("test query")

        # Should treat string as research quest directly
        mock_react_agent.research.assert_called_once_with("test query")
        self.assertIn("Research Report: test query", result)

    @patch('inference.research_tool.ReActAgent')
    def test_call_with_json_string_params(self, mock_react_agent_class):
        """Test tool call with JSON string parameters."""
        mock_react_agent = Mock()
        mock_react_agent.research.return_value = "Research result here"
        mock_react_agent_class.return_value = mock_react_agent

        tool = ResearchTool()
        result = tool.call('{"research_quest": "test query"}')

        # Should parse JSON and extract research_quest
        mock_react_agent.research.assert_called_once_with("test query")
        self.assertIn("Research Report: test query", result)

    def test_call_with_empty_params(self):
        """Test tool call with empty or missing research quest."""
        # Create tool with None agent for this test
        tool_with_no_agent = ResearchTool()
        tool_with_no_agent.react_agent = None

        # Test with empty string
        result = tool_with_no_agent.call("")
        self.assertIn("Error", result)

        # Test with empty dict
        result = tool_with_no_agent.call({})
        self.assertIn("Error", result)

        # Test with None
        result = tool_with_no_agent.call(None)
        self.assertIn("Error", result)

    def test_call_with_no_react_agent(self):
        """Test tool call when ReActAgent is not available."""
        self.research_tool.react_agent = None

        result = self.research_tool.call({"research_quest": "test query"})
        self.assertIn("Error", result)
        self.assertIn("ReActAgent is not available", result)

    @patch('inference.research_tool.ReActAgent')
    def test_call_with_react_exception(self, mock_react_agent_class):
        """Test tool call when ReActAgent raises exception."""
        mock_react_agent = Mock()
        mock_react_agent.research.side_effect = Exception("Research failed")
        mock_react_agent_class.return_value = mock_react_agent

        tool = ResearchTool()
        result = tool.call({"research_quest": "test query"})

        self.assertIn("Error during research execution", result)
        self.assertIn("Research failed", result)

    @patch('inference.research_tool.ReActAgent')
    def test_format_research_result(self, mock_react_agent_class):
        """Test research result formatting."""
        mock_react_agent = Mock()
        mock_react_agent.llm_calls = 5
        mock_react_agent.messages = [{"role": "user", "content": "test"}]
        mock_react_agent.tools = {"search": "tool1", "scholar": "tool2"}
        mock_react_agent_class.return_value = mock_react_agent

        tool = ResearchTool()
        result = tool._format_research_result("test question", "test result")

        self.assertIn("Research Report: test question", result)
        self.assertIn("test result", result)
        self.assertIn("LLM Calls: 5", result)
        self.assertIn("Research completed using ReActAgent", result)

    @patch('inference.research_tool.ReActAgent')
    def test_get_research_stats(self, mock_react_agent_class):
        """Test getting research statistics."""
        mock_react_agent = Mock()
        mock_react_agent.llm_calls = 3
        mock_react_agent.messages = [{"role": "user"}, {"role": "assistant"}]
        mock_react_agent.tools = {"search": "tool1"}
        mock_react_agent_class.return_value = mock_react_agent

        tool = ResearchTool()
        stats = tool.get_research_stats()

        self.assertEqual(stats["llm_calls"], 3)
        self.assertEqual(stats["message_count"], 2)
        self.assertEqual(stats["available_tools"], ["search"])

    def test_get_research_stats_no_agent(self):
        """Test getting stats when ReActAgent is not available."""
        self.research_tool.react_agent = None

        stats = self.research_tool.get_research_stats()
        self.assertIn("error", stats)

    @patch('inference.research_tool.ReActAgent')
    def test_reset_research_agent(self, mock_react_agent_class):
        """Test resetting research agent."""
        mock_react_agent = Mock()
        mock_react_agent_class.return_value = mock_react_agent

        tool = ResearchTool()
        tool.reset_research_agent()

        mock_react_agent.reset.assert_called_once()

    def test_parameter_validation(self):
        """Test parameter validation."""
        # Test with too short research quest - should pass to ReActAgent
        result = self.research_tool.call({"research_quest": "abc"})
        self.research_tool.react_agent.research.assert_called_with("abc")

        # Test with valid research quest
        result = self.research_tool.call({"research_quest": "valid research question here"})
        self.research_tool.react_agent.research.assert_called_with("valid research question here")


class TestResearchToolIntegration(unittest.TestCase):
    """Integration tests for ResearchTool (requires API keys)."""

    @unittest.skipUnless(os.getenv('GLM_API_KEY'), "GLM_API_KEY required for integration test")
    def test_integration_with_real_api(self):
        """Test ResearchTool with real API (if GLM_API_KEY is available)."""
        tool = ResearchTool()

        # Test with a simple research question
        result = tool.call({"research_quest": "What is artificial intelligence?"})

        # Should get a meaningful result
        self.assertIsInstance(result, str)
        self.assertIn("Research Report", result)
        self.assertNotIn("Error", result)

        # Check stats
        stats = tool.get_research_stats()
        self.assertGreater(stats["llm_calls"], 0)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)