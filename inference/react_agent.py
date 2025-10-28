"""
ReAct Agent for ResearchAgent

This module implements a ReAct (Reasoning and Acting) Agent that uses
the FnCallAgent pattern from Qwen-Agent with GLM-4.5-air LLM.
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from openai import OpenAI

from qwen_agent.agents.fncall_agent import FnCallAgent
from inference import GoogleSearchTool, GoogleScholarTool, JinaURLVisitTool, PythonSandboxTool


# Control Constants
MAX_LLM_CALLS = 100
MAX_CONTEXT_TOKENS = 12000  # Leave room for final answer (GLM-4.5-air has higher limits)


class ReActAgent:
    """
    ReAct Agent for comprehensive research tasks.
    
    This agent uses the ReAct (Reasoning and Acting) pattern to perform
    systematic research using available tools (search, google_scholar, visit).
    """
    
    def __init__(self):
        """Initialize the ReAct Agent with LLM client and tools."""
        # Initialize LLM client for GLM-4.5-air
        api_key = os.getenv('GLM_API_KEY')
        if not api_key:
            raise ValueError("GLM_API_KEY environment variable is required")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://open.bigmodel.cn/api/paas/v4"
        )
        self.model = "glm-4.5-air"
        
        # Initialize available tools
        self.tools = {
            'search': GoogleSearchTool(),
            'google_scholar': GoogleScholarTool(),
            'visit': JinaURLVisitTool(),
            'python_sandbox': PythonSandboxTool()
        }
        
        # Control parameters
        self.llm_calls = 0
        self.messages = []
    
    def _get_tools_signatures(self) -> str:
        """Generate XML-formatted tools signatures for the system prompt."""
        tools_xml = "<tools>\n"
        
        for tool_name, tool_instance in self.tools.items():
            tool_signature = {
                'type': 'function',
                'function': {
                    'name': tool_instance.name,
                    'description': tool_instance.description,
                    'parameters': tool_instance.parameters
                }
            }
            tools_xml += f"{json.dumps(tool_signature, indent=2, ensure_ascii=False)}\n"
        
        tools_xml += "</tools>"
        return tools_xml
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt with agent purpose, tools, and instructions."""
        current_date = datetime.now().strftime("%Y-%m-%d")
        tools_signatures = self._get_tools_signatures()
        
        system_prompt = f"""You are a comprehensive research agent designed to conduct deep, systematic investigations on any topic. Your purpose is to gather, analyze, and synthesize information from multiple sources to provide thorough and accurate answers.

{tools_signatures}

Tool Call Format:
When you need to use a tool, respond with ONLY the JSON object on a separate line:
{{"name": "tool_name", "arguments": {{"parameter": "value"}}}}

CRITICAL REQUIREMENTS:
- ALWAYS use the exact format: {{"name": "tool_name", "arguments": {{"parameter": "value"}}}}
- The "name" field must contain the tool name
- The "arguments" field must contain a JSON object with parameters
- NO alternative formats are supported
- NO additional text or formatting before/after the JSON object
- Each tool call must be on its own line

Research Guidelines:
1. Start with broad searches to understand the topic landscape
2. Use Google Scholar for academic and research-oriented information
3. Visit specific URLs to get detailed information from key sources
4. Use python_sandbox for computational tasks, data analysis, mathematical calculations, or code execution
5. Synthesize findings from multiple sources
6. Always provide comprehensive, well-structured answers

Python Sandbox Tool Usage:
- Use for mathematical calculations, data processing, or algorithmic analysis
- Execute code to verify calculations, generate data, or perform computations
- Example: {{"name": "python_sandbox", "arguments": {{"code": "import math; print(f'Pi = {{math.pi}}')}}}}
- Use print() statements to get output from the code execution

Response Format:
- When you have completed your research and have a comprehensive answer, wrap it between <answer></answer> tags
- Be thorough and cite your sources where appropriate
- Provide actionable insights when applicable
- Include computational results when relevant to support your findings

Current Date: {current_date}

Remember: Use tools systematically to gather comprehensive information before providing your final answer."""
        
        return system_prompt
    
    def _detect_tool_calls(self, content: str) -> List[Dict[str, Any]]:
        """Detect and parse tool calls in LLM response."""
        tool_calls = []

        # Look for JSON objects that contain both "name" and "arguments" fields
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line or not line.startswith('{') or not line.endswith('}'):
                continue

            try:
                tool_call = json.loads(line)
                if 'name' in tool_call and 'arguments' in tool_call:
                    tool_calls.append(tool_call)
            except json.JSONDecodeError:
                continue

        return tool_calls
    
        
    def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Execute a tool with given arguments."""
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found. Available tools: {list(self.tools.keys())}"
        
        try:
            tool_instance = self.tools[tool_name]
            result = tool_instance.call(arguments)
            return result
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"
    
    def _should_exit(self, content: str) -> bool:
        """Check if the agent should exit (has provided final answer)."""
        return "<answer>" in content and "</answer>" in content
    
    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation (1 token ≈ 4 characters for Chinese/English mixed content)."""
        return len(text) // 4
    
    def _truncate_messages_if_needed(self):
        """Truncate early messages if context is approaching limit."""
        total_tokens = sum(self._estimate_tokens(msg.get('content', '')) for msg in self.messages)
        
        # Keep system message and last few user/assistant exchanges
        if total_tokens > MAX_CONTEXT_TOKENS:
            # Keep system message and last 8 exchanges
            system_msg = [msg for msg in self.messages if msg['role'] == 'system']
            recent_msgs = self.messages[-16:]  # Last 8 exchanges (user+assistant pairs)
            self.messages = system_msg + recent_msgs
    
    def _llm_call(self, messages: List[Dict[str, str]]) -> str:
        """Make LLM API call and return the response."""
        try:
            self.llm_calls += 1
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                stream=False  # Wait for complete response
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"LLM API Error: {str(e)}"
    
    def research(self, question: str) -> str:
        """
        Conduct comprehensive research on the given question.
        
        Args:
            question: The research question or topic
            
        Returns:
            Comprehensive research answer
        """
        # Initialize messages
        system_prompt = self._create_system_prompt()
        self.messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
        
        print(f"🔍 Starting research on: {question}")
        print("=" * 60)
        
        # ReAct Loop
        while self.llm_calls < MAX_LLM_CALLS:
            print(f"\n🤖 LLM Call #{self.llm_calls + 1}")
            
            # Check context limit and truncate if needed
            self._truncate_messages_if_needed()
            
            # Get LLM response
            llm_response = self._llm_call(self.messages)
            print(f"🧠 LLM Response: {llm_response[:200]}...")
            
            # Check if we should exit (final answer provided)
            if self._should_exit(llm_response):
                print("✅ Final answer received!")
                self.messages.append({"role": "assistant", "content": llm_response})
                break
            
            # Detect tool calls
            tool_calls = self._detect_tool_calls(llm_response)
            
            if not tool_calls:
                print("⚠️ No tool calls detected, asking for clarification...")
                self.messages.append({"role": "assistant", "content": llm_response})
                self.messages.append({
                    "role": "user", 
                    "content": "Please use the available tools to gather more information for your research."
                })
                continue
            
            # Execute tool calls
            self.messages.append({"role": "assistant", "content": llm_response})
            
            for tool_call in tool_calls:
                tool_name = tool_call.get('name')
                arguments = tool_call.get('arguments', {})
                
                print(f"🔧 Executing tool: {tool_name} with args: {arguments}")
                
                tool_response = self._execute_tool(tool_name, arguments)
                
                # Wrap tool response
                wrapped_response = f"<tool_response>\n{tool_response}\n</tool_response>"
                
                print(f"📋 Tool response length: {len(tool_response)} characters")
                
                self.messages.append({
                    "role": "user",
                    "content": wrapped_response
                })
        
        # Check if we exited due to max calls
        if self.llm_calls >= MAX_LLM_CALLS:
            print("⚠️ Maximum LLM calls reached, forcing summary...")
            self.messages.append({
                "role": "user",
                "content": "Please provide a comprehensive answer based on the information gathered so far, wrapping it in <answer></answer> tags."
            })
            final_response = self._llm_call(self.messages)
            self.messages.append({"role": "assistant", "content": final_response})
        
        # Extract final answer
        for msg in reversed(self.messages):
            if msg['role'] == 'assistant' and '<answer>' in msg['content'] and '</answer>' in msg['content']:
                answer_match = re.search(r'<answer>(.*?)</answer>', msg['content'], re.DOTALL)
                if answer_match:
                    return answer_match.group(1).strip()
        
        # Fallback: return last assistant message
        for msg in reversed(self.messages):
            if msg['role'] == 'assistant':
                return msg['content']
        
        return "No answer could be generated."
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the full conversation history."""
        return self.messages
    
    def reset(self):
        """Reset the agent state for a new research session."""
        self.llm_calls = 0
        self.messages = []
