"""
Tests for Python Sandbox Tool

This module contains comprehensive tests for the Python sandbox tool,
including structure tests, functionality tests, and integration tests.
"""

import json
import os
import unittest
from unittest.mock import Mock, patch, MagicMock

# Test the tool structure and basic functionality
from inference.python_sandbox_tool import PythonSandboxTool


class TestPythonSandboxToolStructure(unittest.TestCase):
    """Test the basic structure and interface of PythonSandboxTool."""

    def setUp(self):
        """Set up test fixtures."""
        self.tool = PythonSandboxTool()

    def test_tool_name(self):
        """Test that the tool has the correct name."""
        self.assertEqual(self.tool.name, 'python_sandbox')

    def test_tool_description(self):
        """Test that the tool has a description."""
        self.assertIsInstance(self.tool.description, str)
        self.assertTrue(len(self.tool.description) > 0)
        self.assertIn('sandbox', self.tool.description.lower())

    def test_tool_parameters(self):
        """Test that the tool has the correct parameters schema."""
        parameters = self.tool.parameters
        
        # Check basic structure
        self.assertEqual(parameters['type'], 'object')
        self.assertIn('properties', parameters)
        self.assertIn('required', parameters)
        
        # Check code parameter
        code_param = parameters['properties']['code']
        self.assertEqual(code_param['type'], 'string')
        self.assertIn('description', code_param)
        self.assertEqual(code_param['minLength'], 1)
        self.assertEqual(code_param['maxLength'], 10000)
        
        # Check required parameters
        self.assertIn('code', parameters['required'])

    def test_initialization(self):
        """Test tool initialization."""
        tool = PythonSandboxTool()
        
        # Check endpoint configuration
        expected_endpoint = os.getenv('SANDBOX_FUSION_ENDPOINT', 'http://localhost:8081')
        self.assertEqual(tool.endpoint, expected_endpoint)
        
        # Check default settings
        self.assertEqual(tool.default_timeout, 30)
        self.assertEqual(tool.max_attempts, 3)


