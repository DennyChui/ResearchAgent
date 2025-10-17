"""
Tests for Python Sandbox Tool

This module contains comprehensive tests for the Python sandbox tool,
including structure tests, functionality tests, and integration tests.
"""

import json
import os
import unittest
from unittest.mock import patch

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
            mock_execute.return_value = {'success': True, 'response': {'stdout': 'test'}}
            
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

    def test_successful_code_execution(self):
        """Test successful code execution with real sandbox."""
        print("\n🔍 Testing real Python sandbox execution...")
        
        # Check if sandbox endpoint is available
        import os
        sandbox_endpoint = os.getenv('SANDBOX_FUSION_ENDPOINT', 'http://localhost:8081')
        
        tool = PythonSandboxTool()
        
        try:
            # Test simple code execution
            result = tool.call({"code": "print('Hello, World!')"})
            
            # Check result
            self.assertIn("Hello, World!", result)
            self.assertIn("Python Code Execution Result:", result)
            print("✓ Real sandbox execution successful")
            
        except Exception as e:
            # If sandbox is not available, provide helpful message
            if "Connection refused" in str(e) or "Failed to establish" in str(e):
                self.skipTest(f"Sandbox service not available at {sandbox_endpoint}. Start sandbox service to run this test.")
            else:
                self.fail(f"Real sandbox execution failed: {e}")

    def test_code_execution_with_mathematical_operation(self):
        """Test code execution with mathematical operations."""
        print("\n🔍 Testing mathematical operations in real sandbox...")
        
        tool = PythonSandboxTool()
        
        try:
            # Test mathematical calculation
            result = tool.call({"code": "result = sum(range(1, 11)); print(f'Sum of 1-10: {result}')"})
            
            # Check result contains expected output
            self.assertIn("Sum of 1-10: 55", result)
            self.assertIn("Python Code Execution Result:", result)
            print("✓ Mathematical operations test successful")
            
        except Exception as e:
            if "Connection refused" in str(e) or "Failed to establish" in str(e):
                self.skipTest("Sandbox service not available")
            else:
                self.fail(f"Mathematical operations test failed: {e}")

    def test_endpoint_configuration(self):
        """Test endpoint configuration during initialization."""
        # Test with custom endpoint
        with patch.dict(os.environ, {'SANDBOX_FUSION_ENDPOINT': 'http://custom:8080'}):
            tool = PythonSandboxTool()
            self.assertEqual(tool.endpoint, 'http://custom:8080')
        
        # Test with default endpoint
        with patch.dict(os.environ, {}, clear=True):
            tool = PythonSandboxTool()
            self.assertEqual(tool.endpoint, 'http://localhost:8081')

    def test_endpoint_configuration_error_handling(self):
        """Test handling of endpoint configuration errors."""
        # Tool should handle missing endpoint gracefully
        tool = PythonSandboxTool()
        
        # Tool should still be created even if endpoint is invalid
        self.assertIsNotNone(tool)
        self.assertIsInstance(tool.endpoint, str)


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
