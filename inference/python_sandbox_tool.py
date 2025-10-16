"""
Python Sandbox Tool for Qwen-Agent

This module implements a Python code execution tool using SandboxFusion
to provide secure Python code execution capabilities to Qwen-Agent.
"""

import json
import os
import logging
from typing import Union, Dict, Any

from qwen_agent.tools.base import BaseTool, register_tool

# Try to import sandbox-fusion
try:
    from sandbox_fusion import run_code, RunCodeRequest, set_endpoint
    SANDBOX_FUSION_AVAILABLE = True
except ImportError:
    SANDBOX_FUSION_AVAILABLE = False
    logging.warning("sandbox-fusion package not available. Python sandbox tool will not function.")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@register_tool('python_sandbox')
class PythonSandboxTool(BaseTool):
    """
    Python Sandbox tool using SandboxFusion to execute Python code securely.

    This tool allows Qwen-Agent to execute Python code in a secure sandboxed
    environment and return the execution results.
    """

    name = 'python_sandbox'
    description = 'Execute Python code in a secure sandbox environment. Use this tool to run Python code and get the output. The code should be self-contained and use print() statements for output.'

    parameters = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "Python code to execute in the sandbox. The code should be self-contained and use print() statements to produce output.",
                "minLength": 1,
                "maxLength": 10000
            }
        },
        "required": ["code"]
    }

    def __init__(self):
        """Initialize the Python Sandbox tool."""
        super().__init__()
        
        # Check if sandbox-fusion is available
        if not SANDBOX_FUSION_AVAILABLE:
            logger.error("sandbox-fusion package is not installed. Python sandbox tool will not work.")
            return
        
        # Configure endpoint from environment variable or default to localhost:8081
        self.endpoint = os.getenv('SANDBOX_FUSION_ENDPOINT', 'http://localhost:8081')
        
        # Set the global endpoint for sandbox-fusion
        try:
            set_endpoint(self.endpoint)
            logger.info(f"Python sandbox endpoint set to: {self.endpoint}")
        except Exception as e:
            logger.error(f"Failed to set sandbox endpoint: {str(e)}")
        
        # Default configuration
        self.default_timeout = 30  # 30 seconds timeout
        self.max_attempts = 3  # Maximum retry attempts

    def call(self, params: Union[str, dict], **kwargs) -> str:
        """
        Execute Python code using SandboxFusion.

        Args:
            params: Parameters containing the Python code to execute
            **kwargs: Additional keyword arguments

        Returns:
            Execution results as formatted string
        """
        if not SANDBOX_FUSION_AVAILABLE:
            return "Error: sandbox-fusion package is not installed. Please install it with 'pip install sandbox-fusion'"

        try:
            # Parse parameters
            if isinstance(params, str):
                try:
                    params_dict = json.loads(params)
                    code = params_dict.get('code', '')
                except json.JSONDecodeError:
                    # If params is not valid JSON, treat it as the code directly
                    code = params
            elif isinstance(params, dict):
                code = params.get('code', '')
            else:
                return "Error: Invalid parameters format. Expected string or dictionary."

            if not code or not str(code).strip():
                return "Error: Python code cannot be empty."

            code = str(code).strip()
            
            # Execute the code
            result = self._execute_code(code)
            return self._format_result(code, result)

        except Exception as e:
            logger.error(f"Error in Python sandbox execution: {str(e)}")
            return f"Error executing Python code: {str(e)}"

    def _execute_code(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code using SandboxFusion.

        Args:
            code: Python code to execute

        Returns:
            Execution response from sandbox
        """
        try:
            # Create the request
            request = RunCodeRequest(
                code=code,
                language='python'
            )
            
            # Execute with timeout and retry
            response = run_code(
                request,
                max_attempts=self.max_attempts,
                client_timeout=self.default_timeout
            )
            
            return {
                'success': True,
                'response': response
            }
            
        except Exception as e:
            logger.error(f"Error executing code in sandbox: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def _format_result(self, code: str, result: Dict[str, Any]) -> str:
        """
        Format the execution result into a readable string.

        Args:
            code: The original Python code
            result: Execution result from sandbox

        Returns:
            Formatted result string
        """
        if not result['success']:
            return f"Python Code Execution Failed:\n\nError: {result['error']}\n\nCode:\n```python\n{code}\n```"
        
        response = result['response']
        
        # Extract information from SandboxFusion response
        try:
            # Handle SandboxFusion response structure
            if hasattr(response, 'run_result'):
                run_result = response.run_result
                status = run_result.status
                return_code = run_result.return_code
                stdout = run_result.stdout or ''
                stderr = run_result.stderr or ''
                execution_time = run_result.execution_time
                
                # Format the result
                result_parts = ["Python Code Execution Result:"]
                
                if stdout and stdout.strip():
                    result_parts.append(f"Output:\n{stdout.strip()}")
                
                if stderr and stderr.strip():
                    result_parts.append(f"Error/Stderr:\n{stderr.strip()}")
                
                if return_code != 0:
                    result_parts.append(f"Exit Code: {return_code}")
                
                if execution_time:
                    result_parts.append(f"Execution Time: {execution_time:.3f}s")
                
                result_parts.append(f"\nCode:\n```python\n{code}\n```")
                
                return "\n\n".join(result_parts)
            
            # Fallback to generic response handling
            else:
                # Try to access common response attributes
                if hasattr(response, 'stdout'):
                    output = response.stdout
                elif hasattr(response, 'output'):
                    output = response.output
                elif isinstance(response, dict):
                    output = response.get('stdout', response.get('output', ''))
                else:
                    output = str(response)
                
                if hasattr(response, 'stderr'):
                    error = response.stderr
                elif isinstance(response, dict):
                    error = response.get('stderr', '')
                else:
                    error = ''
                
                if hasattr(response, 'exit_code'):
                    exit_code = response.exit_code
                elif isinstance(response, dict):
                    exit_code = response.get('exit_code', 0)
                else:
                    exit_code = 0
                
                # Format the result
                result_parts = ["Python Code Execution Result:"]
                
                if output and output.strip():
                    result_parts.append(f"Output:\n{output}")
                
                if error and error.strip():
                    result_parts.append(f"Error/Stderr:\n{error}")
                
                if exit_code != 0:
                    result_parts.append(f"Exit Code: {exit_code}")
                
                result_parts.append(f"\nCode:\n```python\n{code}\n```")
                
                return "\n\n".join(result_parts)
            
        except Exception as e:
            logger.error(f"Error formatting sandbox result: {str(e)}")
            return f"Python Code Execution Result:\n\nRaw Response:\n{str(response)}\n\nCode:\n```python\n{code}\n```"


# For direct testing
if __name__ == "__main__":
    # Create tool instance
    tool = PythonSandboxTool()
    
    # Test code snippets
    test_codes = [
        "print('Hello, World!')",
        "import math\nprint(f'Pi = {math.pi}')",
        "x = [i for i in range(5)]\nprint(f'List: {x}')\nprint(f'Sum: {sum(x)}')"
    ]
    
    for code in test_codes:
        print(f"\n{'='*60}")
        print(f"Testing Python code:")
        print(f"```python\n{code}\n```")
        print(f"{'='*60}")
        
        result = tool.call({"code": code})
        print(result)
        print()