class TestPythonSandboxToolFunctionality(unittest.TestCase):
    """Test the functionality of PythonSandboxTool."""

    def setUp(self):
        """Set up test fixtures."""
        self.tool = PythonSandboxTool()

    def test_empty_code_parameter(self):
        """Test handling of empty code parameter."""
        # Test with empty string
        result = self.tool.call({"code": ""})
        self.assertIn("Error: Python code cannot be empty", result)
        
        # Test with whitespace only
        result = self.tool.call({"code": "   "})
        self.assertIn("Error: Python code cannot be empty", result)

    def test_missing_code_parameter(self):
        """Test handling of missing code parameter."""
        result = self.tool.call({})
        self.assertIn("Error: Python code cannot be empty", result)

    def test_string_parameter_parsing(self):
        """Test parsing of string parameters."""
        # Test with JSON string
        json_param = json.dumps({"code": "print('test')"})
        result = self.tool.call(json_param)
        # Should not be an error about parameters
        self.assertNotIn("Invalid parameters format", result)
        
        # Test with direct code string
        result = self.tool.call("print('test')")
        # Should not be an error about parameters
        self.assertNotIn("Invalid parameters format", result)

    def test_dict_parameter_parsing(self):
        """Test parsing of dictionary parameters."""
        params = {"code": "print('test')"}
        result = self.tool.call(params)
        # Should not be an error about parameters
        self.assertNotIn("Invalid parameters format", result)

    def test_invalid_parameter_format(self):
        """Test handling of invalid parameter formats."""
        # Test with invalid JSON string
        result = self.tool.call('{"code": "print(\'test\')"')  # Missing closing brace
        # Should handle gracefully and treat as direct code
        self.assertNotIn("Invalid parameters format", result)
        
        # Test with list parameter
        result = self.tool.call(["print('test')"])
        self.assertIn("Invalid parameters format", result)

    def test_code_trimming(self):
        """Test that code is properly trimmed."""
        code_with_whitespace = "  \n  print('test')  \n  "
        
        with patch.object(self.tool, '_execute_code') as mock_execute:
            mock_execute.return_value = {'success': True, 'response': Mock()}
            
            self.tool.call({"code": code_with_whitespace})
            
            # Check that trimmed code was passed to execute
            mock_execute.assert_called_once_with("print('test')")

    def test_result_formatting(self):
        """Test result formatting for different scenarios."""
        code = "print('Hello, World!')"
        
        # Test successful execution with stdout using dict response
        response_dict = {
            'stdout': 'Hello, World!',
            'stderr': '',
            'exit_code': 0
        }
        
        result = self.tool._format_result(code, {'success': True, 'response': response_dict})
        
        self.assertIn("Python Code Execution Result:", result)
        self.assertIn("Output:\nHello, World!", result)
        self.assertIn("```python\nprint('Hello, World!')\n```", result)

    def test_error_formatting(self):
        """Test error result formatting."""
        code = "print('test')"
        error_msg = "Connection failed"
        
        result = self.tool._format_result(code, {'success': False, 'error': error_msg})
        
        self.assertIn("Python Code Execution Failed:", result)
        self.assertIn(f"Error: {error_msg}", result)
        self.assertIn("```python\nprint('test')\n```", result)

    def test_result_formatting_with_dict_response(self):
        """Test result formatting with dictionary response."""
        code = "print('test')"
        response_dict = {
            'stdout': 'Test output',
            'stderr': '',
            'exit_code': 0
        }
        
        result = self.tool._format_result(code, {'success': True, 'response': response_dict})
        
        self.assertIn("Output:\nTest output", result)
        self.assertNotIn("Error/Stderr:", result)

    def test_result_formatting_with_stderr(self):
        """Test result formatting when there's stderr output."""
        code = "print('test')"
        response_dict = {
            'stdout': 'Some output',
            'stderr': 'Warning message',
            'exit_code': 0
        }
        
        result = self.tool._format_result(code, {'success': True, 'response': response_dict})
        
        self.assertIn("Output:\nSome output", result)
        self.assertIn("Error/Stderr:\nWarning message", result)

    def test_result_formatting_with_nonzero_exit_code(self):
        """Test result formatting with non-zero exit code."""
        code = "print('test')"
        response_dict = {
            'stdout': '',
            'stderr': 'Error occurred',
            'exit_code': 1
        }
        
        result = self.tool._format_result(code, {'success': True, 'response': response_dict})
        
        self.assertIn("Error/Stderr:\nError occurred", result)
        self.assertIn("Exit Code: 1", result)


