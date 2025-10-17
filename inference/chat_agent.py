"""
Chat Agent for ResearchAgent

This module implements a conversational AI agent that can chat with users
and delegate research tasks to the ResearchTool when needed.
"""

import json
import logging
import os
import re
from typing import Dict, List, Any, Optional
from openai import OpenAI

from inference.research_tool import ResearchTool

# Set up logging
logger = logging.getLogger(__name__)


class ChatAgent:
    """
    Chat Agent for conversational AI with research capabilities.

    This agent maintains a conversation with users and can delegate
    research tasks to the ResearchTool when comprehensive research
    is needed.
    """

    def __init__(self):
        """Initialize the Chat Agent with LLM client and research tool."""
        # Initialize LLM client for GLM-4.5-air
        api_key = os.getenv('GLM_API_KEY')
        if not api_key:
            raise ValueError("GLM_API_KEY environment variable is required")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://open.bigmodel.cn/api/paas/v4"
        )
        self.model = "glm-4.5-air"

        # Initialize research tool
        self.research_tool = ResearchTool()

        # Conversation state
        self.messages = []
        self.is_research_mode = False
        self.pending_research_result = None

        # System prompt
        self.system_prompt = self._create_system_prompt()

    def _create_system_prompt(self) -> str:
        """Create the system prompt for the chat agent."""
        return """You are a helpful AI assistant with deep research capabilities. You can engage in natural conversation and also conduct comprehensive research when needed.

Your abilities:
1. **Conversation**: Chat naturally with users about various topics
2. **Research Clarification**: When a user asks for research, help clarify and refine their question
3. **Deep Research**: Use the research tool to conduct thorough investigations on any topic

Research Tool Usage:
- When users ask questions that require comprehensive investigation, current information, or academic research
- Clarify ambiguous research questions before delegating to the research tool
- Use the research tool for: current events, scientific topics, historical analysis, technology trends, academic subjects, etc.

Conversation Flow:
1. **Normal Chat**: Respond conversationally to general questions and casual conversation
2. **Research Detection**: Identify when a user wants deep research on a topic
3. **Question Clarification**: Help refine unclear or broad research questions
4. **Research Delegation**: Use the research tool when comprehensive investigation is needed
5. **Result Presentation**: Present research findings in a clear, helpful way

Tool Call Format:
When you need to conduct research, respond with ONLY the JSON object:
{"name": "research", "arguments": {"research_quest": "clarified research question"}}

Guidelines:
- Be conversational and helpful
- Ask follow-up questions to clarify research needs
- Use research tool for comprehensive, multi-source investigations
- Present research results in an accessible, user-friendly format
- Maintain conversation context across multiple exchanges
- Always be honest about what you know and don't know

Remember: You excel at both conversation and research. Choose the appropriate approach based on the user's needs."""

    def _detect_tool_calls(self, content: str) -> List[Dict[str, Any]]:
        """Detect and parse tool calls in LLM response."""
        tool_calls = []

        # Look for JSON tool calls - more permissive pattern
        json_patterns = [
            r'\{[^{}]*"name"[^{}]*"arguments"[^{}]*\}',  # Standard format
            r'\{[^{}]*"name"[^{}]*"research_quest"[^{}]*\}',  # Alternative format
            r'"name":\s*"research"[^}]*"arguments"[^}]*\}',  # Research tool specific
        ]

        for pattern in json_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            for match in matches:
                try:
                    # Try to extract valid JSON
                    if match.startswith('{'):
                        tool_call = json.loads(match)
                    else:
                        # Wrap in braces if needed
                        tool_call = json.loads('{' + match + '}')
                    
                    if 'name' in tool_call and 'arguments' in tool_call:
                        tool_calls.append(tool_call)
                except json.JSONDecodeError:
                    continue

        return tool_calls

    def _execute_research_tool(self, research_quest: str) -> str:
        """Execute the research tool with the given question."""
        try:
            print(f"🔍 Starting research on: {research_quest}")
            research_result = self.research_tool.call({"research_quest": research_quest})
            print(f"✅ Research completed for: {research_quest}")
            return research_result
        except Exception as e:
            print(f"❌ Research failed: {str(e)}")
            return f"Research failed: {str(e)}"

    def _is_research_request(self, user_message: str) -> bool:
        """Determine if the user is requesting research."""
        research_indicators = [
            "research", "investigate", "study", "analyze", "find information about",
            "look into", "explore", "examine", "investigation", "tell me about",
            "what is", "how does", "why is", "where can I find", "latest developments",
            "current status", "recent advances", "state of the art", "comprehensive"
        ]

        user_message_lower = user_message.lower()
        return any(indicator in user_message_lower for indicator in research_indicators)

    def _should_ask_for_clarification(self, user_message: str) -> bool:
        """Determine if the research question needs clarification."""
        # Very short or vague questions
        if len(user_message.strip()) < 10:
            return True

        # Vague question patterns
        vague_patterns = [
            r"^tell me about .*$",
            r"^what is .*$",
            r"^how does .*$",
            r"^why is .*$",
            r"^research .*$",
            r"^information about .*$"
        ]

        user_message_lower = user_message.lower().strip()
        for pattern in vague_patterns:
            if re.match(pattern, user_message_lower):
                # Allow more specific versions of these questions
                if len(user_message_lower.split()) > 6:  # More than 6 words might be specific enough
                    return False
                return True

        return False

    def _generate_clarification_questions(self, user_message: str) -> str:
        """Generate clarification questions for ambiguous research requests."""
        return """I'd be happy to help research that topic! To provide you with the most comprehensive and relevant information, could you help clarify a few things:

1. **Specific Focus**: What particular aspect of this topic interests you most?
2. **Time Range**: Are you looking for current information, historical context, or both?
3. **Purpose**: How will you use this information (academic paper, business decision, general knowledge, etc.)?
4. **Depth**: Do you want a broad overview or deep technical details?

For example, instead of "tell me about AI", you might want:
- "Current applications of AI in healthcare in 2024"
- "Ethical implications of AI in hiring processes"
- "Technical challenges in developing large language models"

What specific aspect would you like me to research?"""

    def _format_research_result_for_chat(self, research_result: str) -> str:
        """Format research results for chat presentation."""
        # Extract the main content from the research result
        if "Research Report:" in research_result or "📋 Research Report:" in research_result:
            # Remove the header and stats for cleaner presentation
            lines = research_result.split('\n')
            content_lines = []
            skip_header = True

            for line in lines:
                if "🔍 Research completed using ReActAgent" in line:
                    # Found end marker, stop processing
                    break
                if skip_header:
                    # Skip header until we find the first === line
                    if line.startswith('='):
                        skip_header = False
                        continue
                else:
                    # After header, collect content until we hit footer
                    if line.startswith('='):
                        # Found footer, stop collecting
                        break
                    if line.strip():
                        content_lines.append(line)
            
            formatted_content = '\n'.join(content_lines).strip()
        else:
            formatted_content = research_result

        # Ensure we have content
        if not formatted_content:
            formatted_content = "Research completed but no content was generated."

        # Add a nice presentation wrapper
        result = f"""📊 **Research Results**

{formatted_content}

---

💡 *If you'd like me to research this topic further or explore a different aspect, just let me know!*"""

        return result

    def chat(self, user_message: str) -> str:
        """
        Process a user message and generate a response.

        Args:
            user_message: The user's input message

        Returns:
            The assistant's response
        """
        # Check for empty or whitespace-only messages
        if not user_message or not user_message.strip():
            return "Please provide a message to continue our conversation."

        # Check if we have a pending research result to deliver
        if self.pending_research_result:
            result = self.pending_research_result
            self.pending_research_result = None
            self.is_research_mode = False
            return result

        # Add user message to conversation
        self.messages.append({"role": "user", "content": user_message})

        # Check if this is a research request
        if self._is_research_request(user_message):
            # Check if clarification is needed
            if self._should_ask_for_clarification(user_message):
                return self._generate_clarification_questions(user_message)

            # Set research mode and add system instruction
            self.is_research_mode = True
            research_instruction = """The user is asking for research. Please clarify their question if needed, then use the research tool to conduct comprehensive research. Use this format for tool calls:
{"name": "research", "arguments": {"research_quest": "clarified research question"}}"""

            # Add research instruction to messages
            temp_messages = [{"role": "system", "content": self.system_prompt}]
            temp_messages.append({"role": "system", "content": research_instruction})
            temp_messages.extend(self.messages)
        else:
            # Normal conversation
            temp_messages = [{"role": "system", "content": self.system_prompt}]
            temp_messages.extend(self.messages)

        try:
            # Get LLM response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=temp_messages,
                temperature=0.7,
                stream=False
            )

            assistant_response = response.choices[0].message.content

            # Check for tool calls
            tool_calls = self._detect_tool_calls(assistant_response)

            if tool_calls:
                # Execute tool calls
                for tool_call in tool_calls:
                    if tool_call['name'] == 'research':
                        research_quest = tool_call['arguments'].get('research_quest', '')
                        if research_quest:
                            # Conduct research
                            research_result = self._execute_research_tool(research_quest)
                            logger.info(f"Research completed: {research_quest}")
                            # Format for chat presentation
                            formatted_result = self._format_research_result_for_chat(research_result)

                            # Store result for next turn
                            self.pending_research_result = formatted_result

                            # Return acknowledgment
                            return f"🔍 **Conducting Research...**\n\nI'm researching \"{research_quest}\" for you. This may take a moment as I gather comprehensive information from multiple sources.\n\n*(Please wait for the detailed research results...)*"

            # Add assistant response to conversation
            self.messages.append({"role": "assistant", "content": assistant_response})

            return assistant_response

        except Exception as e:
            error_msg = f"I apologize, but I encountered an error: {str(e)}"
            self.messages.append({"role": "assistant", "content": error_msg})
            return error_msg

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history."""
        return self.messages.copy()

    def reset_conversation(self):
        """Reset the conversation for a new session."""
        self.messages = []
        self.is_research_mode = False
        self.pending_research_result = None

    def get_stats(self) -> Dict[str, Any]:
        """Get conversation and research statistics."""
        stats = {
            "conversation_length": len(self.messages),
            "is_research_mode": self.is_research_mode,
            "has_pending_research": self.pending_research_result is not None
        }

        # Get research tool stats if available
        if hasattr(self.research_tool, 'get_research_stats'):
            try:
                research_stats = self.research_tool.get_research_stats()
                stats["research_stats"] = research_stats
            except:
                stats["research_stats"] = "Unavailable"

        return stats


# For direct testing
if __name__ == "__main__":
    # Simple interactive test
    print("🤖 Chat Agent Test Session")
    print("=" * 50)
    print("Type 'quit' to exit, 'reset' to clear conversation")
    print("=" * 50)

    try:
        agent = ChatAgent()
        print("✅ Chat Agent initialized successfully!")

        while True:
            user_input = input("\n💬 You: ").strip()

            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'reset':
                agent.reset_conversation()
                print("🔄 Conversation reset!")
                continue
            elif not user_input:
                continue

            # Get agent response
            response = agent.chat(user_input)
            print(f"\n🤖 Assistant: {response}")

    except Exception as e:
        print(f"❌ Error initializing Chat Agent: {str(e)}")
        print("Please make sure GLM_API_KEY environment variable is set.")