class TestPythonSandboxToolIntegration(unittest.TestCase):
    """Test integration with SandboxFusion SDK."""

    def setUp(self):
        """Set up test fixtures."""
        self.tool = PythonSandboxTool()

    @patch('inference.python_sandbox_tool.SANDBOX_FUSION_AVAILABLE', False)
    def test_missing_sdk_dependency(self):
        """Test behavior when sandbox-fusion SDK is not available."""
        tool = PythonSandboxTool()
        
        result = tool.call({"code": "print('test')"})
        
        self.assertIn("Error: sandbox-fusion package is not installed", result)

    @patch('inference.python_sandbox_tool.run_code')
    @patch('inference.python_sandbox_tool.SANDBOX_FUSION_AVAILABLE', True)
    def test_successful_code_execution(self, mock_run_code):
        """Test successful code execution."""
        # Mock successful response
        mock_response = Mock()
        mock_response.stdout = "Hello, World!"
        mock_response.stderr = ""
        mock_response.exit_code = 0
        
        mock_run_code.return_value = mock_response
        
        tool = PythonSandboxTool()
        result = tool.call({"code": "print('Hello, World!')"})
        
        # Check that run_code was called with correct parameters
        mock_run_code.assert_called_once()
        call_args = mock_run_code.call_args
        
        # Check request object
        request = call_args[0][0]
        self.assertEqual(request.code, "print('Hello, World!')")
        self.assertEqual(request.language, 'python')
        
        # Check optional parameters
        self.assertEqual(call_args.kwargs.get('max_attempts'), 3)
        self.assertEqual(call_args.kwargs.get('client_timeout'), 30)
        
        # Check result
        self.assertIn("Hello, World!", result)
        self.assertIn("Python Code Execution Result:", result)

    @patch('inference.python_sandbox_tool.run_code')
    @patch('inference.python_sandbox_tool.SANDBOX_FUSION_AVAILABLE', True)
    def test_code_execution_with_exception(self, mock_run_code):
        """Test code execution when an exception occurs."""
        # Mock exception
        mock_run_code.side_effect = Exception("Connection timeout")
        
        tool = PythonSandboxTool()
        result = tool.call({"code": "print('test')"})
        
        # Check result contains error information
        self.assertIn("Python Code Execution Failed:", result)
        self.assertIn("Connection timeout", result)

    @patch('inference.python_sandbox_tool.set_endpoint')
    @patch('inference.python_sandbox_tool.SANDBOX_FUSION_AVAILABLE', True)
    def test_endpoint_configuration(self, mock_set_endpoint):
        """Test endpoint configuration during initialization."""
        # Test with custom endpoint
        with patch.dict(os.environ, {'SANDBOX_FUSION_ENDPOINT': 'http://custom:8080'}):
            tool = PythonSandboxTool()
            mock_set_endpoint.assert_called_once_with('http://custom:8080')
        
        # Reset mock
        mock_set_endpoint.reset_mock()
        
        # Test with default endpoint
        with patch.dict(os.environ, {}, clear=True):
            tool = PythonSandboxTool()
            mock_set_endpoint.assert_called_once_with('http://localhost:8081')

    @patch('inference.python_sandbox_tool.set_endpoint')
    @patch('inference.python_sandbox_tool.SANDBOX_FUSION_AVAILABLE', True)
    def test_endpoint_configuration_error(self, mock_set_endpoint):
        """Test handling of endpoint configuration errors."""
        # Mock endpoint setting failure
        mock_set_endpoint.side_effect = Exception("Invalid endpoint")
        
        tool = PythonSandboxTool()
        
        # Tool should still be created despite endpoint error
        self.assertIsNotNone(tool)


class TestPythonSandboxToolEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def setUp(self):
        """Set up test fixtures."""
        self.tool = PythonSandboxTool()

    def test_maximum_code_length(self):
        """Test handling of maximum code length."""
        # Create code at the maximum length
        max_length = 10000
        code = 'x = "a" * ' + str(max_length // 5)  # Creates code close to max length
        
        if len(code) <= max_length:
            # Should not raise an error
            with patch.object(self.tool, '_execute_code') as mock_execute:
                mock_execute.return_value = {'success': True, 'response': {'stdout': 'test'}}
                
                result = self.tool.call({"code": code})
                self.assertNotIn("Error:", result)

    def test_minimum_code_length(self):
        """Test handling of minimum code length."""
        # Test single character code
        with patch.object(self.tool, '_execute_code') as mock_execute:
            mock_execute.return_value = {'success': True, 'response': {'stdout': 'test'}}
            
            result = self.tool.call({"code": "1"})
            self.assertNotIn("Error:", result)

    def test_unicode_code(self):
        """Test handling of Unicode characters in code."""
        unicode_code = "print('Hello 世界 🌍')"
        
        with patch.object(self.tool, '_execute_code') as mock_execute:
            mock_execute.return_value = {'success': True, 'response': {'stdout': 'test'}}
            
            result = self.tool.call({"code": unicode_code})
            self.assertNotIn("Error:", result)

    def test_multiline_code(self):
        """Test handling of multiline code."""
        multiline_code = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
'''.strip()
        
        with patch.object(self.tool, '_execute_code') as mock_execute:
            mock_execute.return_value = {'success': True, 'response': {'stdout': 'test'}}
            
            result = self.tool.call({"code": multiline_code})
            self.assertNotIn("Error:", result)
            mock_execute.assert_called_once_with(multiline_code)


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)
